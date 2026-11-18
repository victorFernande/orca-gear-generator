"""Strict 2-manifold watertightness, topological genus, body-feature, preset, and Fit-Test Kit tests."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import copy
import math
import unittest
from collections import Counter, deque
from pathlib import Path

import os

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROJECT_SRC = PROJECT_ROOT / "src"
_CP_TAG = f"cp{sys.version_info.major}{sys.version_info.minor}"
_ORCA_ROOTS = [
    Path(os.environ["APPDATA"]) / "OrcaSlicer" if os.environ.get("APPDATA") else None,
    Path.home() / "Library" / "Application Support" / "OrcaSlicer",
    Path(os.environ.get("XDG_CONFIG_HOME") or (Path.home() / ".config")) / "OrcaSlicer",
]
for _r in _ORCA_ROOTS:
    if _r is not None:
        for _cand in (_r / "python" / "packages" / _CP_TAG, _r / "python" / "packages" / "cp312"):
            if _cand.is_dir() and str(_cand) not in sys.path:
                sys.path.insert(0, str(_cand))
if str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))

import numpy as np

from gear_studio.mesh_generator import (
    MeshData,
    collect_target_meshes,
    generate_fit_test_kit,
    generate_gear_mesh,
)
from gear_studio.presets_catalog import BUILTIN_PRESETS
from gear_studio.schema import DEFAULT_PARAMS, normalize_params


class TestGearManifoldAndFitKit(unittest.TestCase):
    """Verify strict 2-manifold directed-edge pairing across all gear types, bores, features, presets, and fit kit."""

    def assert_strict_2_manifold(
        self,
        mesh: MeshData,
        label: str,
        *,
        expected_genus: int | None = None,
        min_volume_cm3: float = 0.02,
        max_xy_drift_mm: float = 15.0,
    ) -> dict[str, float | int]:
        """Verify MeshData satisfies every geometric and topological 2-manifold invariant."""
        self.assertIsInstance(mesh, MeshData, f"{label}: must be MeshData")

        verts = mesh.vertices
        tris = mesh.triangles
        normals = mesh.face_normals

        self.assertIsInstance(verts, np.ndarray, f"{label}: vertices must be ndarray")
        self.assertIsInstance(tris, np.ndarray, f"{label}: triangles must be ndarray")
        self.assertIsInstance(normals, np.ndarray, f"{label}: face_normals must be ndarray")

        self.assertEqual(verts.ndim, 2, f"{label}: vertices ndim != 2")
        self.assertEqual(verts.shape[1], 3, f"{label}: vertices shape[1] != 3")
        self.assertGreaterEqual(verts.shape[0], 4, f"{label}: fewer than 4 vertices")

        self.assertEqual(tris.ndim, 2, f"{label}: triangles ndim != 2")
        self.assertEqual(tris.shape[1], 3, f"{label}: triangles shape[1] != 3")
        self.assertGreaterEqual(tris.shape[0], 4, f"{label}: fewer than 4 triangles")

        self.assertEqual(
            normals.shape,
            tris.shape,
            f"{label}: face_normals shape {normals.shape} != triangles shape {tris.shape}",
        )

        # 1. Finite vertices, normals, volume, overhang angles
        self.assertTrue(np.all(np.isfinite(verts)), f"{label}: NaN/Inf in vertices")
        self.assertTrue(np.all(np.isfinite(normals)), f"{label}: NaN/Inf in face_normals")
        self.assertTrue(math.isfinite(float(mesh.volume_cm3)), f"{label}: non-finite volume_cm3")
        self.assertEqual(mesh.overhang_angles_deg.shape, (tris.shape[0],), f"{label}: invalid overhang_angles_deg shape")
        self.assertTrue(np.all(np.isfinite(mesh.overhang_angles_deg)), f"{label}: NaN/Inf in overhang_angles_deg")

        # 2. Valid triangle index bounds
        n_verts = int(verts.shape[0])
        self.assertGreaterEqual(int(tris.min()), 0, f"{label}: negative vertex index")
        self.assertLess(int(tris.max()), n_verts, f"{label}: out-of-bounds vertex index")

        # 3. Bed placement min(Z) == 0.0 and XY centering
        min_xyz = verts.min(axis=0)
        max_xyz = verts.max(axis=0)
        self.assertAlmostEqual(
            float(min_xyz[2]),
            0.0,
            places=4,
            msg=f"{label}: min(Z) must equal 0.0, got {float(min_xyz[2]):.6f}",
        )
        center_x = 0.5 * float(min_xyz[0] + max_xyz[0])
        center_y = 0.5 * float(min_xyz[1] + max_xyz[1])
        self.assertLess(abs(center_x), max_xy_drift_mm, f"{label}: X center drifted ({center_x:.2f} mm)")
        self.assertLess(abs(center_y), max_xy_drift_mm, f"{label}: Y center drifted ({center_y:.2f} mm)")

        # 4. Bounds consistency
        for bkey in ("min", "max", "size"):
            self.assertIn(bkey, mesh.bounds_mm, f"{label}: bounds_mm missing {bkey!r}")
        np.testing.assert_allclose(mesh.bounds_mm["min"], min_xyz, atol=1e-2)
        np.testing.assert_allclose(mesh.bounds_mm["max"], max_xyz, atol=1e-2)
        np.testing.assert_allclose(mesh.bounds_mm["size"], max_xyz - min_xyz, atol=1e-2)

        # 5. Zero degenerate triangles & unit normals aligned with CCW winding
        u_idx = tris[:, 0]
        v_idx = tris[:, 1]
        w_idx = tris[:, 2]
        repeated = np.any((u_idx == v_idx) | (v_idx == w_idx) | (w_idx == u_idx))
        self.assertFalse(bool(repeated), f"{label}: triangle has repeated vertex indices")

        v0 = verts[u_idx].astype(np.float64)
        v1 = verts[v_idx].astype(np.float64)
        v2 = verts[w_idx].astype(np.float64)
        cross = np.cross(v1 - v0, v2 - v0)
        double_areas = np.linalg.norm(cross, axis=1)
        min_double_area = float(double_areas.min())
        self.assertGreater(
            min_double_area,
            1e-9,
            f"{label}: degenerate face detected (min 2*area = {min_double_area:.3e})",
        )

        norm_lengths = np.linalg.norm(normals.astype(np.float64), axis=1)
        np.testing.assert_allclose(
            norm_lengths,
            1.0,
            atol=1e-2,
            err_msg=f"{label}: face_normals are not unit vectors",
        )
        computed_normals = cross / double_areas[:, None]
        alignment = np.einsum("ij,ij->i", normals.astype(np.float64), computed_normals)
        self.assertGreater(
            float(alignment.min()),
            0.95,
            f"{label}: stored face_normals disagree with CCW winding (min dot={alignment.min():.4f})",
        )

        # 6. Strict directed-edge pairing: EVERY directed edge (u, v) has count == 1 and (v, u) == 1
        edge_counter: Counter[tuple[int, int]] = Counter()
        for a, b, c in tris.tolist():
            edge_counter[(a, b)] += 1
            edge_counter[(b, c)] += 1
            edge_counter[(c, a)] += 1

        n_faces = int(tris.shape[0])
        non_unit_edges = [(e, cnt) for e, cnt in edge_counter.items() if cnt != 1]
        self.assertEqual(
            len(non_unit_edges),
            0,
            f"{label}: {len(non_unit_edges)} duplicate directed edges (sample: {non_unit_edges[:5]})",
        )
        self.assertEqual(
            len(edge_counter),
            3 * n_faces,
            f"{label}: unique directed edge count {len(edge_counter)} != 3*F ({3 * n_faces})",
        )

        open_boundary_edges = [e for e in edge_counter if edge_counter.get((e[1], e[0]), 0) != 1]
        self.assertEqual(
            len(open_boundary_edges),
            0,
            f"{label}: {len(open_boundary_edges)} open/unpaired boundary edges (sample: {open_boundary_edges[:5]})",
        )

        # Geometric seam check at 1e-4 mm quantization to ensure no unwelded duplicate seams
        quantized = np.round(verts.astype(np.float64) * 10000.0).astype(np.int64)
        _, inv_map = np.unique(quantized, axis=0, return_inverse=True)
        geom_tris = inv_map[tris]
        geom_deg = int(
            np.sum(
                (geom_tris[:, 0] == geom_tris[:, 1])
                | (geom_tris[:, 1] == geom_tris[:, 2])
                | (geom_tris[:, 2] == geom_tris[:, 0])
            )
        )
        self.assertEqual(geom_deg, 0, f"{label}: geometrically collapsed triangles at 1e-4 mm ({geom_deg})")

        # 7. Positive outward signed divergence volume
        signed_vol_mm3 = float(np.sum(np.einsum("ij,ij->i", v0, cross))) / 6.0
        signed_vol_cm3 = signed_vol_mm3 / 1000.0
        self.assertGreater(
            signed_vol_cm3,
            min_volume_cm3,
            f"{label}: signed volume {signed_vol_cm3:.4f} <= {min_volume_cm3} cm3",
        )
        self.assertAlmostEqual(
            float(mesh.volume_cm3),
            signed_vol_cm3,
            delta=max(0.04, abs(signed_vol_cm3) * 0.03),
            msg=f"{label}: mesh.volume_cm3 ({mesh.volume_cm3:.4f}) != divergence volume ({signed_vol_cm3:.4f})",
        )

        # 8. Connected component & optional Euler characteristic / genus check: V - E + F == 2 - 2g
        used_verts = set(tris.reshape(-1).tolist())
        v_used = len(used_verts)
        e_undirected = (3 * n_faces) // 2
        euler_chi = v_used - e_undirected + n_faces
        if expected_genus is not None:
            adj: dict[int, list[int]] = {v: [] for v in used_verts}
            for u, v in edge_counter:
                adj[u].append(v)
            start_v = next(iter(used_verts))
            visited = {start_v}
            q = deque([start_v])
            while q:
                cur = q.popleft()
                for nxt in adj[cur]:
                    if nxt not in visited:
                        visited.add(nxt)
                        q.append(nxt)
            self.assertEqual(
                len(visited),
                v_used,
                f"{label}: expected single connected component ({len(visited)} / {v_used} vertices)",
            )
            expected_chi = 2 - 2 * expected_genus
            self.assertEqual(
                euler_chi,
                expected_chi,
                f"{label}: Euler characteristic V-E+F={euler_chi} != {expected_chi} for expected_genus={expected_genus}",
            )

        return {
            "vertices": n_verts,
            "faces": n_faces,
            "volume_cm3": signed_vol_cm3,
            "euler_chi": euler_chi,
        }

    def test_01_spur_helical_45_and_herringbone_35_manifold(self) -> None:
        configs = [
            ("spur", 0.0),
            ("helical", 45.0),
            ("herringbone", 35.0),
        ]
        for gear_type, beta_deg in configs:
            for which in ("pinion", "gear"):
                with self.subTest(gear_type=gear_type, beta_deg=beta_deg, which=which):
                    p = normalize_params(
                        {
                            "gear_type": gear_type,
                            "helix_angle_deg": beta_deg,
                            "face_width_mm": 14.0,
                            "module_mm": 2.0,
                            "elephant_foot_chamfer_mm": 0.4,
                            "pinion": {"teeth": 16, "bore_type": "round", "bore_diameter_mm": 5.0, "lightening_mode": "solid"},
                            "gear": {"teeth": 30, "bore_type": "round", "bore_diameter_mm": 8.0, "lightening_mode": "solid"},
                        }
                    )
                    mesh = generate_gear_mesh(p, which=which, resolution="low")
                    self.assert_strict_2_manifold(
                        mesh,
                        f"{gear_type}_{beta_deg}_{which}",
                        expected_genus=1,
                    )
                    self.assertAlmostEqual(float(mesh.bounds_mm["size"][2]), 14.0, delta=0.1)

    def test_02_all_6_bore_types_manifold(self) -> None:
        bore_types = ("none", "round", "d_shaft", "double_d", "hex", "keyway")
        for btype in bore_types:
            with self.subTest(bore_type=btype):
                p = normalize_params(
                    {
                        "gear_type": "spur",
                        "module_mm": 2.2,
                        "face_width_mm": 10.0,
                        "pinion": {
                            "teeth": 18,
                            "bore_type": btype,
                            "bore_diameter_mm": 6.0,
                            "bore_clearance_mm": 0.12,
                            "d_flat_depth_mm": 0.6,
                            "keyway_width_mm": 2.0,
                            "keyway_depth_mm": 1.0,
                            "lightening_mode": "solid",
                        },
                    }
                )
                mesh = generate_gear_mesh(p, which="pinion", resolution="low")
                exp_genus = 0 if btype == "none" else 1
                self.assert_strict_2_manifold(
                    mesh,
                    f"bore[{btype}]",
                    expected_genus=exp_genus,
                )

    def test_03_hub_recess_sides_and_lightening_modes_with_genus(self) -> None:
        base_gear_body = {
            "teeth": 36,
            "bore_type": "round",
            "bore_diameter_mm": 8.0,
            "bore_clearance_mm": 0.12,
            "hub_enabled": False,
            "hub_diameter_mm": 20.0,
            "hub_height_mm": 5.0,
            "recess_enabled": False,
            "recess_side": "top",
            "recess_diameter_mm": 22.0,
            "recess_depth_mm": 3.0,
            "lightening_mode": "solid",
            "web_thickness_mm": 4.0,
            "lightening_hole_count": 6,
            "lightening_hole_diameter_mm": 9.0,
        }
        base_params = normalize_params(
            {
                "gear_type": "spur",
                "module_mm": 2.5,
                "face_width_mm": 12.0,
                "gear": base_gear_body,
            }
        )

        # 1. Solid baseline (genus = 1)
        solid_mesh = generate_gear_mesh(base_params, which="gear", resolution="low")
        solid_stats = self.assert_strict_2_manifold(solid_mesh, "gear[solid]", expected_genus=1)

        # 2. Hub enabled (top height grows from 12.0 to 17.0 mm, volume grows)
        p_hub = copy.deepcopy(base_params)
        p_hub["gear"]["hub_enabled"] = True
        hub_mesh = generate_gear_mesh(p_hub, which="gear", resolution="low")
        hub_stats = self.assert_strict_2_manifold(hub_mesh, "gear[hub]", expected_genus=1)
        self.assertAlmostEqual(float(hub_mesh.bounds_mm["size"][2]), 17.0, delta=0.15)
        self.assertGreater(hub_stats["volume_cm3"], solid_stats["volume_cm3"])

        # 3. Bearing/bolt recess on top, bottom, and both
        for r_side in ("top", "bottom", "both"):
            with self.subTest(recess_side=r_side):
                p_rec = copy.deepcopy(base_params)
                p_rec["gear"]["recess_enabled"] = True
                p_rec["gear"]["recess_side"] = r_side
                rec_mesh = generate_gear_mesh(p_rec, which="gear", resolution="low")
                rec_stats = self.assert_strict_2_manifold(
                    rec_mesh,
                    f"gear[recess={r_side}]",
                    expected_genus=1,
                )
                self.assertLess(rec_stats["volume_cm3"], solid_stats["volume_cm3"])

        # 4. Web recess lightening mode (genus = 1, lower volume)
        p_web = copy.deepcopy(base_params)
        p_web["gear"]["lightening_mode"] = "web_recess"
        web_mesh = generate_gear_mesh(p_web, which="gear", resolution="low")
        web_stats = self.assert_strict_2_manifold(web_mesh, "gear[web_recess]", expected_genus=1)
        self.assertLess(web_stats["volume_cm3"], solid_stats["volume_cm3"])

        # 5. Lightening through-holes with exact topological genus = 1 + hole_count
        for hole_count in (4, 6, 8):
            with self.subTest(lightening_hole_count=hole_count):
                p_holes = copy.deepcopy(base_params)
                p_holes["gear"]["lightening_mode"] = "lightening_holes"
                p_holes["gear"]["lightening_hole_count"] = hole_count
                p_holes["gear"]["lightening_hole_diameter_mm"] = 8.5
                holes_mesh = generate_gear_mesh(p_holes, which="gear", resolution="low")
                holes_stats = self.assert_strict_2_manifold(
                    holes_mesh,
                    f"gear[lightening_holes={hole_count}]",
                    expected_genus=1 + hole_count,
                )
                self.assertLess(holes_stats["volume_cm3"], solid_stats["volume_cm3"])

        # 6. Combined helical 45 + hub + recess + lightening holes
        p_combo = copy.deepcopy(base_params)
        p_combo["gear_type"] = "helical"
        p_combo["helix_angle_deg"] = 45.0
        p_combo["gear"]["hub_enabled"] = True
        p_combo["gear"]["hub_diameter_mm"] = 18.0
        p_combo["gear"]["recess_enabled"] = True
        p_combo["gear"]["recess_side"] = "bottom"
        p_combo["gear"]["recess_diameter_mm"] = 16.0
        p_combo["gear"]["lightening_mode"] = "lightening_holes"
        p_combo["gear"]["lightening_hole_count"] = 6
        combo_mesh = generate_gear_mesh(p_combo, which="gear", resolution="low")
        self.assert_strict_2_manifold(
            combo_mesh,
            "gear[helical45+hub+recess+6holes]",
            expected_genus=7,
        )

    def test_04_all_12_builtin_presets_pinion_and_gear_manifold(self) -> None:
        self.assertEqual(
            len(BUILTIN_PRESETS),
            12,
            f"Expected 12 BUILTIN_PRESETS, got {len(BUILTIN_PRESETS)}",
        )
        for idx, preset in enumerate(BUILTIN_PRESETS):
            pid = preset.get("id", f"preset_{idx}")
            params = normalize_params(preset["params"])
            for which in ("pinion", "gear"):
                with self.subTest(preset_id=pid, which=which):
                    mesh = generate_gear_mesh(params, which=which, resolution="low")
                    self.assert_strict_2_manifold(mesh, f"preset[{pid}].{which}")

    def test_05_fit_test_kit_and_collect_target_meshes_manifold(self) -> None:
        for gear_type, beta_deg, btype in (
            ("spur", 0.0, "d_shaft"),
            ("helical", 45.0, "hex"),
            ("herringbone", 30.0, "keyway"),
        ):
            with self.subTest(gear_type=gear_type, beta_deg=beta_deg, bore_type=btype):
                params = normalize_params(
                    {
                        "gear_type": gear_type,
                        "helix_angle_deg": beta_deg,
                        "module_mm": 2.0,
                        "face_width_mm": 10.0,
                        "pinion": {"teeth": 15, "bore_type": btype, "bore_diameter_mm": 5.0},
                        "gear": {"teeth": 30, "bore_type": "round", "bore_diameter_mm": 8.0},
                    }
                )
                kit = generate_fit_test_kit(params)
                expected_keys = {"sector_pinion", "sector_gear", "center_jig_base", "bore_fit_gauge"}
                self.assertEqual(set(kit.keys()), expected_keys)

                self.assert_strict_2_manifold(
                    kit["sector_pinion"],
                    f"fit_kit[{gear_type}].sector_pinion",
                    min_volume_cm3=0.01,
                    max_xy_drift_mm=30.0,
                )
                self.assert_strict_2_manifold(
                    kit["sector_gear"],
                    f"fit_kit[{gear_type}].sector_gear",
                    min_volume_cm3=0.01,
                    max_xy_drift_mm=30.0,
                )
                self.assert_strict_2_manifold(
                    kit["center_jig_base"],
                    f"fit_kit[{gear_type}].center_jig_base",
                    expected_genus=0,
                    min_volume_cm3=0.05,
                    max_xy_drift_mm=20.0,
                )
                self.assert_strict_2_manifold(
                    kit["bore_fit_gauge"],
                    f"fit_kit[{gear_type}].bore_fit_gauge",
                    expected_genus=4,
                    min_volume_cm3=0.05,
                    max_xy_drift_mm=20.0,
                )

        # Verify collect_target_meshes target routing
        p_default = normalize_params(DEFAULT_PARAMS)
        self.assertEqual(len(collect_target_meshes(p_default, target="pinion_only")), 1)
        self.assertEqual(len(collect_target_meshes(p_default, target="gear_only")), 1)
        self.assertEqual(len(collect_target_meshes(p_default, target="pair_separated")), 2)
        self.assertEqual(len(collect_target_meshes(p_default, target="fit_test_kit")), 4)
        self.assertEqual(len(collect_target_meshes(p_default, target="full_suite")), 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
