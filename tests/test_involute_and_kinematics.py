"""Comprehensive tests for gear schema normalization, ISO 21771 involute geometry,
helical/herringbone twist continuity, dual tooth-height scaling, anti-undercut profile shift,
2D meshed tooth clearance across rotation steps, and kinematic/fit diagnostics.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import copy
import math
import unittest
from pathlib import Path
from typing import Any

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

from gear_studio.fit_and_kinematics import analyze_gear_pair
from gear_studio.involute_math import (
    build_bore_2d_contour,
    build_gear_2d_contour,
    compute_gear_pair_geometry,
    helix_twist_angle_rad,
    inverse_involute_fn,
    involute_fn,
)
from gear_studio.schema import (
    DEFAULT_PARAMS,
    SCHEMA_VERSION,
    effective_helix_angle_deg,
    normalize_gear_body,
    normalize_params,
)


def _pick(mapping: dict[str, Any], candidates: tuple[str, ...]) -> Any:
    for key in candidates:
        if key in mapping:
            return mapping[key]
    raise KeyError(f"None of {candidates} found in keys {sorted(mapping.keys())}")


def _metric(report: dict[str, Any], key: str) -> Any:
    if key in report:
        return report[key]
    for section in ("contact", "fit", "kinematics", "printability"):
        sub = report.get(section)
        if isinstance(sub, dict) and key in sub:
            return sub[key]
    raise KeyError(f"Metric {key!r} not found in report keys {sorted(report.keys())}")


def _polygon_signed_area(pts: np.ndarray) -> float:
    x = pts[:, 0]
    y = pts[:, 1]
    return 0.5 * float(np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y))


def _rotate_2d(pts: np.ndarray, angle_rad: float) -> np.ndarray:
    c = math.cos(angle_rad)
    s = math.sin(angle_rad)
    rot = np.array([[c, -s], [s, c]], dtype=np.float64)
    return pts @ rot.T


def _segments_intersect_or_min_dist(poly_a: np.ndarray, poly_b: np.ndarray, x_min: float, x_max: float, y_abs: float) -> tuple[bool, float]:
    """Exact 2D closed-polygon edge-to-edge intersection and minimum distance in the meshing window."""
    a0 = poly_a
    a1 = np.roll(poly_a, -1, axis=0)
    b0 = poly_b
    b1 = np.roll(poly_b, -1, axis=0)

    mask_a = (
        (np.maximum(a0[:, 0], a1[:, 0]) >= x_min)
        & (np.minimum(a0[:, 0], a1[:, 0]) <= x_max)
        & (np.minimum(np.abs(a0[:, 1]), np.abs(a1[:, 1])) <= y_abs)
    )
    mask_b = (
        (np.maximum(b0[:, 0], b1[:, 0]) >= x_min)
        & (np.minimum(b0[:, 0], b1[:, 0]) <= x_max)
        & (np.minimum(np.abs(b0[:, 1]), np.abs(b1[:, 1])) <= y_abs)
    )

    p0 = a0[mask_a]
    p1 = a1[mask_a]
    q0 = b0[mask_b]
    q1 = b1[mask_b]

    if len(p0) == 0 or len(q0) == 0:
        return False, float("inf")

    # Vectorized segment-segment proper/improper intersection check:
    # p(t) = p0 + t*(p1 - p0), q(u) = q0 + u*(q1 - q0)
    dp = p1[:, None, :] - p0[:, None, :]  # (Na, 1, 2)
    dq = q1[None, :, :] - q0[None, :, :]  # (1, Nb, 2)
    qp = q0[None, :, :] - p0[:, None, :]  # (Na, Nb, 2)

    denom = dp[..., 0] * dq[..., 1] - dp[..., 1] * dq[..., 0]
    valid = np.abs(denom) > 1e-12
    safe_denom = np.where(valid, denom, 1.0)
    t = (qp[..., 0] * dq[..., 1] - qp[..., 1] * dq[..., 0]) / safe_denom
    u = (qp[..., 0] * dp[..., 1] - qp[..., 1] * dp[..., 0]) / safe_denom

    intersects = bool(np.any(valid & (t >= 0.0) & (t <= 1.0) & (u >= 0.0) & (u <= 1.0)))
    if intersects:
        return True, 0.0

    # Point-to-segment distance for all filtered edges (both P->Q_seg and Q->P_seg)
    def _pt_to_segs_min_dist(pts: np.ndarray, s0: np.ndarray, s1: np.ndarray) -> float:
        seg = s1 - s0  # (Ns, 2)
        seg_len2 = np.maximum(np.sum(seg * seg, axis=1), 1e-15)  # (Ns,)
        diff = pts[:, None, :] - s0[None, :, :]  # (Np, Ns, 2)
        proj = np.clip(np.sum(diff * seg[None, :, :], axis=2) / seg_len2[None, :], 0.0, 1.0)
        closest = s0[None, :, :] + proj[:, :, None] * seg[None, :, :]
        dists = np.linalg.norm(pts[:, None, :] - closest, axis=2)
        return float(np.min(dists))

    min_d = min(
        _pt_to_segs_min_dist(p0, q0, q1),
        _pt_to_segs_min_dist(q0, p0, p1),
    )
    return False, min_d


class TestInvoluteAndKinematics(unittest.TestCase):
    """Test suite for schema, ISO involute math, helical/herringbone twist, and meshing diagnostics."""

    def test_01_schema_defaults_clamping_and_effective_helix_angle(self) -> None:
        self.assertEqual(SCHEMA_VERSION, 1)
        required_top_keys = {
            "schema_version",
            "name",
            "gear_type",
            "module_mm",
            "pressure_angle_deg",
            "helix_angle_deg",
            "helix_hand",
            "face_width_mm",
            "addendum_coeff",
            "clearance_coeff",
            "root_fillet_coeff",
            "tip_chamfer_coeff",
            "auto_profile_shift",
            "profile_shift_g1",
            "profile_shift_g2",
            "backlash_mm",
            "xy_compensation_mm",
            "elephant_foot_chamfer_mm",
            "center_distance_offset_mm",
            "input_torque_nm",
            "pinion",
            "gear",
            "sim_rpm",
            "sim_direction",
            "export_target",
            "auto_configure_slicer",
        }
        self.assertTrue(required_top_keys.issubset(set(DEFAULT_PARAMS.keys())))

        required_body_keys = {
            "teeth",
            "bore_type",
            "bore_diameter_mm",
            "bore_clearance_mm",
            "d_flat_depth_mm",
            "keyway_width_mm",
            "keyway_depth_mm",
            "hub_enabled",
            "hub_diameter_mm",
            "hub_height_mm",
            "recess_enabled",
            "recess_side",
            "recess_diameter_mm",
            "recess_depth_mm",
            "lightening_mode",
            "web_thickness_mm",
            "lightening_hole_count",
            "lightening_hole_diameter_mm",
        }
        self.assertTrue(required_body_keys.issubset(set(DEFAULT_PARAMS["pinion"].keys())))
        self.assertTrue(required_body_keys.issubset(set(DEFAULT_PARAMS["gear"].keys())))

        # Deep copy isolation
        p_norm = normalize_params(None)
        p_norm["pinion"]["teeth"] = 99
        self.assertEqual(DEFAULT_PARAMS["pinion"]["teeth"], 16)
        self.assertEqual(DEFAULT_PARAMS["gear"]["teeth"], 32)

        # Effective helix angle: 0.0 for spur even when helix_angle_deg is non-zero; preserved otherwise
        spur_p = normalize_params({"gear_type": "spur", "helix_angle_deg": 45.0})
        self.assertEqual(spur_p["helix_angle_deg"], 45.0)
        self.assertEqual(effective_helix_angle_deg(spur_p), 0.0)

        helical_p = normalize_params({"gear_type": "helical", "helix_angle_deg": 45.0})
        self.assertAlmostEqual(effective_helix_angle_deg(helical_p), 45.0, places=6)

        herringbone_p = normalize_params({"gear_type": "herringbone", "helix_angle_deg": 35.0})
        self.assertAlmostEqual(effective_helix_angle_deg(herringbone_p), 35.0, places=6)

        # Out-of-bounds clamping & enum sanitization
        malformed = {
            "name": "X" * 200,
            "gear_type": "worm_invalid",
            "module_mm": "999.0",
            "pressure_angle_deg": "2.0",
            "helix_angle_deg": "88.0",
            "helix_hand": "upside_down",
            "face_width_mm": "-10.0",
            "addendum_coeff": "5.0",
            "clearance_coeff": "0.01",
            "root_fillet_coeff": "2.0",
            "tip_chamfer_coeff": "-1.0",
            "profile_shift_g1": "-5.0",
            "profile_shift_g2": "5.0",
            "backlash_mm": "9.0",
            "xy_compensation_mm": "-5.0",
            "elephant_foot_chamfer_mm": "9.0",
            "center_distance_offset_mm": "-99.0",
            "input_torque_nm": "9999.0",
            "sim_rpm": "0.0",
            "sim_direction": "invalid",
            "export_target": "invalid_target",
            "pinion": {
                "teeth": 2,
                "bore_type": "spline_unknown",
                "recess_side": "left",
                "lightening_mode": "swiss_cheese",
            },
        }
        clamped = normalize_params(malformed)
        self.assertLessEqual(len(clamped["name"]), 80)
        self.assertEqual(clamped["gear_type"], "spur")
        self.assertEqual(clamped["module_mm"], 10.0)
        self.assertEqual(clamped["pressure_angle_deg"], 14.5)
        self.assertEqual(clamped["helix_angle_deg"], 60.0)
        self.assertIn(clamped["helix_hand"], ("right", "left"))
        self.assertEqual(clamped["face_width_mm"], 2.0)
        self.assertEqual(clamped["addendum_coeff"], 1.40)
        self.assertEqual(clamped["clearance_coeff"], 0.10)
        self.assertEqual(clamped["root_fillet_coeff"], 0.45)
        self.assertEqual(clamped["tip_chamfer_coeff"], 0.0)
        self.assertEqual(clamped["profile_shift_g1"], -0.50)
        self.assertEqual(clamped["profile_shift_g2"], 0.80)
        self.assertEqual(clamped["backlash_mm"], 1.00)
        self.assertEqual(clamped["xy_compensation_mm"], -0.20)
        self.assertEqual(clamped["elephant_foot_chamfer_mm"], 1.50)
        self.assertEqual(clamped["center_distance_offset_mm"], -1.50)
        self.assertEqual(clamped["input_torque_nm"], 50.0)
        self.assertEqual(DEFAULT_PARAMS["sim_rpm"], 1.0)
        self.assertEqual(clamped["sim_rpm"], 1.0)
        self.assertEqual(normalize_params({"sim_rpm": 99.0})["sim_rpm"], 10.0)
        self.assertIn(clamped["sim_direction"], ("cw", "ccw"))
        self.assertEqual(clamped["export_target"], "pair_separated")
        self.assertGreaterEqual(clamped["pinion"]["teeth"], 6)
        self.assertIn(clamped["pinion"]["bore_type"], ("none", "round", "d_shaft", "double_d", "hex", "keyway"))
        self.assertIn(clamped["pinion"]["recess_side"], ("top", "bottom", "both"))
        self.assertIn(clamped["pinion"]["lightening_mode"], ("solid", "web_recess", "lightening_holes"))

        body_norm = normalize_gear_body({"bore_type": "hex", "bore_diameter_mm": 6.0}, default_teeth=20)
        self.assertEqual(body_norm["teeth"], 20)
        self.assertEqual(body_norm["bore_type"], "hex")

    def test_02_involute_inverse_and_transverse_module_at_0_30_45_deg(self) -> None:
        # Newton-Raphson inverse involute accuracy
        for alpha_deg in (10.0, 14.5, 20.0, 25.0, 35.0, 48.0):
            alpha_rad = math.radians(alpha_deg)
            inv_val = involute_fn(alpha_rad)
            self.assertAlmostEqual(inv_val, math.tan(alpha_rad) - alpha_rad, places=12)
            recovered = inverse_involute_fn(inv_val)
            self.assertAlmostEqual(recovered, alpha_rad, places=11)

        m_n = 2.0
        alpha_n_deg = 20.0
        alpha_n_rad = math.radians(alpha_n_deg)

        for gear_type, beta_deg in (("spur", 0.0), ("helical", 30.0), ("helical", 45.0)):
            with self.subTest(gear_type=gear_type, beta_deg=beta_deg):
                p = normalize_params(
                    {
                        "gear_type": gear_type,
                        "module_mm": m_n,
                        "pressure_angle_deg": alpha_n_deg,
                        "helix_angle_deg": 45.0 if gear_type == "spur" else beta_deg,
                        "helix_hand": "right",
                        "auto_profile_shift": False,
                        "profile_shift_g1": 0.0,
                        "profile_shift_g2": 0.0,
                        "center_distance_offset_mm": 0.0,
                        "pinion": {"teeth": 18},
                        "gear": {"teeth": 45},
                    }
                )
                geom = compute_gear_pair_geometry(p)
                beta_rad = math.radians(beta_deg)
                expected_mt = m_n / math.cos(beta_rad)
                expected_alpha_t_deg = math.degrees(math.atan(math.tan(alpha_n_rad) / math.cos(beta_rad)))
                expected_a0 = 0.5 * expected_mt * (18 + 45)

                self.assertAlmostEqual(float(geom["beta_deg"]), beta_deg, places=6)
                self.assertAlmostEqual(float(geom["m_n"]), m_n, places=6)
                self.assertAlmostEqual(float(geom["m_t"]), expected_mt, places=6)
                self.assertAlmostEqual(float(geom["alpha_t_deg"]), expected_alpha_t_deg, places=5)
                self.assertAlmostEqual(float(geom["nominal_center_distance_mm"]), expected_a0, places=5)
                self.assertAlmostEqual(float(geom["center_distance_mm"]), expected_a0, places=5)
                self.assertAlmostEqual(float(geom["ratio"]), 45.0 / 18.0, places=6)

                hand_g1 = _pick(geom["pinion"], ("helix_hand", "hand"))
                hand_g2 = _pick(geom["gear"], ("helix_hand", "hand"))
                self.assertEqual(hand_g1, "right")
                self.assertEqual(hand_g2, "left")

        # Flip pinion hand to left -> driven gear must become right
        p_left = normalize_params({"gear_type": "helical", "helix_hand": "left"})
        geom_left = compute_gear_pair_geometry(p_left)
        self.assertEqual(_pick(geom_left["pinion"], ("helix_hand", "hand")), "left")
        self.assertEqual(_pick(geom_left["gear"], ("helix_hand", "hand")), "right")

    def test_03_helix_twist_continuity_and_matching_tangential_displacement(self) -> None:
        # 1. Helical 45 deg: continuous linear twist and exact r1 * psi1(z) == -r2 * psi2(z)
        p_hel = normalize_params(
            {
                "gear_type": "helical",
                "helix_angle_deg": 45.0,
                "helix_hand": "right",
                "face_width_mm": 16.0,
                "module_mm": 2.0,
                "pinion": {"teeth": 16},
                "gear": {"teeth": 32},
            }
        )
        geom_hel = compute_gear_pair_geometry(p_hel)
        r1 = float(_pick(geom_hel["pinion"], ("pitch_radius_mm", "reference_radius_mm", "r_pitch_mm", "r_mm")))
        r2 = float(_pick(geom_hel["gear"], ("pitch_radius_mm", "reference_radius_mm", "r_pitch_mm", "r_mm")))
        hand1 = str(_pick(geom_hel["pinion"], ("helix_hand", "hand")))
        hand2 = str(_pick(geom_hel["gear"], ("helix_hand", "hand")))
        b = float(p_hel["face_width_mm"])

        z_samples = np.linspace(0.0, b, 33)
        psi1_hel = [helix_twist_angle_rad(float(z), b, r1, 45.0, hand1, "helical") for z in z_samples]
        psi2_hel = [helix_twist_angle_rad(float(z), b, r2, 45.0, hand2, "helical") for z in z_samples]

        self.assertAlmostEqual(psi1_hel[0], 0.0, places=9)
        self.assertAlmostEqual(psi2_hel[0], 0.0, places=9)
        self.assertGreater(psi1_hel[-1], 0.0)
        self.assertLess(psi2_hel[-1], 0.0)

        # Continuity: small step changes in z produce small step changes in psi
        max_step_hel = max(abs(psi1_hel[i + 1] - psi1_hel[i]) for i in range(len(psi1_hel) - 1))
        self.assertLess(max_step_hel, 0.05)

        for z, p1_rad, p2_rad in zip(z_samples, psi1_hel, psi2_hel):
            # At beta=45 deg, tan(45)=1 => r1 * psi1(z) == +z and r2 * psi2(z) == -z
            self.assertAlmostEqual(r1 * p1_rad, float(z), places=9)
            self.assertAlmostEqual(r1 * p1_rad, -r2 * p2_rad, places=9)

        # 2. Herringbone 45 deg: psi(0) == psi(b) == 0, peak at z = b/2, exact r1 * psi1(z) == -r2 * psi2(z)
        psi1_hb = [helix_twist_angle_rad(float(z), b, r1, 45.0, hand1, "herringbone") for z in z_samples]
        psi2_hb = [helix_twist_angle_rad(float(z), b, r2, 45.0, hand2, "herringbone") for z in z_samples]

        self.assertAlmostEqual(psi1_hb[0], 0.0, places=9)
        self.assertAlmostEqual(psi1_hb[-1], 0.0, places=9)
        self.assertAlmostEqual(psi2_hb[0], 0.0, places=9)
        self.assertAlmostEqual(psi2_hb[-1], 0.0, places=9)

        mid_idx = len(z_samples) // 2  # z == b / 2
        self.assertAlmostEqual(r1 * psi1_hb[mid_idx], 0.5 * b, places=9)
        self.assertEqual(psi1_hb[mid_idx], max(psi1_hb))

        # Symmetry around b/2 and continuity across apex
        for i in range(len(z_samples)):
            self.assertAlmostEqual(psi1_hb[i], psi1_hb[-1 - i], places=9)
            self.assertAlmostEqual(r1 * psi1_hb[i], -r2 * psi2_hb[i], places=9)

        # Spur always has 0 twist
        self.assertEqual(helix_twist_angle_rad(8.0, b, r1, 45.0, "right", "spur"), 0.0)

    def test_04_dual_tooth_height_scaling_and_9_tooth_anti_undercut(self) -> None:
        # Dual tooth height: stub (0.75x) vs tall (1.25x)
        p_stub = normalize_params(
            {
                "gear_type": "spur",
                "module_mm": 2.0,
                "addendum_coeff": 0.75,
                "clearance_coeff": 0.25,
                "tip_chamfer_coeff": 0.0,
                "auto_profile_shift": False,
                "profile_shift_g1": 0.0,
                "profile_shift_g2": 0.0,
                "pinion": {"teeth": 20},
                "gear": {"teeth": 40},
            }
        )
        p_tall = copy.deepcopy(p_stub)
        p_tall["addendum_coeff"] = 1.25

        g_stub = compute_gear_pair_geometry(p_stub)
        g_tall = compute_gear_pair_geometry(p_tall)

        ra_stub = float(_pick(g_stub["pinion"], ("tip_radius_mm", "outer_radius_mm", "r_a_mm", "r_tip_mm")))
        ra_tall = float(_pick(g_tall["pinion"], ("tip_radius_mm", "outer_radius_mm", "r_a_mm", "r_tip_mm")))
        rf_stub = float(_pick(g_stub["pinion"], ("root_radius_mm", "r_f_mm", "r_root_mm")))
        rf_tall = float(_pick(g_tall["pinion"], ("root_radius_mm", "r_f_mm", "r_root_mm")))

        # Pitch radius r1 = 0.5 * 2.0 * 20 = 20.0 mm
        # Stub addendum = 1.5 mm -> r_a = 21.5 mm; Tall addendum = 2.5 mm -> r_a = 22.5 mm
        self.assertAlmostEqual(ra_stub, 21.5, delta=0.05)
        self.assertAlmostEqual(ra_tall, 22.5, delta=0.05)
        self.assertGreater(ra_tall - rf_tall, ra_stub - rf_stub + 1.5)

        # Verify actual 2D contour outer radius reflects stub vs tall tooth height
        c_stub = build_gear_2d_contour(p_stub, "pinion", samples_per_flank=14)
        c_tall = build_gear_2d_contour(p_tall, "pinion", samples_per_flank=14)
        self.assertGreater(_polygon_signed_area(c_stub), 0.0)
        self.assertGreater(_polygon_signed_area(c_tall), 0.0)
        self.assertGreater(float(np.hypot(c_tall[:, 0], c_tall[:, 1]).max()), float(np.hypot(c_stub[:, 0], c_stub[:, 1]).max()) + 0.8)

        # Anti-elephant-foot radial_inset_mm must preserve exact vertex count N
        c_inset = build_gear_2d_contour(p_stub, "pinion", samples_per_flank=14, radial_inset_mm=0.4)
        self.assertEqual(c_inset.shape, c_stub.shape)
        self.assertLess(float(np.hypot(c_inset[:, 0], c_inset[:, 1]).max()), float(np.hypot(c_stub[:, 0], c_stub[:, 1]).max()))

        # 9-tooth pinion anti-undercut profile shift
        p_9t_unshifted = normalize_params(
            {
                "gear_type": "spur",
                "module_mm": 2.0,
                "pressure_angle_deg": 20.0,
                "addendum_coeff": 1.0,
                "auto_profile_shift": False,
                "profile_shift_g1": 0.0,
                "profile_shift_g2": 0.0,
                "pinion": {"teeth": 9, "bore_type": "round", "bore_diameter_mm": 4.0},
                "gear": {"teeth": 36},
            }
        )
        p_9t_auto = copy.deepcopy(p_9t_unshifted)
        p_9t_auto["auto_profile_shift"] = True

        g_unshifted = compute_gear_pair_geometry(p_9t_unshifted)
        g_auto = compute_gear_pair_geometry(p_9t_auto)

        expected_xmin = 1.0 - 0.5 * 9.0 * (math.sin(math.radians(20.0)) ** 2)
        self.assertAlmostEqual(float(g_unshifted["x1"]), 0.0, places=6)
        self.assertGreaterEqual(float(g_auto["x1"]), expected_xmin - 1e-6)
        self.assertGreater(float(g_auto["nominal_center_distance_mm"]), float(g_unshifted["nominal_center_distance_mm"]))

        rep_unshifted = analyze_gear_pair(p_9t_unshifted)
        rep_auto = analyze_gear_pair(p_9t_auto)
        self.assertTrue(bool(_metric(rep_unshifted, "undercut_g1")))
        self.assertFalse(bool(_metric(rep_auto, "undercut_g1")))

        # Bore 2D contours check
        self.assertIsNone(build_bore_2d_contour({"bore_type": "none", "bore_diameter_mm": 5.0, "bore_clearance_mm": 0.1}, 10.0))
        for btype in ("round", "d_shaft", "double_d", "hex", "keyway"):
            b_cfg = normalize_gear_body({"bore_type": btype, "bore_diameter_mm": 6.0, "bore_clearance_mm": 0.12})
            b_poly = build_bore_2d_contour(b_cfg, max_allowed_radius_mm=8.0, radial_samples=64)
            self.assertIsNotNone(b_poly, f"Bore contour returned None for {btype}")
            assert b_poly is not None
            self.assertEqual(b_poly.ndim, 2)
            self.assertEqual(b_poly.shape[1], 2)
            self.assertGreater(_polygon_signed_area(b_poly), 0.0, f"Bore {btype} must be CCW")
            self.assertLessEqual(float(np.hypot(b_poly[:, 0], b_poly[:, 1]).max()), 8.0 + 1e-6)

    def test_05_meshed_2d_clearance_across_rotation_and_jamming_vs_thrust(self) -> None:
        # 1. Standard backlash at center_distance_offset_mm = 0.0 -> positive clearance across full pitch rotation
        p_ok = normalize_params(
            {
                "gear_type": "spur",
                "module_mm": 2.0,
                "pressure_angle_deg": 20.0,
                "backlash_mm": 0.16,
                "xy_compensation_mm": 0.02,
                "center_distance_offset_mm": 0.0,
                "pinion": {"teeth": 16},
                "gear": {"teeth": 32},
            }
        )
        geom_ok = compute_gear_pair_geometry(p_ok)
        c1_base = build_gear_2d_contour(p_ok, "pinion", samples_per_flank=16)
        c2_base = build_gear_2d_contour(p_ok, "gear", samples_per_flank=16)

        a_ok = float(geom_ok["center_distance_mm"])
        phase_g2 = float(geom_ok["mesh_phase_g2_rad"])
        z1 = int(p_ok["pinion"]["teeth"])
        z2 = int(p_ok["gear"]["teeth"])
        pitch_angle_g1 = 2.0 * math.pi / z1

        min_clearances: list[float] = []
        for theta1 in np.linspace(0.0, pitch_angle_g1, 12, endpoint=False):
            theta2 = phase_g2 - float(theta1) * (z1 / z2)
            g1_world = _rotate_2d(c1_base, float(theta1))
            g2_world = _rotate_2d(c2_base, theta2) + np.array([a_ok, 0.0], dtype=np.float64)
            collided, dist = _segments_intersect_or_min_dist(
                g1_world,
                g2_world,
                x_min=0.5 * geom_ok["m_n"] * z1 - 6.0,
                x_max=0.5 * geom_ok["m_n"] * z1 + 6.0,
                y_abs=8.0,
            )
            self.assertFalse(
                collided,
                f"Standard gear pair collided at theta1={math.degrees(theta1):.2f} deg!",
            )
            min_clearances.append(dist)

        self.assertGreater(min(min_clearances), 0.01)

        rep_ok = analyze_gear_pair(p_ok)
        self.assertFalse(bool(_metric(rep_ok, "jammed")))
        self.assertFalse(bool(_metric(rep_ok, "interference_detected")))
        self.assertGreater(float(_metric(rep_ok, "min_tooth_clearance_mm")), 0.0)
        self.assertGreater(float(_metric(rep_ok, "transverse_ratio")), 1.0)

        # 2. Negative center distance offset (-1.0 mm) -> physical overlap and jammed=True / interference_detected=True
        p_jam = copy.deepcopy(p_ok)
        p_jam["center_distance_offset_mm"] = -1.0
        geom_jam = compute_gear_pair_geometry(p_jam)
        a_jam = float(geom_jam["center_distance_mm"])

        any_2d_collision = False
        for theta1 in np.linspace(0.0, pitch_angle_g1, 12, endpoint=False):
            theta2 = float(geom_jam["mesh_phase_g2_rad"]) - float(theta1) * (z1 / z2)
            g1_world = _rotate_2d(c1_base, float(theta1))
            g2_world = _rotate_2d(c2_base, theta2) + np.array([a_jam, 0.0], dtype=np.float64)
            collided, _ = _segments_intersect_or_min_dist(
                g1_world,
                g2_world,
                x_min=0.5 * geom_jam["m_n"] * z1 - 6.0,
                x_max=0.5 * geom_jam["m_n"] * z1 + 6.0,
                y_abs=8.0,
            )
            if collided:
                any_2d_collision = True
                break
        self.assertTrue(any_2d_collision, "Expected 2D tooth contours to collide when center_distance_offset_mm = -1.0")

        rep_jam = analyze_gear_pair(p_jam)
        self.assertTrue(bool(_metric(rep_jam, "jammed")))
        self.assertTrue(bool(_metric(rep_jam, "interference_detected")))
        self.assertEqual(rep_jam.get("status"), "critical")

        # 3. Axial thrust: > 0 for helical 45 deg, == 0 for herringbone 45 deg (and spur)
        p_hel45 = normalize_params(
            {
                "gear_type": "helical",
                "helix_angle_deg": 45.0,
                "input_torque_nm": 2.0,
                "module_mm": 2.0,
                "pinion": {"teeth": 16},
                "gear": {"teeth": 32},
            }
        )
        rep_hel45 = analyze_gear_pair(p_hel45)
        fa_hel = float(_metric(rep_hel45, "axial_force_n"))
        ft_hel = float(_metric(rep_hel45, "tangential_force_n"))
        self.assertGreater(fa_hel, 0.0)
        # At beta = 45 deg, F_a = F_t * tan(45 deg) == F_t
        self.assertAlmostEqual(fa_hel, ft_hel, delta=max(0.05, 0.02 * ft_hel))
        self.assertFalse(bool(_metric(rep_hel45, "axial_thrust_balanced")))

        p_hb45 = copy.deepcopy(p_hel45)
        p_hb45["gear_type"] = "herringbone"
        rep_hb45 = analyze_gear_pair(p_hb45)
        fa_hb = float(_metric(rep_hb45, "axial_force_n"))
        self.assertAlmostEqual(fa_hb, 0.0, places=6)
        self.assertTrue(bool(_metric(rep_hb45, "axial_thrust_balanced")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
