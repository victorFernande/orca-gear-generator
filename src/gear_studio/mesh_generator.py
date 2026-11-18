"""Strict 2-manifold 3D gear and Fit-Test Kit mesh generator for Orca Gear Studio."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Sequence

try:
    import numpy as np
except ModuleNotFoundError:
    import os as _os
    from pathlib import Path as _Path
    import sys as _sys

    _cp_tag = f"cp{_sys.version_info.major}{_sys.version_info.minor}"
    _orca_roots = [
        _Path(_os.environ["APPDATA"]) / "OrcaSlicer" if _os.environ.get("APPDATA") else None,
        _Path.home() / "Library" / "Application Support" / "OrcaSlicer",
        _Path(_os.environ.get("XDG_CONFIG_HOME") or (_Path.home() / ".config")) / "OrcaSlicer",
    ]
    for _root in _orca_roots:
        if _root is not None:
            _cand = _root / "python" / "packages" / _cp_tag
            if _cand.is_dir() and str(_cand) not in _sys.path:
                _sys.path.insert(0, str(_cand))
    import numpy as np

if "normalize_params" not in globals():
    from .schema import effective_helix_angle_deg, normalize_params

if "compute_gear_pair_geometry" not in globals():
    from .involute_math import (
        build_bore_2d_contour,
        build_gear_2d_contour,
        compute_gear_pair_geometry,
        helix_twist_angle_rad,
    )


@dataclass
class MeshData:
    vertices: np.ndarray            # (V, 3), float32, finite, min(Z) == 0.0, XY centered near (0, 0)
    triangles: np.ndarray           # (F, 3), int32, strict CCW outward winding
    face_normals: np.ndarray        # (F, 3), float32, unit vectors aligned > 0.99 with CCW cross product
    bounds_mm: dict[str, list[float]]  # {"min": [x,y,z], "max": [x,y,z], "size": [dx,dy,dz]}
    volume_cm3: float               # positive signed divergence volume in cm^3
    overhang_angles_deg: np.ndarray  # (F,), float32, downward overhang angle in degrees


# ---------------------------------------------------------------------------
# Mesh Finalization & Topological Builders
# ---------------------------------------------------------------------------


def _finalize_mesh(
    vertices: np.ndarray,
    triangles: np.ndarray,
    *,
    center_xy: bool = False,
) -> MeshData:
    """Finalize raw float64 vertices & int32 CCW triangles into a validated MeshData."""
    verts64 = np.asarray(vertices, dtype=np.float64).copy()
    tris = np.asarray(triangles, dtype=np.int32).reshape(-1, 3).copy()

    if len(verts64) == 0 or len(tris) == 0:
        empty_v = np.zeros((0, 3), dtype=np.float32)
        empty_t = np.zeros((0, 3), dtype=np.int32)
        empty_o = np.zeros((0,), dtype=np.float32)
        return MeshData(
            vertices=empty_v,
            triangles=empty_t,
            face_normals=empty_v.copy(),
            bounds_mm={"min": [0.0, 0.0, 0.0], "max": [0.0, 0.0, 0.0], "size": [0.0, 0.0, 0.0]},
            volume_cm3=0.0,
            overhang_angles_deg=empty_o,
        )

    if center_xy:
        mid_x = 0.5 * float(verts64[:, 0].min() + verts64[:, 0].max())
        mid_y = 0.5 * float(verts64[:, 1].min() + verts64[:, 1].max())
        verts64[:, 0] -= mid_x
        verts64[:, 1] -= mid_y

    z_min64 = float(verts64[:, 2].min())
    verts64[:, 2] -= z_min64
    verts64[np.abs(verts64[:, 2]) < 1e-7, 2] = 0.0

    verts32 = verts64.astype(np.float32)
    z_min32 = float(verts32[:, 2].min())
    if z_min32 != 0.0:
        verts32[:, 2] -= np.float32(z_min32)
    verts32[np.abs(verts32[:, 2]) < 1e-7, 2] = np.float32(0.0)

    v0 = verts32[tris[:, 0]].astype(np.float64)
    v1 = verts32[tris[:, 1]].astype(np.float64)
    v2 = verts32[tris[:, 2]].astype(np.float64)

    cross = np.cross(v1 - v0, v2 - v0)
    norms = np.linalg.norm(cross, axis=1, keepdims=True)
    unit_normals64 = cross / np.maximum(norms, 1e-30)
    face_normals = unit_normals64.astype(np.float32)

    signed_vol_mm3 = float(np.sum(np.einsum("ij,ij->i", v0, cross)) / 6.0)
    volume_cm3 = float(signed_vol_mm3 / 1000.0)

    # Downward overhang angle in degrees (0 deg for vertical/upward or bed-resting faces at Z == 0)
    face_z_max = np.maximum(np.maximum(v0[:, 2], v1[:, 2]), v2[:, 2])
    nz = unit_normals64[:, 2]
    overhang64 = np.zeros(len(tris), dtype=np.float64)
    down_mask = (face_z_max > 1e-3) & (nz < -1e-5)
    if np.any(down_mask):
        overhang64[down_mask] = np.degrees(np.arcsin(np.clip(-nz[down_mask], 0.0, 1.0)))
    overhang_angles_deg = overhang64.astype(np.float32)

    vmin = verts32.min(axis=0)
    vmax = verts32.max(axis=0)
    vsize = vmax - vmin
    bounds_mm = {
        "min": [float(vmin[0]), float(vmin[1]), float(vmin[2])],
        "max": [float(vmax[0]), float(vmax[1]), float(vmax[2])],
        "size": [float(vsize[0]), float(vsize[1]), float(vsize[2])],
    }

    return MeshData(
        vertices=verts32,
        triangles=tris,
        face_normals=face_normals,
        bounds_mm=bounds_mm,
        volume_cm3=volume_cm3,
        overhang_angles_deg=overhang_angles_deg,
    )


class _GearMeshBuilder:
    """Indexed vertex & CCW triangle accumulator guaranteeing zero accidental vertex collisions."""

    def __init__(self) -> None:
        self._verts_chunks: list[np.ndarray] = []
        self._tris_chunks: list[np.ndarray] = []
        self._v_count: int = 0

    def add_vertices(self, pts: np.ndarray) -> np.ndarray:
        arr = np.asarray(pts, dtype=np.float64)
        if arr.ndim == 1:
            arr = arr[None, :]
        n = arr.shape[0]
        start = self._v_count
        self._verts_chunks.append(arr)
        self._v_count += n
        return np.arange(start, start + n, dtype=np.int32)

    def add_vertex(self, x: float, y: float, z: float) -> int:
        idx = self._v_count
        self._verts_chunks.append(np.array([[x, y, z]], dtype=np.float64))
        self._v_count += 1
        return idx

    def add_ring_2d(self, xy: np.ndarray, z: float) -> np.ndarray:
        xy64 = np.asarray(xy, dtype=np.float64)
        pts = np.column_stack((xy64[:, 0], xy64[:, 1], np.full(len(xy64), float(z), dtype=np.float64)))
        return self.add_vertices(pts)

    def add_polar_ring(self, radii: np.ndarray | float, thetas: np.ndarray, z: float) -> np.ndarray:
        r_arr = np.broadcast_to(np.asarray(radii, dtype=np.float64), thetas.shape)
        pts = np.column_stack((
            r_arr * np.cos(thetas),
            r_arr * np.sin(thetas),
            np.full(len(thetas), float(z), dtype=np.float64),
        ))
        return self.add_vertices(pts)

    def add_circle_ring(
        self,
        cx: float,
        cy: float,
        radius: float,
        z: float,
        count: int,
        phase_rad: float = 0.0,
    ) -> np.ndarray:
        phis = phase_rad + np.linspace(0.0, 2.0 * math.pi, count, endpoint=False, dtype=np.float64)
        pts = np.column_stack((
            cx + radius * np.cos(phis),
            cy + radius * np.sin(phis),
            np.full(count, float(z), dtype=np.float64),
        ))
        return self.add_vertices(pts)

    def add_triangles(self, tris: np.ndarray | Sequence[tuple[int, int, int]]) -> None:
        arr = np.asarray(tris, dtype=np.int32)
        if arr.size > 0:
            self._tris_chunks.append(arr.reshape(-1, 3))

    def add_quad_strip(self, ring_a: np.ndarray, ring_b: np.ndarray, reverse: bool = False) -> None:
        """Connect two equal-length closed CCW rings.

        With reverse=False, normal is (+dz * r_hat - dr * z_hat):
        - upward outer wall (dz > 0, dr == 0) -> +r_hat (outward)
        - outward bottom cap (dr > 0, dz == 0) -> -z_hat (downward)
        With reverse=True, normal is (-dz * r_hat + dr * z_hat):
        - upward inner bore/hole tunnel (dz > 0, dr == 0) -> -r_hat (inward into hole)
        - outward top cap (dr > 0, dz == 0) -> +z_hat (upward)
        """
        a0 = np.asarray(ring_a, dtype=np.int32)
        a1 = np.roll(a0, -1)
        b0 = np.asarray(ring_b, dtype=np.int32)
        b1 = np.roll(b0, -1)
        if not reverse:
            t1 = np.column_stack((a0, a1, b1))
            t2 = np.column_stack((a0, b1, b0))
        else:
            t1 = np.column_stack((a0, b1, a1))
            t2 = np.column_stack((a0, b0, b1))
        self.add_triangles(np.vstack((t1, t2)))

    def add_tube_grid(self, rings: Sequence[np.ndarray], reverse: bool = False) -> None:
        arr = np.asarray(rings, dtype=np.int32)
        a0 = arr[:-1, :]
        a1 = np.roll(a0, -1, axis=1)
        b0 = arr[1:, :]
        b1 = np.roll(b0, -1, axis=1)
        if not reverse:
            t1 = np.stack((a0, a1, b1), axis=-1).reshape(-1, 3)
            t2 = np.stack((a0, b1, b0), axis=-1).reshape(-1, 3)
        else:
            t1 = np.stack((a0, b1, a1), axis=-1).reshape(-1, 3)
            t2 = np.stack((a0, b0, b1), axis=-1).reshape(-1, 3)
        self.add_triangles(np.vstack((t1, t2)))

    def add_disk_fan(self, center_idx: int, ring: np.ndarray, normal_up: bool = True) -> None:
        r0 = np.asarray(ring, dtype=np.int32)
        m = len(r0)
        c = np.full(m, int(center_idx), dtype=np.int32)
        r1 = np.roll(r0, -1)
        if normal_up:
            tris = np.column_stack((c, r0, r1))
        else:
            tris = np.column_stack((c, r1, r0))
        self.add_triangles(tris)

    def get_vertices_array(self) -> np.ndarray:
        if not self._verts_chunks:
            return np.zeros((0, 3), dtype=np.float64)
        return np.vstack(self._verts_chunks)

    def build(self, *, center_xy: bool = False) -> MeshData:
        verts64 = self.get_vertices_array()
        tris = (
            np.vstack(self._tris_chunks).astype(np.int32)
            if self._tris_chunks
            else np.zeros((0, 3), dtype=np.int32)
        )
        return _finalize_mesh(verts64, tris, center_xy=center_xy)


# ---------------------------------------------------------------------------
# 2D Loop Bridging & Exact Polygon-With-Holes Ear-Clipping
# ---------------------------------------------------------------------------


def _mg_bridge_convex_loops_up(
    verts_xy: np.ndarray,
    loop_in: Sequence[int] | np.ndarray,
    loop_out: Sequence[int] | np.ndarray,
    center_xy: tuple[float, float],
) -> np.ndarray:
    """Triangulate annulus between two strictly convex/circular CCW loops around center_xy (+Z normal)."""
    lin = [int(i) for i in loop_in]
    lout = [int(i) for i in loop_out]
    m1 = len(lin)
    m2 = len(lout)
    cx, cy = center_xy

    ang_in: list[float] = []
    for p, idx in enumerate(lin):
        a = math.atan2(float(verts_xy[idx, 1]) - cy, float(verts_xy[idx, 0]) - cx)
        if p > 0:
            while a <= ang_in[-1]:
                a += 2.0 * math.pi
        ang_in.append(a)
    ang_in.append(ang_in[0] + 2.0 * math.pi)

    raw_out = [
        math.atan2(float(verts_xy[idx, 1]) - cy, float(verts_xy[idx, 0]) - cx)
        for idx in lout
    ]
    best_s = min(
        range(m2),
        key=lambda s: abs(((raw_out[s] - ang_in[0] + math.pi) % (2.0 * math.pi)) - math.pi),
    )
    lout = lout[best_s:] + lout[:best_s]

    a0 = math.atan2(float(verts_xy[lout[0], 1]) - cy, float(verts_xy[lout[0], 0]) - cx)
    while a0 - ang_in[0] > math.pi:
        a0 -= 2.0 * math.pi
    while ang_in[0] - a0 > math.pi:
        a0 += 2.0 * math.pi

    ang_out: list[float] = [a0]
    for q in range(1, m2):
        idx = lout[q]
        a = math.atan2(float(verts_xy[idx, 1]) - cy, float(verts_xy[idx, 0]) - cx)
        while a <= ang_out[-1]:
            a += 2.0 * math.pi
        ang_out.append(a)
    ang_out.append(ang_out[0] + 2.0 * math.pi)

    tris: list[tuple[int, int, int]] = []
    p = 0
    q = 0
    while p < m1 or q < m2:
        if p == m1:
            advance_out = True
        elif q == m2:
            advance_out = False
        else:
            skew_if_in = abs(ang_in[p + 1] - ang_out[q])
            skew_if_out = abs(ang_out[q + 1] - ang_in[p])
            advance_out = skew_if_out < skew_if_in

        if advance_out:
            tris.append((lin[p % m1], lout[q % m2], lout[(q + 1) % m2]))
            q += 1
        else:
            tris.append((lin[p % m1], lout[q % m2], lin[(p + 1) % m1]))
            p += 1

    return np.asarray(tris, dtype=np.int32)


def _mg_cross2d(
    ax: float,
    ay: float,
    bx: float,
    by: float,
    cx: float,
    cy: float,
) -> float:
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)


def _mg_signed_area_2d(pts_xy: np.ndarray, indices: Sequence[int]) -> float:
    n = len(indices)
    area2 = 0.0
    for i in range(n):
        u = indices[i]
        v = indices[(i + 1) % n]
        area2 += float(pts_xy[u, 0] * pts_xy[v, 1] - pts_xy[v, 0] * pts_xy[u, 1])
    return 0.5 * area2


def _mg_point_in_tri_2d(
    px: float,
    py: float,
    ax: float,
    ay: float,
    bx: float,
    by: float,
    cx: float,
    cy: float,
    eps: float = -1e-10,
) -> bool:
    c1 = _mg_cross2d(ax, ay, bx, by, px, py)
    if c1 < eps:
        return False
    c2 = _mg_cross2d(bx, by, cx, cy, px, py)
    if c2 < eps:
        return False
    c3 = _mg_cross2d(cx, cy, ax, ay, px, py)
    return c3 >= eps


def _mg_find_hole_bridge_pos(
    pts_xy: np.ndarray,
    poly: list[int],
    mx: float,
    my: float,
) -> int:
    """Find a vertex position in `poly` strictly visible from rightmost hole vertex (mx, my)."""
    n = len(poly)
    y_span = max(1.0, float(pts_xy[poly, 1].max() - pts_xy[poly, 1].min()))
    my_ray = my
    if any(abs(float(pts_xy[v, 1]) - my_ray) < 1e-10 for v in poly):
        my_ray = my + 1.37e-8 * y_span

    best_x = float("inf")
    best_edge = -1
    for i in range(n):
        u = poly[i]
        v = poly[(i + 1) % n]
        ux, uy = float(pts_xy[u, 0]), float(pts_xy[u, 1])
        vx, vy = float(pts_xy[v, 0]), float(pts_xy[v, 1])
        if (uy > my_ray) != (vy > my_ray):
            x_int = ux + (my_ray - uy) * (vx - ux) / (vy - uy)
            if x_int > mx and x_int < best_x:
                best_x = x_int
                best_edge = i

    if best_edge < 0:
        return max(range(n), key=lambda k: float(pts_xy[poly[k], 0]))

    i0 = best_edge
    i1 = (best_edge + 1) % n
    cand_pos = i0 if float(pts_xy[poly[i0], 0]) >= float(pts_xy[poly[i1], 0]) else i1
    px, py = float(pts_xy[poly[cand_pos], 0]), float(pts_xy[poly[cand_pos], 1])

    if abs(py - my) <= 1e-10:
        return cand_pos

    # Triangle between M=(mx, my), ray hit I=(best_x, my), and candidate vertex P=(px, py)
    if py > my:
        tax, tay, tbx, tby, tcx, tcy = mx, my, best_x, my, px, py
    else:
        tax, tay, tbx, tby, tcx, tcy = mx, my, px, py, best_x, my

    best_reflex_pos = -1
    best_tan = float("inf")
    best_dist_sq = float("inf")

    cand_vid = poly[cand_pos]
    for k in range(n):
        vid = poly[k]
        if vid == cand_vid:
            continue
        prev_v = poly[k - 1]
        next_v = poly[(k + 1) % n]
        # Only reflex vertices can block visibility
        if _mg_cross2d(
            float(pts_xy[prev_v, 0]),
            float(pts_xy[prev_v, 1]),
            float(pts_xy[vid, 0]),
            float(pts_xy[vid, 1]),
            float(pts_xy[next_v, 0]),
            float(pts_xy[next_v, 1]),
        ) > 1e-11:
            continue
        kx, ky = float(pts_xy[vid, 0]), float(pts_xy[vid, 1])
        if kx < mx:
            continue
        if _mg_point_in_tri_2d(kx, ky, tax, tay, tbx, tby, tcx, tcy, eps=-1e-11):
            dx = kx - mx
            dy = abs(ky - my)
            tan_val = dy / max(dx, 1e-12)
            d2 = dx * dx + dy * dy
            if tan_val < best_tan - 1e-12 or (abs(tan_val - best_tan) <= 1e-12 and d2 < best_dist_sq):
                best_tan = tan_val
                best_dist_sq = d2
                best_reflex_pos = k

    return best_reflex_pos if best_reflex_pos >= 0 else cand_pos


def _mg_triangulate_cell_2d(
    pts_xy: np.ndarray,
    outer_loop: Sequence[int],
    hole_loops: Sequence[Sequence[int]] = (),
) -> np.ndarray:
    """Triangulate a 2D simple polygon (with 0 or more inner CCW hole loops) into +Z CCW triangles.

    Preserves exact input vertex indices along all outer and hole loops with zero T-junctions
    and guarantees strict 2-manifold directed edge pairing.
    """
    poly = [int(i) for i in outer_loop]
    if _mg_signed_area_2d(pts_xy, poly) < 0.0:
        poly.reverse()

    # Sort holes descending by maximum X so horizontal +X visibility rays never hit unmerged holes
    prepared_holes: list[tuple[float, list[int]]] = []
    for h in hole_loops:
        h_list = [int(i) for i in h]
        if len(h_list) < 3:
            continue
        if _mg_signed_area_2d(pts_xy, h_list) < 0.0:
            h_list.reverse()
        h_cw = h_list[::-1]
        max_x = max(float(pts_xy[v, 0]) for v in h_cw)
        prepared_holes.append((max_x, h_cw))

    prepared_holes.sort(key=lambda item: item[0], reverse=True)

    for _, h_cw in prepared_holes:
        m_idx = max(
            range(len(h_cw)),
            key=lambda idx: (float(pts_xy[h_cw[idx], 0]), float(pts_xy[h_cw[idx], 1])),
        )
        h_rot = h_cw[m_idx:] + h_cw[:m_idx]
        m_vid = h_rot[0]
        mx, my = float(pts_xy[m_vid, 0]), float(pts_xy[m_vid, 1])
        v_pos = _mg_find_hole_bridge_pos(pts_xy, poly, mx, my)
        v_vid = poly[v_pos]
        poly = poly[: v_pos + 1] + h_rot + [m_vid, v_vid] + poly[v_pos + 1 :]

    used_undirected: set[tuple[int, int]] = set()
    for i in range(len(poly)):
        u = poly[i]
        v = poly[(i + 1) % len(poly)]
        if u != v:
            used_undirected.add((min(u, v), max(u, v)))

    tris: list[tuple[int, int, int]] = []
    guard = len(poly) * 4 + 16

    while len(poly) > 3 and guard > 0:
        guard -= 1
        m = len(poly)
        best_k = -1
        best_quality = -1.0

        for tol in (1e-8, 1e-12):
            for k in range(m):
                ia = poly[k - 1]
                ib = poly[k]
                ic = poly[(k + 1) % m]
                if ia == ib or ib == ic or ia == ic:
                    continue
                chord = (min(ia, ic), max(ia, ic))
                if chord in used_undirected:
                    continue

                ax, ay = float(pts_xy[ia, 0]), float(pts_xy[ia, 1])
                bx, by = float(pts_xy[ib, 0]), float(pts_xy[ib, 1])
                cx, cy = float(pts_xy[ic, 0]), float(pts_xy[ic, 1])

                area2 = _mg_cross2d(ax, ay, bx, by, cx, cy)
                if area2 <= tol:
                    continue

                contains_other = False
                for p_vid in poly:
                    if p_vid == ia or p_vid == ib or p_vid == ic:
                        continue
                    if _mg_point_in_tri_2d(
                        float(pts_xy[p_vid, 0]),
                        float(pts_xy[p_vid, 1]),
                        ax,
                        ay,
                        bx,
                        by,
                        cx,
                        cy,
                        eps=-1e-10,
                    ):
                        contains_other = True
                        break
                if contains_other:
                    continue

                e2 = (
                    (bx - ax) ** 2 + (by - ay) ** 2
                    + (cx - bx) ** 2 + (cy - by) ** 2
                    + (ax - cx) ** 2 + (ay - cy) ** 2
                )
                quality = area2 / max(e2, 1e-30)
                if quality > best_quality:
                    best_quality = quality
                    best_k = k

            if best_k >= 0:
                break

        if best_k < 0:
            # Emergency convex fallback without chord constraint if polygon collapsed near 4 nodes
            for k in range(m):
                ia = poly[k - 1]
                ib = poly[k]
                ic = poly[(k + 1) % m]
                if ia == ib or ib == ic or ia == ic:
                    continue
                area2 = _mg_cross2d(
                    float(pts_xy[ia, 0]),
                    float(pts_xy[ia, 1]),
                    float(pts_xy[ib, 0]),
                    float(pts_xy[ib, 1]),
                    float(pts_xy[ic, 0]),
                    float(pts_xy[ic, 1]),
                )
                if area2 > 1e-13:
                    best_k = k
                    break
            if best_k < 0:
                break

        ia = poly[best_k - 1]
        ib = poly[best_k]
        ic = poly[(best_k + 1) % m]
        tris.append((ia, ib, ic))
        used_undirected.add((min(ia, ic), max(ia, ic)))
        poly.pop(best_k)

    if len(poly) == 3 and poly[0] != poly[1] and poly[1] != poly[2] and poly[2] != poly[0]:
        tris.append((poly[0], poly[1], poly[2]))

    return np.asarray(tris, dtype=np.int32)


# ---------------------------------------------------------------------------
# Public Gear Mesh Generator
# ---------------------------------------------------------------------------


def _mg_rotate_2d(xy: np.ndarray, angle_rad: float) -> np.ndarray:
    if abs(angle_rad) < 1e-12:
        return xy.copy()
    c = math.cos(angle_rad)
    s = math.sin(angle_rad)
    out = np.empty_like(xy)
    out[:, 0] = xy[:, 0] * c - xy[:, 1] * s
    out[:, 1] = xy[:, 0] * s + xy[:, 1] * c
    return out


def _mg_build_outer_z_schedule(
    face_width_mm: float,
    beta_deg: float,
    gear_type: str,
    chamfer_mm: float,
    resolution: str,
) -> tuple[list[float], list[float]]:
    """Build Z slice levels and corresponding radial insets for spur/helical/herringbone gears."""
    b = float(face_width_mm)
    gt = str(gear_type).strip().lower()
    has_chamfer = chamfer_mm > 0.03

    z_lo = chamfer_mm if has_chamfer else 0.0
    z_hi = (b - chamfer_mm) if has_chamfer else b
    span_mid = max(0.2, z_hi - z_lo)

    if gt == "spur" or abs(beta_deg) < 1e-4:
        if has_chamfer:
            return [0.0, z_lo, z_hi, b], [chamfer_mm, 0.0, 0.0, chamfer_mm]
        return [0.0, b], [0.0, 0.0]

    if resolution == "high":
        n_mid = int(round(max(24.0, min(56.0, 16.0 + 0.85 * b + 0.35 * abs(beta_deg)))))
    else:
        n_mid = int(round(max(16.0, min(28.0, 10.0 + 0.45 * b + 0.20 * abs(beta_deg)))))

    max_by_dz = max(2, int(math.floor(span_mid / 0.12)))
    n_mid = min(n_mid, max_by_dz)
    if n_mid % 2 == 1:
        n_mid = max(2, n_mid + 1 if n_mid + 1 <= max_by_dz else n_mid - 1)
    n_mid = max(2, n_mid)

    z_mid = np.linspace(z_lo, z_hi, n_mid + 1, dtype=np.float64).tolist()
    if gt == "herringbone":
        z_mid[n_mid // 2] = 0.5 * b

    if has_chamfer:
        z_levels = [0.0, *z_mid, b]
        insets = [chamfer_mm, *([0.0] * len(z_mid)), chamfer_mm]
    else:
        z_levels = z_mid
        insets = [0.0] * len(z_mid)

    return z_levels, insets


def _mg_add_k_hole_sectors(
    mb: _GearMeshBuilder,
    in_top_ring: np.ndarray,
    out_top_ring: np.ndarray,
    in_bot_ring: np.ndarray,
    out_bot_ring: np.ndarray,
    ring_thetas: np.ndarray,
    r_ann_in: float,
    r_ann_out: float,
    z_bot_h: float,
    z_top_h: float,
    k_holes: int,
    s_arc: int,
    req_hole_diam_mm: float,
    resolution: str,
) -> None:
    """Connect top & bottom annular sector rings [r_ann_in, r_ann_out] with K strict 2-manifold through-holes."""
    m_ang = k_holes * s_arc
    dpsi = math.pi / float(k_holes)
    r_hole_ring = 0.5 * (r_ann_in + r_ann_out)
    half_radial = 0.5 * (r_ann_out - r_ann_in)
    spoke_dist = r_hole_ring * math.sin(dpsi) if k_holes >= 2 else half_radial
    min_margin = min(0.75, 0.22 * min(half_radial, spoke_dist))
    max_r_h = max(0.22, min(half_radial - min_margin, spoke_dist - min_margin))
    r_h = max(0.22, min(0.5 * float(req_hole_diam_mm), max_r_h))

    n_spoke_mid = 5 if resolution == "high" else 3
    m_hole = 28 if resolution == "high" else 20

    spoke_r_mid = np.linspace(r_ann_in, r_ann_out, n_spoke_mid + 2, dtype=np.float64)[1:-1]

    spokes_top: list[np.ndarray] = []
    spokes_bot: list[np.ndarray] = []
    for k in range(k_holes):
        ang = float(ring_thetas[k * s_arc])
        ca = math.cos(ang)
        sa = math.sin(ang)
        mid_xy = np.column_stack((spoke_r_mid * ca, spoke_r_mid * sa))
        mid_t = mb.add_ring_2d(mid_xy, z_top_h)
        mid_b = mb.add_ring_2d(mid_xy, z_bot_h)
        spokes_top.append(
            np.concatenate((
                np.array([in_top_ring[k * s_arc]], dtype=np.int32),
                mid_t,
                np.array([out_top_ring[k * s_arc]], dtype=np.int32),
            ))
        )
        spokes_bot.append(
            np.concatenate((
                np.array([in_bot_ring[k * s_arc]], dtype=np.int32),
                mid_b,
                np.array([out_bot_ring[k * s_arc]], dtype=np.int32),
            ))
        )

    hole_top_rings: list[np.ndarray] = []
    hole_bot_rings: list[np.ndarray] = []
    for k in range(k_holes):
        psi_k = 2.0 * math.pi * float(k) / float(k_holes)
        cx_k = r_hole_ring * math.cos(psi_k)
        cy_k = r_hole_ring * math.sin(psi_k)
        ht = mb.add_circle_ring(cx_k, cy_k, r_h, z_top_h, m_hole, phase_rad=psi_k)
        hb = mb.add_circle_ring(cx_k, cy_k, r_h, z_bot_h, m_hole, phase_rad=psi_k)
        mb.add_quad_strip(hb, ht, reverse=True)
        hole_top_rings.append(ht)
        hole_bot_rings.append(hb)

    # Build sector 0 local 2D template once, then map identically across all K sectors (top +Z & bottom -Z)
    verts_xy = mb.get_vertices_array()[:, :2]

    def _sector_loops(k: int, is_top: bool) -> tuple[list[int], list[int]]:
        k_next = (k + 1) % k_holes
        sp = spokes_top if is_top else spokes_bot
        in_r = in_top_ring if is_top else in_bot_ring
        out_r = out_top_ring if is_top else out_bot_ring
        h_r = hole_top_rings[k] if is_top else hole_bot_rings[k]

        outer_arc = [int(out_r[(k * s_arc + s) % m_ang]) for s in range(s_arc)]
        inner_arc = [int(in_r[(k * s_arc + s) % m_ang]) for s in range(s_arc, 0, -1)]
        cell_loop = [
            *sp[k][:-1].tolist(),
            *outer_arc,
            *sp[k_next][::-1][:-1].tolist(),
            *inner_arc,
        ]
        return cell_loop, h_r.tolist()

    sec0_outer, sec0_hole = _sector_loops(0, True)
    local_nodes_0 = sec0_outer + sec0_hole
    local_xy_0 = verts_xy[local_nodes_0]
    n_cell = len(sec0_outer)
    n_h = len(sec0_hole)
    template_tris = _mg_triangulate_cell_2d(
        local_xy_0,
        list(range(n_cell)),
        [list(range(n_cell, n_cell + n_h))],
    )

    all_top_tris: list[np.ndarray] = []
    all_bot_tris: list[np.ndarray] = []
    for k in range(k_holes):
        ct, ht = _sector_loops(k, True)
        map_t = np.asarray(ct + ht, dtype=np.int32)
        all_top_tris.append(map_t[template_tris])

        cb, hb = _sector_loops(k, False)
        map_b = np.asarray(cb + hb, dtype=np.int32)
        tris_b = map_b[template_tris][:, [0, 2, 1]]
        all_bot_tris.append(tris_b)

    mb.add_triangles(np.vstack(all_top_tris + all_bot_tris))


def generate_gear_mesh(
    params: dict[str, Any],
    which: str = "pinion",
    resolution: str = "high",
) -> MeshData:
    """Generate a strict 2-manifold 3D gear mesh (spur, helical, or herringbone) with full body features."""
    p = normalize_params(params)
    res = "high" if str(resolution).strip().lower() == "high" else "low"
    body_key = "gear" if str(which).strip().lower() == "gear" else "pinion"
    body_cfg = p[body_key]

    geom = compute_gear_pair_geometry(p)
    g_info = geom[body_key]

    m_n = float(geom["m_n"])
    beta_deg = float(geom["beta_deg"])
    gear_type = str(p["gear_type"])
    face_w = float(p["face_width_mm"])
    pitch_r = float(g_info["pitch_radius_mm"])
    root_r = float(g_info["root_radius_mm"])
    tip_r = float(g_info["tip_radius_mm"])
    hand = str(g_info["helix_hand"])

    samples_per_flank = 12 if res == "high" else 7
    raw_chamfer = float(p["elephant_foot_chamfer_mm"])
    chamfer = min(
        max(0.0, raw_chamfer),
        0.22 * face_w,
        0.30 * m_n,
        0.24 * max(0.2, tip_r - root_r),
    )
    if chamfer < 0.03:
        chamfer = 0.0

    z_levels, insets = _mg_build_outer_z_schedule(
        face_width_mm=face_w,
        beta_deg=beta_deg,
        gear_type=gear_type,
        chamfer_mm=chamfer,
        resolution=res,
    )

    contour_std = build_gear_2d_contour(
        p,
        which=body_key,
        samples_per_flank=samples_per_flank,
        radial_inset_mm=0.0,
    )
    contour_chamf = (
        build_gear_2d_contour(
            p,
            which=body_key,
            samples_per_flank=samples_per_flank,
            radial_inset_mm=chamfer,
        )
        if chamfer > 0.0
        else contour_std
    )

    mb = _GearMeshBuilder()
    outer_rings: list[np.ndarray] = []
    outer_xy_bot: np.ndarray | None = None
    outer_xy_top: np.ndarray | None = None

    for idx_z, (zv, ins) in enumerate(zip(z_levels, insets)):
        base_xy = contour_chamf if ins > 0.0 else contour_std
        psi = helix_twist_angle_rad(zv, face_w, pitch_r, beta_deg, hand, gear_type)
        rot_xy = _mg_rotate_2d(base_xy, psi)
        if idx_z == 0:
            outer_xy_bot = rot_xy
        if idx_z == len(z_levels) - 1:
            outer_xy_top = rot_xy
        outer_rings.append(mb.add_ring_2d(rot_xy, zv))

    mb.add_tube_grid(outer_rings, reverse=False)

    assert outer_xy_bot is not None and outer_xy_top is not None
    r_outer_min = float(
        min(
            np.min(np.hypot(outer_xy_bot[:, 0], outer_xy_bot[:, 1])),
            np.min(np.hypot(outer_xy_top[:, 0], outer_xy_top[:, 1])),
        )
    )

    # Safe inner rim radius strictly inside tooth roots & chamfer
    rim_wall = max(1.2, 0.6 * m_n)
    r_safe_inner = min(root_r - rim_wall - chamfer, r_outer_min - max(0.65, 0.35 * m_n))
    r_safe_inner = max(0.55 * r_outer_min, r_safe_inner)
    r_safe_inner = min(r_safe_inner, r_outer_min - 0.25)

    # Central bore evaluation
    bore_type = str(body_cfg["bore_type"]).strip().lower()
    m_bore = 64 if res == "high" else 48
    max_bore_r = max(0.45, min(r_safe_inner - 1.0, 0.78 * r_safe_inner))
    bore_xy = (
        build_bore_2d_contour(body_cfg, max_allowed_radius_mm=max_bore_r, radial_samples=m_bore)
        if bore_type != "none"
        else None
    )

    if bore_xy is not None:
        r_bore_max = float(np.max(np.hypot(bore_xy[:, 0], bore_xy[:, 1])))
        if r_bore_max >= r_safe_inner - 0.55:
            scale_b = max(0.35, (r_safe_inner - 0.65) / max(r_bore_max, 1e-6))
            bore_xy = bore_xy * scale_b
            r_bore_max = float(np.max(np.hypot(bore_xy[:, 0], bore_xy[:, 1])))
        collar_pad = max(0.45, min(1.1, 0.28 * (r_safe_inner - r_bore_max)))
        r_collar = min(r_safe_inner - 0.25, r_bore_max + collar_pad)
    else:
        r_bore_max = 0.0
        r_collar = min(max(0.8, 0.18 * r_safe_inner), 0.45 * r_safe_inner)

    avail_span = max(0.0, r_safe_inner - r_collar)

    # Resolve concentric body features (hub, recess, web_recess, lightening_holes)
    light_mode = str(body_cfg["lightening_mode"]).strip().lower()
    k_holes = int(body_cfg["lightening_hole_count"])
    holes_active = bool(light_mode == "lightening_holes" and k_holes >= 1 and avail_span >= 1.1)
    web_active = bool(light_mode == "web_recess" and avail_span >= 1.2)

    hub_req = bool(body_cfg["hub_enabled"]) and float(body_cfg["hub_height_mm"]) > 0.08
    rec_req = bool(body_cfg["recess_enabled"]) and float(body_cfg["recess_depth_mm"]) > 0.08
    rec_side = str(body_cfg["recess_side"]).strip().lower()

    if holes_active or web_active:
        rim_step = max(0.30, min(1.0, 0.07 * avail_span))
        r_web_out = r_safe_inner - rim_step
        min_web_span = max(0.95, 0.36 * avail_span)
        r_core_limit = max(r_collar + 0.30, r_web_out - min_web_span)

        r_core_target = r_collar + max(0.35, 0.18 * avail_span)
        if hub_req:
            r_core_target = max(r_core_target, 0.5 * float(body_cfg["hub_diameter_mm"]))
        if rec_req:
            r_core_target = max(r_core_target, 0.5 * float(body_cfg["recess_diameter_mm"]))

        r_web_in = max(r_collar + 0.28, min(r_core_target + 0.35, r_core_limit))
        r_feature_cap = max(r_collar + 0.25, r_web_in - 0.28)
    else:
        r_web_in = 0.0
        r_web_out = 0.0
        r_feature_cap = r_safe_inner - 0.25

    r_hub = 0.0
    hub_h = float(body_cfg["hub_height_mm"])
    if hub_req and r_feature_cap > r_collar + 0.22:
        r_hub = max(r_collar + 0.25, min(0.5 * float(body_cfg["hub_diameter_mm"]), r_feature_cap))

    r_rec = 0.0
    rec_depth = float(body_cfg["recess_depth_mm"])
    if rec_req and r_feature_cap > r_collar + 0.22:
        r_rec = max(r_collar + 0.25, min(0.5 * float(body_cfg["recess_diameter_mm"]), r_feature_cap))
        # Avoid microscopic sub-0.25mm step if hub and recess diameters are nearly equal
        if r_hub > 0.0 and 0.0 < abs(r_rec - r_hub) < 0.25:
            r_rec = r_hub

    # Assemble strictly increasing radial knots from r_collar to r_safe_inner
    raw_knots = [r_collar, r_safe_inner]
    if r_hub > 0.0:
        raw_knots.append(r_hub)
    if r_rec > 0.0:
        raw_knots.append(r_rec)
    if holes_active or web_active:
        raw_knots.extend([r_web_in, r_web_out])

    raw_knots.sort()
    knots: list[float] = [raw_knots[0]]
    for rk in raw_knots[1:]:
        if rk - knots[-1] >= 0.20:
            knots.append(rk)
        elif rk == raw_knots[-1]:
            knots[-1] = rk

    # Ensure [r_web_in, r_web_out] remains an exact single radial interval when holes_active is True
    hole_interval_idx = -1
    if holes_active:
        # Snap closest knots to r_web_in and r_web_out and drop any interior knot strictly between them
        cleaned_knots: list[float] = []
        for rk in knots:
            if r_web_in + 0.05 < rk < r_web_out - 0.05:
                continue
            cleaned_knots.append(rk)
        knots = cleaned_knots
        for idx_k in range(len(knots) - 1):
            mid_k = 0.5 * (knots[idx_k] + knots[idx_k + 1])
            if r_web_in - 0.05 <= mid_k <= r_web_out + 0.05:
                hole_interval_idx = idx_k
                break

    n_intervals = len(knots) - 1
    z_top_intervals: list[float] = []
    z_bot_intervals: list[float] = []
    min_floor = min(1.2, 0.45 * face_w)

    for idx_i in range(n_intervals):
        r_mid = 0.5 * (knots[idx_i] + knots[idx_i + 1])
        zt = face_w
        zb = 0.0

        if r_hub > 0.0 and r_mid < r_hub - 1e-5:
            zt += hub_h

        if r_rec > 0.0 and r_mid < r_rec - 1e-5:
            avail_t = zt - zb
            if rec_side == "top":
                d = min(rec_depth, max(0.0, avail_t - min_floor))
                zt -= d
            elif rec_side == "bottom":
                d = min(rec_depth, max(0.0, avail_t - min_floor))
                zb += d
            else:
                d = min(rec_depth, max(0.0, 0.5 * (avail_t - min_floor)))
                zt -= d
                zb += d

        if web_active and (r_web_in - 1e-5) < r_mid < (r_web_out + 1e-5):
            w_t = max(min_floor, min(float(body_cfg["web_thickness_mm"]), face_w - 0.25))
            d_web = max(0.0, 0.5 * (face_w - w_t))
            if d_web > 0.06:
                zt = face_w - d_web
                zb = d_web

        z_top_intervals.append(zt)
        z_bot_intervals.append(zb)

    # Angular grid for concentric rings
    if holes_active and hole_interval_idx >= 0:
        s_arc = max(8 if res == "high" else 6, int(math.ceil((64.0 if res == "high" else 40.0) / k_holes)))
        m_ang = k_holes * s_arc
        dpsi = math.pi / float(k_holes)
        ring_thetas = -dpsi + np.linspace(0.0, 2.0 * math.pi, m_ang, endpoint=False, dtype=np.float64)
    else:
        s_arc = 0
        m_ang = 64 if res == "high" else 44
        ring_thetas = np.linspace(0.0, 2.0 * math.pi, m_ang, endpoint=False, dtype=np.float64)

    inner_top_ring = mb.add_polar_ring(knots[0], ring_thetas, z_top_intervals[0])
    inner_bot_ring = mb.add_polar_ring(knots[0], ring_thetas, z_bot_intervals[0])

    cur_top = inner_top_ring
    cur_bot = inner_bot_ring

    for idx_i in range(n_intervals):
        r_next = knots[idx_i + 1]
        zt_cur = z_top_intervals[idx_i]
        zb_cur = z_bot_intervals[idx_i]

        next_top = mb.add_polar_ring(r_next, ring_thetas, zt_cur)
        next_bot = mb.add_polar_ring(r_next, ring_thetas, zb_cur)

        if holes_active and idx_i == hole_interval_idx:
            _mg_add_k_hole_sectors(
                mb=mb,
                in_top_ring=cur_top,
                out_top_ring=next_top,
                in_bot_ring=cur_bot,
                out_bot_ring=next_bot,
                ring_thetas=ring_thetas,
                r_ann_in=knots[idx_i],
                r_ann_out=r_next,
                z_bot_h=zb_cur,
                z_top_h=zt_cur,
                k_holes=k_holes,
                s_arc=s_arc,
                req_hole_diam_mm=float(body_cfg["lightening_hole_diameter_mm"]),
                resolution=res,
            )
        else:
            mb.add_quad_strip(cur_top, next_top, reverse=True)
            mb.add_quad_strip(cur_bot, next_bot, reverse=False)

        cur_top = next_top
        cur_bot = next_bot

        # Vertical Z step to next radial interval (or back to z=face_w / z=0 at r_safe_inner)
        zt_target = z_top_intervals[idx_i + 1] if (idx_i + 1) < n_intervals else face_w
        zb_target = z_bot_intervals[idx_i + 1] if (idx_i + 1) < n_intervals else 0.0

        if abs(zt_target - zt_cur) > 1e-5:
            step_top = mb.add_polar_ring(r_next, ring_thetas, zt_target)
            mb.add_quad_strip(cur_top, step_top, reverse=True)
            cur_top = step_top

        if abs(zb_target - zb_cur) > 1e-5:
            step_bot = mb.add_polar_ring(r_next, ring_thetas, zb_target)
            mb.add_quad_strip(cur_bot, step_bot, reverse=False)
            cur_bot = step_bot

    # Close outer rim from cur_top (at r_safe_inner, z=face_w) -> outer_rings[-1]
    # and cur_bot (at r_safe_inner, z=0) -> outer_rings[0] via angle-matched tooth collar circle
    r_tooth_collar = 0.5 * (r_safe_inner + r_outer_min)
    top_tooth_angs = np.arctan2(outer_xy_top[:, 1], outer_xy_top[:, 0])
    bot_tooth_angs = np.arctan2(outer_xy_bot[:, 1], outer_xy_bot[:, 0])

    top_tc_ring = mb.add_polar_ring(r_tooth_collar, top_tooth_angs, face_w)
    bot_tc_ring = mb.add_polar_ring(r_tooth_collar, bot_tooth_angs, 0.0)

    verts_xy_now = mb.get_vertices_array()[:, :2]
    mb.add_triangles(_mg_bridge_convex_loops_up(verts_xy_now, cur_top, top_tc_ring, (0.0, 0.0)))
    mb.add_triangles(_mg_bridge_convex_loops_up(verts_xy_now, cur_bot, bot_tc_ring, (0.0, 0.0))[:, [0, 2, 1]])

    mb.add_quad_strip(top_tc_ring, outer_rings[-1], reverse=True)
    mb.add_quad_strip(bot_tc_ring, outer_rings[0], reverse=False)

    # Close inner center (central bore tunnel or solid center fan)
    zt0 = z_top_intervals[0]
    zb0 = z_bot_intervals[0]
    if bore_xy is None:
        c_top = mb.add_vertex(0.0, 0.0, zt0)
        c_bot = mb.add_vertex(0.0, 0.0, zb0)
        mb.add_disk_fan(c_top, inner_top_ring, normal_up=True)
        mb.add_disk_fan(c_bot, inner_bot_ring, normal_up=False)
    else:
        bore_top_ring = mb.add_ring_2d(bore_xy, zt0)
        bore_bot_ring = mb.add_ring_2d(bore_xy, zb0)
        mb.add_quad_strip(bore_bot_ring, bore_top_ring, reverse=True)

        # Ray-matched intermediate circle guarantees zero inversion even on sharp keyway corners
        bore_angs = np.arctan2(bore_xy[:, 1], bore_xy[:, 0])
        r_bore_mid = 0.5 * (r_bore_max + knots[0])
        if knots[0] - r_bore_max >= 0.28:
            bmid_top = mb.add_polar_ring(r_bore_mid, bore_angs, zt0)
            bmid_bot = mb.add_polar_ring(r_bore_mid, bore_angs, zb0)
            mb.add_quad_strip(bore_top_ring, bmid_top, reverse=True)
            mb.add_quad_strip(bore_bot_ring, bmid_bot, reverse=False)
            verts_xy_all = mb.get_vertices_array()[:, :2]
            mb.add_triangles(_mg_bridge_convex_loops_up(verts_xy_all, bmid_top, inner_top_ring, (0.0, 0.0)))
            mb.add_triangles(
                _mg_bridge_convex_loops_up(verts_xy_all, bmid_bot, inner_bot_ring, (0.0, 0.0))[:, [0, 2, 1]]
            )
        else:
            verts_xy_all = mb.get_vertices_array()[:, :2]
            top_b_tris = _mg_triangulate_cell_2d(verts_xy_all, inner_top_ring.tolist(), [bore_top_ring.tolist()])
            mb.add_triangles(top_b_tris)
            bot_b_tris = _mg_triangulate_cell_2d(
                verts_xy_all, inner_bot_ring.tolist(), [bore_bot_ring.tolist()]
            )[:, [0, 2, 1]]
            mb.add_triangles(bot_b_tris)

    return mb.build(center_xy=False)


# ---------------------------------------------------------------------------
# Fit-Test Kit Generators (Sectors, 2-Pin Center Jig Base, 4-Hole Bore Gauge)
# ---------------------------------------------------------------------------


def _mg_compute_fit_pin_diameter(geom: dict[str, Any]) -> float:
    """Compute test-pin hole diameter (8.0 mm nominal, scaled cleanly for tiny gears)."""
    min_root_d = 2.0 * min(
        float(geom["pinion"]["root_radius_mm"]),
        float(geom["gear"]["root_radius_mm"]),
    )
    a = float(geom["center_distance_mm"])
    if min_root_d >= 9.0 and a >= 6.8:
        return max(4.0, min(8.0, 0.45 * min_root_d))
    return max(1.6, min(8.0, 0.45 * min_root_d, 0.58 * a))


def _mg_build_sector_2d_contour(
    full_contour: np.ndarray,
    z_teeth: int,
    sector_teeth: int,
    r_hub_out: float,
) -> np.ndarray:
    """Extract a 5-tooth arc sector and close around (0, 0) via flared radial spokes & circular back hub.

    Every point on the returned CCW contour has strictly increasing polar angle around (0, 0)
    and radius >= r_hub_out, enabling analytical 2-manifold bridging at arbitrary helix twist!
    """
    n_total = len(full_contour)
    pts_per_tooth = n_total // z_teeth

    # Centered 5-tooth slice around Tooth 0 (+X): teeth [-half .. +half]
    n_left = sector_teeth // 2
    n_right = sector_teeth - n_left  # e.g. for 5 teeth: 2 before tooth 0, plus teeth 0, 1, 2
    start_idx = (z_teeth - n_left) * pts_per_tooth
    end_idx = n_right * pts_per_tooth

    arc_pts = np.vstack((full_contour[start_idx:], full_contour[:end_idx]))

    # Unwrap start and end polar angles of the 5-tooth arc
    p_first = arc_pts[0]
    p_last = arc_pts[-1]
    r_first = math.hypot(float(p_first[0]), float(p_first[1]))
    r_last = math.hypot(float(p_last[0]), float(p_last[1]))

    ang_first = math.atan2(float(p_first[1]), float(p_first[0]))  # negative (~ -5*pi/Z)
    ang_last = math.atan2(float(p_last[1]), float(p_last[0]))    # positive (~ +5*pi/Z)
    while ang_last <= ang_first:
        ang_last += 2.0 * math.pi

    back_span = (ang_first + 2.0 * math.pi) - ang_last
    spoke_flare = min(0.14, 0.16 * back_span)

    # Left spoke: inward from (r_last, ang_last) -> (r_hub_out, ang_last + spoke_flare)
    n_spoke = 6
    u_sp = np.linspace(0.0, 1.0, n_spoke + 1, dtype=np.float64)[1:]
    left_angs = ang_last + u_sp * spoke_flare
    left_rads = r_last + u_sp * (r_hub_out - r_last)
    left_spoke_xy = np.column_stack((left_rads * np.cos(left_angs), left_rads * np.sin(left_angs)))

    # Circular back hub arc from (ang_last + spoke_flare) to (ang_first + 2*pi - spoke_flare)
    hub_a0 = ang_last + spoke_flare
    hub_a1 = ang_first + 2.0 * math.pi - spoke_flare
    n_hub_arc = max(24, int(round(36.0 * (hub_a1 - hub_a0) / math.pi)))
    hub_angs = np.linspace(hub_a0, hub_a1, n_hub_arc + 1, dtype=np.float64)[1:-1]
    hub_arc_xy = np.column_stack((r_hub_out * np.cos(hub_angs), r_hub_out * np.sin(hub_angs)))

    # Right spoke: outward from (r_hub_out, hub_a1) -> just before (r_first, ang_first + 2*pi)
    u_sp_r = np.linspace(0.0, 1.0, n_spoke + 1, dtype=np.float64)[:-1]
    right_angs = hub_a1 + u_sp_r * spoke_flare
    right_rads = r_hub_out + u_sp_r * (r_first - r_hub_out)
    right_spoke_xy = np.column_stack((right_rads * np.cos(right_angs), right_rads * np.sin(right_angs)))

    return np.vstack((arc_pts, left_spoke_xy, hub_arc_xy, right_spoke_xy))


def _mg_generate_sector_mesh(
    p: dict[str, Any],
    geom: dict[str, Any],
    which: str,
    d_pin_hole: float,
    sector_h: float,
) -> MeshData:
    """Build strict 2-manifold 5-tooth gear sector (or full gear when Z <= 8) with vertical test-pin bore."""
    body_key = "gear" if which == "gear" else "pinion"
    g_info = geom[body_key]
    z_teeth = int(g_info["teeth"])
    r_pin_hole = 0.5 * d_pin_hole

    # If Z <= 8, full gear with round test-pin bore drops straight onto the 2-pin center jig
    if z_teeth <= 8:
        p_full = normalize_params(p)
        p_full["face_width_mm"] = sector_h
        p_full[body_key]["bore_type"] = "round"
        p_full[body_key]["bore_diameter_mm"] = d_pin_hole
        p_full[body_key]["bore_clearance_mm"] = 0.0
        p_full[body_key]["hub_enabled"] = False
        p_full[body_key]["recess_enabled"] = False
        p_full[body_key]["lightening_mode"] = "solid"
        return generate_gear_mesh(p_full, which=body_key, resolution="high")

    m_n = float(geom["m_n"])
    beta_deg = float(geom["beta_deg"])
    gear_type = str(p["gear_type"])
    pitch_r = float(g_info["pitch_radius_mm"])
    root_r = float(g_info["root_radius_mm"])
    tip_r = float(g_info["tip_radius_mm"])
    hand = str(g_info["helix_hand"])

    chamfer = min(
        max(0.0, float(p["elephant_foot_chamfer_mm"])),
        0.20 * sector_h,
        0.28 * m_n,
        0.22 * max(0.2, tip_r - root_r),
    )
    if chamfer < 0.03:
        chamfer = 0.0

    p_sec = dict(p)
    p_sec["face_width_mm"] = sector_h

    full_std = build_gear_2d_contour(p_sec, which=body_key, samples_per_flank=10, radial_inset_mm=0.0)
    full_chm = (
        build_gear_2d_contour(p_sec, which=body_key, samples_per_flank=10, radial_inset_mm=chamfer)
        if chamfer > 0.0
        else full_std
    )

    r_root_eff = float(np.min(np.hypot(full_chm[:, 0], full_chm[:, 1])))
    hub_wall = max(2.2, min(4.0, 0.45 * (r_root_eff - r_pin_hole)))
    r_hub_out = min(r_root_eff - 0.5, r_pin_hole + max(1.0, hub_wall))
    r_hub_out_chm = max(r_pin_hole + 0.65, r_hub_out - 0.5 * chamfer)

    sec_teeth = min(5, z_teeth)
    sec_std = _mg_build_sector_2d_contour(full_std, z_teeth, sec_teeth, r_hub_out)
    sec_chm = (
        _mg_build_sector_2d_contour(full_chm, z_teeth, sec_teeth, r_hub_out_chm)
        if chamfer > 0.0
        else sec_std
    )

    z_levels, insets = _mg_build_outer_z_schedule(
        face_width_mm=sector_h,
        beta_deg=beta_deg,
        gear_type=gear_type,
        chamfer_mm=chamfer,
        resolution="high",
    )

    mb = _GearMeshBuilder()
    outer_rings: list[np.ndarray] = []
    bot_xy: np.ndarray | None = None
    top_xy: np.ndarray | None = None

    for idx_z, (zv, ins) in enumerate(zip(z_levels, insets)):
        c_xy = sec_chm if ins > 0.0 else sec_std
        psi = helix_twist_angle_rad(zv, sector_h, pitch_r, beta_deg, hand, gear_type)
        r_xy = _mg_rotate_2d(c_xy, psi)
        if idx_z == 0:
            bot_xy = r_xy
        if idx_z == len(z_levels) - 1:
            top_xy = r_xy
        outer_rings.append(mb.add_ring_2d(r_xy, zv))

    mb.add_tube_grid(outer_rings, reverse=False)
    assert bot_xy is not None and top_xy is not None

    # Central vertical pin hole + ray-matched collar ring for twist-proof positive triangles
    m_pin = 48
    pin_bot = mb.add_circle_ring(0.0, 0.0, r_pin_hole, 0.0, m_pin)
    pin_top = mb.add_circle_ring(0.0, 0.0, r_pin_hole, sector_h, m_pin)
    mb.add_quad_strip(pin_bot, pin_top, reverse=True)

    r_min_outer = float(
        min(
            np.min(np.hypot(bot_xy[:, 0], bot_xy[:, 1])),
            np.min(np.hypot(top_xy[:, 0], top_xy[:, 1])),
        )
    )
    r_collar = 0.5 * (r_pin_hole + r_min_outer)
    bot_angs = np.arctan2(bot_xy[:, 1], bot_xy[:, 0])
    top_angs = np.arctan2(top_xy[:, 1], top_xy[:, 0])

    col_bot = mb.add_polar_ring(r_collar, bot_angs, 0.0)
    col_top = mb.add_polar_ring(r_collar, top_angs, sector_h)

    verts_xy = mb.get_vertices_array()[:, :2]
    mb.add_triangles(_mg_bridge_convex_loops_up(verts_xy, pin_top, col_top, (0.0, 0.0)))
    mb.add_triangles(_mg_bridge_convex_loops_up(verts_xy, pin_bot, col_bot, (0.0, 0.0))[:, [0, 2, 1]])

    mb.add_quad_strip(col_top, outer_rings[-1], reverse=True)
    mb.add_quad_strip(col_bot, outer_rings[0], reverse=False)

    return mb.build(center_xy=True)


def _mg_generate_center_jig_base(
    geom: dict[str, Any],
    d_pin_hole: float,
    sector_h: float,
) -> MeshData:
    """Build strict 2-manifold rounded-rectangle base plate with two integral slip-fit pins (genus == 0)."""
    a = float(geom["center_distance_mm"])
    slip_clearance = min(0.22, 0.08 * d_pin_hole)
    r_pin = max(0.6, 0.5 * (d_pin_hole - slip_clearance))

    z_plate = 3.0
    pin_h = sector_h + 1.5
    z_pin_top = z_plate + pin_h
    pin_chamfer = min(0.6, 0.30 * r_pin, 0.25 * pin_h)

    r_pad = max(r_pin + 4.2, 8.0)
    hx = 0.5 * a + r_pad
    hy = r_pad
    rc = min(5.5, 0.45 * hy)

    # Half-perimeters split cleanly at x == 0 so left & right pin cells are 100% convex D-regions
    n_corner = 8
    n_horiz = 6
    n_vert = 5

    # Right half CCW from (0, -hy) -> (+hx, -hy) -> (+hx, +hy) -> (0, +hy)
    rx_bot_edge = np.linspace(0.0, hx - rc, n_horiz + 1, dtype=np.float64)[1:-1]
    right_pts_list: list[tuple[float, float]] = [(float(x), -hy) for x in rx_bot_edge]

    ang_br = np.linspace(-0.5 * math.pi, 0.0, n_corner, dtype=np.float64)
    for ang in ang_br:
        right_pts_list.append((hx - rc + rc * math.cos(ang), -hy + rc + rc * math.sin(ang)))

    ry_side = np.linspace(-hy + rc, hy - rc, n_vert + 1, dtype=np.float64)[1:-1]
    for y in ry_side:
        right_pts_list.append((hx, float(y)))

    ang_tr = np.linspace(0.0, 0.5 * math.pi, n_corner, dtype=np.float64)
    for ang in ang_tr:
        right_pts_list.append((hx - rc + rc * math.cos(ang), hy - rc + rc * math.sin(ang)))

    rx_top_edge = np.linspace(hx - rc, 0.0, n_horiz + 1, dtype=np.float64)[1:-1]
    for x in rx_top_edge:
        right_pts_list.append((float(x), hy))

    right_xy = np.asarray(right_pts_list, dtype=np.float64)
    # Left half is exact 180-degree rotation (-x, -y) of right_xy
    left_xy = -right_xy

    mb = _GearMeshBuilder()

    # Plate bottom perimeter at Z = 0.0
    bot_pole_b = mb.add_vertex(0.0, -hy, 0.0)
    right_arc_b = mb.add_ring_2d(right_xy, 0.0)
    top_pole_b = mb.add_vertex(0.0, hy, 0.0)
    left_arc_b = mb.add_ring_2d(left_xy, 0.0)
    plate_bot = np.concatenate((
        np.array([bot_pole_b], dtype=np.int32),
        right_arc_b,
        np.array([top_pole_b], dtype=np.int32),
        left_arc_b,
    ))

    # Plate top perimeter at Z = z_plate
    bot_pole_t = mb.add_vertex(0.0, -hy, z_plate)
    right_arc_t = mb.add_ring_2d(right_xy, z_plate)
    top_pole_t = mb.add_vertex(0.0, hy, z_plate)
    left_arc_t = mb.add_ring_2d(left_xy, z_plate)
    plate_top = np.concatenate((
        np.array([bot_pole_t], dtype=np.int32),
        right_arc_t,
        np.array([top_pole_t], dtype=np.int32),
        left_arc_t,
    ))

    # Outer plate vertical wall & solid convex bottom fan
    mb.add_quad_strip(plate_bot, plate_top, reverse=False)
    c_bot = mb.add_vertex(0.0, 0.0, 0.0)
    mb.add_disk_fan(c_bot, plate_bot, normal_up=False)

    # Interior seam along x == 0 on top deck (from -hy to +hy)
    seam_ys = np.linspace(-hy, hy, 9, dtype=np.float64)[1:-1]
    seam_top = mb.add_ring_2d(np.column_stack((np.zeros_like(seam_ys), seam_ys)), z_plate)

    right_cell = [bot_pole_t, *right_arc_t.tolist(), top_pole_t, *seam_top[::-1].tolist()]
    left_cell = [top_pole_t, *left_arc_t.tolist(), bot_pole_t, *seam_top.tolist()]

    m_pin = 40
    pin_r_base = mb.add_circle_ring(+0.5 * a, 0.0, r_pin, z_plate, m_pin)
    pin_l_base = mb.add_circle_ring(-0.5 * a, 0.0, r_pin, z_plate, m_pin)

    verts_xy = mb.get_vertices_array()[:, :2]
    mb.add_triangles(_mg_bridge_convex_loops_up(verts_xy, pin_r_base, right_cell, (+0.5 * a, 0.0)))
    mb.add_triangles(_mg_bridge_convex_loops_up(verts_xy, pin_l_base, left_cell, (-0.5 * a, 0.0)))

    for cx, base_ring in ((+0.5 * a, pin_r_base), (-0.5 * a, pin_l_base)):
        cyl_top = mb.add_circle_ring(cx, 0.0, r_pin, z_pin_top - pin_chamfer, m_pin)
        tip_ring = mb.add_circle_ring(cx, 0.0, r_pin - pin_chamfer, z_pin_top, m_pin)
        mb.add_tube_grid([base_ring, cyl_top, tip_ring], reverse=False)
        tip_c = mb.add_vertex(cx, 0.0, z_pin_top)
        mb.add_disk_fan(tip_c, tip_ring, normal_up=True)

    return mb.build(center_xy=False)


def _mg_generate_bore_fit_gauge(p: dict[str, Any]) -> MeshData:
    """Build strict 2-manifold 4-hole bore calibration strip with 1..4 V-notch markers (genus == 4)."""
    bore_cfg = dict(p["pinion"])
    if str(bore_cfg.get("bore_type", "round")).strip().lower() == "none":
        bore_cfg["bore_type"] = "round"

    nom_d = float(bore_cfg["bore_diameter_mm"])
    if nom_d > 24.0:
        bore_cfg["bore_diameter_mm"] = 24.0
        nom_d = 24.0
    max_r = max(2.0, 0.5 * nom_d + 2.5)

    extra_clearances = (-0.05, 0.00, +0.05, +0.10)
    local_holes: list[np.ndarray] = []
    for delta_c in extra_clearances:
        hc = build_bore_2d_contour(
            bore_cfg,
            max_allowed_radius_mm=max_r,
            radial_samples=48,
            extra_clearance_mm=delta_c,
        )
        assert hc is not None
        local_holes.append(hc)

    r_hole_max = max(float(np.max(np.hypot(h[:, 0], h[:, 1]))) for h in local_holes)
    cell_w = max(2.0 * r_hole_max + 5.0, 12.0)
    hy = max(r_hole_max + 4.5, 7.5)
    z_h = 5.0

    x_splits = [-2.0 * cell_w, -1.0 * cell_w, 0.0, +1.0 * cell_w, +2.0 * cell_w]
    centers_x = [(-1.5 + float(i)) * cell_w for i in range(4)]

    # Build front (-Y) edge segments for each of the 4 cells with (i + 1) crisp V-notches
    notch_half_w = 0.55
    notch_depth = 0.85
    notch_pitch = 1.9

    front_interiors_xy: list[np.ndarray] = []
    top_interiors_xy: list[np.ndarray] = []
    for i in range(4):
        x0 = x_splits[i]
        x1 = x_splits[i + 1]
        cx = centers_x[i]
        n_notches = i + 1
        span_n = (n_notches - 1) * notch_pitch
        pts_f: list[tuple[float, float]] = []
        for idx_n in range(n_notches):
            nx = cx - 0.5 * span_n + idx_n * notch_pitch
            pts_f.append((nx - notch_half_w, -hy))
            pts_f.append((nx, -hy + notch_depth))
            pts_f.append((nx + notch_half_w, -hy))
        front_interiors_xy.append(np.asarray(pts_f, dtype=np.float64))

        tx = np.linspace(x1, x0, 6, dtype=np.float64)[1:-1]
        top_interiors_xy.append(np.column_stack((tx, np.full_like(tx, hy))))

    vert_ys = np.linspace(-hy, hy, 7, dtype=np.float64)[1:-1]

    mb = _GearMeshBuilder()

    # Vertical split lines x_splits[0..4] (from y = -hy up to y = +hy) on Z = 0 and Z = z_h
    vlines_top: list[np.ndarray] = []
    vlines_bot: list[np.ndarray] = []
    for xs in x_splits:
        col_xy = np.column_stack((
            np.full(len(vert_ys) + 2, xs, dtype=np.float64),
            np.concatenate(([-hy], vert_ys, [hy])),
        ))
        vlines_top.append(mb.add_ring_2d(col_xy, z_h))
        vlines_bot.append(mb.add_ring_2d(col_xy, 0.0))

    front_top_segs: list[np.ndarray] = []
    front_bot_segs: list[np.ndarray] = []
    back_top_segs: list[np.ndarray] = []
    back_bot_segs: list[np.ndarray] = []
    hole_top_rings: list[np.ndarray] = []
    hole_bot_rings: list[np.ndarray] = []

    for i in range(4):
        front_top_segs.append(mb.add_ring_2d(front_interiors_xy[i], z_h))
        front_bot_segs.append(mb.add_ring_2d(front_interiors_xy[i], 0.0))
        back_top_segs.append(mb.add_ring_2d(top_interiors_xy[i], z_h))
        back_bot_segs.append(mb.add_ring_2d(top_interiors_xy[i], 0.0))

        h_xy = local_holes[i].copy()
        h_xy[:, 0] += centers_x[i]
        ht = mb.add_ring_2d(h_xy, z_h)
        hb = mb.add_ring_2d(h_xy, 0.0)
        mb.add_quad_strip(hb, ht, reverse=True)
        hole_top_rings.append(ht)
        hole_bot_rings.append(hb)

    # Full CCW outer perimeter of strip (for vertical outer wall)
    def _full_strip_perimeter(is_top: bool) -> np.ndarray:
        vl = vlines_top if is_top else vlines_bot
        fs = front_top_segs if is_top else front_bot_segs
        bs = back_top_segs if is_top else back_bot_segs

        seq: list[int] = []
        # Bottom (-Y) edge from x_splits[0] -> x_splits[4]
        for i in range(4):
            seq.append(int(vl[i][0]))
            seq.extend(fs[i].tolist())
        # Right (+X) edge from -hy -> +hy (excluding top corner added next)
        seq.extend(vl[4][:-1].tolist())
        # Top (+Y) edge from x_splits[4] -> x_splits[0]
        for i in range(3, -1, -1):
            seq.append(int(vl[i + 1][-1]))
            seq.extend(bs[i].tolist())
        # Left (-X) edge from +hy -> just above -hy
        seq.extend(vl[0][::-1][:-1].tolist())
        return np.asarray(seq, dtype=np.int32)

    outer_perim_bot = _full_strip_perimeter(False)
    outer_perim_top = _full_strip_perimeter(True)
    mb.add_quad_strip(outer_perim_bot, outer_perim_top, reverse=False)

    # Triangulate each of the 4 cells on Z = z_h (+Z) and Z = 0.0 (-Z)
    verts_xy = mb.get_vertices_array()[:, :2]
    for i in range(4):
        cell_top = [
            int(vlines_top[i][0]),
            *front_top_segs[i].tolist(),
            *vlines_top[i + 1][:-1].tolist(),
            int(vlines_top[i + 1][-1]),
            *back_top_segs[i].tolist(),
            *vlines_top[i][::-1][:-1].tolist(),
        ]
        cell_bot = [
            int(vlines_bot[i][0]),
            *front_bot_segs[i].tolist(),
            *vlines_bot[i + 1][:-1].tolist(),
            int(vlines_bot[i + 1][-1]),
            *back_bot_segs[i].tolist(),
            *vlines_bot[i][::-1][:-1].tolist(),
        ]

        local_ids = cell_top + hole_top_rings[i].tolist()
        local_xy = verts_xy[local_ids]
        nc = len(cell_top)
        nh = len(hole_top_rings[i])
        local_tris = _mg_triangulate_cell_2d(
            local_xy,
            list(range(nc)),
            [list(range(nc, nc + nh))],
        )

        map_top = np.asarray(local_ids, dtype=np.int32)
        map_bot = np.asarray(cell_bot + hole_bot_rings[i].tolist(), dtype=np.int32)
        mb.add_triangles(map_top[local_tris])
        mb.add_triangles(map_bot[local_tris][:, [0, 2, 1]])

    return mb.build(center_xy=False)


def generate_fit_test_kit(params: dict[str, Any]) -> dict[str, MeshData]:
    """Generate the 4-piece 10-minute FDM Fit-Test Kit (sectors, 2-pin center jig, 4-hole bore gauge)."""
    p = normalize_params(params)
    geom = compute_gear_pair_geometry(p)
    d_pin_hole = _mg_compute_fit_pin_diameter(geom)
    sector_h = min(float(p["face_width_mm"]), 8.0)

    sector_pinion = _mg_generate_sector_mesh(p, geom, "pinion", d_pin_hole, sector_h)
    sector_gear = _mg_generate_sector_mesh(p, geom, "gear", d_pin_hole, sector_h)
    center_jig_base = _mg_generate_center_jig_base(geom, d_pin_hole, sector_h)
    bore_fit_gauge = _mg_generate_bore_fit_gauge(p)

    return {
        "sector_pinion": sector_pinion,
        "sector_gear": sector_gear,
        "center_jig_base": center_jig_base,
        "bore_fit_gauge": bore_fit_gauge,
    }


def collect_target_meshes(
    params: dict[str, Any],
    target: str | None = None,
    lang: str = "pt",
) -> list[tuple[str, MeshData]]:
    """Build localized `(name, MeshData)` export list for the requested export_target."""
    p = normalize_params(params)
    resolved_target = str(target or p.get("export_target") or "pair_separated").strip().lower()
    is_en = str(lang).strip().lower().startswith("en")

    pinion_name = "Pinion_G1" if is_en else "Pinhao_G1"
    gear_name = "Gear_G2" if is_en else "Coroa_G2"
    sec_pinion_name = "FitSector_Pinion_G1" if is_en else "SetorTeste_Pinhao_G1"
    sec_gear_name = "FitSector_Gear_G2" if is_en else "SetorTeste_Coroa_G2"
    jig_name = "CenterJig_Base" if is_en else "BaseGabarito_2Pinos"
    gauge_name = "BoreFit_Gauge" if is_en else "ReguaCalibracao_Eixo"

    if resolved_target == "pinion_only":
        return [(pinion_name, generate_gear_mesh(p, which="pinion", resolution="high"))]

    if resolved_target == "gear_only":
        return [(gear_name, generate_gear_mesh(p, which="gear", resolution="high"))]

    if resolved_target == "fit_test_kit":
        kit = generate_fit_test_kit(p)
        return [
            (sec_pinion_name, kit["sector_pinion"]),
            (sec_gear_name, kit["sector_gear"]),
            (jig_name, kit["center_jig_base"]),
            (gauge_name, kit["bore_fit_gauge"]),
        ]

    if resolved_target == "full_suite":
        geom = compute_gear_pair_geometry(p)
        d_pin_hole = _mg_compute_fit_pin_diameter(geom)
        sector_h = min(float(p["face_width_mm"]), 8.0)
        return [
            (pinion_name, generate_gear_mesh(p, which="pinion", resolution="high")),
            (gear_name, generate_gear_mesh(p, which="gear", resolution="high")),
            (jig_name, _mg_generate_center_jig_base(geom, d_pin_hole, sector_h)),
            (gauge_name, _mg_generate_bore_fit_gauge(p)),
        ]

    # Default: "pair_separated"
    return [
        (pinion_name, generate_gear_mesh(p, which="pinion", resolution="high")),
        (gear_name, generate_gear_mesh(p, which="gear", resolution="high")),
    ]
