"""Contact ratio, 2D polygon interference/jamming detection, kinematics, and FDM printability."""

from __future__ import annotations

import math
from typing import Any

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
        build_gear_2d_contour,
        compute_gear_pair_geometry,
        involute_fn,
    )

PLA_DENSITY_G_CM3: float = 1.24


def _ctx_float(ctx: dict[str, Any], key: str, default: float, lo: float, hi: float) -> float:
    val = ctx.get(key, default)
    if isinstance(val, (list, tuple)) and len(val) > 0:
        val = val[0]
    if isinstance(val, str):
        val = val.strip().rstrip("%mM ").strip()
    try:
        f = float(val)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(f) or f <= 0.0:
        return default
    return max(lo, min(hi, f))


def _rotate_2d(pts: np.ndarray, angle_rad: float) -> np.ndarray:
    c = math.cos(angle_rad)
    s = math.sin(angle_rad)
    out = np.empty_like(pts)
    out[:, 0] = pts[:, 0] * c - pts[:, 1] * s
    out[:, 1] = pts[:, 0] * s + pts[:, 1] * c
    return out


def _points_inside_star_ccw_polygon(
    query_pts: np.ndarray,
    poly_centered: np.ndarray,
) -> np.ndarray:
    """Return boolean mask of query_pts (in same local frame as poly_centered) strictly inside CCW star polygon."""
    if len(query_pts) == 0:
        return np.zeros(0, dtype=bool)

    angles = np.arctan2(poly_centered[:, 1], poly_centered[:, 0])
    start_idx = int(np.argmin(angles))
    p_rot = np.roll(poly_centered, -start_idx, axis=0)
    a_rot = np.roll(angles, -start_idx)

    # Ensure monotonic non-decreasing angles (handle tiny wrap numerical jitter if any)
    q_ang = np.arctan2(query_pts[:, 1], query_pts[:, 0])
    idx_hi = np.searchsorted(a_rot, q_ang, side="right")
    n = len(p_rot)
    i0 = (idx_hi - 1) % n
    i1 = idx_hi % n

    v0 = p_rot[i0]
    v1 = p_rot[i1]
    ex = v1[:, 0] - v0[:, 0]
    ey = v1[:, 1] - v0[:, 1]
    qx = query_pts[:, 0] - v0[:, 0]
    qy = query_pts[:, 1] - v0[:, 1]

    # For CCW star polygon around (0, 0), origin lies strictly on the left (cross > 0) of every edge v0 -> v1
    cross = ex * qy - ey * qx
    edge_len = np.hypot(ex, ey) + 1e-12
    signed_inward = cross / edge_len
    return signed_inward > 1e-6


def _point_to_segments_min_dist(pts: np.ndarray, s0: np.ndarray, s1: np.ndarray) -> np.ndarray:
    """Return (P,) array of minimum Euclidean distance from each point in `pts` (P, 2) to segments s0->s1 (S, 2)."""
    if len(pts) == 0 or len(s0) == 0:
        return np.full(len(pts), float("inf"), dtype=np.float64)

    seg_v = s1 - s0  # (S, 2)
    seg_len_sq = np.sum(seg_v * seg_v, axis=1)  # (S,)
    safe_len_sq = np.where(seg_len_sq > 1e-18, seg_len_sq, 1.0)

    # diff: (P, S, 2)
    diff = pts[:, None, :] - s0[None, :, :]
    t = (diff[:, :, 0] * seg_v[None, :, 0] + diff[:, :, 1] * seg_v[None, :, 1]) / safe_len_sq[None, :]
    t = np.clip(t, 0.0, 1.0)

    proj_x = s0[None, :, 0] + t * seg_v[None, :, 0]
    proj_y = s0[None, :, 1] + t * seg_v[None, :, 1]
    dx = pts[:, None, 0] - proj_x
    dy = pts[:, None, 1] - proj_y
    dist_sq = dx * dx + dy * dy
    return np.sqrt(np.min(dist_sq, axis=1))


def _segments_intersect_any(a0: np.ndarray, a1: np.ndarray, b0: np.ndarray, b1: np.ndarray) -> bool:
    """Vectorized 2D segment-segment intersection test between A (M1, 2) and B (M2, 2)."""
    if len(a0) == 0 or len(b0) == 0:
        return False

    # Bounding-box reject first
    a_min_x = np.minimum(a0[:, 0], a1[:, 0])[:, None]
    a_max_x = np.maximum(a0[:, 0], a1[:, 0])[:, None]
    b_min_x = np.minimum(b0[:, 0], b1[:, 0])[None, :]
    b_max_x = np.maximum(b0[:, 0], b1[:, 0])[None, :]

    a_min_y = np.minimum(a0[:, 1], a1[:, 1])[:, None]
    a_max_y = np.maximum(a0[:, 1], a1[:, 1])[:, None]
    b_min_y = np.minimum(b0[:, 1], b1[:, 1])[None, :]
    b_max_y = np.maximum(b0[:, 1], b1[:, 1])[None, :]

    bbox_hit = (a_max_x >= b_min_x - 1e-9) & (b_max_x >= a_min_x - 1e-9) & (
        a_max_y >= b_min_y - 1e-9
    ) & (b_max_y >= a_min_y - 1e-9)
    if not np.any(bbox_hit):
        return False

    ia, ib = np.nonzero(bbox_hit)
    pa0 = a0[ia]
    pa1 = a1[ia]
    pb0 = b0[ib]
    pb1 = b1[ib]

    da = pa1 - pa0
    db = pb1 - pb0

    def _cross2(u: np.ndarray, v: np.ndarray) -> np.ndarray:
        return u[:, 0] * v[:, 1] - u[:, 1] * v[:, 0]

    c1 = _cross2(da, pb0 - pa0)
    c2 = _cross2(da, pb1 - pa0)
    c3 = _cross2(db, pa0 - pb0)
    c4 = _cross2(db, pa1 - pb0)

    proper = (c1 * c2 < -1e-16) & (c3 * c4 < -1e-16)
    return bool(np.any(proper))


def evaluate_meshed_2d_clearance(
    params: dict[str, Any],
    steps: int = 9,
) -> dict[str, Any]:
    """Evaluate real 2D polygon clearance & collision between meshed G1 and G2 across sub-pitch steps."""
    p = normalize_params(params)
    geom = compute_gear_pair_geometry(p)

    z1 = int(geom["pinion"]["teeth"])
    z2 = int(geom["gear"]["teeth"])
    a = float(geom["center_distance_mm"])
    phase2 = float(geom["mesh_phase_g2_rad"])
    ra1 = float(geom["pinion"]["tip_radius_mm"])
    ra2 = float(geom["gear"]["tip_radius_mm"])
    m_t = float(geom["m_t"])

    if a >= ra1 + ra2 + 1e-6:
        sep = a - (ra1 + ra2)
        return {
            "min_clearance_mm": sep,
            "collision_detected": False,
            "disengaged": True,
        }

    poly1_base = build_gear_2d_contour(p, "pinion", samples_per_flank=11, radial_inset_mm=0.0)
    poly2_base = build_gear_2d_contour(p, "gear", samples_per_flank=11, radial_inset_mm=0.0)

    n_steps = max(3, int(steps))
    pitch_angle_1 = (2.0 * math.pi) / float(z1)

    min_signed_clearance = float("inf")
    any_collision = False

    cull_r2_sq = (ra2 + 2.5 * m_t) ** 2
    cull_r1_sq = (ra1 + 2.5 * m_t) ** 2

    for k in range(n_steps):
        theta1 = (float(k) / float(n_steps)) * pitch_angle_1
        phi2 = phase2 - theta1 * (float(z1) / float(z2))

        p1 = _rotate_2d(poly1_base, theta1)
        p2_centered = _rotate_2d(poly2_base, phi2)
        p2 = p2_centered.copy()
        p2[:, 0] += a

        a0 = p1
        a1 = np.roll(p1, -1, axis=0)
        b0 = p2
        b1 = np.roll(p2, -1, axis=0)

        # Cull to segments near the meshing zone between (0, 0) and (a, 0)
        d1_to_g2_sq = np.minimum(
            (a0[:, 0] - a) ** 2 + a0[:, 1] ** 2,
            (a1[:, 0] - a) ** 2 + a1[:, 1] ** 2,
        )
        d2_to_g1_sq = np.minimum(
            b0[:, 0] ** 2 + b0[:, 1] ** 2,
            b1[:, 0] ** 2 + b1[:, 1] ** 2,
        )

        act_a = d1_to_g2_sq <= cull_r2_sq
        act_b = d2_to_g1_sq <= cull_r1_sq
        if not (np.any(act_a) and np.any(act_b)):
            continue

        aa0 = a0[act_a]
        aa1 = a1[act_a]
        bb0 = b0[act_b]
        bb1 = b1[act_b]

        # Test vertices + edge midpoints for penetration into opposing star polygon
        cand1 = np.vstack((aa0, 0.5 * (aa0 + aa1)))
        cand1_in_g2_frame = cand1.copy()
        cand1_in_g2_frame[:, 0] -= a
        cand1_near = (
            cand1_in_g2_frame[:, 0] ** 2 + cand1_in_g2_frame[:, 1] ** 2
        ) < (ra2 * ra2)
        in_g2_mask = np.zeros(len(cand1), dtype=bool)
        if np.any(cand1_near):
            in_g2_mask[cand1_near] = _points_inside_star_ccw_polygon(
                cand1_in_g2_frame[cand1_near], p2_centered
            )

        cand2 = np.vstack((bb0, 0.5 * (bb0 + bb1)))
        cand2_near = (cand2[:, 0] ** 2 + cand2[:, 1] ** 2) < (ra1 * ra1)
        in_g1_mask = np.zeros(len(cand2), dtype=bool)
        if np.any(cand2_near):
            in_g1_mask[cand2_near] = _points_inside_star_ccw_polygon(cand2[cand2_near], p1)

        seg_cross = _segments_intersect_any(aa0, aa1, bb0, bb1)

        if seg_cross or np.any(in_g2_mask) or np.any(in_g1_mask):
            any_collision = True
            pen_d = 1e-4
            if np.any(in_g2_mask):
                d_pen1 = _point_to_segments_min_dist(cand1[in_g2_mask], bb0, bb1)
                pen_d = max(pen_d, float(np.max(d_pen1)))
            if np.any(in_g1_mask):
                d_pen2 = _point_to_segments_min_dist(cand2[in_g1_mask], aa0, aa1)
                pen_d = max(pen_d, float(np.max(d_pen2)))
            step_clear = -pen_d
        else:
            d_ab = _point_to_segments_min_dist(aa0, bb0, bb1)
            d_ba = _point_to_segments_min_dist(bb0, aa0, aa1)
            step_clear = min(float(np.min(d_ab)), float(np.min(d_ba)))

        if step_clear < min_signed_clearance:
            min_signed_clearance = step_clear

    if not math.isfinite(min_signed_clearance):
        min_signed_clearance = max(0.0, a - (ra1 + ra2))

    return {
        "min_clearance_mm": min_signed_clearance,
        "collision_detected": any_collision,
        "disengaged": False,
    }


def _estimate_single_gear_volume_cm3(
    body_cfg: dict[str, Any],
    g_geom: dict[str, Any],
    face_w_mm: float,
) -> float:
    """Analytical volume estimate (cm^3) used when pre-built MeshData objects are not passed in."""
    r_pitch = float(g_geom["pitch_radius_mm"])
    r_root = float(g_geom["root_radius_mm"])
    area_gear = math.pi * (r_pitch * r_pitch)

    if str(body_cfg["bore_type"]) != "none":
        r_bore = 0.5 * (float(body_cfg["bore_diameter_mm"]) + float(body_cfg["bore_clearance_mm"]))
        r_bore = min(r_bore, 0.85 * r_root)
        area_bore = math.pi * (r_bore * r_bore)
    else:
        r_bore = 0.0
        area_bore = 0.0

    vol_mm3 = max(10.0, (area_gear - area_bore) * face_w_mm)

    if body_cfg["hub_enabled"]:
        r_hub = min(0.5 * float(body_cfg["hub_diameter_mm"]), 0.90 * r_root)
        if r_hub > r_bore + 0.5:
            vol_mm3 += math.pi * (r_hub * r_hub - r_bore * r_bore) * float(body_cfg["hub_height_mm"])

    if body_cfg["recess_enabled"]:
        r_rec = min(0.5 * float(body_cfg["recess_diameter_mm"]), 0.88 * r_root)
        if r_rec > r_bore + 0.4:
            depth = min(float(body_cfg["recess_depth_mm"]), 0.42 * face_w_mm)
            sides = 2.0 if body_cfg["recess_side"] == "both" else 1.0
            vol_mm3 -= sides * math.pi * (r_rec * r_rec - r_bore * r_bore) * depth

    l_mode = str(body_cfg["lightening_mode"])
    r_web_in = max(r_bore + 2.0, 0.32 * r_root)
    r_web_out = 0.82 * r_root
    if l_mode == "web_recess" and r_web_out > r_web_in + 1.5:
        pocket_h = max(0.0, face_w_mm - float(body_cfg["web_thickness_mm"]))
        vol_mm3 -= math.pi * (r_web_out * r_web_out - r_web_in * r_web_in) * pocket_h
    elif l_mode == "lightening_holes" and r_web_out > r_web_in + 2.0:
        k_holes = int(body_cfg["lightening_hole_count"])
        r_hole = min(0.5 * float(body_cfg["lightening_hole_diameter_mm"]), 0.42 * (r_web_out - r_web_in))
        if r_hole > 0.5:
            vol_mm3 -= float(k_holes) * math.pi * (r_hole * r_hole) * face_w_mm

    return max(0.05, vol_mm3 / 1000.0)


def analyze_gear_pair(
    params: dict[str, Any],
    host_context: dict[str, Any] | None = None,
    meshes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Comprehensive engineering & FDM printability diagnostics for the parametric gear pair."""
    p = normalize_params(params)
    ctx = host_context if isinstance(host_context, dict) else {}
    geom = compute_gear_pair_geometry(p)

    bed_x = _ctx_float(ctx, "bed_x", 220.0, 50.0, 2000.0)
    bed_y = _ctx_float(ctx, "bed_y", 220.0, 50.0, 2000.0)
    line_w = _ctx_float(ctx, "line_width_mm", 0.42, 0.15, 2.5)
    layer_h = _ctx_float(ctx, "layer_height_mm", 0.20, 0.05, 1.0)

    gear_type = str(p["gear_type"])
    beta_deg = effective_helix_angle_deg(p)
    beta_rad = math.radians(beta_deg)
    cos_beta = math.cos(beta_rad)
    sin_beta = math.sin(beta_rad)

    m_n = float(geom["m_n"])
    m_t = float(geom["m_t"])
    alpha_t_rad = math.radians(float(geom["alpha_t_deg"]))
    cos_alpha_t = math.cos(alpha_t_rad)

    z1 = int(geom["pinion"]["teeth"])
    z2 = int(geom["gear"]["teeth"])
    z_sum = float(z1 + z2)

    a0 = float(geom["nominal_center_distance_mm"])
    a = float(geom["center_distance_mm"])
    min_non_jam_a = float(geom["min_non_jam_center_distance_mm"])
    delta_a = a - a0

    rb1 = float(geom["pinion"]["base_radius_mm"])
    rb2 = float(geom["gear"]["base_radius_mm"])
    ra1 = float(geom["pinion"]["tip_radius_mm"])
    ra2 = float(geom["gear"]["tip_radius_mm"])
    rf1 = float(geom["pinion"]["root_radius_mm"])
    rf2 = float(geom["gear"]["root_radius_mm"])
    rw1 = float(geom["pinion"]["working_pitch_radius_mm"])
    psi_b1 = float(geom["pinion"]["base_half_angle_rad"])
    psi_b2 = float(geom["gear"]["base_half_angle_rad"])
    face_w = float(p["face_width_mm"])

    # Operating pressure angle at actual center distance a
    cos_alpha_op = max(0.0, min(1.0, (rb1 + rb2) / max(1e-6, a)))
    alpha_op_rad = math.acos(cos_alpha_op)
    sin_alpha_op = math.sin(alpha_op_rad)
    tan_alpha_op = math.tan(alpha_op_rad) if cos_alpha_op > 1e-5 else 0.0

    # 1. Contact Ratios (ISO 21771)
    t1t2_len = a * sin_alpha_op
    disengaged = bool(a >= ra1 + ra2 - 1e-5)

    if disengaged:
        g_alpha = 0.0
        involute_base_interference = False
    else:
        seg_g1 = math.sqrt(max(0.0, ra1 * ra1 - rb1 * rb1))
        seg_g2 = math.sqrt(max(0.0, ra2 * ra2 - rb2 * rb2))
        # Base-tangent interference occurs if mating tip reaches beyond tangent point T1 or T2
        involute_base_interference = bool(
            (seg_g1 > t1t2_len + 0.02 * m_n) or (seg_g2 > t1t2_len + 0.02 * m_n)
        )
        g_alpha = max(0.0, min(seg_g1, t1t2_len) + min(seg_g2, t1t2_len) - t1t2_len)

    p_bt = math.pi * m_t * cos_alpha_t
    eps_alpha = g_alpha / max(1e-6, p_bt)

    if gear_type == "spur" or beta_deg <= 1e-6:
        eps_beta = 0.0
    elif gear_type == "herringbone":
        eps_beta = (0.5 * face_w * sin_beta) / (math.pi * m_n)
    else:
        eps_beta = (face_w * sin_beta) / (math.pi * m_n)

    eps_gamma = eps_alpha + eps_beta

    # 2. Fit, Backlash & Real 2D Polygon Clearance
    j_wt = (2.0 * a / z_sum) * (
        math.pi - float(z1) * psi_b1 - float(z2) * psi_b2 + z_sum * involute_fn(alpha_op_rad)
    )
    eff_backlash_mm = j_wt * cos_beta

    rad_clear_g1 = a - ra1 - rf2
    rad_clear_g2 = a - ra2 - rf1

    mesh_2d = evaluate_meshed_2d_clearance(p, steps=9)
    min_tooth_clear = float(mesh_2d["min_clearance_mm"])
    poly_collision = bool(mesh_2d["collision_detected"])

    jammed = bool(
        poly_collision
        or (a < min_non_jam_a - 1e-3)
        or (eff_backlash_mm < -1e-3)
        or (rad_clear_g1 < -1e-3)
        or (rad_clear_g2 < -1e-3)
    )
    interference_detected = bool(jammed or involute_base_interference)

    undercut_g1 = bool(geom["pinion"]["undercut"])
    undercut_g2 = bool(geom["gear"]["undercut"])
    thin_tip_limit = max(0.35, 0.22 * m_n)
    thin_tip_g1 = bool(float(geom["pinion"]["tip_thickness_mm"]) < thin_tip_limit)
    thin_tip_g2 = bool(float(geom["gear"]["tip_thickness_mm"]) < thin_tip_limit)

    # 3. Kinematics & Forces
    ratio = float(geom["ratio"])
    rpm_g1 = float(p["sim_rpm"])
    rpm_g2 = rpm_g1 / ratio
    omega_g1 = (2.0 * math.pi * rpm_g1) / 60.0
    v_pitch_mm_s = omega_g1 * rw1

    torque_g1 = float(p["input_torque_nm"])
    torque_g2 = torque_g1 * ratio

    # Tangential, radial, and net axial thrust forces at working pitch point
    f_tangential = (torque_g1 * 1000.0) / max(0.5, rw1)
    f_radial = f_tangential * tan_alpha_op
    axial_balanced = bool(gear_type in ("spur", "herringbone") or beta_deg <= 1e-6)
    f_axial = 0.0 if axial_balanced else f_tangential * math.tan(beta_rad)

    # 4. Printability, Bed Fit, Volume, Weight & Wall Loops
    helix_overhang_deg = 0.0 if gear_type == "spur" else beta_deg
    has_bottom_recess = bool(
        (p["pinion"]["recess_enabled"] and p["pinion"]["recess_side"] in ("bottom", "both"))
        or (p["gear"]["recess_enabled"] and p["gear"]["recess_side"] in ("bottom", "both"))
        or p["pinion"]["lightening_mode"] == "web_recess"
        or p["gear"]["lightening_mode"] == "web_recess"
    )
    supports_needed = bool(helix_overhang_deg > 48.0 or has_bottom_recess)

    gap_mm = 8.0
    d_out_1 = 2.0 * ra1
    d_out_2 = 2.0 * ra2
    h_1 = face_w + (float(p["pinion"]["hub_height_mm"]) if p["pinion"]["hub_enabled"] else 0.0)
    h_2 = face_w + (float(p["gear"]["hub_height_mm"]) if p["gear"]["hub_enabled"] else 0.0)

    fp_x = d_out_1 + gap_mm + d_out_2
    fp_y = max(d_out_1, d_out_2)
    fp_z = max(h_1, h_2)

    est_vol_cm3 = 0.0
    if isinstance(meshes, dict) and meshes:
        for m_obj in meshes.values():
            vol_attr = getattr(m_obj, "volume_cm3", None)
            if vol_attr is not None and math.isfinite(float(vol_attr)):
                est_vol_cm3 += max(0.0, float(vol_attr))
    if est_vol_cm3 <= 1e-4:
        est_vol_cm3 = _estimate_single_gear_volume_cm3(
            p["pinion"], geom["pinion"], face_w
        ) + _estimate_single_gear_volume_cm3(p["gear"], geom["gear"], face_w)

    # Account for ~55% effective solid fraction (4-6 solid tooth walls + 35% gyroid core)
    effective_printed_vol_cm3 = max(0.10, est_vol_cm3 * 0.72)
    est_weight_g = effective_printed_vol_cm3 * PLA_DENSITY_G_CM3
    # Realistic FDM volumetric flow (~7.5 mm^3/s average including perimeters/retractions)
    est_time_min = max(3.0, (effective_printed_vol_cm3 * 1000.0) / (7.5 * 60.0) * (0.20 / layer_h))

    rec_walls = int(max(4, min(6, round((1.8 * m_n) / (2.0 * line_w)))))

    fits_bed = bool(
        (fp_x <= bed_x + 1e-3 and fp_y <= bed_y + 1e-3)
        or (fp_y <= bed_x + 1e-3 and fp_x <= bed_y + 1e-3)
    )

    # 5. Bilingual Issues & Overall Status
    issues: list[dict[str, str]] = []

    if disengaged:
        issues.append(
            {
                "severity": "critical",
                "code": "TEETH_DISENGAGED",
                "pt": (
                    f"Engrenagens desacopladas (a = {a:.2f} mm >= r_a1 + r_a2 = {ra1 + ra2:.2f} mm). "
                    "Reduza o deslocamento de distancia entre centros."
                ),
                "en": (
                    f"Gears are disengaged (a = {a:.2f} mm >= r_a1 + r_a2 = {ra1 + ra2:.2f} mm). "
                    "Reduce center distance offset."
                ),
            }
        )
    elif jammed:
        issues.append(
            {
                "severity": "critical",
                "code": "GEAR_MESH_JAMMED",
                "pt": (
                    f"Travamento / colisao fisica detectada (a = {a:.2f} mm < minimo livre "
                    f"{min_non_jam_a:.2f} mm, folga 2D = {min_tooth_clear:.3f} mm). Aumente Δa ou a folga (backlash)."
                ),
                "en": (
                    f"Physical mesh lockup / collision detected (a = {a:.2f} mm < min non-jam "
                    f"{min_non_jam_a:.2f} mm, 2D clearance = {min_tooth_clear:.3f} mm). Increase Δa or backlash."
                ),
            }
        )
    elif interference_detected:
        issues.append(
            {
                "severity": "critical",
                "code": "INVOLUTE_INTERFERENCE",
                "pt": (
                    "Interferencia evolvente abaixo do circulo de base detectada. "
                    "Ative o Deslocamento de Perfil Automatico (x) ou reduza a altura do adendo."
                ),
                "en": (
                    "Involute base-circle interference detected. "
                    "Enable Auto Profile Shift (x) or reduce addendum coefficient."
                ),
            }
        )

    if not disengaged and eps_gamma < 1.0:
        issues.append(
            {
                "severity": "critical",
                "code": "LOW_CONTACT_RATIO_CRITICAL",
                "pt": (
                    f"Razao de contato total critica (ε_γ = {eps_gamma:.2f} < 1.00): perda de continuidade de giro."
                ),
                "en": (
                    f"Critical total contact ratio (ε_γ = {eps_gamma:.2f} < 1.00): loss of continuous mesh action."
                ),
            }
        )
    elif not disengaged and eps_gamma < 1.20:
        issues.append(
            {
                "severity": "warn",
                "code": "MARGINAL_CONTACT_RATIO",
                "pt": (
                    f"Razao de contato justa (ε_γ = {eps_gamma:.2f} < 1.20). "
                    "Considere engrenagem helicoidal ou mais dentes para giro mais silencioso."
                ),
                "en": (
                    f"Marginal contact ratio (ε_γ = {eps_gamma:.2f} < 1.20). "
                    "Consider helical teeth or higher tooth count for smoother operation."
                ),
            }
        )

    if not jammed and eff_backlash_mm < 0.05:
        issues.append(
            {
                "severity": "warn",
                "code": "TIGHT_FDM_BACKLASH",
                "pt": (
                    f"Folga efetiva muito baixa ({eff_backlash_mm:.2f} mm) para impressao FDM. "
                    "Recomenda-se >= 0.10 mm ou imprimir o Kit de Teste Rapido antes."
                ),
                "en": (
                    f"Effective backlash ({eff_backlash_mm:.2f} mm) is tight for FDM printing. "
                    "Recommend >= 0.10 mm or printing the Quick Fit-Test Kit first."
                ),
            }
        )

    if undercut_g1 or undercut_g2:
        which_lbl_pt = "Pinhao (G1) e Coroa (G2)" if (undercut_g1 and undercut_g2) else (
            "Pinhao (G1)" if undercut_g1 else "Coroa (G2)"
        )
        which_lbl_en = "Pinion (G1) and Gear (G2)" if (undercut_g1 and undercut_g2) else (
            "Pinion (G1)" if undercut_g1 else "Gear (G2)"
        )
        issues.append(
            {
                "severity": "warn",
                "code": "UNDERCUT_RISK",
                "pt": f"Risco de undercut na raiz de {which_lbl_pt}. Ative 'Auto Profile Shift' para reforcar o pe do dente.",
                "en": f"Root undercut risk on {which_lbl_en}. Enable 'Auto Profile Shift' to strengthen tooth root.",
            }
        )

    if thin_tip_g1 or thin_tip_g2:
        issues.append(
            {
                "severity": "warn",
                "code": "THIN_TOOTH_TIP",
                "pt": (
                    f"Topo do dente fino (< {thin_tip_limit:.2f} mm) para bico FDM. "
                    "Reduza o deslocamento de perfil ou o fator de adendo."
                ),
                "en": (
                    f"Thin tooth tip (< {thin_tip_limit:.2f} mm) for FDM nozzle extrusion. "
                    "Reduce profile shift or addendum coefficient."
                ),
            }
        )

    if helix_overhang_deg > 48.0:
        issues.append(
            {
                "severity": "warn",
                "code": "HELIX_OVERHANG_HIGH",
                "pt": (
                    f"Angulo de helice elevado ({helix_overhang_deg:.1f}° > 48°): pode exigir suportes ou camadas finas (0.12 mm)."
                ),
                "en": (
                    f"Steep helix overhang ({helix_overhang_deg:.1f}° > 48°): may require supports or thin layers (0.12 mm)."
                ),
            }
        )
    elif has_bottom_recess:
        issues.append(
            {
                "severity": "warn",
                "code": "BOTTOM_RECESS_BRIDGE",
                "pt": "Rebaixo na face inferior detectado — verifique pontes/suportes no fatiador.",
                "en": "Bottom-side recess detected — verify bridging or enable supports in slicer.",
            }
        )

    if gear_type == "helical" and f_axial > 8.0:
        issues.append(
            {
                "severity": "info",
                "code": "AXIAL_THRUST_NOTICE",
                "pt": (
                    f"Empuxo axial lateral de {f_axial:.1f} N na helice simples. "
                    "Use encosto axial ou mude para Espinha de Peixe (Herringbone) para anular o empuxo (0 N)."
                ),
                "en": (
                    f"Unbalanced axial thrust of {f_axial:.1f} N on single helical gear. "
                    "Use thrust washers or switch to Herringbone to cancel axial thrust (0 N)."
                ),
            }
        )

    if not fits_bed:
        issues.append(
            {
                "severity": "critical",
                "code": "BED_OVERFLOW",
                "pt": (
                    f"Par lado a lado ({fp_x:.1f} x {fp_y:.1f} mm) excede a mesa ({bed_x:.0f} x {bed_y:.0f} mm). "
                    "Exporte Pinhao e Coroa separadamente."
                ),
                "en": (
                    f"Side-by-side pair ({fp_x:.1f} x {fp_y:.1f} mm) exceeds build plate ({bed_x:.0f} x {bed_y:.0f} mm). "
                    "Export Pinion and Gear individually."
                ),
            }
        )

    has_critical = any(it["severity"] == "critical" for it in issues)
    has_warn = any(it["severity"] == "warn" for it in issues)
    status = "critical" if has_critical else ("warn" if has_warn else "ok")

    return {
        "status": status,
        "geometry": geom,
        "contact": {
            "transverse_ratio": round(eps_alpha, 4),
            "axial_overlap_ratio": round(eps_beta, 4),
            "total_contact_ratio": round(eps_gamma, 4),
            "line_of_action_length_mm": round(g_alpha, 4),
        },
        "fit": {
            "effective_backlash_mm": round(eff_backlash_mm, 4),
            "radial_clearance_g1_mm": round(rad_clear_g1, 4),
            "radial_clearance_g2_mm": round(rad_clear_g2, 4),
            "min_tooth_clearance_mm": round(min_tooth_clear, 4),
            "interference_detected": interference_detected,
            "jammed": jammed,
            "undercut_g1": undercut_g1,
            "undercut_g2": undercut_g2,
            "thin_tip_g1": thin_tip_g1,
            "thin_tip_g2": thin_tip_g2,
            "center_distance_mm": round(a, 4),
            "nominal_center_distance_mm": round(a0, 4),
            "min_non_jam_center_distance_mm": round(min_non_jam_a, 4),
            "delta_a_mm": round(delta_a, 4),
        },
        "kinematics": {
            "ratio": round(ratio, 4),
            "rpm_g1": round(rpm_g1, 2),
            "rpm_g2": round(rpm_g2, 2),
            "pitch_line_velocity_mm_s": round(v_pitch_mm_s, 3),
            "torque_g1_nm": round(torque_g1, 4),
            "torque_g2_nm": round(torque_g2, 4),
            "tangential_force_n": round(f_tangential, 3),
            "radial_force_n": round(f_radial, 3),
            "axial_force_n": round(f_axial, 3),
            "axial_thrust_balanced": axial_balanced,
        },
        "printability": {
            "helix_overhang_deg": round(helix_overhang_deg, 1),
            "supports_needed": supports_needed,
            "fits_bed": fits_bed,
            "bed_x_mm": round(bed_x, 1),
            "bed_y_mm": round(bed_y, 1),
            "pair_footprint_mm": [round(fp_x, 2), round(fp_y, 2), round(fp_z, 2)],
            "estimated_volume_cm3": round(est_vol_cm3, 2),
            "estimated_weight_g": round(est_weight_g, 1),
            "estimated_print_time_min": round(est_time_min, 1),
            "recommended_wall_loops": rec_walls,
        },
        "issues": issues,
    }
