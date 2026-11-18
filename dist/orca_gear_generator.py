# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy>=1.26"]
#
# [tool.orcaslicer.plugin]
# name = "Orca Gear Studio"
# description = "Estudio parametrico 3D de engrenagens com simulacao de giro, testes de encaixe e envio direto para a mesa"
# author = "Orca Gear Studio"
# version = "1.2.0"
# ///

from __future__ import annotations

import sys as _orca_init_sys
import types as _orca_init_types
if __name__ not in _orca_init_sys.modules:
    _orca_init_sys.modules[__name__] = _orca_init_types.ModuleType(__name__)

# ===========================================================================
# MODULE: gear_studio.schema
# ===========================================================================

"""Unified parameter schema and validation for Orca Gear Studio."""

pass  # [bundled] hoisted __future__ import

import copy
import math
from typing import Any

SCHEMA_VERSION: int = 1

VALID_GEAR_TYPES: tuple[str, ...] = ("spur", "helical", "herringbone")
VALID_HELIX_HANDS: tuple[str, ...] = ("right", "left")
VALID_BORE_TYPES: tuple[str, ...] = ("none", "round", "d_shaft", "double_d", "hex", "keyway")
VALID_RECESS_SIDES: tuple[str, ...] = ("top", "bottom", "both")
VALID_LIGHTENING_MODES: tuple[str, ...] = ("solid", "web_recess", "lightening_holes")
VALID_SIM_DIRECTIONS: tuple[str, ...] = ("cw", "ccw")
VALID_EXPORT_TARGETS: tuple[str, ...] = (
    "pair_separated",
    "pinion_only",
    "gear_only",
    "fit_test_kit",
    "full_suite",
)

DEFAULT_PARAMS: dict[str, Any] = {
    "schema_version": SCHEMA_VERSION,
    "name": "Par Engrenagens",
    "gear_type": "spur",
    "module_mm": 2.0,
    "pressure_angle_deg": 20.0,
    "helix_angle_deg": 30.0,
    "helix_hand": "right",
    "face_width_mm": 12.0,
    "addendum_coeff": 1.00,
    "clearance_coeff": 0.25,
    "root_fillet_coeff": 0.30,
    "tip_chamfer_coeff": 0.06,
    "auto_profile_shift": True,
    "profile_shift_g1": 0.0,
    "profile_shift_g2": 0.0,
    "backlash_mm": 0.15,
    "xy_compensation_mm": 0.02,
    "elephant_foot_chamfer_mm": 0.40,
    "center_distance_offset_mm": 0.0,
    "input_torque_nm": 1.0,
    "pinion": {
        "teeth": 16,
        "bore_type": "d_shaft",
        "bore_diameter_mm": 5.0,
        "bore_clearance_mm": 0.12,
        "d_flat_depth_mm": 0.50,
        "keyway_width_mm": 2.0,
        "keyway_depth_mm": 1.0,
        "hub_enabled": False,
        "hub_diameter_mm": 14.0,
        "hub_height_mm": 5.0,
        "recess_enabled": False,
        "recess_side": "top",
        "recess_diameter_mm": 16.0,
        "recess_depth_mm": 4.0,
        "lightening_mode": "solid",
        "web_thickness_mm": 4.0,
        "lightening_hole_count": 6,
        "lightening_hole_diameter_mm": 5.0,
    },
    "gear": {
        "teeth": 32,
        "bore_type": "round",
        "bore_diameter_mm": 8.0,
        "bore_clearance_mm": 0.12,
        "d_flat_depth_mm": 0.60,
        "keyway_width_mm": 3.0,
        "keyway_depth_mm": 1.4,
        "hub_enabled": False,
        "hub_diameter_mm": 20.0,
        "hub_height_mm": 5.0,
        "recess_enabled": False,
        "recess_side": "top",
        "recess_diameter_mm": 22.0,
        "recess_depth_mm": 3.5,
        "lightening_mode": "lightening_holes",
        "web_thickness_mm": 4.0,
        "lightening_hole_count": 6,
        "lightening_hole_diameter_mm": 8.0,
    },
    "sim_rpm": 24.0,
    "sim_direction": "cw",
    "export_target": "pair_separated",
    "auto_configure_slicer": True,
}


def _to_float(val: Any, default: float, lo: float, hi: float) -> float:
    if isinstance(val, bool):
        return default
    try:
        f = float(val)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(f):
        return default
    return max(lo, min(hi, f))


def _to_int(val: Any, default: int, lo: int, hi: int) -> int:
    if isinstance(val, bool):
        return default
    try:
        f = float(val)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(f):
        return default
    i = int(round(f))
    return max(lo, min(hi, i))


def _to_bool(val: Any, default: bool) -> bool:
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        if math.isfinite(val):
            return bool(val)
        return default
    if isinstance(val, str):
        s = val.strip().lower()
        if s in ("true", "1", "yes", "on"):
            return True
        if s in ("false", "0", "no", "off", ""):
            return False
    return default


def _to_choice(val: Any, default: str, valid: tuple[str, ...]) -> str:
    if isinstance(val, str):
        s = val.strip().lower()
        if s in valid:
            return s
    return default


def normalize_gear_body(
    raw_body: dict[str, Any] | None,
    default_teeth: int = 16,
    default_bore_type: str = "round",
    default_bore_mm: float = 8.0,
    *,
    defaults_template: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Normalize and clamp a single gear body sub-dictionary (pinion or gear)."""
    if isinstance(defaults_template, dict):
        base = copy.deepcopy(defaults_template)
    else:
        safe_bore_type = default_bore_type if default_bore_type in VALID_BORE_TYPES else "round"
        base = {
            "teeth": int(default_teeth),
            "bore_type": safe_bore_type,
            "bore_diameter_mm": float(default_bore_mm),
            "bore_clearance_mm": 0.12,
            "d_flat_depth_mm": 0.50,
            "keyway_width_mm": 2.0,
            "keyway_depth_mm": 1.0,
            "hub_enabled": False,
            "hub_diameter_mm": max(14.0, float(default_bore_mm) + 8.0),
            "hub_height_mm": 5.0,
            "recess_enabled": False,
            "recess_side": "top",
            "recess_diameter_mm": max(16.0, float(default_bore_mm) + 10.0),
            "recess_depth_mm": 4.0,
            "lightening_mode": "solid",
            "web_thickness_mm": 4.0,
            "lightening_hole_count": 6,
            "lightening_hole_diameter_mm": 5.0,
        }

    src = raw_body if isinstance(raw_body, dict) else {}

    return {
        "teeth": _to_int(src.get("teeth", base["teeth"]), int(base["teeth"]), 6, 240),
        "bore_type": _to_choice(
            src.get("bore_type", base["bore_type"]),
            str(base["bore_type"]),
            VALID_BORE_TYPES,
        ),
        "bore_diameter_mm": _to_float(
            src.get("bore_diameter_mm", base["bore_diameter_mm"]),
            float(base["bore_diameter_mm"]),
            1.0,
            160.0,
        ),
        "bore_clearance_mm": _to_float(
            src.get("bore_clearance_mm", base["bore_clearance_mm"]),
            float(base["bore_clearance_mm"]),
            -0.25,
            1.50,
        ),
        "d_flat_depth_mm": _to_float(
            src.get("d_flat_depth_mm", base["d_flat_depth_mm"]),
            float(base["d_flat_depth_mm"]),
            0.05,
            25.0,
        ),
        "keyway_width_mm": _to_float(
            src.get("keyway_width_mm", base["keyway_width_mm"]),
            float(base["keyway_width_mm"]),
            0.50,
            40.0,
        ),
        "keyway_depth_mm": _to_float(
            src.get("keyway_depth_mm", base["keyway_depth_mm"]),
            float(base["keyway_depth_mm"]),
            0.25,
            25.0,
        ),
        "hub_enabled": _to_bool(src.get("hub_enabled", base["hub_enabled"]), bool(base["hub_enabled"])),
        "hub_diameter_mm": _to_float(
            src.get("hub_diameter_mm", base["hub_diameter_mm"]),
            float(base["hub_diameter_mm"]),
            3.0,
            300.0,
        ),
        "hub_height_mm": _to_float(
            src.get("hub_height_mm", base["hub_height_mm"]),
            float(base["hub_height_mm"]),
            0.5,
            80.0,
        ),
        "recess_enabled": _to_bool(
            src.get("recess_enabled", base["recess_enabled"]),
            bool(base["recess_enabled"]),
        ),
        "recess_side": _to_choice(
            src.get("recess_side", base["recess_side"]),
            str(base["recess_side"]),
            VALID_RECESS_SIDES,
        ),
        "recess_diameter_mm": _to_float(
            src.get("recess_diameter_mm", base["recess_diameter_mm"]),
            float(base["recess_diameter_mm"]),
            3.0,
            300.0,
        ),
        "recess_depth_mm": _to_float(
            src.get("recess_depth_mm", base["recess_depth_mm"]),
            float(base["recess_depth_mm"]),
            0.5,
            60.0,
        ),
        "lightening_mode": _to_choice(
            src.get("lightening_mode", base["lightening_mode"]),
            str(base["lightening_mode"]),
            VALID_LIGHTENING_MODES,
        ),
        "web_thickness_mm": _to_float(
            src.get("web_thickness_mm", base["web_thickness_mm"]),
            float(base["web_thickness_mm"]),
            1.2,
            80.0,
        ),
        "lightening_hole_count": _to_int(
            src.get("lightening_hole_count", base["lightening_hole_count"]),
            int(base["lightening_hole_count"]),
            3,
            18,
        ),
        "lightening_hole_diameter_mm": _to_float(
            src.get("lightening_hole_diameter_mm", base["lightening_hole_diameter_mm"]),
            float(base["lightening_hole_diameter_mm"]),
            1.5,
            100.0,
        ),
    }


def effective_helix_angle_deg(params: dict[str, Any] | None) -> float:
    """Return effective helix angle in degrees (0.0 when gear_type == 'spur')."""
    if not isinstance(params, dict):
        return 0.0
    gear_type = _to_choice(params.get("gear_type"), DEFAULT_PARAMS["gear_type"], VALID_GEAR_TYPES)
    if gear_type == "spur":
        return 0.0
    return _to_float(params.get("helix_angle_deg"), DEFAULT_PARAMS["helix_angle_deg"], 0.0, 60.0)


def normalize_params(raw: dict[str, Any] | None) -> dict[str, Any]:
    """Deep-copy DEFAULT_PARAMS, merge raw values, coerce types, and clamp bounds."""
    d = DEFAULT_PARAMS
    src = raw if isinstance(raw, dict) else {}

    raw_name = src.get("name", d["name"])
    if isinstance(raw_name, str) and raw_name.strip():
        clean_name = raw_name.strip()[:80]
    else:
        clean_name = str(d["name"])

    pinion = normalize_gear_body(
        src.get("pinion") if isinstance(src.get("pinion"), dict) else None,
        default_teeth=int(d["pinion"]["teeth"]),
        default_bore_type=str(d["pinion"]["bore_type"]),
        default_bore_mm=float(d["pinion"]["bore_diameter_mm"]),
        defaults_template=d["pinion"],
    )
    gear = normalize_gear_body(
        src.get("gear") if isinstance(src.get("gear"), dict) else None,
        default_teeth=int(d["gear"]["teeth"]),
        default_bore_type=str(d["gear"]["bore_type"]),
        default_bore_mm=float(d["gear"]["bore_diameter_mm"]),
        defaults_template=d["gear"],
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "name": clean_name,
        "gear_type": _to_choice(src.get("gear_type"), d["gear_type"], VALID_GEAR_TYPES),
        "module_mm": _to_float(src.get("module_mm"), d["module_mm"], 0.5, 10.0),
        "pressure_angle_deg": _to_float(
            src.get("pressure_angle_deg"), d["pressure_angle_deg"], 14.5, 30.0
        ),
        "helix_angle_deg": _to_float(src.get("helix_angle_deg"), d["helix_angle_deg"], 0.0, 60.0),
        "helix_hand": _to_choice(src.get("helix_hand"), d["helix_hand"], VALID_HELIX_HANDS),
        "face_width_mm": _to_float(src.get("face_width_mm"), d["face_width_mm"], 2.0, 120.0),
        "addendum_coeff": _to_float(src.get("addendum_coeff"), d["addendum_coeff"], 0.40, 1.40),
        "clearance_coeff": _to_float(src.get("clearance_coeff"), d["clearance_coeff"], 0.10, 0.50),
        "root_fillet_coeff": _to_float(
            src.get("root_fillet_coeff"), d["root_fillet_coeff"], 0.05, 0.45
        ),
        "tip_chamfer_coeff": _to_float(
            src.get("tip_chamfer_coeff"), d["tip_chamfer_coeff"], 0.00, 0.25
        ),
        "auto_profile_shift": _to_bool(src.get("auto_profile_shift"), d["auto_profile_shift"]),
        "profile_shift_g1": _to_float(
            src.get("profile_shift_g1"), d["profile_shift_g1"], -0.50, 0.80
        ),
        "profile_shift_g2": _to_float(
            src.get("profile_shift_g2"), d["profile_shift_g2"], -0.50, 0.80
        ),
        "backlash_mm": _to_float(src.get("backlash_mm"), d["backlash_mm"], 0.00, 1.00),
        "xy_compensation_mm": _to_float(
            src.get("xy_compensation_mm"), d["xy_compensation_mm"], -0.20, 0.30
        ),
        "elephant_foot_chamfer_mm": _to_float(
            src.get("elephant_foot_chamfer_mm"), d["elephant_foot_chamfer_mm"], 0.00, 1.50
        ),
        "center_distance_offset_mm": _to_float(
            src.get("center_distance_offset_mm"), d["center_distance_offset_mm"], -1.50, 3.00
        ),
        "input_torque_nm": _to_float(src.get("input_torque_nm"), d["input_torque_nm"], 0.05, 50.0),
        "pinion": pinion,
        "gear": gear,
        "sim_rpm": _to_float(src.get("sim_rpm"), d["sim_rpm"], 1.0, 300.0),
        "sim_direction": _to_choice(src.get("sim_direction"), d["sim_direction"], VALID_SIM_DIRECTIONS),
        "export_target": _to_choice(src.get("export_target"), d["export_target"], VALID_EXPORT_TARGETS),
        "auto_configure_slicer": _to_bool(
            src.get("auto_configure_slicer"), d["auto_configure_slicer"]
        ),
    }

# ===========================================================================
# MODULE: gear_studio.involute_math
# ===========================================================================

"""ISO 21771 / ISO 53 transverse + normal involute gear geometry and 2D contour builders."""

pass  # [bundled] hoisted __future__ import

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
    pass  # [bundled] resolved intra-package import


def involute_fn(alpha_rad: float) -> float:
    """Standard involute function inv(a) = tan(a) - a (cancellation-free for small angles)."""
    if abs(alpha_rad) < 0.08:
        a2 = alpha_rad * alpha_rad
        a3 = a2 * alpha_rad
        return a3 * (
            (1.0 / 3.0)
            + a2 * (
                (2.0 / 15.0)
                + a2 * ((17.0 / 315.0) + a2 * ((62.0 / 2835.0) + a2 * (1382.0 / 155925.0)))
            )
        )
    return math.tan(alpha_rad) - alpha_rad


def inverse_involute_fn(inv_val: float) -> float:
    """Solve tan(a) - a = inv_val for a in [0, pi/2) via Newton-Raphson accurate to < 1e-14."""
    if not math.isfinite(inv_val) or inv_val <= 0.0:
        return 0.0

    max_alpha = 0.5 * math.pi - 1e-9
    if inv_val < 0.5:
        c = (3.0 * inv_val) ** (1.0 / 3.0)
        alpha = c / (1.0 + 0.4 * c * c / 3.0)
    else:
        alpha = min(max_alpha, 0.5 * math.pi - 1.0 / (inv_val + 0.5 * math.pi))

    alpha = max(1e-15, min(max_alpha, alpha))

    for _ in range(40):
        t = math.tan(alpha)
        t2 = t * t
        if t2 <= 1e-30:
            break
        residual = involute_fn(alpha) - inv_val
        step = residual / t2
        next_alpha = alpha - step
        if next_alpha <= 0.0:
            alpha *= 0.5
        elif next_alpha >= max_alpha:
            alpha = 0.5 * (alpha + max_alpha)
        else:
            alpha = next_alpha
        if abs(step) <= 1e-15:
            break

    return alpha


def _transverse_tooth_thickness_at_radius(
    r: float,
    rb: float,
    psi_b: float,
) -> float:
    """Return transverse arc tooth thickness s_t(r) at radius r >= rb."""
    if r <= 0.0:
        return 0.0
    if r <= rb:
        return 2.0 * r * psi_b
    cos_a = max(-1.0, min(1.0, rb / r))
    alpha_r = math.acos(cos_a)
    psi_r = psi_b - involute_fn(alpha_r)
    return 2.0 * r * psi_r


def _clamp_tip_radius_non_pointed(
    ra_target: float,
    r_ref: float,
    rb: float,
    rf: float,
    psi_b: float,
    min_tip_thickness_mm: float,
) -> tuple[float, float]:
    """Ensure s_t(r_a) >= min_tip_thickness_mm via exact bisection so teeth never self-intersect."""
    s_target = _transverse_tooth_thickness_at_radius(ra_target, rb, psi_b)
    if s_target > min_tip_thickness_mm:
        return ra_target, s_target

    r_lo = max(rf + 0.05, min(r_ref, rb))
    s_lo = _transverse_tooth_thickness_at_radius(r_lo, rb, psi_b)
    if s_lo <= min_tip_thickness_mm:
        return r_lo, max(1e-4, s_lo)

    lo = r_lo
    hi = ra_target
    for _ in range(48):
        mid = 0.5 * (lo + hi)
        s_mid = _transverse_tooth_thickness_at_radius(mid, rb, psi_b)
        if s_mid >= min_tip_thickness_mm:
            lo = mid
        else:
            hi = mid

    s_final = _transverse_tooth_thickness_at_radius(lo, rb, psi_b)
    return lo, max(1e-4, s_final)


def compute_gear_pair_geometry(params: dict[str, Any]) -> dict[str, Any]:
    """Compute ISO 21771 / ISO 53 transverse & normal involute geometry for the gear pair."""
    p = normalize_params(params)

    beta_deg = effective_helix_angle_deg(p)
    beta_rad = math.radians(beta_deg)
    cos_beta = math.cos(beta_rad)

    m_n = float(p["module_mm"])
    m_t = m_n / cos_beta

    alpha_n_deg = float(p["pressure_angle_deg"])
    alpha_n_rad = math.radians(alpha_n_deg)
    tan_alpha_n = math.tan(alpha_n_rad)

    alpha_t_rad = math.atan(tan_alpha_n / cos_beta)
    alpha_t_deg = math.degrees(alpha_t_rad)
    cos_alpha_t = math.cos(alpha_t_rad)
    sin_alpha_t = math.sin(alpha_t_rad)
    inv_alpha_t = involute_fn(alpha_t_rad)

    z1 = int(p["pinion"]["teeth"])
    z2 = int(p["gear"]["teeth"])
    z_sum = float(z1 + z2)

    h_a_coeff = float(p["addendum_coeff"])
    c_coeff = float(p["clearance_coeff"])

    x_min_1 = max(0.0, h_a_coeff - 0.5 * z1 * (sin_alpha_t * sin_alpha_t))
    x_min_2 = max(0.0, h_a_coeff - 0.5 * z2 * (sin_alpha_t * sin_alpha_t))

    raw_x1 = float(p["profile_shift_g1"])
    raw_x2 = float(p["profile_shift_g2"])
    if p["auto_profile_shift"]:
        x1 = max(raw_x1, x_min_1)
        x2 = max(raw_x2, x_min_2)
    else:
        x1 = raw_x1
        x2 = raw_x2

    inv_alpha_tw_raw = inv_alpha_t + 2.0 * tan_alpha_n * (x1 + x2) / z_sum
    alpha_tw_rad = inverse_involute_fn(max(0.0, inv_alpha_tw_raw))
    alpha_tw_deg = math.degrees(alpha_tw_rad)
    cos_alpha_tw = max(1e-6, math.cos(alpha_tw_rad))

    a0 = 0.5 * m_t * z_sum * cos_alpha_t / cos_alpha_tw
    a = max(2.0, a0 + float(p["center_distance_offset_mm"]))

    rw1 = a * float(z1) / z_sum
    rw2 = a * float(z2) / z_sum

    r1 = 0.5 * m_t * float(z1)
    r2 = 0.5 * m_t * float(z2)
    rb1 = r1 * cos_alpha_t
    rb2 = r2 * cos_alpha_t

    backlash_mm = float(p["backlash_mm"])
    xy_comp_mm = float(p["xy_compensation_mm"])
    s_min_pitch = 0.15 * m_t
    s_max_pitch = 0.90 * math.pi * m_t

    s_t1 = m_t * (0.5 * math.pi + 2.0 * x1 * tan_alpha_n) - backlash_mm / (2.0 * cos_beta) - 2.0 * xy_comp_mm
    s_t2 = m_t * (0.5 * math.pi + 2.0 * x2 * tan_alpha_n) - backlash_mm / (2.0 * cos_beta) - 2.0 * xy_comp_mm
    s_t1 = max(s_min_pitch, min(s_max_pitch, s_t1))
    s_t2 = max(s_min_pitch, min(s_max_pitch, s_t2))

    psi_b1 = s_t1 / (2.0 * r1) + inv_alpha_t
    psi_b2 = s_t2 / (2.0 * r2) + inv_alpha_t

    ded1 = max(0.10 * m_n, m_n * (h_a_coeff + c_coeff - x1))
    ded2 = max(0.10 * m_n, m_n * (h_a_coeff + c_coeff - x2))
    rf1 = max(0.8, r1 - ded1)
    rf2 = max(0.8, r2 - ded2)

    add1_raw = max(0.10 * m_n, m_n * (h_a_coeff + x1))
    add2_raw = max(0.10 * m_n, m_n * (h_a_coeff + x2))
    ra1_raw = r1 + add1_raw
    ra2_raw = r2 + add2_raw

    min_tip_s = 0.08 * m_n
    ra1, s_a1 = _clamp_tip_radius_non_pointed(ra1_raw, r1, rb1, rf1, psi_b1, min_tip_s)
    ra2, s_a2 = _clamp_tip_radius_non_pointed(ra2_raw, r2, rb2, rf2, psi_b2, min_tip_s)

    add1 = ra1 - r1
    add2 = ra2 - r2

    # Minimum center distance before zero-backlash dual-flank lockup or tip-to-root bottoming out
    inv_lock_rhs = (float(z1) * psi_b1 + float(z2) * psi_b2 - math.pi) / z_sum
    alpha_lock_rad = inverse_involute_fn(max(0.0, inv_lock_rhs))
    a_inv_lock = (rb1 + rb2) / max(1e-6, math.cos(alpha_lock_rad))
    a_bottom = max(ra1 + rf2, ra2 + rf1)
    min_non_jam_a = max(a_inv_lock, a_bottom)

    pinion_hand = str(p["helix_hand"])
    gear_hand = "left" if pinion_hand == "right" else "right"
    face_w = float(p["face_width_mm"])

    mesh_phase_g2_rad = math.pi - (math.pi / float(z2))
    ratio = float(z2) / float(z1)

    pinion_geom: dict[str, Any] = {
        "teeth": z1,
        "profile_shift": x1,
        "min_profile_shift_no_undercut": x_min_1,
        "undercut": bool(x1 < x_min_1 - 1e-4),
        "pitch_radius_mm": r1,
        "pitch_diameter_mm": 2.0 * r1,
        "working_pitch_radius_mm": rw1,
        "working_pitch_diameter_mm": 2.0 * rw1,
        "base_radius_mm": rb1,
        "base_diameter_mm": 2.0 * rb1,
        "tip_radius_mm": ra1,
        "tip_diameter_mm": 2.0 * ra1,
        "root_radius_mm": rf1,
        "root_diameter_mm": 2.0 * rf1,
        "addendum_mm": add1,
        "dedendum_mm": r1 - rf1,
        "tooth_height_mm": ra1 - rf1,
        "tooth_thickness_pitch_mm": s_t1,
        "tip_thickness_mm": s_a1,
        "base_half_angle_rad": psi_b1,
        "helix_hand": pinion_hand,
        "face_width_mm": face_w,
    }

    gear_geom: dict[str, Any] = {
        "teeth": z2,
        "profile_shift": x2,
        "min_profile_shift_no_undercut": x_min_2,
        "undercut": bool(x2 < x_min_2 - 1e-4),
        "pitch_radius_mm": r2,
        "pitch_diameter_mm": 2.0 * r2,
        "working_pitch_radius_mm": rw2,
        "working_pitch_diameter_mm": 2.0 * rw2,
        "base_radius_mm": rb2,
        "base_diameter_mm": 2.0 * rb2,
        "tip_radius_mm": ra2,
        "tip_diameter_mm": 2.0 * ra2,
        "root_radius_mm": rf2,
        "root_diameter_mm": 2.0 * rf2,
        "addendum_mm": add2,
        "dedendum_mm": r2 - rf2,
        "tooth_height_mm": ra2 - rf2,
        "tooth_thickness_pitch_mm": s_t2,
        "tip_thickness_mm": s_a2,
        "base_half_angle_rad": psi_b2,
        "helix_hand": gear_hand,
        "face_width_mm": face_w,
    }

    return {
        "beta_deg": beta_deg,
        "beta_rad": beta_rad,
        "alpha_n_deg": alpha_n_deg,
        "alpha_t_deg": alpha_t_deg,
        "alpha_tw_deg": alpha_tw_deg,
        "m_n": m_n,
        "m_t": m_t,
        "x1": x1,
        "x2": x2,
        "nominal_center_distance_mm": a0,
        "center_distance_mm": a,
        "min_non_jam_center_distance_mm": min_non_jam_a,
        "ratio": ratio,
        "mesh_phase_g2_rad": mesh_phase_g2_rad,
        "pinion": pinion_geom,
        "gear": gear_geom,
    }


def helix_twist_angle_rad(
    z_mm: float,
    face_width_mm: float,
    pitch_radius_mm: float,
    beta_deg: float,
    hand: str,
    gear_type: str,
) -> float:
    """Compute cross-section axial twist angle psi(z) in radians."""
    gt = str(gear_type).strip().lower()
    if gt == "spur" or abs(beta_deg) < 1e-6 or pitch_radius_mm <= 1e-6:
        return 0.0

    sign = 1.0 if str(hand).strip().lower() == "right" else -1.0
    if gt == "herringbone":
        z_eff = min(float(z_mm), float(face_width_mm) - float(z_mm))
    else:
        z_eff = float(z_mm)

    return sign * z_eff * math.tan(math.radians(float(beta_deg))) / float(pitch_radius_mm)


def build_gear_2d_contour(
    params: dict[str, Any],
    which: str = "pinion",
    samples_per_flank: int = 14,
    radial_inset_mm: float = 0.0,
) -> np.ndarray:
    """Build strictly CCW-ordered (N, 2) float64 array of all Z teeth centered at (0, 0).

    Tooth 0 is centered symmetrically on +X (angle = 0).
    Vertex count is strictly Z * (2 * max(4, samples_per_flank) + 10) regardless of radial_inset_mm
    or tip_chamfer_coeff so Z-rings stitch 1-to-1 without degenerate edges.
    """
    p = normalize_params(params)
    geom = compute_gear_pair_geometry(p)
    key = "gear" if str(which).strip().lower() == "gear" else "pinion"
    g = geom[key]

    z_teeth = int(g["teeth"])
    m_n = float(geom["m_n"])
    m_t = float(geom["m_t"])
    alpha_t_rad = math.radians(float(geom["alpha_t_deg"]))
    alpha_n_rad = math.radians(float(geom["alpha_n_deg"]))
    inv_alpha_t = involute_fn(alpha_t_rad)

    r_ref = float(g["pitch_radius_mm"])
    rb = float(g["base_radius_mm"])
    ra_base = float(g["tip_radius_mm"])
    rf_base = float(g["root_radius_mm"])
    s_t_base = float(g["tooth_thickness_pitch_mm"])

    n_flank = max(4, int(samples_per_flank))
    n_inv = n_flank - 1

    tau_half = math.pi / float(z_teeth)

    # Apply smooth inward bevel offset for anti-elephant-foot chamfer while keeping exact vertex count
    inset = max(0.0, float(radial_inset_mm))
    if inset > 0.0:
        max_safe_inset = min(0.32 * m_n, 0.25 * (ra_base - rf_base), 0.20 * s_t_base)
        eff_inset = min(inset, max(0.0, max_safe_inset))
        rf = max(0.5, rf_base - eff_inset)
        ra_target = max(rf + 0.20 * m_n, ra_base - eff_inset)
        s_t = max(0.16 * m_t, s_t_base - 2.0 * eff_inset / max(0.5, math.cos(alpha_n_rad)))
    else:
        rf = rf_base
        ra_target = ra_base
        s_t = s_t_base

    psi_b = s_t / (2.0 * r_ref) + inv_alpha_t
    ra, _ = _clamp_tip_radius_non_pointed(ra_target, r_ref, rb, rf, psi_b, 0.06 * m_n)

    def _inv_half_angle(radius_val: float) -> float:
        if radius_val <= rb:
            return psi_b
        cos_a = max(-1.0, min(1.0, rb / radius_val))
        return psi_b - involute_fn(math.acos(cos_a))

    # Root fillet join radius & smooth tangent arc to root circle rf
    rho_fillet = max(0.02 * m_n, min(float(p["root_fillet_coeff"]) * m_n, 0.45 * (ra - rf)))
    r_join = max(rb, min(rf + rho_fillet, rf + 0.48 * (ra - rf)))
    r_join = min(r_join, ra - 0.08 * (ra - rf))

    psi_join = _inv_half_angle(r_join)
    # Guarantee root valley angular clearance even on extreme positive profile shift
    max_psi_join = 0.86 * tau_half
    if psi_join > max_psi_join:
        angle_scale = max_psi_join / psi_join
    else:
        angle_scale = 1.0

    def _scaled_psi(radius_val: float) -> float:
        return max(1e-5, _inv_half_angle(radius_val) * angle_scale)

    psi_join_eff = _scaled_psi(r_join)

    # Tip chamfer bevel near r_a
    c_tip_raw = float(p["tip_chamfer_coeff"]) * m_n
    c_tip = max(0.0, min(c_tip_raw, 0.28 * (ra - r_join)))
    psi_ra = _scaled_psi(ra)

    if c_tip > 1e-5:
        r_chamf = ra - c_tip
        psi_tip_corner = max(0.22 * psi_ra, psi_ra - 0.85 * c_tip / max(1.0, ra))
    else:
        # Pure unchamfered involute up to ra with identical vertex count
        r_chamf = r_join + (float(n_inv - 1) / float(n_inv)) * (ra - r_join)
        psi_tip_corner = psi_ra

    # Sample involute flank from r_join to r_chamf with sqrt-biased density near base circle
    u_inv = np.linspace(0.0, 1.0, n_inv, dtype=np.float64)
    # Blend quadratic and linear parameter so base curvature is extra crisp
    s_param = 0.55 * (u_inv * u_inv) + 0.45 * u_inv
    r_inv_pts = r_join + s_param * (r_chamf - r_join)
    psi_inv_pts = np.array([_scaled_psi(float(rv)) for rv in r_inv_pts], dtype=np.float64)

    # Smooth root fillet (3 interior/end samples u in [0.30, 0.65, 1.0]) tangent to root circle rf
    avail_valley = max(1e-4, tau_half - psi_join_eff)
    delta_psi_fil = min(max(rho_fillet / max(1.0, rf), 0.16 * avail_valley), 0.68 * avail_valley)
    psi_fil_end = psi_join_eff + delta_psi_fil

    u_fil = np.array([0.32, 0.68, 1.0], dtype=np.float64)
    psi_fil_upper = psi_join_eff + u_fil * delta_psi_fil
    r_fil_upper = rf + (r_join - rf) * (1.0 - np.sin(0.5 * math.pi * u_fil))

    psi_root_mid = 0.5 * (psi_fil_end + tau_half)

    # Assemble single-tooth polar coordinates (phi, r) in strictly increasing angle order (-tau_half, +tau_half]
    # Count = 1 + 3 + n_flank + 1 + n_flank + 3 + 2 = 2 * n_flank + 10
    phi_lower_flank = np.concatenate((-psi_inv_pts, np.array([-psi_tip_corner], dtype=np.float64)))
    r_lower_flank = np.concatenate((r_inv_pts, np.array([ra], dtype=np.float64)))

    phi_upper_flank = np.concatenate((np.array([psi_tip_corner], dtype=np.float64), psi_inv_pts[::-1]))
    r_upper_flank = np.concatenate((np.array([ra], dtype=np.float64), r_inv_pts[::-1]))

    phi_tooth = np.concatenate(
        (
            np.array([-psi_root_mid], dtype=np.float64),
            -psi_fil_upper[::-1],
            phi_lower_flank,
            np.array([0.0], dtype=np.float64),
            phi_upper_flank,
            psi_fil_upper,
            np.array([psi_root_mid, tau_half], dtype=np.float64),
        )
    )
    r_tooth = np.concatenate(
        (
            np.array([rf], dtype=np.float64),
            r_fil_upper[::-1],
            r_lower_flank,
            np.array([ra], dtype=np.float64),
            r_upper_flank,
            r_fil_upper,
            np.array([rf, rf], dtype=np.float64),
        )
    )

    # Replicate across all Z teeth in vectorized NumPy
    tooth_offsets = (np.arange(z_teeth, dtype=np.float64) * (2.0 * math.pi / float(z_teeth)))[:, None]
    all_angles = (tooth_offsets + phi_tooth[None, :]).reshape(-1)
    all_radii = np.broadcast_to(r_tooth[None, :], (z_teeth, len(r_tooth))).reshape(-1)

    pts = np.empty((len(all_angles), 2), dtype=np.float64)
    pts[:, 0] = all_radii * np.cos(all_angles)
    pts[:, 1] = all_radii * np.sin(all_angles)
    return pts


def _distribute_monotonic_angles(
    critical_angles: list[float],
    total_samples: int,
    interval_weights: list[float] | None = None,
) -> np.ndarray:
    """Distribute `total_samples` strictly increasing angles in [0, 2*pi) hitting every critical corner."""
    two_pi = 2.0 * math.pi
    cleaned: list[float] = []
    for a in sorted(x % two_pi for x in critical_angles):
        if not cleaned or (a - cleaned[-1]) > 1e-5:
            cleaned.append(a)
    if len(cleaned) > 1 and (two_pi + cleaned[0] - cleaned[-1]) <= 1e-5:
        cleaned.pop()
    if not cleaned:
        cleaned = [0.0]

    k = len(cleaned)
    if total_samples <= k:
        return np.linspace(0.0, two_pi, total_samples, endpoint=False, dtype=np.float64)

    spans = [
        (cleaned[(i + 1) % k] - cleaned[i]) % two_pi or two_pi
        for i in range(k)
    ]
    if interval_weights is not None and len(interval_weights) == k:
        weights = [max(1e-4, spans[i] * interval_weights[i]) for i in range(k)]
    else:
        weights = spans

    w_sum = sum(weights)
    raw_counts = [total_samples * (w / w_sum) for w in weights]
    counts = [max(1, int(math.floor(rc))) for rc in raw_counts]

    diff = total_samples - sum(counts)
    if diff > 0:
        remainders = sorted(
            range(k),
            key=lambda idx: (raw_counts[idx] - counts[idx], weights[idx]),
            reverse=True,
        )
        for idx in remainders[:diff]:
            counts[idx] += 1
    elif diff < 0:
        reducibles = sorted(
            range(k),
            key=lambda idx: (counts[idx], -(raw_counts[idx] - counts[idx])),
            reverse=True,
        )
        idx_ptr = 0
        while diff < 0 and idx_ptr < len(reducibles) * 4:
            cand = reducibles[idx_ptr % len(reducibles)]
            if counts[cand] > 1:
                counts[cand] -= 1
                diff += 1
            idx_ptr += 1

    out: list[float] = []
    for i in range(k):
        a0 = cleaned[i]
        span = spans[i]
        c = counts[i]
        for j in range(c):
            out.append((a0 + (float(j) / float(c)) * span) % two_pi)

    # Rotate sequence if cleaned[0] > 0 isn't needed; cleaned[0] == 0.0 keeps strict [0, 2*pi) order
    return np.asarray(out, dtype=np.float64)


def build_bore_2d_contour(
    bore_cfg: dict[str, Any],
    max_allowed_radius_mm: float,
    radial_samples: int = 64,
    extra_clearance_mm: float = 0.0,
) -> np.ndarray | None:
    """Build strictly CCW-ordered (M, 2) float64 closed bore contour, or None if bore_type == 'none'.

    All 5 active bore shapes ('round', 'd_shaft', 'double_d', 'hex', 'keyway') preserve exact
    sharp mechanical corners, strictly monotonic polar angle in [0, 2*pi), fixed length M == radial_samples,
    and outer radius clamped <= max_allowed_radius_mm.
    """
    cfg = normalize_gear_body(bore_cfg if isinstance(bore_cfg, dict) else {})
    bore_type = str(cfg.get("bore_type", "round")).strip().lower()
    if bore_type == "none" or bore_type not in VALID_BORE_TYPES:
        return None

    m_samples = max(18, int(radial_samples))
    max_r = max(0.4, float(max_allowed_radius_mm))

    d_eff = (
        float(cfg["bore_diameter_mm"])
        + float(cfg["bore_clearance_mm"])
        + float(extra_clearance_mm)
    )
    r_nom = max(0.35, min(max_r, 0.5 * d_eff))

    if bore_type == "round":
        angles = np.linspace(0.0, 2.0 * math.pi, m_samples, endpoint=False, dtype=np.float64)
        pts = np.empty((m_samples, 2), dtype=np.float64)
        pts[:, 0] = r_nom * np.cos(angles)
        pts[:, 1] = r_nom * np.sin(angles)
        return pts

    if bore_type in ("d_shaft", "double_d"):
        flat_depth = max(0.05 * r_nom, min(float(cfg["d_flat_depth_mm"]), 0.68 * r_nom))
        y_flat = r_nom - flat_depth
        theta_c = math.asin(max(0.05, min(0.999, y_flat / r_nom)))

        if bore_type == "d_shaft":
            crit = [0.0, theta_c, math.pi - theta_c]
            weights = [1.0, 1.35, 1.0]
        else:
            crit = [0.0, theta_c, math.pi - theta_c, math.pi + theta_c, 2.0 * math.pi - theta_c]
            weights = [1.0, 1.35, 1.0, 1.35, 1.0]

        angles = _distribute_monotonic_angles(crit, m_samples, weights)
        radii = np.full(m_samples, r_nom, dtype=np.float64)
        sin_a = np.sin(angles)
        if bore_type == "d_shaft":
            mask = sin_a > 1e-7
            radii[mask] = np.minimum(r_nom, y_flat / sin_a[mask])
        else:
            abs_sin = np.abs(sin_a)
            mask = abs_sin > 1e-7
            radii[mask] = np.minimum(r_nom, y_flat / abs_sin[mask])

        pts = np.empty((m_samples, 2), dtype=np.float64)
        pts[:, 0] = radii * np.cos(angles)
        pts[:, 1] = radii * sin_a
        return pts

    if bore_type == "hex":
        # Across-flats = 2 * apothem; corner circumradius = apothem / cos(30 deg)
        cos30 = math.cos(math.pi / 6.0)
        apothem = min(r_nom, max_r * cos30)
        crit = [k * (math.pi / 3.0) for k in range(6)]
        angles = _distribute_monotonic_angles(crit, m_samples)
        sector_idx = np.floor((angles % (2.0 * math.pi)) / (math.pi / 3.0)).astype(np.int32)
        sector_idx = np.clip(sector_idx, 0, 5)
        mid_angles = (sector_idx.astype(np.float64) + 0.5) * (math.pi / 3.0)
        radii = np.minimum(max_r, apothem / np.cos(angles - mid_angles))

        pts = np.empty((m_samples, 2), dtype=np.float64)
        pts[:, 0] = radii * np.cos(angles)
        pts[:, 1] = radii * np.sin(angles)
        return pts

    # bore_type == "keyway"
    # Rectangular slot of width keyway_width_mm x radial depth keyway_depth_mm at +Y
    r_circle = min(r_nom, 0.92 * max_r)
    half_w = max(0.15 * r_circle, min(0.5 * float(cfg["keyway_width_mm"]), 0.65 * r_circle))
    y_circle = math.sqrt(max(1e-6, r_circle * r_circle - half_w * half_w))

    max_y_top = math.sqrt(max(y_circle * y_circle + 1e-5, max_r * max_r - half_w * half_w))
    raw_y_top = r_circle + max(0.15, float(cfg["keyway_depth_mm"]))
    y_top = min(raw_y_top, max_y_top)
    if y_top <= y_circle + 0.05:
        # Ultra-tight outer boundary: shrink r_circle slightly so keyway notch stays distinct
        r_circle = max(0.30, 0.80 * max_r)
        half_w = max(0.15 * r_circle, min(0.5 * float(cfg["keyway_width_mm"]), 0.60 * r_circle))
        y_circle = math.sqrt(max(1e-6, r_circle * r_circle - half_w * half_w))
        max_y_top = math.sqrt(max(y_circle * y_circle + 1e-5, max_r * max_r - half_w * half_w))
        y_top = min(r_circle + max(0.15, float(cfg["keyway_depth_mm"])), max_y_top)

    t1 = math.atan2(y_circle, half_w)
    t2 = math.atan2(y_top, half_w)
    t3 = math.pi - t2
    t4 = math.pi - t1

    crit = [0.0, t1, t2, t3, t4]
    weights = [1.0, 2.5, 2.0, 2.5, 1.0]
    angles = _distribute_monotonic_angles(crit, m_samples, weights)

    pts = np.empty((m_samples, 2), dtype=np.float64)
    eps = 1e-9
    for idx, ang in enumerate(angles):
        if t1 - eps <= ang <= t2 + eps:
            x = half_w
            y = min(y_top, max(y_circle, half_w * math.tan(ang)))
        elif t2 - eps < ang < t3 + eps:
            y = y_top
            tan_a = math.tan(ang)
            x = 0.0 if abs(tan_a) > 1e12 else max(-half_w, min(half_w, y_top / tan_a))
        elif t3 - eps <= ang <= t4 + eps:
            x = -half_w
            y = min(y_top, max(y_circle, -half_w * math.tan(ang)))
        else:
            x = r_circle * math.cos(ang)
            y = r_circle * math.sin(ang)
        pts[idx, 0] = x
        pts[idx, 1] = y

    # Final safety radial clamp
    rad_sq = pts[:, 0] * pts[:, 0] + pts[:, 1] * pts[:, 1]
    over_mask = rad_sq > (max_r * max_r)
    if np.any(over_mask):
        scale = max_r / np.sqrt(rad_sq[over_mask])
        pts[over_mask, 0] *= scale
        pts[over_mask, 1] *= scale

    return pts

# ===========================================================================
# MODULE: gear_studio.fit_and_kinematics
# ===========================================================================

"""Contact ratio, 2D polygon interference/jamming detection, kinematics, and FDM printability."""

pass  # [bundled] hoisted __future__ import

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
    pass  # [bundled] resolved intra-package import

if "compute_gear_pair_geometry" not in globals():
    pass  # [bundled] resolved intra-package import

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

# ===========================================================================
# MODULE: gear_studio.mesh_generator
# ===========================================================================

"""Strict 2-manifold 3D gear and Fit-Test Kit mesh generator for Orca Gear Studio."""

pass  # [bundled] hoisted __future__ import

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
    pass  # [bundled] resolved intra-package import

if "compute_gear_pair_geometry" not in globals():
    pass  # [bundled] resolved intra-package import


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

# ===========================================================================
# MODULE: gear_studio.presets_catalog
# ===========================================================================

"""Curated built-in mechanical gear presets, user preset storage, and smart printable randomizer."""

pass  # [bundled] hoisted __future__ import

import copy
import datetime as _dt
import json
import math
import random
import re
import uuid
from pathlib import Path
from typing import Any

_PRESETS_FALLBACK_GEAR_BODY: dict[str, Any] = {
    "teeth": 16,
    "bore_type": "round",
    "bore_diameter_mm": 8.0,
    "bore_clearance_mm": 0.12,
    "d_flat_depth_mm": 0.50,
    "keyway_width_mm": 2.0,
    "keyway_depth_mm": 1.0,
    "hub_enabled": False,
    "hub_diameter_mm": 14.0,
    "hub_height_mm": 5.0,
    "recess_enabled": False,
    "recess_side": "top",
    "recess_diameter_mm": 16.0,
    "recess_depth_mm": 4.0,
    "lightening_mode": "solid",
    "web_thickness_mm": 4.0,
    "lightening_hole_count": 6,
    "lightening_hole_diameter_mm": 5.0,
}

_PRESETS_FALLBACK_DEFAULT_PARAMS: dict[str, Any] = {
    "schema_version": 1,
    "name": "Par Engrenagens",
    "gear_type": "spur",
    "module_mm": 2.0,
    "pressure_angle_deg": 20.0,
    "helix_angle_deg": 30.0,
    "helix_hand": "right",
    "face_width_mm": 12.0,
    "addendum_coeff": 1.00,
    "clearance_coeff": 0.25,
    "root_fillet_coeff": 0.30,
    "tip_chamfer_coeff": 0.06,
    "auto_profile_shift": True,
    "profile_shift_g1": 0.0,
    "profile_shift_g2": 0.0,
    "backlash_mm": 0.15,
    "xy_compensation_mm": 0.02,
    "elephant_foot_chamfer_mm": 0.40,
    "center_distance_offset_mm": 0.0,
    "input_torque_nm": 1.0,
    "pinion": {
        **_PRESETS_FALLBACK_GEAR_BODY,
        "teeth": 16,
        "bore_type": "d_shaft",
        "bore_diameter_mm": 5.0,
        "bore_clearance_mm": 0.12,
        "d_flat_depth_mm": 0.50,
        "keyway_width_mm": 2.0,
        "keyway_depth_mm": 1.0,
        "hub_enabled": False,
        "hub_diameter_mm": 14.0,
        "hub_height_mm": 5.0,
        "recess_enabled": False,
        "recess_side": "top",
        "recess_diameter_mm": 16.0,
        "recess_depth_mm": 4.0,
        "lightening_mode": "solid",
        "web_thickness_mm": 4.0,
        "lightening_hole_count": 6,
        "lightening_hole_diameter_mm": 5.0,
    },
    "gear": {
        **_PRESETS_FALLBACK_GEAR_BODY,
        "teeth": 32,
        "bore_type": "round",
        "bore_diameter_mm": 8.0,
        "bore_clearance_mm": 0.12,
        "d_flat_depth_mm": 0.60,
        "keyway_width_mm": 3.0,
        "keyway_depth_mm": 1.4,
        "hub_enabled": False,
        "hub_diameter_mm": 20.0,
        "hub_height_mm": 5.0,
        "recess_enabled": False,
        "recess_side": "top",
        "recess_diameter_mm": 22.0,
        "recess_depth_mm": 3.5,
        "lightening_mode": "lightening_holes",
        "web_thickness_mm": 4.0,
        "lightening_hole_count": 6,
        "lightening_hole_diameter_mm": 8.0,
    },
    "sim_rpm": 24.0,
    "sim_direction": "cw",
    "export_target": "pair_separated",
    "auto_configure_slicer": True,
}


def _presets_clamp_float(val: Any, lo: float, hi: float, default: float) -> float:
    try:
        num = float(val)
        if not math.isfinite(num):
            return default
        return max(lo, min(hi, num))
    except (TypeError, ValueError):
        return default


def _presets_clamp_int(val: Any, lo: int, hi: int, default: int) -> int:
    try:
        num = int(round(float(val)))
        return max(lo, min(hi, num))
    except (TypeError, ValueError):
        return default


def _presets_deep_merge(dst: dict[str, Any], src: dict[str, Any]) -> None:
    for k, v in src.items():
        if isinstance(v, dict) and isinstance(dst.get(k), dict):
            _presets_deep_merge(dst[k], v)
        else:
            dst[k] = copy.deepcopy(v)


def _presets_fallback_normalize_body(
    raw_body: Any,
    default_teeth: int = 16,
    default_bore_type: str = "round",
    default_bore_mm: float = 8.0,
    default_lightening: str = "solid",
) -> dict[str, Any]:
    src = raw_body if isinstance(raw_body, dict) else {}
    bt = str(src.get("bore_type", default_bore_type)).strip().lower()
    if bt not in ("none", "round", "d_shaft", "double_d", "hex", "keyway"):
        bt = default_bore_type
    rs = str(src.get("recess_side", "top")).strip().lower()
    if rs not in ("top", "bottom", "both"):
        rs = "top"
    lm = str(src.get("lightening_mode", default_lightening)).strip().lower()
    if lm not in ("solid", "web_recess", "lightening_holes"):
        lm = default_lightening

    return {
        "teeth": _presets_clamp_int(src.get("teeth"), 6, 200, default_teeth),
        "bore_type": bt,
        "bore_diameter_mm": _presets_clamp_float(src.get("bore_diameter_mm"), 1.5, 80.0, default_bore_mm),
        "bore_clearance_mm": _presets_clamp_float(src.get("bore_clearance_mm"), -0.10, 0.80, 0.12),
        "d_flat_depth_mm": _presets_clamp_float(src.get("d_flat_depth_mm"), 0.10, 8.0, 0.50),
        "keyway_width_mm": _presets_clamp_float(src.get("keyway_width_mm"), 1.0, 20.0, 2.0),
        "keyway_depth_mm": _presets_clamp_float(src.get("keyway_depth_mm"), 0.5, 12.0, 1.0),
        "hub_enabled": bool(src.get("hub_enabled", False)),
        "hub_diameter_mm": _presets_clamp_float(src.get("hub_diameter_mm"), 4.0, 160.0, 16.0),
        "hub_height_mm": _presets_clamp_float(src.get("hub_height_mm"), 0.5, 60.0, 5.0),
        "recess_enabled": bool(src.get("recess_enabled", False)),
        "recess_side": rs,
        "recess_diameter_mm": _presets_clamp_float(src.get("recess_diameter_mm"), 4.0, 160.0, 20.0),
        "recess_depth_mm": _presets_clamp_float(src.get("recess_depth_mm"), 0.5, 60.0, 3.5),
        "lightening_mode": lm,
        "web_thickness_mm": _presets_clamp_float(src.get("web_thickness_mm"), 1.2, 60.0, 4.0),
        "lightening_hole_count": _presets_clamp_int(src.get("lightening_hole_count"), 3, 12, 6),
        "lightening_hole_diameter_mm": _presets_clamp_float(
            src.get("lightening_hole_diameter_mm"), 2.0, 60.0, 6.0
        ),
    }


def _presets_fallback_normalize(raw: dict[str, Any] | None = None) -> dict[str, Any]:
    out = copy.deepcopy(_PRESETS_FALLBACK_DEFAULT_PARAMS)
    if isinstance(raw, dict):
        _presets_deep_merge(out, raw)

    out["schema_version"] = 1
    out["name"] = str(out.get("name") or "Par Engrenagens").strip()[:80] or "Par Engrenagens"

    gt = str(out.get("gear_type", "spur")).strip().lower()
    out["gear_type"] = gt if gt in ("spur", "helical", "herringbone") else "spur"

    out["module_mm"] = _presets_clamp_float(out.get("module_mm"), 0.5, 10.0, 2.0)
    out["pressure_angle_deg"] = _presets_clamp_float(out.get("pressure_angle_deg"), 14.5, 30.0, 20.0)
    out["helix_angle_deg"] = _presets_clamp_float(out.get("helix_angle_deg"), 0.0, 60.0, 30.0)

    hh = str(out.get("helix_hand", "right")).strip().lower()
    out["helix_hand"] = hh if hh in ("right", "left") else "right"

    out["face_width_mm"] = _presets_clamp_float(out.get("face_width_mm"), 2.0, 120.0, 12.0)
    out["addendum_coeff"] = _presets_clamp_float(out.get("addendum_coeff"), 0.40, 1.40, 1.00)
    out["clearance_coeff"] = _presets_clamp_float(out.get("clearance_coeff"), 0.10, 0.50, 0.25)
    out["root_fillet_coeff"] = _presets_clamp_float(out.get("root_fillet_coeff"), 0.05, 0.45, 0.30)
    out["tip_chamfer_coeff"] = _presets_clamp_float(out.get("tip_chamfer_coeff"), 0.00, 0.25, 0.06)

    out["auto_profile_shift"] = bool(out.get("auto_profile_shift", True))
    out["profile_shift_g1"] = _presets_clamp_float(out.get("profile_shift_g1"), -0.50, 0.80, 0.0)
    out["profile_shift_g2"] = _presets_clamp_float(out.get("profile_shift_g2"), -0.50, 0.80, 0.0)

    out["backlash_mm"] = _presets_clamp_float(out.get("backlash_mm"), 0.00, 1.00, 0.15)
    out["xy_compensation_mm"] = _presets_clamp_float(out.get("xy_compensation_mm"), -0.20, 0.30, 0.02)
    out["elephant_foot_chamfer_mm"] = _presets_clamp_float(out.get("elephant_foot_chamfer_mm"), 0.00, 1.50, 0.40)
    out["center_distance_offset_mm"] = _presets_clamp_float(out.get("center_distance_offset_mm"), -1.50, 3.00, 0.0)
    out["input_torque_nm"] = _presets_clamp_float(out.get("input_torque_nm"), 0.05, 50.0, 1.0)

    out["pinion"] = _presets_fallback_normalize_body(
        out.get("pinion"),
        default_teeth=16,
        default_bore_type="d_shaft",
        default_bore_mm=5.0,
        default_lightening="solid",
    )
    out["gear"] = _presets_fallback_normalize_body(
        out.get("gear"),
        default_teeth=32,
        default_bore_type="round",
        default_bore_mm=8.0,
        default_lightening="lightening_holes",
    )

    out["sim_rpm"] = _presets_clamp_float(out.get("sim_rpm"), 1.0, 300.0, 24.0)
    sd = str(out.get("sim_direction", "cw")).strip().lower()
    out["sim_direction"] = sd if sd in ("cw", "ccw") else "cw"

    et = str(out.get("export_target", "pair_separated")).strip().lower()
    if et not in ("pair_separated", "pinion_only", "gear_only", "fit_test_kit", "full_suite"):
        et = "pair_separated"
    out["export_target"] = et
    out["auto_configure_slicer"] = bool(out.get("auto_configure_slicer", True))
    return out


if "DEFAULT_PARAMS" not in globals() or "normalize_params" not in globals():
    try:
        pass  # [bundled] resolved intra-package import
    except (ImportError, KeyError, ValueError):
        DEFAULT_PARAMS = _PRESETS_FALLBACK_DEFAULT_PARAMS
        normalize_params = _presets_fallback_normalize


_USER_PRESETS_FILENAME = "user_presets.json"


def _make_preset_params(overrides: dict[str, Any]) -> dict[str, Any]:
    """Build a normalized preset parameter dictionary from clean base defaults + overrides."""
    base = copy.deepcopy(DEFAULT_PARAMS)
    base["pinion"]["hub_enabled"] = False
    base["pinion"]["recess_enabled"] = False
    base["pinion"]["lightening_mode"] = "solid"
    base["gear"]["hub_enabled"] = False
    base["gear"]["recess_enabled"] = False
    base["gear"]["lightening_mode"] = "solid"
    _presets_deep_merge(base, overrides)
    return normalize_params(base)


def _make_builtin_entry(
    preset_id: str,
    name_pt: str,
    name_en: str,
    category: str,
    desc_pt: str,
    desc_en: str,
    overrides: dict[str, Any],
) -> dict[str, Any]:
    params_override = {"name": name_pt, **overrides}
    return {
        "id": preset_id,
        "name_pt": name_pt,
        "name_en": name_en,
        "title_pt": name_pt,
        "title_en": name_en,
        "category": category,
        "desc_pt": desc_pt,
        "desc_en": desc_en,
        "description_pt": desc_pt,
        "description_en": desc_en,
        "params": _make_preset_params(params_override),
    }


BUILTIN_PRESETS: list[dict[str, Any]] = [
    _make_builtin_entry(
        preset_id="spur_classic_1_2",
        name_pt="Redutor Clássico Reto 1:2",
        name_en="Classic 1:2 Spur Reducer",
        category="standard",
        desc_pt="Par reto ISO módulo 2.0 (16:32 dentes) versátil e fácil de imprimir sem empuxo axial.",
        desc_en="Versatile ISO module 2.0 spur pair (16:32 teeth) with zero axial thrust.",
        overrides={
            "gear_type": "spur",
            "module_mm": 2.0,
            "pressure_angle_deg": 20.0,
            "face_width_mm": 12.0,
            "pinion": {
                "teeth": 16,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 5.0,
                "d_flat_depth_mm": 0.50,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 32,
                "bore_type": "round",
                "bore_diameter_mm": 8.0,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 6,
                "lightening_hole_diameter_mm": 8.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="helical_silent_45",
        name_pt="Helicoidal Silenciosa 45° Sem Suporte",
        name_en="Silent 45° Support-Free Helical",
        category="helical",
        desc_pt="Hélice a 45° auto-suportada em FDM com engrenamento progressivo ultra-silencioso (1:3).",
        desc_en="Support-free 45° helix angle for FDM with ultra-quiet progressive meshing (1:3).",
        overrides={
            "gear_type": "helical",
            "helix_angle_deg": 45.0,
            "helix_hand": "right",
            "module_mm": 1.75,
            "face_width_mm": 14.0,
            "pinion": {
                "teeth": 15,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 5.0,
                "d_flat_depth_mm": 0.50,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 45,
                "bore_type": "round",
                "bore_diameter_mm": 8.0,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 6,
                "lightening_hole_diameter_mm": 12.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="herringbone_extruder_1_4",
        name_pt="Extrusora Espinha de Peixe Alto Torque",
        name_en="High-Torque Herringbone Extruder 1:4",
        category="herringbone",
        desc_pt="Dupla hélice simétrica em V (30°, 11:44) auto-centrante com empuxo axial líquido nulo.",
        desc_en="Self-centering V-shaped double helical pair (30°, 11:44) with zero net axial thrust.",
        overrides={
            "gear_type": "herringbone",
            "helix_angle_deg": 30.0,
            "module_mm": 1.5,
            "face_width_mm": 10.0,
            "auto_profile_shift": True,
            "pinion": {
                "teeth": 11,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 5.0,
                "d_flat_depth_mm": 0.50,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 44,
                "bore_type": "hex",
                "bore_diameter_mm": 8.0,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 6,
                "lightening_hole_diameter_mm": 9.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="nema17_to_m8_1_5",
        name_pt="NEMA 17 Eixo-D 5mm -> Eixo M8 1:5",
        name_en="NEMA 17 5mm D-Shaft to M8 1:5",
        category="robotics",
        desc_pt="Redução direta 1:5 acoplando motor de passo NEMA 17 (eixo D 5mm) a varão/parafuso M8.",
        desc_en="Direct 1:5 reduction stage coupling a NEMA 17 stepper (5mm D-shaft) to an M8 shaft.",
        overrides={
            "gear_type": "helical",
            "helix_angle_deg": 25.0,
            "module_mm": 2.0,
            "face_width_mm": 12.0,
            "pinion": {
                "teeth": 12,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 5.0,
                "d_flat_depth_mm": 0.50,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 60,
                "bore_type": "round",
                "bore_diameter_mm": 8.0,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 6,
                "lightening_hole_diameter_mm": 14.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="stub_heavy_duty",
        name_pt="Dente Curto Stub Ultra-Robusto",
        name_en="Heavy-Duty Stub Tooth Reducer",
        category="industrial",
        desc_pt="Perfil stub (adendo 0.75× e filete de raiz amplo 0.38×) para máxima resistência à flexão.",
        desc_en="Short stub tooth profile (0.75× addendum, 0.38× root fillet) for maximum bending strength.",
        overrides={
            "gear_type": "spur",
            "module_mm": 2.5,
            "face_width_mm": 16.0,
            "addendum_coeff": 0.75,
            "clearance_coeff": 0.25,
            "root_fillet_coeff": 0.38,
            "input_torque_nm": 4.0,
            "pinion": {
                "teeth": 14,
                "bore_type": "double_d",
                "bore_diameter_mm": 8.0,
                "d_flat_depth_mm": 0.80,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 28,
                "bore_type": "round",
                "bore_diameter_mm": 10.0,
                "lightening_mode": "web_recess",
                "web_thickness_mm": 6.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="high_contact_smooth",
        name_pt="Alta Razão de Contato Suave",
        name_en="Smooth High-Contact-Ratio Drive",
        category="helical",
        desc_pt="Dentes alongados (adendo 1.20×) combinados com hélice de 35° para múltiplos dentes em carga.",
        desc_en="Tall addendum (1.20×) paired with a 35° helix for continuous multi-tooth load sharing.",
        overrides={
            "gear_type": "helical",
            "helix_angle_deg": 35.0,
            "module_mm": 1.5,
            "face_width_mm": 14.0,
            "addendum_coeff": 1.20,
            "clearance_coeff": 0.30,
            "pinion": {
                "teeth": 20,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 5.0,
                "d_flat_depth_mm": 0.50,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 40,
                "bore_type": "round",
                "bore_diameter_mm": 8.0,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 6,
                "lightening_hole_diameter_mm": 8.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="micro_pinion_shifted",
        name_pt="Micro Pinhão 9 Dentes Anti-Undercut",
        name_en="9-Tooth Shifted Micro Pinion",
        category="precision",
        desc_pt="Pinhão compacto de 9 dentes com correção positiva de perfil (+0.35) eliminando adelgaçamento.",
        desc_en="Compact 9-tooth pinion with positive profile shift (+0.35) eliminating root undercut.",
        overrides={
            "gear_type": "spur",
            "module_mm": 2.0,
            "face_width_mm": 12.0,
            "auto_profile_shift": True,
            "profile_shift_g1": 0.35,
            "profile_shift_g2": 0.0,
            "pinion": {
                "teeth": 9,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 4.0,
                "d_flat_depth_mm": 0.40,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 36,
                "bore_type": "round",
                "bore_diameter_mm": 8.0,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 6,
                "lightening_hole_diameter_mm": 9.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="sync_1_1_helical_45",
        name_pt="Transmissão 1:1 Helicoidal 45°",
        name_en="1:1 Synchronous 45° Helical",
        category="helical",
        desc_pt="Par síncrono 1:1 (22:22 dentes) com hélice de 45° para inversão suave de rotação entre eixos.",
        desc_en="Synchronous 1:1 pair (22:22 teeth) with 45° helix for smooth counter-rotating shafts.",
        overrides={
            "gear_type": "helical",
            "helix_angle_deg": 45.0,
            "module_mm": 2.0,
            "face_width_mm": 14.0,
            "pinion": {
                "teeth": 22,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 6.0,
                "d_flat_depth_mm": 0.60,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 5,
                "lightening_hole_diameter_mm": 7.0,
            },
            "gear": {
                "teeth": 22,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 6.0,
                "d_flat_depth_mm": 0.60,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 5,
                "lightening_hole_diameter_mm": 7.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="bearing_608_spoked",
        name_pt="Coroa c/ Alojamento Rolamento 608ZZ",
        name_en="608ZZ Bearing-Seated Gear Pair",
        category="robotics",
        desc_pt="Coroa helicoidal com rebaixo de precisão Ø22.2×7.0 mm pronto para prensar rolamento 608ZZ.",
        desc_en="Helical driven gear featuring a Ø22.2×7.0 mm pocket engineered for a standard 608ZZ bearing.",
        overrides={
            "gear_type": "helical",
            "helix_angle_deg": 20.0,
            "module_mm": 2.0,
            "face_width_mm": 10.0,
            "pinion": {
                "teeth": 15,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 5.0,
                "d_flat_depth_mm": 0.50,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 42,
                "bore_type": "round",
                "bore_diameter_mm": 8.0,
                "recess_enabled": True,
                "recess_side": "top",
                "recess_diameter_mm": 22.2,
                "recess_depth_mm": 7.0,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 6,
                "lightening_hole_diameter_mm": 9.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="robotics_compact_m125",
        name_pt="Robótica Compacta Módulo 1.25",
        name_en="Compact Robotics Module 1.25",
        category="herringbone",
        desc_pt="Transmissão espinha de peixe fina (m=1.25, 35°, 16:48) com arraste sextavado na coroa.",
        desc_en="Fine-pitch herringbone drive (m=1.25, 35°, 16:48) with hex shaft/nut drive on the gear.",
        overrides={
            "gear_type": "herringbone",
            "helix_angle_deg": 35.0,
            "module_mm": 1.25,
            "face_width_mm": 10.0,
            "pinion": {
                "teeth": 16,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 5.0,
                "d_flat_depth_mm": 0.50,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 48,
                "bore_type": "hex",
                "bore_diameter_mm": 8.0,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 6,
                "lightening_hole_diameter_mm": 8.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="industrial_keyway_m35",
        name_pt="Industrial Módulo 3.5 Chaveta DIN",
        name_en="Industrial Module 3.5 DIN Keyway",
        category="industrial",
        desc_pt="Engrenagens pesadas módulo 3.5 (14:26) com rasgos de chaveta DIN e cubos reforçados.",
        desc_en="Heavy-duty module 3.5 gears (14:26) equipped with DIN keyway bores and reinforced hubs.",
        overrides={
            "gear_type": "spur",
            "module_mm": 3.5,
            "face_width_mm": 18.0,
            "input_torque_nm": 8.0,
            "pinion": {
                "teeth": 14,
                "bore_type": "keyway",
                "bore_diameter_mm": 10.0,
                "keyway_width_mm": 3.0,
                "keyway_depth_mm": 1.4,
                "hub_enabled": True,
                "hub_diameter_mm": 22.0,
                "hub_height_mm": 6.0,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 26,
                "bore_type": "keyway",
                "bore_diameter_mm": 12.0,
                "keyway_width_mm": 4.0,
                "keyway_depth_mm": 1.8,
                "hub_enabled": True,
                "hub_diameter_mm": 28.0,
                "hub_height_mm": 6.0,
                "lightening_mode": "web_recess",
                "web_thickness_mm": 8.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="quick_fit_calibration",
        name_pt="Calibração Rápida de Encaixe FDM",
        name_en="Quick FDM Fit Calibration Kit",
        category="calibration",
        desc_pt="Kit rápido de 10 minutos (setores 45°, base de 2 pinos na distância entre centros e régua de furo).",
        desc_en="Fast 10-minute calibration kit (45° sectors, 2-pin center-distance jig, and 4-step bore gauge).",
        overrides={
            "gear_type": "helical",
            "helix_angle_deg": 45.0,
            "module_mm": 2.0,
            "face_width_mm": 10.0,
            "export_target": "fit_test_kit",
            "pinion": {
                "teeth": 14,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 5.0,
                "d_flat_depth_mm": 0.50,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 24,
                "bore_type": "round",
                "bore_diameter_mm": 8.0,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 6,
                "lightening_hole_diameter_mm": 6.5,
            },
        },
    ),
]


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")
    return slug[:32] or "preset"


def _user_presets_path(presets_dir: str | Path) -> Path:
    return Path(presets_dir) / _USER_PRESETS_FILENAME


def _sanitize_user_preset_entry(entry: dict[str, Any]) -> dict[str, Any] | None:
    if not isinstance(entry, dict):
        return None
    raw_params = entry.get("params")
    if not isinstance(raw_params, dict):
        return None
    name = (
        str(entry.get("name") or entry.get("name_pt") or entry.get("title_pt") or raw_params.get("name") or "Meu Par")
        .strip()[:80]
    )
    if not name:
        name = "Meu Par"
    preset_id = str(entry.get("id") or "").strip() or f"user_{_slugify(name)}_{uuid.uuid4().hex[:6]}"
    norm_params = normalize_params(raw_params)
    norm_params["name"] = name
    now_iso = _dt.datetime.now(_dt.timezone.utc).isoformat()
    desc_pt = str(entry.get("desc_pt") or entry.get("description_pt") or "Preset mecânico salvo pelo usuário")
    desc_en = str(entry.get("desc_en") or entry.get("description_en") or "User-saved custom gear preset")
    name_pt = str(entry.get("name_pt") or entry.get("title_pt") or name)
    name_en = str(entry.get("name_en") or entry.get("title_en") or name)
    return {
        "id": preset_id,
        "name": name,
        "name_pt": name_pt,
        "name_en": name_en,
        "title_pt": name_pt,
        "title_en": name_en,
        "category": "user",
        "desc_pt": desc_pt,
        "desc_en": desc_en,
        "description_pt": desc_pt,
        "description_en": desc_en,
        "created_at": str(entry.get("created_at") or now_iso),
        "updated_at": str(entry.get("updated_at") or now_iso),
        "params": norm_params,
    }


def _write_user_presets_file(presets_dir: str | Path, presets: list[dict[str, Any]]) -> None:
    folder = Path(presets_dir)
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)
    target = folder / _USER_PRESETS_FILENAME
    payload = {"version": "1.0", "presets": presets}
    with open(target, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)


def load_user_presets(presets_dir: str | Path) -> list[dict[str, Any]]:
    """Load and validate user-saved presets from presets_dir/user_presets.json."""
    target = _user_presets_path(presets_dir)
    if not target.is_file():
        return []
    try:
        with open(target, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return []

    raw_list = raw.get("presets") if isinstance(raw, dict) else raw
    if not isinstance(raw_list, list):
        return []

    cleaned: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for item in raw_list:
        sanitized = _sanitize_user_preset_entry(item)
        if sanitized is not None and sanitized["id"] not in seen_ids:
            seen_ids.add(sanitized["id"])
            cleaned.append(sanitized)
    return cleaned


def save_user_preset(
    presets_dir: str | Path,
    name: str,
    params: dict[str, Any],
    preset_id: str | None = None,
) -> list[dict[str, Any]]:
    """Save or update a user preset in presets_dir and return the updated list."""
    existing = load_user_presets(presets_dir)
    clean_name = str(name or "").strip()[:80]
    if not clean_name:
        clean_name = str((params or {}).get("name") or "Meu Par").strip()[:80] or "Meu Par"

    norm_params = normalize_params(params if isinstance(params, dict) else {})
    norm_params["name"] = clean_name
    now_iso = _dt.datetime.now(_dt.timezone.utc).isoformat()

    target_id = str(preset_id).strip() if preset_id else ""
    updated = False
    if target_id:
        for idx, item in enumerate(existing):
            if item.get("id") == target_id:
                existing[idx] = {
                    **item,
                    "id": target_id,
                    "name": clean_name,
                    "name_pt": clean_name,
                    "name_en": clean_name,
                    "title_pt": clean_name,
                    "title_en": clean_name,
                    "updated_at": now_iso,
                    "params": norm_params,
                }
                updated = True
                break

    if not updated:
        if not target_id:
            target_id = f"user_{_slugify(clean_name)}_{uuid.uuid4().hex[:8]}"
        existing.append(
            {
                "id": target_id,
                "name": clean_name,
                "name_pt": clean_name,
                "name_en": clean_name,
                "title_pt": clean_name,
                "title_en": clean_name,
                "category": "user",
                "desc_pt": "Preset mecânico salvo pelo usuário",
                "desc_en": "User-saved custom gear preset",
                "description_pt": "Preset mecânico salvo pelo usuário",
                "description_en": "User-saved custom gear preset",
                "created_at": now_iso,
                "updated_at": now_iso,
                "params": norm_params,
            }
        )

    _write_user_presets_file(presets_dir, existing)
    return existing


def delete_user_preset(presets_dir: str | Path, preset_id: str) -> list[dict[str, Any]]:
    """Delete a user preset by preset_id and return the remaining presets list."""
    target_id = str(preset_id or "").strip()
    existing = load_user_presets(presets_dir)
    remaining = [item for item in existing if item.get("id") != target_id]
    if len(remaining) != len(existing) or _user_presets_path(presets_dir).is_file():
        _write_user_presets_file(presets_dir, remaining)
    return remaining


def generate_random_printable_params(
    seed: int | None = None,
    current_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Generate a mechanically valid, non-jamming, bed-fitting random gear pair."""
    actual_seed = int(seed) if seed is not None else random.SystemRandom().randint(1, 99999)
    rng = random.Random(actual_seed)

    base_state = normalize_params(current_params) if isinstance(current_params, dict) else copy.deepcopy(DEFAULT_PARAMS)
    params = copy.deepcopy(DEFAULT_PARAMS)

    if isinstance(current_params, dict):
        for keep_key in ("auto_configure_slicer", "export_target", "sim_rpm", "sim_direction"):
            params[keep_key] = copy.deepcopy(base_state[keep_key])

    archetypes = [
        ("Redutor Reto", "spur", [0.0]),
        ("Transmissão Helicoidal", "helical", [20.0, 25.0, 30.0, 35.0, 45.0]),
        ("Helicoidal 45° Silenciosa", "helical", [45.0]),
        ("Espinha de Peixe", "herringbone", [25.0, 30.0, 35.0, 40.0]),
    ]
    arch_label, gear_type, beta_choices = rng.choice(archetypes)
    beta_deg = rng.choice(beta_choices)
    eff_beta_rad = 0.0 if gear_type == "spur" else math.radians(beta_deg)

    module_mm = rng.choice([1.25, 1.5, 1.75, 2.0, 2.25, 2.5])
    m_t = module_mm / max(0.5, math.cos(eff_beta_rad))

    z1 = rng.randint(11, 22)
    # Constrain Z2 so combined side-by-side footprint stays comfortably within 195 mm (< 220x220 bed)
    max_z2_for_bed = max(z1, int((182.0 - 4.5 * module_mm) / m_t) - z1)
    max_z2 = min(56, max(z1 + 4, max_z2_for_bed))
    z2 = rng.randint(min(z1, max_z2), max_z2)

    face_width = round(rng.uniform(max(8.0, 4.5 * module_mm), min(22.0, 9.5 * module_mm)), 1)
    addendum_coeff = rng.choice([0.80, 0.90, 1.00, 1.00, 1.00, 1.10])
    clearance_coeff = round(rng.uniform(0.22, 0.30), 2)
    root_fillet_coeff = round(rng.uniform(0.25, 0.36), 2)

    params["gear_type"] = gear_type
    params["module_mm"] = module_mm
    params["pressure_angle_deg"] = rng.choice([20.0, 20.0, 20.0, 22.5])
    params["helix_angle_deg"] = beta_deg if gear_type != "spur" else 30.0
    params["helix_hand"] = rng.choice(["right", "left"])
    params["face_width_mm"] = face_width
    params["addendum_coeff"] = addendum_coeff
    params["clearance_coeff"] = clearance_coeff
    params["root_fillet_coeff"] = root_fillet_coeff
    params["tip_chamfer_coeff"] = round(rng.uniform(0.04, 0.09), 2)
    params["auto_profile_shift"] = True
    params["profile_shift_g1"] = 0.0
    params["profile_shift_g2"] = 0.0
    params["backlash_mm"] = round(rng.uniform(0.12, 0.20), 2)
    params["xy_compensation_mm"] = 0.02
    params["elephant_foot_chamfer_mm"] = 0.40
    params["center_distance_offset_mm"] = 0.0

    r_root_1 = 0.5 * m_t * z1 - module_mm * (addendum_coeff + clearance_coeff)
    r_root_2 = 0.5 * m_t * z2 - module_mm * (addendum_coeff + clearance_coeff)

    pinion_bore_mm = 5.0 if r_root_1 >= 6.5 else 4.0
    gear_bore_mm = rng.choice([6.0, 8.0, 10.0]) if r_root_2 >= 12.0 else 5.0

    params["pinion"] = {
        **params["pinion"],
        "teeth": z1,
        "bore_type": rng.choice(["d_shaft", "round", "double_d"]),
        "bore_diameter_mm": pinion_bore_mm,
        "d_flat_depth_mm": 0.50,
        "hub_enabled": rng.choice([False, False, True]) if r_root_1 >= 10.0 else False,
        "hub_diameter_mm": round(min(2.0 * r_root_1 - 3.0, pinion_bore_mm + 8.0), 1),
        "hub_height_mm": 4.5,
        "recess_enabled": False,
        "lightening_mode": "solid",
    }

    gear_lightening = "solid"
    hole_diam = 6.0
    if r_root_2 >= 20.0:
        gear_lightening = rng.choice(["lightening_holes", "web_recess", "solid"])
        ann_span = (r_root_2 - 3.0) - (0.5 * gear_bore_mm + 3.0)
        hole_diam = round(max(4.0, min(12.0, 0.48 * ann_span)), 1)

    params["gear"] = {
        **params["gear"],
        "teeth": z2,
        "bore_type": rng.choice(["round", "hex", "d_shaft", "keyway"]),
        "bore_diameter_mm": gear_bore_mm,
        "d_flat_depth_mm": 0.60,
        "keyway_width_mm": 3.0,
        "keyway_depth_mm": 1.2,
        "hub_enabled": False,
        "recess_enabled": False,
        "lightening_mode": gear_lightening,
        "web_thickness_mm": round(max(3.0, 0.38 * face_width), 1),
        "lightening_hole_count": rng.choice([5, 6, 8]),
        "lightening_hole_diameter_mm": hole_diam,
    }

    params["name"] = f"{arch_label} {z1}:{z2} #{actual_seed % 10000:04d}"
    return normalize_params(params)

# ===========================================================================
# MODULE: gear_studio.exporters
# ===========================================================================

"""Binary STL and OrcaSlicer 2.5.1+ multi-object 3MF project exporters for Orca Gear Studio."""

pass  # [bundled] hoisted __future__ import

import datetime as _dt
import json
import math
import re
import struct
import uuid
import zipfile
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape as _xml_escape

import numpy as np

_STL_RECORD_DTYPE = np.dtype(
    [
        ("normal", "<f4", (3,)),
        ("v0", "<f4", (3,)),
        ("v1", "<f4", (3,)),
        ("v2", "<f4", (3,)),
        ("attr", "<u2"),
    ]
)

_CONTENT_TYPES_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
 <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
 <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>
 <Default Extension="config" ContentType="text/xml"/>
 <Default Extension="png" ContentType="image/png"/>
 <Default Extension="json" ContentType="application/json"/>
</Types>
"""

_RELS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
</Relationships>
"""


def _extract_mesh_arrays(mesh: Any) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Extract validated (vertices, triangles, face_normals) arrays from duck-typed MeshData."""
    vertices = np.asarray(mesh.vertices, dtype=np.float32)
    if vertices.ndim != 2 or vertices.shape[1] != 3:
        raise ValueError(f"Expected vertices shape (V, 3), got {vertices.shape!r}")
    vertices = np.nan_to_num(vertices, nan=0.0, posinf=0.0, neginf=0.0).astype(np.float32, copy=False)

    triangles = np.asarray(mesh.triangles, dtype=np.int32)
    if triangles.size == 0:
        triangles = np.zeros((0, 3), dtype=np.int32)
    elif triangles.ndim != 2 or triangles.shape[1] != 3:
        raise ValueError(f"Expected triangles shape (F, 3), got {triangles.shape!r}")

    num_tris = triangles.shape[0]
    raw_normals = getattr(mesh, "face_normals", None)
    if (
        raw_normals is not None
        and np.asarray(raw_normals).shape == (num_tris, 3)
        and np.all(np.isfinite(raw_normals))
    ):
        normals = np.asarray(raw_normals, dtype=np.float32)
    elif num_tris > 0:
        tris_xyz = vertices[triangles]
        e1 = tris_xyz[:, 1, :] - tris_xyz[:, 0, :]
        e2 = tris_xyz[:, 2, :] - tris_xyz[:, 0, :]
        cross = np.cross(e1, e2)
        lengths = np.linalg.norm(cross, axis=1, keepdims=True)
        safe_lengths = np.where(lengths > 1e-12, lengths, 1.0)
        normals = (cross / safe_lengths).astype(np.float32)
        normals = np.where(lengths > 1e-12, normals, np.array([[0.0, 0.0, 1.0]], dtype=np.float32))
    else:
        normals = np.zeros((0, 3), dtype=np.float32)

    return vertices, triangles, normals


def _mesh_xy_extents(mesh: Any, vertices: np.ndarray | None = None) -> tuple[float, float]:
    """Return (width_x_mm, depth_y_mm) of a mesh from vertices or bounds_mm."""
    verts = vertices if vertices is not None else np.asarray(getattr(mesh, "vertices", []), dtype=np.float32)
    if verts.ndim == 2 and verts.shape[0] > 0 and verts.shape[1] >= 2:
        dx = float(np.max(verts[:, 0]) - np.min(verts[:, 0]))
        dy = float(np.max(verts[:, 1]) - np.min(verts[:, 1]))
        return max(dx, 1.0), max(dy, 1.0)
    bounds = getattr(mesh, "bounds_mm", None)
    if isinstance(bounds, dict):
        size = bounds.get("size")
        if isinstance(size, (list, tuple)) and len(size) >= 2:
            return max(float(size[0]), 1.0), max(float(size[1]), 1.0)
        bmin = bounds.get("min")
        bmax = bounds.get("max")
        if isinstance(bmin, (list, tuple)) and isinstance(bmax, (list, tuple)) and len(bmin) >= 2 and len(bmax) >= 2:
            return max(float(bmax[0]) - float(bmin[0]), 1.0), max(float(bmax[1]) - float(bmin[1]), 1.0)
    return 10.0, 10.0


def _mesh_xy_center_offset(mesh: Any, vertices: np.ndarray | None = None) -> tuple[float, float]:
    """Return the local XY bounding-box midpoint `(mid_x, mid_y)` of `mesh`."""
    verts = vertices if vertices is not None else np.asarray(mesh.vertices, dtype=np.float32)
    if verts.shape[0] == 0:
        return 0.0, 0.0
    mx = 0.5 * float(np.max(verts[:, 0]) + np.min(verts[:, 0]))
    my = 0.5 * float(np.max(verts[:, 1]) + np.min(verts[:, 1]))
    return mx, my


def _resolve_bed_dimensions(host_config: dict[str, Any] | None) -> tuple[float, float]:
    """Extract (bed_x, bed_y) in mm from host_config with 220x220 fallback."""
    bed_x = 220.0
    bed_y = 220.0
    if isinstance(host_config, dict):
        if "bed_x" in host_config:
            try:
                bed_x = max(float(host_config["bed_x"]), 60.0)
            except (TypeError, ValueError):
                pass
        if "bed_y" in host_config:
            try:
                bed_y = max(float(host_config["bed_y"]), 60.0)
            except (TypeError, ValueError):
                pass
        printer = host_config.get("printer")
        if isinstance(printer, dict):
            if "bed_x" in printer and "bed_x" not in host_config:
                try:
                    bed_x = max(float(printer["bed_x"]), 60.0)
                except (TypeError, ValueError):
                    pass
            if "bed_y" in printer and "bed_y" not in host_config:
                try:
                    bed_y = max(float(printer["bed_y"]), 60.0)
                except (TypeError, ValueError):
                    pass
    return bed_x, bed_y


def _resolve_line_width(host_config: dict[str, Any] | None) -> float:
    """Resolve active outer wall line width in mm from host_config (default 0.42 mm)."""
    if isinstance(host_config, dict):
        for direct_key in ("line_width_mm",):
            if direct_key in host_config:
                try:
                    lw = float(host_config[direct_key])
                    if 0.18 <= lw <= 2.5:
                        return lw
                except (TypeError, ValueError):
                    pass
        printer = host_config.get("printer")
        if isinstance(printer, dict) and "line_width_mm" in printer:
            try:
                lw = float(printer["line_width_mm"])
                if 0.18 <= lw <= 2.5:
                    return lw
            except (TypeError, ValueError):
                pass
        ps = host_config.get("project_settings")
        if isinstance(ps, dict):
            raw_lw = ps.get("outer_wall_line_width") or ps.get("line_width")
            if isinstance(raw_lw, (list, tuple)) and raw_lw:
                raw_lw = raw_lw[0]
            if raw_lw is not None:
                s = str(raw_lw).strip()
                if not s.endswith("%"):
                    m = re.search(r"[-+]?\d*\.?\d+", s)
                    if m:
                        try:
                            lw = float(m.group(0))
                            if 0.18 <= lw <= 2.5:
                                return lw
                        except ValueError:
                            pass
    return 0.42


def _positions_overlap(
    positions: list[tuple[float, float, float]],
    extents: list[tuple[float, float]],
    min_clearance_mm: float = 3.0,
) -> bool:
    """Return True if any two axis-aligned bounding boxes overlap on the XY build plate."""
    n = len(positions)
    for i in range(n):
        xi, yi, _ = positions[i]
        wxi, wyi = extents[i]
        for j in range(i + 1, n):
            xj, yj, _ = positions[j]
            wxj, wyj = extents[j]
            overlap_x = abs(xi - xj) < (0.5 * (wxi + wxj) + min_clearance_mm)
            overlap_y = abs(yi - yj) < (0.5 * (wyi + wyj) + min_clearance_mm)
            if overlap_x and overlap_y:
                return True
    return False


def _pack_shelves(
    ordered_indices: list[int],
    extents: list[tuple[float, float]],
    max_row_width: float,
    gap_mm: float,
) -> tuple[list[list[int]], float, float]:
    """Pack `ordered_indices` greedily into horizontal shelves bounded by `max_row_width`."""
    rows: list[list[int]] = []
    cur_row: list[int] = []
    cur_w = 0.0

    for idx in ordered_indices:
        w, _ = extents[idx]
        needed_w = w if not cur_row else (cur_w + gap_mm + w)
        if cur_row and needed_w > max_row_width:
            rows.append(cur_row)
            cur_row = [idx]
            cur_w = w
        else:
            cur_row.append(idx)
            cur_w = needed_w
    if cur_row:
        rows.append(cur_row)

    total_w = 0.0
    total_h = 0.0
    for r_idx, row in enumerate(rows):
        rw = sum(extents[i][0] for i in row) + gap_mm * (len(row) - 1)
        rh = max(extents[i][1] for i in row)
        total_w = max(total_w, rw)
        total_h += rh + (gap_mm if r_idx > 0 else 0.0)

    return rows, total_w, total_h


def _arrange_items_on_bed(
    extents: list[tuple[float, float]],
    z_offsets: list[float],
    bed_x: float,
    bed_y: float,
    gap_mm: float = 8.0,
) -> list[tuple[float, float, float]]:
    """Arrange 1 to 6+ items in a compact 2D multi-row shelf/grid layout centered on `(bed_x/2, bed_y/2)`."""
    cx = bed_x * 0.5
    cy = bed_y * 0.5
    count = len(extents)
    if count == 0:
        return []
    if count == 1:
        return [(cx, cy, z_offsets[0])]

    usable_x = max(bed_x - 8.0, 40.0)
    usable_y = max(bed_y - 8.0, 40.0)

    if count == 2:
        (w0, d0), (w1, d1) = extents
        total_w = w0 + gap_mm + w1
        if total_w <= usable_x:
            left_edge = cx - 0.5 * total_w
            x0 = left_edge + 0.5 * w0
            x1 = left_edge + w0 + gap_mm + 0.5 * w1
            return [(x0, cy, z_offsets[0]), (x1, cy, z_offsets[1])]

        total_h = d0 + gap_mm + d1
        if total_h <= usable_y and max(w0, w1) <= usable_x:
            bot_edge = cy - 0.5 * total_h
            y0 = bot_edge + 0.5 * d0
            y1 = bot_edge + d0 + gap_mm + 0.5 * d1
            return [(cx, y0, z_offsets[0]), (cx, y1, z_offsets[1])]

        # Place along bed diagonal with guaranteed AABB clearance when side-by-side exceeds bed width
        sep_x = 0.5 * (w0 + w1) + gap_mm
        sep_y = 0.5 * (d0 + d1) + gap_mm
        dx = min(sep_x, max(0.5 * sep_x + 1.0, usable_x - 0.5 * (w0 + w1)))
        dy = sep_y if dx < sep_x else 0.0
        return [(cx - 0.5 * dx, cy - 0.5 * dy, z_offsets[0]), (cx + 0.5 * dx, cy + 0.5 * dy, z_offsets[1])]

    # Multi-item 2D shelf bin-packing for 3..N items (e.g. 4-item fit_test_kit or full_suite)
    sum_w = sum(w for w, _ in extents) + gap_mm * (count - 1)
    max_single_w = max(w for w, _ in extents)

    # Evaluate both natural order and height-sorted order across candidate shelf widths
    orderings = [
        list(range(count)),
        sorted(range(count), key=lambda i: (-extents[i][1], -extents[i][0], i)),
    ]
    candidate_widths = sorted(
        {
            max(max_single_w, usable_x),
            max(max_single_w, 0.88 * usable_x),
            max(max_single_w, 0.74 * usable_x),
            max(max_single_w, 0.60 * usable_x),
            max(max_single_w, 0.52 * sum_w),
            max(max_single_w, sum_w + 1.0),
        }
    )

    best_rows: list[list[int]] | None = None
    best_total_h = 0.0
    best_score: tuple[int, float, float] | None = None

    for order in orderings:
        for cap_w in candidate_widths:
            rows, tw, th = _pack_shelves(order, extents, cap_w, gap_mm)
            fits = 0 if (tw <= usable_x and th <= usable_y) else 1
            norm_aspect = max(tw / usable_x, th / usable_y)
            area_box = tw * th
            score = (fits, round(norm_aspect, 4), round(area_box, 2))
            if best_score is None or score < best_score:
                best_score = score
                best_rows = rows
                best_total_h = th

    assert best_rows is not None
    placed: list[tuple[float, float, float]] = [(cx, cy, 0.0)] * count
    y_cursor = cy - 0.5 * best_total_h

    for row in best_rows:
        row_w = sum(extents[i][0] for i in row) + gap_mm * (len(row) - 1)
        row_h = max(extents[i][1] for i in row)
        row_cy = y_cursor + 0.5 * row_h
        x_cursor = cx - 0.5 * row_w
        for orig_idx in row:
            w_i, _ = extents[orig_idx]
            px = x_cursor + 0.5 * w_i
            placed[orig_idx] = (px, row_cy, z_offsets[orig_idx])
            x_cursor += w_i + gap_mm
        y_cursor += row_h + gap_mm

    return placed


def _build_project_settings_dict(params: dict[str, Any] | None, host_config: dict[str, Any] | None) -> dict[str, Any]:
    """Merge host project settings with structural mechanical gear overrides for OrcaSlicer 2.5.1+."""
    merged: dict[str, Any] = {}
    if isinstance(host_config, dict):
        raw_ps = host_config.get("project_settings")
        if isinstance(raw_ps, dict):
            merged.update(raw_ps)

    p = params if isinstance(params, dict) else {}

    # Gears are structural mechanical components: NEVER slice in spiral vase mode!
    merged["spiral_mode"] = "0"
    merged["spiral_mode_smooth"] = "0"

    if bool(p.get("auto_configure_slicer", True)):
        module_mm = max(0.5, float(p.get("module_mm", 2.0)))
        line_width = max(0.20, _resolve_line_width(host_config))
        wall_loops = max(4, min(6, int(round((1.8 * module_mm) / (2.0 * line_width)))))

        merged["wall_loops"] = str(wall_loops)
        merged["top_shell_layers"] = "5"
        merged["bottom_shell_layers"] = "5"
        merged["sparse_infill_density"] = "35%"
        merged["sparse_infill_pattern"] = "gyroid"
        merged["elefant_foot_compensation"] = "0.15"

    return merged


def write_binary_stl(path: str | Path, mesh: Any, header_name: str = "OrcaGearStudio") -> Path:
    """Write a duck-typed MeshData object to a standard little-endian binary STL file.

    Binary layout: 80-byte ASCII header + uint32 triangle count + F * 50-byte facet records.
    """
    out_path = Path(path)
    if not out_path.parent.exists():
        out_path.parent.mkdir(parents=True, exist_ok=True)

    vertices, triangles, normals = _extract_mesh_arrays(mesh)
    num_triangles = int(triangles.shape[0])

    clean_header = str(header_name or "OrcaGearStudio").strip() or "OrcaGearStudio"
    if clean_header.lower().startswith("solid"):
        clean_header = f"Orca_{clean_header}"
    header_text = f"{clean_header} - Orca Gear Studio Binary STL"
    header_bytes = header_text.encode("ascii", errors="replace")[:80].ljust(80, b"\x00")

    records = np.zeros(num_triangles, dtype=_STL_RECORD_DTYPE)
    if num_triangles > 0:
        tris_xyz = vertices[triangles]
        records["normal"] = normals.astype("<f4", copy=False)
        records["v0"] = tris_xyz[:, 0, :].astype("<f4", copy=False)
        records["v1"] = tris_xyz[:, 1, :].astype("<f4", copy=False)
        records["v2"] = tris_xyz[:, 2, :].astype("<f4", copy=False)
        records["attr"] = 0

    with open(out_path, "wb") as fh:
        fh.write(header_bytes)
        fh.write(struct.pack("<I", num_triangles))
        if num_triangles > 0:
            fh.write(records.tobytes())

    return out_path


def write_orca_3mf(
    path: str | Path,
    items: list[tuple[str, Any] | tuple[str, Any, tuple[float, float, float] | None]],
    params: dict[str, Any],
    host_config: dict[str, Any] | None = None,
) -> Path:
    """Write an OrcaSlicer 2.5.1+ compatible .3mf project archive with multi-object layout & slicer settings."""
    if not items:
        raise ValueError("write_orca_3mf requires at least one item in 'items'.")

    out_path = Path(path)
    if not out_path.parent.exists():
        out_path.parent.mkdir(parents=True, exist_ok=True)

    bed_x, bed_y = _resolve_bed_dimensions(host_config)
    cx, cy = bed_x * 0.5, bed_y * 0.5

    parsed_items: list[tuple[str, np.ndarray, np.ndarray, tuple[float, float], tuple[float, float]]] = []
    raw_positions: list[tuple[float, float, float] | None] = []
    z_offsets: list[float] = []

    for idx, entry in enumerate(items):
        if len(entry) == 2:
            raw_name, mesh = entry  # type: ignore[misc]
            raw_pos = None
        elif len(entry) >= 3:
            raw_name, mesh, raw_pos = entry[0], entry[1], entry[2]
        else:
            raise ValueError(f"Invalid item tuple at index {idx}: {entry!r}")

        item_name = str(raw_name or f"Gear_{idx + 1}").strip() or f"Gear_{idx + 1}"
        vertices, triangles, _ = _extract_mesh_arrays(mesh)
        ext = _mesh_xy_extents(mesh, vertices)
        local_mid = _mesh_xy_center_offset(mesh, vertices)
        parsed_items.append((item_name, vertices, triangles, ext, local_mid))

        if raw_pos is None:
            raw_positions.append(None)
            z_offsets.append(0.0)
        else:
            px, py, pz = float(raw_pos[0]), float(raw_pos[1]), float(raw_pos[2])
            raw_positions.append((px, py, pz))
            z_offsets.append(pz)

    extents_list = [it[3] for it in parsed_items]
    if any(pos is None for pos in raw_positions):
        if len(parsed_items) == 1:
            box_centers = [(cx, cy, z_offsets[0])]
        else:
            box_centers = _arrange_items_on_bed(extents_list, z_offsets, bed_x, bed_y, gap_mm=8.0)
        # Subtract local mesh midpoint so even asymmetric sector/gauge meshes land centered on their box!
        final_positions = [
            (bx - parsed_items[i][4][0], by - parsed_items[i][4][1], bz)
            for i, (bx, by, bz) in enumerate(box_centers)
        ]
    else:
        concrete_centers = [
            (pos[0] + parsed_items[i][4][0], pos[1] + parsed_items[i][4][1], pos[2])
            for i, pos in enumerate(raw_positions)
            if pos is not None
        ]
        if len(concrete_centers) >= 2 and _positions_overlap(concrete_centers, extents_list, min_clearance_mm=3.0):
            box_centers = _arrange_items_on_bed(extents_list, z_offsets, bed_x, bed_y, gap_mm=8.0)
            final_positions = [
                (bx - parsed_items[i][4][0], by - parsed_items[i][4][1], bz)
                for i, (bx, by, bz) in enumerate(box_centers)
            ]
        else:
            final_positions = [pos for pos in raw_positions if pos is not None]

    title = str((params or {}).get("name") or parsed_items[0][0] or "Orca Gear Studio").strip()
    escaped_title = _xml_escape(title, {'"': "&quot;"})
    today_iso = _dt.date.today().isoformat()
    ns_seed = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
    build_uuid = str(uuid.uuid5(ns_seed, f"orca-gear-build-{title}"))

    object_blocks: list[str] = []
    build_items_xml: list[str] = []
    model_settings_objects: list[str] = []
    model_settings_instances: list[str] = []
    model_settings_assemble: list[str] = []

    for idx, (item_name, vertices, triangles, _, _) in enumerate(parsed_items):
        obj_id = idx + 1
        tx, ty, tz = final_positions[idx]
        esc_name = _xml_escape(item_name, {'"': "&quot;"})
        obj_uuid = str(uuid.uuid5(ns_seed, f"orca-gear-obj-{obj_id}-{item_name}"))
        item_uuid = str(uuid.uuid5(ns_seed, f"orca-gear-item-{obj_id}-{item_name}"))

        verts_py = vertices.tolist()
        tris_py = triangles.tolist()

        vertex_lines = "\n".join(
            f'     <vertex x="{vx:.5f}" y="{vy:.5f}" z="{vz:.5f}"/>'
            for vx, vy, vz in verts_py
        )
        triangle_lines = "\n".join(
            f'     <triangle v1="{v1}" v2="{v2}" v3="{v3}"/>'
            for v1, v2, v3 in tris_py
        )

        object_blocks.append(
            f'  <object id="{obj_id}" p:UUID="{obj_uuid}" name="{esc_name}" type="model">\n'
            f"   <mesh>\n"
            f"    <vertices>\n"
            f"{vertex_lines}\n"
            f"    </vertices>\n"
            f"    <triangles>\n"
            f"{triangle_lines}\n"
            f"    </triangles>\n"
            f"   </mesh>\n"
            f"  </object>"
        )

        transform_3x4 = f"1 0 0 0 1 0 0 0 1 {tx:.4f} {ty:.4f} {tz:.4f}"
        build_items_xml.append(
            f'  <item objectid="{obj_id}" p:UUID="{item_uuid}" transform="{transform_3x4}" printable="1"/>'
        )

        model_settings_objects.append(
            f'  <object id="{obj_id}">\n'
            f'    <metadata key="name" value="{esc_name}"/>\n'
            f'    <metadata key="extruder" value="1"/>\n'
            f'    <part id="1" subtype="normal_part">\n'
            f'      <metadata key="name" value="{esc_name}"/>\n'
            f'      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>\n'
            f'      <mesh_stat edges_fixed="0" degenerate_facets="0" facets_removed="0" facets_reversed="0" backwards_edges="0"/>\n'
            f"    </part>\n"
            f"  </object>"
        )
        model_settings_instances.append(
            f"    <model_instance>\n"
            f'      <metadata key="object_id" value="{obj_id}"/>\n'
            f'      <metadata key="instance_id" value="0"/>\n'
            f'      <metadata key="identify_id" value="{100 + obj_id}"/>\n'
            f"    </model_instance>"
        )
        model_settings_assemble.append(
            f'    <assemble_item object_id="{obj_id}" instance_id="0" transform="{transform_3x4}" offset="0 0 0"/>'
        )

    model_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<model unit="millimeter" xml:lang="en-US" '
        'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
        'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" '
        'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" '
        'requiredextensions="p">\n'
        ' <metadata name="Application">OrcaSlicer-2.5.1</metadata>\n'
        ' <metadata name="OrcaSlicer">2.5.1</metadata>\n'
        ' <metadata name="BambuStudio:3mfVersion">1</metadata>\n'
        f' <metadata name="Title">{escaped_title}</metadata>\n'
        f' <metadata name="CreationDate">{today_iso}</metadata>\n'
        " <resources>\n"
        + "\n".join(object_blocks)
        + "\n </resources>\n"
        + f' <build p:UUID="{build_uuid}">\n'
        + "\n".join(build_items_xml)
        + "\n </build>\n"
        "</model>\n"
    )

    model_settings_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<config>\n"
        + "\n".join(model_settings_objects)
        + "\n  <plate>\n"
        '    <metadata key="plater_id" value="1"/>\n'
        '    <metadata key="plater_name" value=""/>\n'
        '    <metadata key="locked" value="false"/>\n'
        + "\n".join(model_settings_instances)
        + "\n  </plate>\n"
        "  <assemble>\n"
        + "\n".join(model_settings_assemble)
        + "\n  </assemble>\n"
        "</config>\n"
    )

    project_settings = _build_project_settings_dict(params, host_config)
    project_settings_json = json.dumps(project_settings, indent=2, ensure_ascii=False)

    with zipfile.ZipFile(out_path, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        zf.writestr("[Content_Types].xml", _CONTENT_TYPES_XML)
        zf.writestr("_rels/.rels", _RELS_XML)
        zf.writestr("3D/3dmodel.model", model_xml)
        zf.writestr("Metadata/model_settings.config", model_settings_xml)
        zf.writestr("Metadata/project_settings.config", project_settings_json)

    return out_path

# ===========================================================================
# MODULE: gear_studio.studio_ui
# ===========================================================================

"""Self-contained offline HTML5 + CSS3 + WebGL2 + 2D Tooth-Mesh Loupe Studio UI for Orca Gear Studio.

Generates the interactive 3D & 2D parametric mechanical gear design studio for both:
- `mode="page"`: Wide 3-column engineering studio tab inside OrcaSlicer (`PagesPluginCapabilityBase`)
- `mode="dock"`: Compact tabbed side-docked panel beside OrcaSlicer's 3D Plater (`UiDockPanel`)

Zero external CDN scripts, stylesheets, or web fonts are referenced so WebView2 runs 100% offline
without network permission prompts.
"""

pass  # [bundled] hoisted __future__ import

import copy
import json
from typing import Any

if "DEFAULT_PARAMS" not in globals():
    try:
        pass  # [bundled] resolved intra-package import
    except Exception:
        DEFAULT_PARAMS = None  # type: ignore[assignment]

if "BUILTIN_PRESETS" not in globals():
    try:
        pass  # [bundled] resolved intra-package import
    except Exception:
        BUILTIN_PRESETS = None  # type: ignore[assignment]

__all__ = ["get_studio_html"]


def _studio_ui_safe_json(payload: dict[str, Any]) -> str:
    """Serialize payload into script-safe JSON (escaping `</` and Unicode line separators)."""
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return (
        raw.replace("</", "<\\/")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


_STUDIO_UI_HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="__INITIAL_LANG__" data-theme="__INITIAL_THEME__">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Orca Gear Studio</title>
<style>
:root,
[data-theme="dark"] {
  --bg-app: #15171b;
  --bg-panel: #1d2026;
  --bg-card: #242830;
  --bg-card-hover: #2b303a;
  --bg-input: #16181d;
  --bg-viewport-top: #222731;
  --bg-viewport-bot: #111318;
  --bg-hud: rgba(23, 26, 33, 0.88);
  --border-subtle: #313641;
  --border-strong: #434b5a;
  --text-main: #eef2f7;
  --text-muted: #9aa4b4;
  --text-dim: #6d7788;
  --orca-accent: #00a896;
  --orca-accent-hover: #00bfa5;
  --orca-accent-soft: rgba(0, 191, 165, 0.15);
  --orca-accent-border: rgba(0, 191, 165, 0.48);
  --gear2-accent: #4f9cf9;
  --gear2-soft: rgba(79, 156, 249, 0.15);
  --status-ok: #00c853;
  --status-warn: #ffb300;
  --status-crit: #ff5252;
  --shadow-soft: 0 8px 24px rgba(0, 0, 0, 0.36);
  --radius-sm: 6px;
  --radius-md: 9px;
  --radius-lg: 12px;
  --font-sans: var(--orca-font, "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, Ubuntu, sans-serif);
  --font-mono: "Cascadia Code", Consolas, "SFMono-Regular", monospace;
}

[data-theme="light"] {
  --bg-app: #edf1f6;
  --bg-panel: #ffffff;
  --bg-card: #f5f7fb;
  --bg-card-hover: #eaeff6;
  --bg-input: #ffffff;
  --bg-viewport-top: #dce3ec;
  --bg-viewport-bot: #c6d0dc;
  --bg-hud: rgba(255, 255, 255, 0.91);
  --border-subtle: #d4dce5;
  --border-strong: #b6c2cf;
  --text-main: #1b222c;
  --text-muted: #525e6f;
  --text-dim: #798596;
  --orca-accent: #00897b;
  --orca-accent-hover: #00796b;
  --orca-accent-soft: rgba(0, 137, 123, 0.12);
  --orca-accent-border: rgba(0, 137, 123, 0.45);
  --gear2-accent: #2563eb;
  --gear2-soft: rgba(37, 99, 235, 0.12);
  --status-ok: #169c46;
  --status-warn: #d47f00;
  --status-crit: #d93025;
  --shadow-soft: 0 8px 24px rgba(15, 25, 40, 0.10);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: var(--bg-app);
  color: var(--text-main);
  font-family: var(--font-sans);
  font-size: 12.2px;
  line-height: 1.38;
  user-select: none;
  -webkit-font-smoothing: antialiased;
}

::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: var(--border-strong);
  border-radius: 99px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--orca-accent);
}

button, input, select {
  font-family: inherit;
  font-size: inherit;
  color: inherit;
}

.studio-shell {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}

/* Header Bar */
.studio-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 6px 12px;
  background: var(--bg-panel);
  border-bottom: 1px solid var(--border-subtle);
  flex-shrink: 0;
  z-index: 20;
}

.brand-group {
  display: flex;
  align-items: center;
  gap: 9px;
  min-width: 0;
}

.brand-logo {
  width: 26px;
  height: 26px;
  border-radius: 7px;
  background: linear-gradient(135deg, #00bfa5 0%, #00796b 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 191, 165, 0.30);
}

.brand-name-row {
  display: flex;
  align-items: center;
  gap: 7px;
}

.brand-title {
  font-weight: 700;
  font-size: 13.5px;
  letter-spacing: 0.2px;
  white-space: nowrap;
}

.gear-name-input {
  background: var(--bg-input);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 3px 8px;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-main);
  width: 175px;
  transition: border-color 0.15s;
}
.gear-name-input:focus {
  outline: none;
  border-color: var(--orca-accent);
}

.printer-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 9px;
  border-radius: 99px;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  color: var(--text-muted);
  font-size: 11px;
  white-space: nowrap;
  max-width: 340px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.printer-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--orca-accent-hover);
  flex-shrink: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 5px;
  flex-shrink: 0;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 5px 9px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background: var(--bg-card);
  color: var(--text-main);
  font-weight: 600;
  font-size: 11.2px;
  cursor: pointer;
  transition: background 0.14s, border-color 0.14s, transform 0.08s;
  white-space: nowrap;
}
.btn:hover:not(:disabled) {
  background: var(--bg-card-hover);
  border-color: var(--border-strong);
}
.btn:active:not(:disabled) {
  transform: translateY(1px);
}
.btn:disabled {
  opacity: 0.42;
  cursor: not-allowed;
}

.btn-icon {
  padding: 5px 7px;
}

.btn-accent {
  background: linear-gradient(135deg, var(--orca-accent) 0%, #00897b 100%);
  border-color: transparent;
  color: #ffffff;
}
.btn-accent:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--orca-accent-hover) 0%, var(--orca-accent) 100%);
  border-color: transparent;
}

.btn-soft {
  background: var(--orca-accent-soft);
  border-color: var(--orca-accent-border);
  color: var(--orca-accent-hover);
}
[data-theme="light"] .btn-soft {
  color: var(--orca-accent);
}
.btn-soft:hover:not(:disabled) {
  background: var(--orca-accent);
  color: #ffffff;
}

/* Main Workspace Grid */
.studio-workspace {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: 344px minmax(380px, 1fr) 356px;
  overflow: hidden;
}

.col-panel {
  display: flex;
  flex-direction: column;
  min-height: 0;
  background: var(--bg-panel);
  overflow: hidden;
}
.col-left {
  border-right: 1px solid var(--border-subtle);
}
.col-right {
  border-left: 1px solid var(--border-subtle);
}

.col-scroll {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 9px;
  display: flex;
  flex-direction: column;
  gap: 9px;
}

/* Dock Mode Navigation Tabs */
.dock-tabs {
  display: none;
  background: var(--bg-panel);
  border-bottom: 1px solid var(--border-subtle);
  padding: 4px 6px;
  gap: 4px;
  flex-shrink: 0;
}

.dock-tab-btn {
  flex: 1;
  padding: 5px 4px;
  border-radius: var(--radius-sm);
  border: 1px solid transparent;
  background: transparent;
  color: var(--text-muted);
  font-size: 10.8px;
  font-weight: 600;
  cursor: pointer;
  text-align: center;
  transition: all 0.14s;
}
.dock-tab-btn:hover {
  color: var(--text-main);
  background: var(--bg-card);
}
.dock-tab-btn.active {
  background: var(--orca-accent-soft);
  border-color: var(--orca-accent-border);
  color: var(--orca-accent-hover);
}
[data-theme="light"] .dock-tab-btn.active {
  color: var(--orca-accent);
}

/* Cards & Sections */
.studio-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 9px 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
}

.card-title {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-main);
  display: flex;
  align-items: center;
  gap: 5px;
}

.card-badge {
  font-size: 10px;
  font-weight: 700;
  font-family: var(--font-mono);
  padding: 2px 7px;
  border-radius: 99px;
  background: var(--orca-accent-soft);
  color: var(--orca-accent-hover);
  white-space: nowrap;
}
[data-theme="light"] .card-badge {
  color: var(--orca-accent);
}

/* Quick Pills Row */
.pill-row {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.quick-pill {
  flex: 1;
  min-width: 0;
  padding: 3px 6px;
  font-size: 10.5px;
  font-weight: 600;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background: var(--bg-input);
  color: var(--text-muted);
  cursor: pointer;
  text-align: center;
  transition: all 0.12s;
  white-space: nowrap;
}
.quick-pill:hover {
  border-color: var(--border-strong);
  color: var(--text-main);
}
.quick-pill.active {
  background: var(--orca-accent);
  border-color: var(--orca-accent);
  color: #ffffff;
}

/* Presets Grid */
.preset-filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.filter-chip {
  padding: 2px 7px;
  font-size: 10.2px;
  font-weight: 600;
  border-radius: 99px;
  border: 1px solid var(--border-subtle);
  background: var(--bg-input);
  color: var(--text-muted);
  cursor: pointer;
}
.filter-chip.active {
  background: var(--orca-accent);
  border-color: var(--orca-accent);
  color: #ffffff;
}

.presets-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 5px;
  max-height: 178px;
  overflow-y: auto;
  padding-right: 2px;
}

.preset-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 6px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background: var(--bg-panel);
  cursor: pointer;
  transition: border-color 0.14s, background 0.14s;
  text-align: left;
}
.preset-card:hover {
  background: var(--bg-card-hover);
  border-color: var(--border-strong);
}
.preset-card.active {
  border-color: var(--orca-accent-hover);
  background: var(--orca-accent-soft);
}

.preset-thumb {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preset-meta {
  min-width: 0;
  flex: 1;
}

.preset-name {
  font-size: 10.8px;
  font-weight: 600;
  color: var(--text-main);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.preset-sub {
  font-size: 9.6px;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.preset-del-btn {
  position: absolute;
  top: 2px;
  right: 2px;
  width: 16px;
  height: 16px;
  border-radius: 4px;
  border: none;
  background: rgba(255, 82, 82, 0.16);
  color: var(--status-crit);
  font-size: 11px;
  line-height: 1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.preset-del-btn:hover {
  background: var(--status-crit);
  color: #ffffff;
}

.save-preset-bar {
  display: none;
  gap: 5px;
  align-items: center;
  padding-top: 4px;
  border-top: 1px dashed var(--border-subtle);
}
.save-preset-bar.open {
  display: flex;
}
.save-preset-input {
  flex: 1;
  min-width: 0;
  background: var(--bg-input);
  border: 1px solid var(--orca-accent-border);
  border-radius: var(--radius-sm);
  padding: 4px 7px;
  font-size: 11.2px;
}

/* Segmented Mode Switch */
.seg-group {
  display: flex;
  background: var(--bg-input);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 2px;
  gap: 2px;
}

.seg-btn {
  flex: 1;
  padding: 5px 5px;
  border: none;
  border-radius: 4px;
  background: transparent;
  color: var(--text-muted);
  font-size: 10.8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.14s;
  white-space: nowrap;
}
.seg-btn.active {
  background: var(--orca-accent);
  color: #ffffff;
}
.seg-btn.active-g2 {
  background: var(--gear2-accent);
  color: #ffffff;
}

/* Slider Controls & Dual Badges */
.ctrl-row {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.ctrl-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
}

.ctrl-label {
  font-size: 11.1px;
  color: var(--text-muted);
  font-weight: 500;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ctrl-val-wrap {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
}

.dual-mm-badge {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  padding: 1px 5px;
  border-radius: 4px;
  background: var(--orca-accent-soft);
  color: var(--orca-accent-hover);
  border: 1px solid var(--orca-accent-border);
  white-space: nowrap;
}
[data-theme="light"] .dual-mm-badge {
  color: var(--orca-accent);
}

.ctrl-num {
  width: 56px;
  background: var(--bg-input);
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
  padding: 2px 5px;
  text-align: right;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-main);
}
.ctrl-num:focus {
  outline: none;
  border-color: var(--orca-accent);
}

.ctrl-unit {
  font-size: 10px;
  color: var(--text-dim);
  min-width: 16px;
}

.studio-select {
  width: 100%;
  background: var(--bg-input);
  color: var(--text-main);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 5px 8px;
  font-size: 11.3px;
  font-weight: 600;
  cursor: pointer;
}
.studio-select:focus {
  outline: none;
  border-color: var(--orca-accent);
}

input[type="range"].orca-slider {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 5px;
  border-radius: 99px;
  background: var(--border-strong);
  outline: none;
  cursor: pointer;
}
input[type="range"].orca-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 13px;
  height: 13px;
  border-radius: 50%;
  background: var(--orca-accent-hover);
  border: 2px solid #ffffff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.4);
  cursor: grab;
  transition: transform 0.1s;
}
input[type="range"].orca-slider::-webkit-slider-thumb:hover {
  transform: scale(1.15);
}

/* Toggle Switch */
.switch-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 34px;
  height: 18px;
  flex-shrink: 0;
}
.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}
.toggle-track {
  position: absolute;
  inset: 0;
  background: var(--border-strong);
  border-radius: 99px;
  cursor: pointer;
  transition: background 0.18s;
}
.toggle-track::before {
  content: "";
  position: absolute;
  width: 14px;
  height: 14px;
  left: 2px;
  top: 2px;
  border-radius: 50%;
  background: #ffffff;
  transition: transform 0.18s;
}
.toggle-switch input:checked + .toggle-track {
  background: var(--orca-accent);
}
.toggle-switch input:checked + .toggle-track::before {
  transform: translateX(16px);
}

.sub-feature-box {
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 7px 8px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

/* Center Column: 3D Stage + Sim Transport Bar + 2D Tooth-Mesh Loupe */
.viewport-col {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
  background: var(--bg-app);
  overflow: hidden;
}

.vp-stage-3d {
  position: relative;
  flex: 1;
  min-height: 180px;
  background: radial-gradient(circle at 50% 35%, var(--bg-viewport-top) 0%, var(--bg-viewport-bot) 100%);
  overflow: hidden;
}

#gl-canvas {
  width: 100%;
  height: 100%;
  display: block;
  touch-action: none;
  cursor: grab;
}
#gl-canvas:active {
  cursor: grabbing;
}

.vp-toolbar-left {
  position: absolute;
  top: 9px;
  left: 9px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px;
  max-width: calc(100% - 225px);
  z-index: 10;
}

.vp-glass {
  background: var(--bg-hud);
  backdrop-filter: blur(8px);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-soft);
}

.vp-chip {
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background: var(--bg-hud);
  color: var(--text-muted);
  font-size: 10.8px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
.vp-chip:hover {
  color: var(--text-main);
  border-color: var(--border-strong);
}
.vp-chip.active {
  background: var(--orca-accent);
  border-color: var(--orca-accent);
  color: #ffffff;
}

.vp-cam-bar {
  position: absolute;
  bottom: 9px;
  left: 9px;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  z-index: 10;
}

.vp-cut-bar {
  position: absolute;
  bottom: 9px;
  right: 9px;
  width: 248px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 9px;
  z-index: 10;
}

.vp-cut-label {
  font-size: 10.5px;
  font-weight: 600;
  white-space: nowrap;
  color: var(--text-muted);
}

/* 3D Force Vectors & Status HUD */
.vp-hud-right {
  position: absolute;
  top: 9px;
  right: 9px;
  width: 210px;
  padding: 8px 10px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  z-index: 10;
}

.hud-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-muted);
}

.hud-status-pill {
  padding: 1px 7px;
  border-radius: 99px;
  font-size: 9.8px;
  font-weight: 700;
}
.hud-status-pill.ok {
  background: rgba(0, 200, 83, 0.18);
  color: var(--status-ok);
}
.hud-status-pill.warn {
  background: rgba(255, 179, 0, 0.20);
  color: var(--status-warn);
}
.hud-status-pill.crit {
  background: rgba(255, 82, 82, 0.22);
  color: var(--status-crit);
}

.hud-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px 7px;
}

.hud-metric {
  display: flex;
  flex-direction: column;
}
.hud-metric-k {
  font-size: 9.5px;
  color: var(--text-dim);
}
.hud-metric-v {
  font-family: var(--font-mono);
  font-size: 10.8px;
  font-weight: 600;
  color: var(--text-main);
}

.thrust-banner {
  font-size: 10px;
  font-weight: 600;
  padding: 3px 6px;
  border-radius: 4px;
  background: rgba(0, 191, 165, 0.12);
  border-left: 2px solid var(--orca-accent);
  color: var(--text-main);
}
.thrust-banner.axial-active {
  background: rgba(255, 179, 0, 0.14);
  border-left-color: #f59e0b;
}

.heatmap-legend {
  display: none;
  align-items: center;
  gap: 6px;
  font-size: 9.8px;
  padding-top: 4px;
  border-top: 1px solid var(--border-subtle);
  color: var(--text-muted);
}
.heatmap-legend.visible {
  display: flex;
}
.legend-swatch {
  width: 8px;
  height: 8px;
  border-radius: 2px;
  display: inline-block;
}

/* Micro-Simulation Transport & Live Delta_a Bar */
.sim-transport-bar {
  background: var(--bg-panel);
  border-top: 1px solid var(--border-subtle);
  border-bottom: 1px solid var(--border-subtle);
  padding: 6px 10px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  flex-shrink: 0;
}

.sim-row {
  display: flex;
  align-items: center;
  gap: 7px;
  flex-wrap: wrap;
}

.sim-group {
  display: flex;
  align-items: center;
  gap: 4px;
}

.sim-flex-slider {
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
  min-width: 135px;
}

.sim-tag {
  font-size: 10.3px;
  font-weight: 700;
  color: var(--text-muted);
  white-space: nowrap;
}

.sim-mono {
  font-family: var(--font-mono);
  font-size: 10.8px;
  font-weight: 700;
  color: var(--orca-accent-hover);
  min-width: 52px;
  text-align: right;
  white-space: nowrap;
}
[data-theme="light"] .sim-mono {
  color: var(--orca-accent);
}

.step-btn {
  padding: 2px 5px;
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  border-radius: 4px;
  border: 1px solid var(--border-subtle);
  background: var(--bg-card);
  color: var(--text-main);
  cursor: pointer;
}
.step-btn:hover {
  background: var(--bg-card-hover);
  border-color: var(--orca-accent);
}

/* Synchronized 2D Tooth-Mesh Loupe Panel */
.loupe-panel {
  height: 196px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  background: var(--bg-input);
  position: relative;
  overflow: hidden;
}
.loupe-panel.collapsed {
  height: 28px;
}

.loupe-header {
  height: 28px;
  padding: 0 10px;
  background: var(--bg-card);
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  flex-shrink: 0;
}

.loupe-title {
  font-size: 10.8px;
  font-weight: 700;
  color: var(--text-main);
  display: flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
}

.jam-alert-badge {
  display: none;
  align-items: center;
  gap: 5px;
  padding: 2px 8px;
  border-radius: 99px;
  background: rgba(255, 42, 42, 0.22);
  border: 1px solid var(--status-crit);
  color: #ff6b6b;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.3px;
  animation: jamPulse 0.9s infinite alternate;
}
[data-theme="light"] .jam-alert-badge {
  color: #c62828;
  background: rgba(217, 48, 37, 0.15);
}
.jam-alert-badge.visible {
  display: inline-flex;
}

@keyframes jamPulse {
  from { transform: scale(1.0); box-shadow: 0 0 0 rgba(255, 82, 82, 0); }
  to   { transform: scale(1.02); box-shadow: 0 0 10px rgba(255, 82, 82, 0.45); }
}

.loupe-canvas-wrap {
  position: relative;
  flex: 1;
  min-height: 0;
}

#loupe-canvas {
  width: 100%;
  height: 100%;
  display: block;
}

/* Diagnostics Grid in Right Column */
.diag-section-title {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.45px;
  color: var(--orca-accent-hover);
  padding-top: 4px;
  border-top: 1px solid var(--border-subtle);
}
[data-theme="light"] .diag-section-title {
  color: var(--orca-accent);
}

.diag-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 5px 8px;
}

.diag-cell {
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: 5px;
  padding: 4px 7px;
  display: flex;
  flex-direction: column;
}

.diag-k {
  font-size: 9.6px;
  color: var(--text-dim);
}
.diag-v {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 700;
  color: var(--text-main);
}

.issues-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-height: 120px;
  overflow-y: auto;
}

.issue-item {
  font-size: 10.3px;
  padding: 4px 7px;
  border-radius: 4px;
  background: rgba(0, 200, 83, 0.10);
  border-left: 2.5px solid var(--status-ok);
  color: var(--text-main);
}
.issue-item.warn {
  background: rgba(255, 179, 0, 0.13);
  border-left-color: var(--status-warn);
}
.issue-item.critical {
  background: rgba(255, 82, 82, 0.16);
  border-left-color: var(--status-crit);
}

.helper-note {
  font-size: 10.3px;
  color: var(--text-muted);
  background: var(--bg-input);
  border-left: 2px solid var(--orca-accent);
  padding: 5px 7px;
  border-radius: 0 4px 4px 0;
}

/* Sticky Action Footer */
.action-footer {
  padding: 9px 10px;
  background: var(--bg-panel);
  border-top: 1px solid var(--border-subtle);
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex-shrink: 0;
}

.btn-hero {
  width: 100%;
  padding: 10px 14px;
  font-size: 12.8px;
  font-weight: 700;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, #00bfa5 0%, #00897b 100%);
  color: #ffffff;
  border: none;
  box-shadow: 0 4px 14px rgba(0, 191, 165, 0.32);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: filter 0.15s, transform 0.08s;
}
.btn-hero:hover:not(:disabled) {
  filter: brightness(1.07);
}
.btn-hero:active:not(:disabled) {
  transform: translateY(1px);
}
.btn-hero:disabled {
  opacity: 0.55;
  cursor: wait;
}

.export-btn-row {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: 6px;
}

/* Toast Notification */
.toast-banner {
  position: fixed;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%) translateY(20px);
  opacity: 0;
  pointer-events: none;
  padding: 8px 16px;
  border-radius: var(--radius-md);
  background: var(--bg-card);
  border: 1px solid var(--orca-accent);
  color: var(--text-main);
  font-size: 12px;
  font-weight: 600;
  box-shadow: var(--shadow-soft);
  transition: opacity 0.2s, transform 0.2s;
  z-index: 999;
  max-width: 90vw;
}
.toast-banner.visible {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}
.toast-banner.error {
  border-color: var(--status-crit);
}

.dock-global-footer {
  display: none;
}

/* ============================================================================
   COMPACT SIDE-DOCK MODE (`data-mode="dock"`)
   ============================================================================ */
body[data-mode="dock"] .printer-pill,
body[data-mode="dock"] .brand-title {
  display: none;
}

body[data-mode="dock"] .gear-name-input {
  width: 118px;
}

body[data-mode="dock"] .studio-workspace {
  display: flex;
  flex-direction: column;
}

body[data-mode="dock"] .viewport-col {
  order: -1;
  height: 318px;
  flex-shrink: 0;
  border-bottom: 1px solid var(--border-subtle);
}

body[data-mode="dock"] .vp-stage-3d {
  min-height: 130px;
}

body[data-mode="dock"] .loupe-panel {
  height: 112px;
}
body[data-mode="dock"] .loupe-panel.collapsed {
  height: 26px;
}

body[data-mode="dock"] .vp-hud-right,
body[data-mode="dock"] .vp-cam-bar,
body[data-mode="dock"] .vp-cut-bar {
  display: none;
}

body[data-mode="dock"] .dock-tabs {
  display: flex;
  order: 0;
}

body[data-mode="dock"] .col-left,
body[data-mode="dock"] .col-right {
  border: none;
  flex: 1;
  min-height: 0;
}

body[data-mode="dock"] .col-right .action-footer {
  display: none;
}
body[data-mode="dock"] .dock-global-footer {
  display: flex;
}

body[data-mode="dock"][data-dock-tab="gears"] .col-right,
body[data-mode="dock"][data-dock-tab="gears"] #card-presets,
body[data-mode="dock"][data-dock-tab="gears"] #card-bodies {
  display: none;
}

body[data-mode="dock"][data-dock-tab="bodies"] .col-right,
body[data-mode="dock"][data-dock-tab="bodies"] #card-presets,
body[data-mode="dock"][data-dock-tab="bodies"] #card-transmission,
body[data-mode="dock"][data-dock-tab="bodies"] #card-tooth-profile {
  display: none;
}

body[data-mode="dock"][data-dock-tab="export"] .col-left {
  display: none;
}

body[data-mode="dock"][data-dock-tab="presets"] .col-right,
body[data-mode="dock"][data-dock-tab="presets"] #card-transmission,
body[data-mode="dock"][data-dock-tab="presets"] #card-tooth-profile,
body[data-mode="dock"][data-dock-tab="presets"] #card-bodies {
  display: none;
}
body[data-mode="dock"][data-dock-tab="presets"] .presets-grid {
  max-height: none;
}

@media (max-width: 1020px) {
  .printer-pill {
    display: none;
  }
  .studio-workspace {
    grid-template-columns: 300px minmax(280px, 1fr) 310px;
  }
}
</style>
</head>
<body data-mode="__INITIAL_MODE__" data-dock-tab="gears">
<div class="studio-shell">
  <!-- TOP HEADER -->
  <header class="studio-header">
    <div class="brand-group">
      <div class="brand-logo" title="Orca Gear Studio">
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="9.5" cy="9.5" r="3.2"/>
          <path d="M9.5 3.5v1.6M9.5 13.9v1.6M3.5 9.5h1.6M13.9 9.5h1.6M5.3 5.3l1.1 1.1M12.6 12.6l1.1 1.1M13.7 5.3l-1.1 1.1M6.4 12.6l-1.1 1.1"/>
          <circle cx="17" cy="16.5" r="2.3"/>
          <path d="M17 12.2v1.1M17 19.7v1.1M12.7 16.5h1.1M20.2 16.5h1.1"/>
        </svg>
      </div>
      <div class="brand-name-row">
        <span class="brand-title">Orca Gear Studio</span>
        <input id="inp-gear-name" class="gear-name-input" type="text" maxlength="80" value="Par Engrenagens" aria-label="Gear Pair Name" />
      </div>
      <div id="printer-pill" class="printer-pill" title="Active OrcaSlicer Printer Profile">
        <span class="printer-dot"></span>
        <span id="printer-pill-text">Generic FDM · 220×220×250 mm · 0.4mm</span>
      </div>
    </div>

    <div class="header-actions">
      <button id="btn-undo" class="btn btn-icon" title="Undo (Ctrl+Z)" disabled>↶</button>
      <button id="btn-redo" class="btn btn-icon" title="Redo (Ctrl+Y)" disabled>↷</button>
      <button id="btn-randomize" class="btn btn-soft">
        <span>🎲</span>
        <span data-i18n="btn_random">Aleatório</span>
      </button>
      <button id="btn-reset" class="btn btn-icon" title="Reset">↺</button>
      <button id="btn-lang" class="btn btn-icon" title="Português / English">PT</button>
      <button id="btn-theme" class="btn btn-icon" title="Dark / Light">☾</button>
    </div>
  </header>

  <!-- DOCK MODE TABS -->
  <nav class="dock-tabs" aria-label="Studio Sections">
    <button class="dock-tab-btn active" data-tab="gears" data-i18n="tab_gears">Engrenamento</button>
    <button class="dock-tab-btn" data-tab="bodies" data-i18n="tab_bodies">Eixos &amp; Cubos</button>
    <button class="dock-tab-btn" data-tab="export" data-i18n="tab_export">Diagnóstico</button>
    <button class="dock-tab-btn" data-tab="presets" data-i18n="tab_presets">Presets</button>
  </nav>

  <!-- MAIN 3-COLUMN WORKSPACE -->
  <main class="studio-workspace">
    <!-- LEFT COLUMN: PRESETS + GEAR TRANSMISSION + DUAL TOOTH HEIGHT + PINION/GEAR BODIES -->
    <section class="col-panel col-left">
      <div class="col-scroll">
        <!-- 1. Mechanical Presets Gallery -->
        <div id="card-presets" class="studio-card">
          <div class="card-head">
            <span class="card-title" data-i18n="sec_presets">Presets Mecânicos</span>
            <button id="btn-toggle-save-preset" class="btn btn-soft" style="padding:2px 8px;font-size:10.5px;" data-i18n="btn_save_preset">+ Salvar</button>
          </div>
          <div id="save-preset-bar" class="save-preset-bar">
            <input id="inp-save-preset-name" class="save-preset-input" type="text" maxlength="64" placeholder="Nome do preset..." />
            <button id="btn-confirm-save-preset" class="btn btn-accent" style="padding:4px 8px;" data-i18n="btn_ok">Salvar</button>
          </div>
          <div id="preset-filters" class="preset-filter-row">
            <button class="filter-chip active" data-cat="all" data-i18n="cat_all">Todos</button>
            <button class="filter-chip" data-cat="spur_ind" data-i18n="cat_spur">Retas/Ind</button>
            <button class="filter-chip" data-cat="helical" data-i18n="cat_helical">Helicoidal</button>
            <button class="filter-chip" data-cat="herringbone" data-i18n="cat_herringbone">Espinha V</button>
            <button class="filter-chip" data-cat="robotics_cal" data-i18n="cat_robotics">Robótica/Fit</button>
            <button class="filter-chip" data-cat="user" data-i18n="cat_user">Meus</button>
          </div>
          <div id="presets-grid" class="presets-grid"></div>
        </div>

        <!-- 2. Transmission Type, Helix Angle & Teeth Pair -->
        <div id="card-transmission" class="studio-card">
          <div class="card-head">
            <span class="card-title" data-i18n="sec_transmission">Transmissão &amp; Hélice</span>
            <span id="badge-ratio" class="card-badge">1 : 2.00</span>
          </div>

          <div class="seg-group" role="radiogroup" aria-label="Gear Type">
            <button class="seg-btn active" data-gear-type="spur" data-i18n="gt_spur">Reta (Spur)</button>
            <button class="seg-btn" data-gear-type="helical" data-i18n="gt_helical">Helicoidal</button>
            <button class="seg-btn" data-gear-type="herringbone" data-i18n="gt_herringbone">Espinha de Peixe</button>
          </div>

          <!-- Helix Quick Pills (0°, 15°, 30°, 45° — 1-click auto-switches spur -> helical!) -->
          <div style="display:flex;flex-direction:column;gap:5px;">
            <div class="ctrl-top">
              <span class="ctrl-label" data-i18n="lbl_helix_quick">Ângulo de Hélice Rápido</span>
              <span id="badge-eff-helix" class="card-badge">β_eff 0.0°</span>
            </div>
            <div class="pill-row">
              <button class="quick-pill" data-helix-pill="0">0° (Reta)</button>
              <button class="quick-pill" data-helix-pill="15">15°</button>
              <button class="quick-pill" data-helix-pill="30">30°</button>
              <button class="quick-pill" data-helix-pill="45">45° Sem Suporte</button>
            </div>
            <div data-slider="helix_angle_deg"></div>
            <div id="row-helix-hand" class="seg-group">
              <button class="seg-btn active" data-helix-hand="right" data-i18n="hand_right">Mão Destra (G1 R / G2 L)</button>
              <button class="seg-btn" data-helix-hand="left" data-i18n="hand_left">Mão Canhota (G1 L / G2 R)</button>
            </div>
          </div>

          <div style="border-top:1px solid var(--border-subtle);padding-top:6px;display:flex;flex-direction:column;gap:6px;">
            <div data-slider="pinion.teeth"></div>
            <div data-slider="gear.teeth"></div>
            <button id="btn-swap-teeth" class="btn" style="padding:3px 8px;font-size:10.5px;" data-i18n="btn_swap_teeth">⇄ Inverter Pinhão / Coroa (Z1 ↔ Z2)</button>
          </div>

          <div style="border-top:1px solid var(--border-subtle);padding-top:6px;display:flex;flex-direction:column;gap:6px;">
            <div data-slider="module_mm"></div>
            <div class="pill-row">
              <button class="quick-pill" data-mod-pill="1.0">m 1.0</button>
              <button class="quick-pill" data-mod-pill="1.5">m 1.5</button>
              <button class="quick-pill" data-mod-pill="2.0">m 2.0</button>
              <button class="quick-pill" data-mod-pill="2.5">m 2.5</button>
              <button class="quick-pill" data-mod-pill="3.0">m 3.0</button>
            </div>
            <div data-slider="pressure_angle_deg"></div>
            <div data-slider="face_width_mm"></div>
          </div>
        </div>

        <!-- 3. Dual Tooth-Height Badges (Factor x | Real mm) & Profile Shift -->
        <div id="card-tooth-profile" class="studio-card">
          <div class="card-head">
            <span class="card-title" data-i18n="sec_tooth_height">Altura do Dente (Fator × | mm)</span>
            <span id="badge-total-tooth-h" class="card-badge">h = 4.50 mm</span>
          </div>

          <div class="pill-row">
            <button class="quick-pill" data-tooth-preset="iso" data-i18n="tp_iso">ISO Padrão 1.00×</button>
            <button class="quick-pill" data-tooth-preset="stub" data-i18n="tp_stub">Stub Robusto 0.75×</button>
            <button class="quick-pill" data-tooth-preset="high" data-i18n="tp_high">Alto Contato 1.20×</button>
          </div>

          <div data-slider="addendum_coeff" data-dual-mm="1"></div>
          <div data-slider="clearance_coeff" data-dual-mm="1"></div>
          <div data-slider="root_fillet_coeff" data-dual-mm="1"></div>
          <div data-slider="tip_chamfer_coeff" data-dual-mm="1"></div>

          <div style="border-top:1px solid var(--border-subtle);padding-top:6px;display:flex;flex-direction:column;gap:6px;">
            <div class="switch-row">
              <span class="ctrl-label" data-i18n="lbl_auto_shift">Auto Correção Anti-Undercut (x)</span>
              <label class="toggle-switch">
                <input id="chk-auto-shift" type="checkbox" checked />
                <span class="toggle-track"></span>
              </label>
            </div>
            <div id="badge-eff-shifts" class="helper-note">x₁ efetivo: +0.00 · x₂ efetivo: +0.00</div>
            <div data-slider="profile_shift_g1"></div>
            <div data-slider="profile_shift_g2"></div>
          </div>
        </div>

        <!-- 4. Independent Shafts, Hubs, Recesses & Lightening for Pinion (G1) and Gear (G2) -->
        <div id="card-bodies" class="studio-card">
          <div class="card-head">
            <span class="card-title" data-i18n="sec_bodies">Furos, Cubos &amp; Alívio</span>
          </div>

          <div class="seg-group">
            <button id="btn-body-tab-pinion" class="seg-btn active" data-i18n="body_pinion">⚙ Pinhão G1 (Motriz)</button>
            <button id="btn-body-tab-gear" class="seg-btn" data-i18n="body_gear">⚙ Coroa G2 (Movida)</button>
          </div>

          <!-- PINION G1 BODY PANE -->
          <div id="body-pane-pinion" style="display:flex;flex-direction:column;gap:7px;">
            <div class="ctrl-row">
              <span class="ctrl-label" data-i18n="lbl_bore_type">Tipo de Furo / Eixo (G1)</span>
              <select id="sel-pinion-bore-type" class="studio-select">
                <option value="none" data-i18n="bore_none">Sem Furo (Sólido)</option>
                <option value="round" data-i18n="bore_round">Circular Liso</option>
                <option value="d_shaft" data-i18n="bore_d">Eixo em D (NEMA / Motor)</option>
                <option value="double_d" data-i18n="bore_dd">Duplo D</option>
                <option value="hex" data-i18n="bore_hex">Sextavado (Hex / Porca)</option>
                <option value="keyway" data-i18n="bore_keyway">Rasgo de Chaveta DIN</option>
              </select>
            </div>
            <div id="box-pinion-bore-dims" style="display:flex;flex-direction:column;gap:6px;">
              <div data-slider="pinion.bore_diameter_mm"></div>
              <div data-slider="pinion.bore_clearance_mm"></div>
              <div id="box-pinion-dflat" data-slider="pinion.d_flat_depth_mm"></div>
              <div id="box-pinion-keyway" style="display:none;flex-direction:column;gap:6px;">
                <div data-slider="pinion.keyway_width_mm"></div>
                <div data-slider="pinion.keyway_depth_mm"></div>
              </div>
            </div>

            <!-- Hub G1 -->
            <div class="sub-feature-box">
              <div class="switch-row">
                <span class="ctrl-label" data-i18n="lbl_hub">Cubo Saliente Central (Hub)</span>
                <label class="toggle-switch">
                  <input id="chk-pinion-hub" type="checkbox" />
                  <span class="toggle-track"></span>
                </label>
              </div>
              <div id="box-pinion-hub" style="display:none;flex-direction:column;gap:6px;">
                <div data-slider="pinion.hub_diameter_mm"></div>
                <div data-slider="pinion.hub_height_mm"></div>
              </div>
            </div>

            <!-- Recess G1 -->
            <div class="sub-feature-box">
              <div class="switch-row">
                <span class="ctrl-label" data-i18n="lbl_recess">Alojamento Rolamento / Rebaixo</span>
                <label class="toggle-switch">
                  <input id="chk-pinion-recess" type="checkbox" />
                  <span class="toggle-track"></span>
                </label>
              </div>
              <div id="box-pinion-recess" style="display:none;flex-direction:column;gap:6px;">
                <select id="sel-pinion-recess-side" class="studio-select">
                  <option value="top" data-i18n="side_top">Topo (+Z)</option>
                  <option value="bottom" data-i18n="side_bottom">Base (Z=0)</option>
                  <option value="both" data-i18n="side_both">Ambos os Lados</option>
                </select>
                <div data-slider="pinion.recess_diameter_mm"></div>
                <div data-slider="pinion.recess_depth_mm"></div>
              </div>
            </div>

            <!-- Lightening G1 -->
            <div class="sub-feature-box">
              <span class="ctrl-label" data-i18n="lbl_lightening">Alívio de Massa do Corpo</span>
              <select id="sel-pinion-lightening" class="studio-select">
                <option value="solid" data-i18n="light_solid">Corpo Maciço</option>
                <option value="web_recess" data-i18n="light_web">Alma Rebaixada (Web)</option>
                <option value="lightening_holes" data-i18n="light_holes">Furos Circulares de Alívio</option>
              </select>
              <div id="box-pinion-web" style="display:none;" data-slider="pinion.web_thickness_mm"></div>
              <div id="box-pinion-holes" style="display:none;flex-direction:column;gap:6px;">
                <div data-slider="pinion.lightening_hole_count"></div>
                <div data-slider="pinion.lightening_hole_diameter_mm"></div>
              </div>
            </div>
          </div>

          <!-- DRIVEN GEAR G2 BODY PANE -->
          <div id="body-pane-gear" style="display:none;flex-direction:column;gap:7px;">
            <div class="ctrl-row">
              <span class="ctrl-label" data-i18n="lbl_bore_type_g2">Tipo de Furo / Eixo (G2)</span>
              <select id="sel-gear-bore-type" class="studio-select">
                <option value="none" data-i18n="bore_none">Sem Furo (Sólido)</option>
                <option value="round" data-i18n="bore_round">Circular Liso</option>
                <option value="d_shaft" data-i18n="bore_d">Eixo em D (NEMA / Motor)</option>
                <option value="double_d" data-i18n="bore_dd">Duplo D</option>
                <option value="hex" data-i18n="bore_hex">Sextavado (Hex / Porca)</option>
                <option value="keyway" data-i18n="bore_keyway">Rasgo de Chaveta DIN</option>
              </select>
            </div>
            <div id="box-gear-bore-dims" style="display:flex;flex-direction:column;gap:6px;">
              <div data-slider="gear.bore_diameter_mm"></div>
              <div data-slider="gear.bore_clearance_mm"></div>
              <div id="box-gear-dflat" style="display:none;" data-slider="gear.d_flat_depth_mm"></div>
              <div id="box-gear-keyway" style="display:none;flex-direction:column;gap:6px;">
                <div data-slider="gear.keyway_width_mm"></div>
                <div data-slider="gear.keyway_depth_mm"></div>
              </div>
            </div>

            <!-- Hub G2 -->
            <div class="sub-feature-box">
              <div class="switch-row">
                <span class="ctrl-label" data-i18n="lbl_hub">Cubo Saliente Central (Hub)</span>
                <label class="toggle-switch">
                  <input id="chk-gear-hub" type="checkbox" />
                  <span class="toggle-track"></span>
                </label>
              </div>
              <div id="box-gear-hub" style="display:none;flex-direction:column;gap:6px;">
                <div data-slider="gear.hub_diameter_mm"></div>
                <div data-slider="gear.hub_height_mm"></div>
              </div>
            </div>

            <!-- Recess G2 -->
            <div class="sub-feature-box">
              <div class="switch-row">
                <span class="ctrl-label" data-i18n="lbl_recess">Alojamento Rolamento / Rebaixo</span>
                <label class="toggle-switch">
                  <input id="chk-gear-recess" type="checkbox" />
                  <span class="toggle-track"></span>
                </label>
              </div>
              <div id="box-gear-recess" style="display:none;flex-direction:column;gap:6px;">
                <button id="btn-608-gear" class="btn btn-soft" style="padding:3px 7px;font-size:10px;">🎯 Preset Rolamento 608ZZ (Ø22.2×7mm)</button>
                <select id="sel-gear-recess-side" class="studio-select">
                  <option value="top" data-i18n="side_top">Topo (+Z)</option>
                  <option value="bottom" data-i18n="side_bottom">Base (Z=0)</option>
                  <option value="both" data-i18n="side_both">Ambos os Lados</option>
                </select>
                <div data-slider="gear.recess_diameter_mm"></div>
                <div data-slider="gear.recess_depth_mm"></div>
              </div>
            </div>

            <!-- Lightening G2 -->
            <div class="sub-feature-box">
              <span class="ctrl-label" data-i18n="lbl_lightening">Alívio de Massa do Corpo</span>
              <select id="sel-gear-lightening" class="studio-select">
                <option value="solid" data-i18n="light_solid">Corpo Maciço</option>
                <option value="web_recess" data-i18n="light_web">Alma Rebaixada (Web)</option>
                <option value="lightening_holes" data-i18n="light_holes">Furos Circulares de Alívio</option>
              </select>
              <div id="box-gear-web" style="display:none;" data-slider="gear.web_thickness_mm"></div>
              <div id="box-gear-holes" style="display:flex;flex-direction:column;gap:6px;">
                <div data-slider="gear.lightening_hole_count"></div>
                <div data-slider="gear.lightening_hole_diameter_mm"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CENTER COLUMN: 60 FPS 3D WEBGL2 VIEWPORT + MICRO-SIMULATION BAR + 2D TOOTH-MESH LOUPE -->
    <section class="viewport-col">
      <div class="vp-stage-3d">
        <canvas id="gl-canvas"></canvas>

        <!-- Top-Left View Mode & Shader Overlays -->
        <div class="vp-toolbar-left">
          <button class="vp-chip active" data-vp-view="meshed" data-i18n="vp_meshed">⚙ Par Engrenado</button>
          <button class="vp-chip" data-vp-view="plater" data-i18n="vp_plater">🖨 Mesa de Impressão</button>
          <button class="vp-chip" data-vp-view="fit_kit" data-i18n="vp_fit_kit">🧪 Kit de Teste Rápido</button>
          <button id="btn-vp-heatmap" class="vp-chip" data-i18n="vp_heatmap">🔥 Overhang</button>
          <button id="btn-vp-forces" class="vp-chip active" data-i18n="vp_forces">⚡ Forças 3D</button>
          <button id="btn-vp-wire" class="vp-chip" data-i18n="vp_wire">⌗ Malha</button>
        </div>

        <!-- Top-Right Live Force Vectors & Printability HUD -->
        <aside class="vp-hud-right vp-glass">
          <div class="hud-title-row">
            <span data-i18n="hud_title">Cargas &amp; Malha</span>
            <span id="hud-status-pill" class="hud-status-pill ok">OK</span>
          </div>
          <div class="hud-grid">
            <div class="hud-metric">
              <span class="hud-metric-k" data-i18n="hud_cd">Centros a (mm)</span>
              <span id="hud-cd" class="hud-metric-v">48.00</span>
            </div>
            <div class="hud-metric">
              <span class="hud-metric-k" data-i18n="hud_ft">Tangencial Ft</span>
              <span id="hud-ft" class="hud-metric-v">62.5 N</span>
            </div>
            <div class="hud-metric">
              <span class="hud-metric-k" data-i18n="hud_fr">Radial Fr</span>
              <span id="hud-fr" class="hud-metric-v">22.7 N</span>
            </div>
            <div class="hud-metric">
              <span class="hud-metric-k" data-i18n="hud_fa">Empuxo Axial Fa</span>
              <span id="hud-fa" class="hud-metric-v">0.0 N</span>
            </div>
          </div>
          <div id="hud-thrust-note" class="thrust-banner">Empuxo Axial Nulo (0 N)</div>
          <div id="heatmap-legend" class="heatmap-legend">
            <span><i class="legend-swatch" style="background:#00c853"></i>≤45°</span>
            <span><i class="legend-swatch" style="background:#ffb300"></i>45–55°</span>
            <span><i class="legend-swatch" style="background:#ff3d00"></i>&gt;55°</span>
          </div>
        </aside>

        <!-- Bottom-Left Camera Presets -->
        <div class="vp-cam-bar">
          <button class="vp-chip" data-cam="iso" data-i18n="cam_iso">Perspectiva</button>
          <button class="vp-chip" data-cam="top" data-i18n="cam_top">Topo (Engrenamento)</button>
          <button class="vp-chip" data-cam="front" data-i18n="cam_front">Frontal (Hélice)</button>
          <button class="vp-chip" data-cam="reset" data-i18n="cam_reset">Reset</button>
        </div>

        <!-- Bottom-Right Z Cross-Section Clipping Bar -->
        <div class="vp-cut-bar vp-glass">
          <span id="lbl-cut-axis" class="vp-cut-label" style="cursor:pointer;" title="Toggle Z / Y Cut Plane">✂ Corte Z</span>
          <input id="inp-cross-cut" class="orca-slider" type="range" min="0" max="100" step="1" value="0" />
          <span id="lbl-cross-cut" class="ctrl-num" style="width:40px;text-align:center;">Off</span>
          <button id="btn-cut-half" class="step-btn">50%</button>
        </div>
      </div>

      <!-- DEDICATED MICRO-SIMULATION & LIVE DELTA_A TRANSPORT BAR -->
      <div class="sim-transport-bar">
        <div class="sim-row">
          <div class="sim-group">
            <button id="btn-sim-play" class="btn btn-accent" style="min-width:74px;padding:4px 9px;" title="Play / Pause (Space)">⏸ Pause</button>
            <button id="btn-sim-dir" class="btn" style="padding:4px 8px;" title="Toggle CW / CCW">CW ↻</button>
          </div>

          <div class="sim-flex-slider">
            <span class="sim-tag">RPM</span>
            <input id="inp-sim-rpm" class="orca-slider" type="range" min="1" max="300" step="1" value="24" />
            <span id="lbl-sim-rpm" class="sim-mono" style="min-width:48px;">24 rpm</span>
          </div>

          <div class="sim-flex-slider">
            <span class="sim-tag" data-i18n="sim_scrub">Ângulo θ₁</span>
            <input id="inp-sim-angle" class="orca-slider" type="range" min="0" max="360" step="0.1" value="0" />
            <span id="lbl-sim-angle" class="sim-mono" style="min-width:46px;">0.0°</span>
            <div class="sim-group">
              <button class="step-btn" data-angle-step="-1">-1°</button>
              <button class="step-btn" data-angle-step="-0.2">-0.2°</button>
              <button class="step-btn" data-angle-step="0.2">+0.2°</button>
              <button class="step-btn" data-angle-step="1">+1°</button>
            </div>
          </div>
        </div>

        <div class="sim-row">
          <span class="sim-tag" data-i18n="sim_delta_a">Afaste / Aproxime Eixos (Δa):</span>
          <input id="inp-sim-delta-a" class="orca-slider" style="flex:1;" type="range" min="-1.00" max="2.00" step="0.01" value="0.00" />
          <span id="lbl-sim-delta-a" class="sim-mono" style="min-width:66px;">+0.00 mm</span>
          <button id="btn-sim-delta-reset" class="step-btn" data-i18n="btn_reset_da">Reset 0.00 mm</button>
        </div>
      </div>

      <!-- SYNCHRONIZED HIGH-DPI 2D TOOTH-MESH LOUPE -->
      <div id="loupe-panel" class="loupe-panel">
        <div class="loupe-header">
          <div class="loupe-title">
            <span data-i18n="loupe_title">🔍 Lupa 2D de Engrenamento &amp; Linha de Pressão</span>
            <span id="loupe-jam-badge" class="jam-alert-badge">
              <span>⚠</span>
              <span data-i18n="jam_alert">INTERFERÊNCIA / TRAVAMENTO DETECTADO</span>
            </span>
          </div>
          <div class="sim-group">
            <button class="step-btn" data-loupe-zoom="1.0">1×</button>
            <button class="step-btn" data-loupe-zoom="1.7">1.7×</button>
            <button class="step-btn" data-loupe-zoom="2.6">2.6×</button>
            <button id="btn-loupe-collapse" class="step-btn" title="Expand / Collapse 2D Loupe">▾</button>
          </div>
        </div>
        <div class="loupe-canvas-wrap">
          <canvas id="loupe-canvas" width="640" height="168"></canvas>
        </div>
      </div>
    </section>

    <!-- RIGHT COLUMN: FDM FIT TOLERANCES + FULL DIAGNOSTICS REPORT + ORCASLICER EXPORT -->
    <section class="col-panel col-right">
      <div class="col-scroll">
        <!-- 1. FDM Fit Tolerances & Input Torque -->
        <div id="card-tolerances" class="studio-card">
          <div class="card-head">
            <span class="card-title" data-i18n="sec_tolerances">Folgas FDM &amp; Torque Motriz</span>
          </div>
          <div data-slider="backlash_mm"></div>
          <div data-slider="xy_compensation_mm"></div>
          <div data-slider="elephant_foot_chamfer_mm"></div>
          <div data-slider="center_distance_offset_mm"></div>
          <div data-slider="input_torque_nm"></div>
        </div>

        <!-- 2. Comprehensive Engineering & Fit Diagnostics -->
        <div id="card-diagnostics" class="studio-card">
          <div class="card-head">
            <span class="card-title" data-i18n="sec_diagnostics">Diagnóstico de Engrenamento</span>
            <span id="diag-status-pill" class="hud-status-pill ok">ÓTIMO</span>
          </div>

          <div class="diag-section-title" data-i18n="diag_sec_contact">Razão de Contato &amp; Envolvente</div>
          <div class="diag-grid">
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_eps_a">Transversal ε_α</span>
              <span id="dv-eps-a" class="diag-v">1.58</span>
            </div>
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_eps_b">Recobrimento Axial ε_β</span>
              <span id="dv-eps-b" class="diag-v">0.00</span>
            </div>
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_eps_g">Contato Total ε_γ</span>
              <span id="dv-eps-g" class="diag-v">1.58</span>
            </div>
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_loa">Linha de Ação</span>
              <span id="dv-loa" class="diag-v">9.35 mm</span>
            </div>
          </div>

          <div class="diag-section-title" data-i18n="diag_sec_fit">Encaixe, Folga &amp; Cinemática</div>
          <div class="diag-grid">
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_cd">Distância Centros a</span>
              <span id="dv-cd" class="diag-v">48.00 mm</span>
            </div>
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_clr">Folga Mín. Dentes</span>
              <span id="dv-clr" class="diag-v">0.14 mm</span>
            </div>
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_t2">Torque Saída (G2)</span>
              <span id="dv-t2" class="diag-v">2.00 N·m</span>
            </div>
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_rpm2">Rotação Saída / Vel.</span>
              <span id="dv-rpm2" class="diag-v">12.0 rpm</span>
            </div>
          </div>

          <div class="diag-section-title" data-i18n="diag_sec_print">Impressão Mecânica FDM</div>
          <div class="diag-grid">
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_ovh">Overhang Hélice</span>
              <span id="dv-ovh" class="diag-v">0.0° (Livre)</span>
            </div>
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_walls">Paredes Sugeridas</span>
              <span id="dv-walls" class="diag-v">4 loops</span>
            </div>
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_wgt">Peso / Tempo Est.</span>
              <span id="dv-wgt" class="diag-v">~34 g · 42 min</span>
            </div>
            <div class="diag-cell">
              <span class="diag-k" data-i18n="dk_bed">Área na Mesa</span>
              <span id="dv-bed" class="diag-v">112×68 mm</span>
            </div>
          </div>

          <div id="diag-issues-list" class="issues-list"></div>
        </div>

        <!-- 3. Export Target & Mechanical Slicer Auto-Configuration -->
        <div id="card-export-cfg" class="studio-card">
          <div class="card-head">
            <span class="card-title" data-i18n="sec_export_pkg">Pacote de Saída &amp; Fatiamento</span>
          </div>

          <div class="ctrl-row">
            <span class="ctrl-label" data-i18n="lbl_export_target">O que enviar / exportar:</span>
            <select id="sel-export-target" class="studio-select">
              <option value="pair_separated" data-i18n="exp_pair">Par Separado (Pronto p/ Imprimir)</option>
              <option value="pinion_only" data-i18n="exp_pinion">Apenas Pinhão (G1)</option>
              <option value="gear_only" data-i18n="exp_gear">Apenas Coroa (G2)</option>
              <option value="fit_test_kit" data-i18n="exp_kit">Kit de Teste Rápido (Setores + Base 2 Pinos + Régua Eixo)</option>
              <option value="full_suite" data-i18n="exp_full">Conjunto Completo (Par + Gabaritos)</option>
            </select>
          </div>

          <div id="export-target-note" class="helper-note" data-i18n="note_exp_pair">
            Posiciona Pinhão (G1) e Coroa (G2) separados com margem segura na mesa, prontos para fatiar sem fusão de dentes.
          </div>

          <div class="switch-row" style="padding-top:3px;">
            <span class="ctrl-label" style="white-space:normal;" data-i18n="lbl_auto_slicer">Auto-Ajustar Fatiamento Mecânico (4–6 paredes maciças + Gyroid)</span>
            <label class="toggle-switch">
              <input id="chk-auto-slicer" type="checkbox" checked />
              <span class="toggle-track"></span>
            </label>
          </div>
        </div>
      </div>

      <!-- Wide Mode Sticky Action Footer -->
      <footer class="action-footer">
        <button class="btn-hero" data-action="send_to_plater">
          <span>🚀</span>
          <span data-i18n="btn_send_plater">Enviar para a Mesa do OrcaSlicer</span>
        </button>
        <div class="export-btn-row">
          <button class="btn" data-action="export_3mf">💾 <span data-i18n="btn_exp_3mf">Exportar .3MF</span></button>
          <button class="btn" data-action="export_stl">📐 <span data-i18n="btn_exp_stl">Exportar .STL</span></button>
          <button class="btn btn-icon" data-action="open_folder" title="Abrir Pasta de Exportação">📂</button>
        </div>
      </footer>
    </section>
  </main>

  <!-- Compact Dock Mode Sticky Footer -->
  <footer class="action-footer dock-global-footer">
    <button class="btn-hero" data-action="send_to_plater" style="padding:8px 10px;font-size:12px;">
      <span>🚀</span>
      <span data-i18n="btn_send_plater">Enviar para a Mesa do OrcaSlicer</span>
    </button>
    <div class="export-btn-row">
      <button class="btn" data-action="export_3mf">💾 .3MF</button>
      <button class="btn" data-action="export_stl">📐 .STL</button>
      <button class="btn btn-icon" data-action="open_folder" title="Abrir Pasta">📂</button>
    </div>
  </footer>
</div>

<div id="toast-banner" class="toast-banner" role="status" aria-live="polite"></div>

<script>
(function () {
  "use strict";

  const BOOT_PAYLOAD = __ORCA_GEAR_STUDIO_BOOT_JSON__;
  const DEG2RAD = Math.PI / 180.0;
  const RAD2DEG = 180.0 / Math.PI;
  const TWO_PI = 2.0 * Math.PI;

  // ==========================================================================
  // 1. Canonical Parameter Schema & Normalization (100% Parity with schema.py)
  // ==========================================================================
  const VALID_GEAR_TYPES = ["spur", "helical", "herringbone"];
  const VALID_HELIX_HANDS = ["right", "left"];
  const VALID_BORE_TYPES = ["none", "round", "d_shaft", "double_d", "hex", "keyway"];
  const VALID_RECESS_SIDES = ["top", "bottom", "both"];
  const VALID_LIGHTENING_MODES = ["solid", "web_recess", "lightening_holes"];
  const VALID_SIM_DIRECTIONS = ["cw", "ccw"];
  const VALID_EXPORT_TARGETS = ["pair_separated", "pinion_only", "gear_only", "fit_test_kit", "full_suite"];

  const JS_DEFAULT_PARAMS = {
    schema_version: 1,
    name: "Par Engrenagens",
    gear_type: "spur",
    module_mm: 2.0,
    pressure_angle_deg: 20.0,
    helix_angle_deg: 30.0,
    helix_hand: "right",
    face_width_mm: 12.0,
    addendum_coeff: 1.00,
    clearance_coeff: 0.25,
    root_fillet_coeff: 0.30,
    tip_chamfer_coeff: 0.06,
    auto_profile_shift: true,
    profile_shift_g1: 0.0,
    profile_shift_g2: 0.0,
    backlash_mm: 0.15,
    xy_compensation_mm: 0.02,
    elephant_foot_chamfer_mm: 0.40,
    center_distance_offset_mm: 0.0,
    input_torque_nm: 1.0,
    pinion: {
      teeth: 16,
      bore_type: "d_shaft",
      bore_diameter_mm: 5.0,
      bore_clearance_mm: 0.12,
      d_flat_depth_mm: 0.50,
      keyway_width_mm: 2.0,
      keyway_depth_mm: 1.0,
      hub_enabled: false,
      hub_diameter_mm: 14.0,
      hub_height_mm: 5.0,
      recess_enabled: false,
      recess_side: "top",
      recess_diameter_mm: 16.0,
      recess_depth_mm: 4.0,
      lightening_mode: "solid",
      web_thickness_mm: 4.0,
      lightening_hole_count: 6,
      lightening_hole_diameter_mm: 5.0
    },
    gear: {
      teeth: 32,
      bore_type: "round",
      bore_diameter_mm: 8.0,
      bore_clearance_mm: 0.12,
      d_flat_depth_mm: 0.60,
      keyway_width_mm: 3.0,
      keyway_depth_mm: 1.4,
      hub_enabled: false,
      hub_diameter_mm: 20.0,
      hub_height_mm: 5.0,
      recess_enabled: false,
      recess_side: "top",
      recess_diameter_mm: 22.0,
      recess_depth_mm: 3.5,
      lightening_mode: "lightening_holes",
      web_thickness_mm: 4.0,
      lightening_hole_count: 6,
      lightening_hole_diameter_mm: 8.0
    },
    sim_rpm: 24.0,
    sim_direction: "cw",
    export_target: "pair_separated",
    auto_configure_slicer: true
  };

  function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
  }

  function clampFloat(val, defVal, lo, hi) {
    if (typeof val === "boolean" || val === null || val === undefined || val === "") return defVal;
    const f = Number(val);
    if (!Number.isFinite(f)) return defVal;
    return Math.max(lo, Math.min(hi, f));
  }

  function clampInt(val, defVal, lo, hi) {
    if (typeof val === "boolean" || val === null || val === undefined || val === "") return defVal;
    const f = Number(val);
    if (!Number.isFinite(f)) return defVal;
    return Math.max(lo, Math.min(hi, Math.round(f)));
  }

  function toBool(val, defVal) {
    if (typeof val === "boolean") return val;
    if (typeof val === "number") return Number.isFinite(val) ? Boolean(val) : defVal;
    if (typeof val === "string") {
      const s = val.trim().toLowerCase();
      if (s === "true" || s === "1" || s === "yes" || s === "on") return true;
      if (s === "false" || s === "0" || s === "no" || s === "off" || s === "") return false;
    }
    return defVal;
  }

  function toChoice(val, defVal, allowed) {
    if (typeof val === "string") {
      const s = val.trim().toLowerCase();
      if (allowed.indexOf(s) >= 0) return s;
    }
    return defVal;
  }

  function normalizeGearBody(rawBody, template) {
    const base = template || JS_DEFAULT_PARAMS.pinion;
    const src = (rawBody && typeof rawBody === "object") ? rawBody : {};
    return {
      teeth: clampInt(src.teeth, base.teeth, 6, 240),
      bore_type: toChoice(src.bore_type, base.bore_type, VALID_BORE_TYPES),
      bore_diameter_mm: clampFloat(src.bore_diameter_mm, base.bore_diameter_mm, 1.0, 160.0),
      bore_clearance_mm: clampFloat(src.bore_clearance_mm, base.bore_clearance_mm, -0.25, 1.50),
      d_flat_depth_mm: clampFloat(src.d_flat_depth_mm, base.d_flat_depth_mm, 0.05, 25.0),
      keyway_width_mm: clampFloat(src.keyway_width_mm, base.keyway_width_mm, 0.50, 40.0),
      keyway_depth_mm: clampFloat(src.keyway_depth_mm, base.keyway_depth_mm, 0.25, 25.0),
      hub_enabled: toBool(src.hub_enabled, base.hub_enabled),
      hub_diameter_mm: clampFloat(src.hub_diameter_mm, base.hub_diameter_mm, 3.0, 300.0),
      hub_height_mm: clampFloat(src.hub_height_mm, base.hub_height_mm, 0.5, 80.0),
      recess_enabled: toBool(src.recess_enabled, base.recess_enabled),
      recess_side: toChoice(src.recess_side, base.recess_side, VALID_RECESS_SIDES),
      recess_diameter_mm: clampFloat(src.recess_diameter_mm, base.recess_diameter_mm, 3.0, 300.0),
      recess_depth_mm: clampFloat(src.recess_depth_mm, base.recess_depth_mm, 0.5, 60.0),
      lightening_mode: toChoice(src.lightening_mode, base.lightening_mode, VALID_LIGHTENING_MODES),
      web_thickness_mm: clampFloat(src.web_thickness_mm, base.web_thickness_mm, 1.2, 80.0),
      lightening_hole_count: clampInt(src.lightening_hole_count, base.lightening_hole_count, 3, 18),
      lightening_hole_diameter_mm: clampFloat(src.lightening_hole_diameter_mm, base.lightening_hole_diameter_mm, 1.5, 100.0)
    };
  }

  function effectiveHelixAngleDeg(params) {
    if (!params || typeof params !== "object") return 0.0;
    const gt = toChoice(params.gear_type, "spur", VALID_GEAR_TYPES);
    if (gt === "spur") return 0.0;
    return clampFloat(params.helix_angle_deg, 30.0, 0.0, 60.0);
  }

  function normalizeParams(raw) {
    const d = JS_DEFAULT_PARAMS;
    const src = (raw && typeof raw === "object") ? raw : {};
    const rawName = typeof src.name === "string" ? src.name.trim() : "";
    const cleanName = (rawName || d.name).slice(0, 80);

    return {
      schema_version: 1,
      name: cleanName,
      gear_type: toChoice(src.gear_type, d.gear_type, VALID_GEAR_TYPES),
      module_mm: clampFloat(src.module_mm, d.module_mm, 0.5, 10.0),
      pressure_angle_deg: clampFloat(src.pressure_angle_deg, d.pressure_angle_deg, 14.5, 30.0),
      helix_angle_deg: clampFloat(src.helix_angle_deg, d.helix_angle_deg, 0.0, 60.0),
      helix_hand: toChoice(src.helix_hand, d.helix_hand, VALID_HELIX_HANDS),
      face_width_mm: clampFloat(src.face_width_mm, d.face_width_mm, 2.0, 120.0),
      addendum_coeff: clampFloat(src.addendum_coeff, d.addendum_coeff, 0.40, 1.40),
      clearance_coeff: clampFloat(src.clearance_coeff, d.clearance_coeff, 0.10, 0.50),
      root_fillet_coeff: clampFloat(src.root_fillet_coeff, d.root_fillet_coeff, 0.05, 0.45),
      tip_chamfer_coeff: clampFloat(src.tip_chamfer_coeff, d.tip_chamfer_coeff, 0.00, 0.25),
      auto_profile_shift: toBool(src.auto_profile_shift, d.auto_profile_shift),
      profile_shift_g1: clampFloat(src.profile_shift_g1, d.profile_shift_g1, -0.50, 0.80),
      profile_shift_g2: clampFloat(src.profile_shift_g2, d.profile_shift_g2, -0.50, 0.80),
      backlash_mm: clampFloat(src.backlash_mm, d.backlash_mm, 0.00, 1.00),
      xy_compensation_mm: clampFloat(src.xy_compensation_mm, d.xy_compensation_mm, -0.20, 0.30),
      elephant_foot_chamfer_mm: clampFloat(src.elephant_foot_chamfer_mm, d.elephant_foot_chamfer_mm, 0.00, 1.50),
      center_distance_offset_mm: clampFloat(src.center_distance_offset_mm, d.center_distance_offset_mm, -1.50, 3.00),
      input_torque_nm: clampFloat(src.input_torque_nm, d.input_torque_nm, 0.05, 50.0),
      pinion: normalizeGearBody(src.pinion, d.pinion),
      gear: normalizeGearBody(src.gear, d.gear),
      sim_rpm: clampFloat(src.sim_rpm, d.sim_rpm, 1.0, 300.0),
      sim_direction: toChoice(src.sim_direction, d.sim_direction, VALID_SIM_DIRECTIONS),
      export_target: toChoice(src.export_target, d.export_target, VALID_EXPORT_TARGETS),
      auto_configure_slicer: toBool(src.auto_configure_slicer, d.auto_configure_slicer)
    };
  }

  // ==========================================================================
  // 2. ISO 21771 / ISO 53 Involute Math & 2D Contour Parity (involute_math.py)
  // ==========================================================================
  function involuteFn(alphaRad) {
    return Math.tan(alphaRad) - alphaRad;
  }

  function inverseInvoluteFn(invVal) {
    if (!Number.isFinite(invVal) || invVal <= 0.0) return 0.0;
    const maxAlpha = 0.5 * Math.PI - 1e-9;
    let alpha;
    if (invVal < 0.5) {
      const c = Math.cbrt(3.0 * invVal);
      alpha = c / (1.0 + 0.4 * c * c / 3.0);
    } else {
      alpha = Math.min(maxAlpha, 0.5 * Math.PI - 1.0 / (invVal + 0.5 * Math.PI));
    }
    alpha = Math.max(1e-12, Math.min(maxAlpha, alpha));
    for (let i = 0; i < 32; i++) {
      const t = Math.tan(alpha);
      const res = t - alpha - invVal;
      if (Math.abs(res) <= 1e-13) break;
      const t2 = t * t;
      if (t2 <= 1e-30) break;
      const step = res / t2;
      const nextA = alpha - step;
      if (nextA <= 0.0) alpha *= 0.5;
      else if (nextA >= maxAlpha) alpha = 0.5 * (alpha + maxAlpha);
      else alpha = nextA;
      if (Math.abs(step) <= 1e-13) break;
    }
    return alpha;
  }

  function transverseToothThicknessAtRadius(r, rb, psiB) {
    if (r <= 0.0) return 0.0;
    if (r <= rb) return 2.0 * r * psiB;
    const cosA = Math.max(-1.0, Math.min(1.0, rb / r));
    const alphaR = Math.acos(cosA);
    return 2.0 * r * (psiB - involuteFn(alphaR));
  }

  function clampTipRadiusNonPointed(raTarget, rRef, rb, rf, psiB, minTipS) {
    const sTarget = transverseToothThicknessAtRadius(raTarget, rb, psiB);
    if (sTarget > minTipS) return [raTarget, sTarget];
    const rLo = Math.max(rf + 0.05, Math.min(rRef, rb));
    const sLo = transverseToothThicknessAtRadius(rLo, rb, psiB);
    if (sLo <= minTipS) return [rLo, Math.max(1e-4, sLo)];
    let lo = rLo;
    let hi = raTarget;
    for (let i = 0; i < 40; i++) {
      const mid = 0.5 * (lo + hi);
      if (transverseToothThicknessAtRadius(mid, rb, psiB) >= minTipS) lo = mid;
      else hi = mid;
    }
    return [lo, Math.max(1e-4, transverseToothThicknessAtRadius(lo, rb, psiB))];
  }

  function computeGearPairGeometry(params) {
    const p = normalizeParams(params);
    const betaDeg = effectiveHelixAngleDeg(p);
    const betaRad = betaDeg * DEG2RAD;
    const cosBeta = Math.cos(betaRad);

    const mN = p.module_mm;
    const mT = mN / cosBeta;

    const alphaNDeg = p.pressure_angle_deg;
    const alphaNRad = alphaNDeg * DEG2RAD;
    const tanAlphaN = Math.tan(alphaNRad);

    const alphaTRad = Math.atan(tanAlphaN / cosBeta);
    const alphaTDeg = alphaTRad * RAD2DEG;
    const cosAlphaT = Math.cos(alphaTRad);
    const sinAlphaT = Math.sin(alphaTRad);
    const invAlphaT = involuteFn(alphaTRad);

    const z1 = p.pinion.teeth;
    const z2 = p.gear.teeth;
    const zSum = z1 + z2;

    const haCoeff = p.addendum_coeff;
    const cCoeff = p.clearance_coeff;

    const xMin1 = Math.max(0.0, haCoeff - 0.5 * z1 * sinAlphaT * sinAlphaT);
    const xMin2 = Math.max(0.0, haCoeff - 0.5 * z2 * sinAlphaT * sinAlphaT);

    const x1 = p.auto_profile_shift ? Math.max(p.profile_shift_g1, xMin1) : p.profile_shift_g1;
    const x2 = p.auto_profile_shift ? Math.max(p.profile_shift_g2, xMin2) : p.profile_shift_g2;

    const invAlphaTwRaw = invAlphaT + 2.0 * tanAlphaN * (x1 + x2) / zSum;
    const alphaTwRad = inverseInvoluteFn(Math.max(0.0, invAlphaTwRaw));
    const alphaTwDeg = alphaTwRad * RAD2DEG;
    const cosAlphaTw = Math.max(1e-6, Math.cos(alphaTwRad));

    const a0 = 0.5 * mT * zSum * cosAlphaT / cosAlphaTw;
    const a = Math.max(2.0, a0 + p.center_distance_offset_mm);

    const rw1 = a * z1 / zSum;
    const rw2 = a * z2 / zSum;

    const r1 = 0.5 * mT * z1;
    const r2 = 0.5 * mT * z2;
    const rb1 = r1 * cosAlphaT;
    const rb2 = r2 * cosAlphaT;

    const sMinPitch = 0.15 * mT;
    const sMaxPitch = 0.90 * Math.PI * mT;
    let sT1 = mT * (0.5 * Math.PI + 2.0 * x1 * tanAlphaN) - p.backlash_mm / (2.0 * cosBeta) - 2.0 * p.xy_compensation_mm;
    let sT2 = mT * (0.5 * Math.PI + 2.0 * x2 * tanAlphaN) - p.backlash_mm / (2.0 * cosBeta) - 2.0 * p.xy_compensation_mm;
    sT1 = Math.max(sMinPitch, Math.min(sMaxPitch, sT1));
    sT2 = Math.max(sMinPitch, Math.min(sMaxPitch, sT2));

    const psiB1 = sT1 / (2.0 * r1) + invAlphaT;
    const psiB2 = sT2 / (2.0 * r2) + invAlphaT;

    const ded1 = Math.max(0.10 * mN, mN * (haCoeff + cCoeff - x1));
    const ded2 = Math.max(0.10 * mN, mN * (haCoeff + cCoeff - x2));
    const rf1 = Math.max(0.8, r1 - ded1);
    const rf2 = Math.max(0.8, r2 - ded2);

    const ra1Raw = r1 + Math.max(0.10 * mN, mN * (haCoeff + x1));
    const ra2Raw = r2 + Math.max(0.10 * mN, mN * (haCoeff + x2));

    const minTipS = 0.08 * mN;
    const res1 = clampTipRadiusNonPointed(ra1Raw, r1, rb1, rf1, psiB1, minTipS);
    const res2 = clampTipRadiusNonPointed(ra2Raw, r2, rb2, rf2, psiB2, minTipS);
    const ra1 = res1[0], sA1 = res1[1];
    const ra2 = res2[0], sA2 = res2[1];

    const invLockRhs = (z1 * psiB1 + z2 * psiB2 - Math.PI) / zSum;
    const alphaLockRad = inverseInvoluteFn(Math.max(0.0, invLockRhs));
    const aInvLock = (rb1 + rb2) / Math.max(1e-6, Math.cos(alphaLockRad));
    const aBottom = Math.max(ra1 + rf2, ra2 + rf1);
    const minNonJamA = Math.max(aInvLock, aBottom);

    const pinionHand = p.helix_hand;
    const gearHand = pinionHand === "right" ? "left" : "right";
    const meshPhaseG2Rad = Math.PI - (Math.PI / z2);

    return {
      beta_deg: betaDeg,
      beta_rad: betaRad,
      alpha_n_deg: alphaNDeg,
      alpha_t_deg: alphaTDeg,
      alpha_tw_deg: alphaTwDeg,
      m_n: mN,
      m_t: mT,
      x1: x1,
      x2: x2,
      nominal_center_distance_mm: a0,
      center_distance_mm: a,
      min_non_jam_center_distance_mm: minNonJamA,
      ratio: z2 / z1,
      mesh_phase_g2_rad: meshPhaseG2Rad,
      pinion: {
        teeth: z1,
        profile_shift: x1,
        min_profile_shift_no_undercut: xMin1,
        undercut: x1 < xMin1 - 1e-4,
        pitch_radius_mm: r1,
        working_pitch_radius_mm: rw1,
        base_radius_mm: rb1,
        tip_radius_mm: ra1,
        root_radius_mm: rf1,
        addendum_mm: ra1 - r1,
        dedendum_mm: r1 - rf1,
        tooth_height_mm: ra1 - rf1,
        tooth_thickness_pitch_mm: sT1,
        tip_thickness_mm: sA1,
        base_half_angle_rad: psiB1,
        helix_hand: pinionHand,
        face_width_mm: p.face_width_mm
      },
      gear: {
        teeth: z2,
        profile_shift: x2,
        min_profile_shift_no_undercut: xMin2,
        undercut: x2 < xMin2 - 1e-4,
        pitch_radius_mm: r2,
        working_pitch_radius_mm: rw2,
        base_radius_mm: rb2,
        tip_radius_mm: ra2,
        root_radius_mm: rf2,
        addendum_mm: ra2 - r2,
        dedendum_mm: r2 - rf2,
        tooth_height_mm: ra2 - rf2,
        tooth_thickness_pitch_mm: sT2,
        tip_thickness_mm: sA2,
        base_half_angle_rad: psiB2,
        helix_hand: gearHand,
        face_width_mm: p.face_width_mm
      }
    };
  }

  function helixTwistAngleRad(zMm, faceWidthMm, pitchRadiusMm, betaDeg, hand, gearType) {
    if (gearType === "spur" || Math.abs(betaDeg) < 1e-6 || pitchRadiusMm <= 1e-6) return 0.0;
    const sign = hand === "right" ? 1.0 : -1.0;
    const zEff = gearType === "herringbone" ? Math.min(zMm, faceWidthMm - zMm) : zMm;
    return sign * zEff * Math.tan(betaDeg * DEG2RAD) / pitchRadiusMm;
  }

  function buildSingleToothPolarTemplate(p, geom, which, samplesPerFlank, radialInsetMm) {
    const g = which === "gear" ? geom.gear : geom.pinion;
    const zTeeth = g.teeth;
    const mN = geom.m_n;
    const mT = geom.m_t;
    const alphaTRad = geom.alpha_t_deg * DEG2RAD;
    const alphaNRad = geom.alpha_n_deg * DEG2RAD;
    const invAlphaT = involuteFn(alphaTRad);

    const rRef = g.pitch_radius_mm;
    const rb = g.base_radius_mm;
    const raBase = g.tip_radius_mm;
    const rfBase = g.root_radius_mm;
    const sTBase = g.tooth_thickness_pitch_mm;

    const nFlank = Math.max(4, samplesPerFlank | 0);
    const nInv = nFlank - 1;
    const tauHalf = Math.PI / zTeeth;

    let rf = rfBase;
    let raTarget = raBase;
    let sT = sTBase;
    const inset = Math.max(0.0, radialInsetMm || 0.0);
    if (inset > 0.0) {
      const maxSafeInset = Math.min(0.32 * mN, 0.25 * (raBase - rfBase), 0.20 * sTBase);
      const effInset = Math.min(inset, Math.max(0.0, maxSafeInset));
      rf = Math.max(0.5, rfBase - effInset);
      raTarget = Math.max(rf + 0.20 * mN, raBase - effInset);
      sT = Math.max(0.16 * mT, sTBase - 2.0 * effInset / Math.max(0.5, Math.cos(alphaNRad)));
    }

    const psiB = sT / (2.0 * rRef) + invAlphaT;
    const ra = clampTipRadiusNonPointed(raTarget, rRef, rb, rf, psiB, 0.06 * mN)[0];

    const invHalfAngle = function (rVal) {
      if (rVal <= rb) return psiB;
      return psiB - involuteFn(Math.acos(Math.max(-1.0, Math.min(1.0, rb / rVal))));
    };

    const rhoFillet = Math.max(0.02 * mN, Math.min(p.root_fillet_coeff * mN, 0.45 * (ra - rf)));
    let rJoin = Math.max(rb, Math.min(rf + rhoFillet, rf + 0.48 * (ra - rf)));
    rJoin = Math.min(rJoin, ra - 0.08 * (ra - rf));

    const psiJoin = invHalfAngle(rJoin);
    const maxPsiJoin = 0.86 * tauHalf;
    const angleScale = psiJoin > maxPsiJoin ? (maxPsiJoin / psiJoin) : 1.0;
    const scaledPsi = function (rVal) {
      return Math.max(1e-5, invHalfAngle(rVal) * angleScale);
    };

    const psiJoinEff = scaledPsi(rJoin);
    const cTip = Math.max(0.0, Math.min(p.tip_chamfer_coeff * mN, 0.28 * (ra - rJoin)));
    const psiRa = scaledPsi(ra);

    let rChamf, psiTipCorner;
    if (cTip > 1e-5) {
      rChamf = ra - cTip;
      psiTipCorner = Math.max(0.22 * psiRa, psiRa - 0.85 * cTip / Math.max(1.0, ra));
    } else {
      rChamf = rJoin + ((nInv - 1) / Math.max(1, nInv)) * (ra - rJoin);
      psiTipCorner = psiRa;
    }

    const rInvPts = new Float64Array(nInv);
    const psiInvPts = new Float64Array(nInv);
    for (let i = 0; i < nInv; i++) {
      const u = nInv > 1 ? (i / (nInv - 1)) : 0.0;
      const sParam = 0.55 * u * u + 0.45 * u;
      const rv = rJoin + sParam * (rChamf - rJoin);
      rInvPts[i] = rv;
      psiInvPts[i] = scaledPsi(rv);
    }

    const availValley = Math.max(1e-4, tauHalf - psiJoinEff);
    const deltaPsiFil = Math.min(Math.max(rhoFillet / Math.max(1.0, rf), 0.16 * availValley), 0.68 * availValley);
    const psiFilEnd = psiJoinEff + deltaPsiFil;
    const uFil = [0.32, 0.68, 1.0];
    const psiFilUpper = uFil.map(function (u) { return psiJoinEff + u * deltaPsiFil; });
    const rFilUpper = uFil.map(function (u) { return rf + (rJoin - rf) * (1.0 - Math.sin(0.5 * Math.PI * u)); });
    const psiRootMid = 0.5 * (psiFilEnd + tauHalf);

    const phi = [];
    const rad = [];
    phi.push(-psiRootMid); rad.push(rf);
    for (let i = 2; i >= 0; i--) { phi.push(-psiFilUpper[i]); rad.push(rFilUpper[i]); }
    for (let i = 0; i < nInv; i++) { phi.push(-psiInvPts[i]); rad.push(rInvPts[i]); }
    phi.push(-psiTipCorner); rad.push(ra);
    phi.push(0.0); rad.push(ra);
    phi.push(psiTipCorner); rad.push(ra);
    for (let i = nInv - 1; i >= 0; i--) { phi.push(psiInvPts[i]); rad.push(rInvPts[i]); }
    for (let i = 0; i < 3; i++) { phi.push(psiFilUpper[i]); rad.push(rFilUpper[i]); }
    phi.push(psiRootMid); rad.push(rf);
    phi.push(tauHalf); rad.push(rf);

    return { phi: phi, rad: rad, rf: rf, ra: ra };
  }

  function buildGear2DContour(p, geom, which, samplesPerFlank, radialInsetMm) {
    const g = which === "gear" ? geom.gear : geom.pinion;
    const zTeeth = g.teeth;
    const tpl = buildSingleToothPolarTemplate(p, geom, which, samplesPerFlank, radialInsetMm);
    const ptsPerTooth = tpl.phi.length;
    const total = zTeeth * ptsPerTooth;
    const xs = new Float64Array(total);
    const ys = new Float64Array(total);
    let ptr = 0;
    for (let k = 0; k < zTeeth; k++) {
      const baseAng = (TWO_PI * k) / zTeeth;
      for (let j = 0; j < ptsPerTooth; j++) {
        const a = baseAng + tpl.phi[j];
        const r = tpl.rad[j];
        xs[ptr] = r * Math.cos(a);
        ys[ptr] = r * Math.sin(a);
        ptr++;
      }
    }
    return { xs: xs, ys: ys, count: total, ptsPerTooth: ptsPerTooth, rf: tpl.rf, ra: tpl.ra };
  }

  function buildBore2DContour(boreCfg, maxAllowedRadiusMm, radialSamples, extraClearanceMm) {
    const bt = boreCfg ? boreCfg.bore_type : "none";
    if (!boreCfg || bt === "none") return null;
    const m = Math.max(24, radialSamples | 0);
    const maxR = Math.max(0.4, maxAllowedRadiusMm);
    const dEff = boreCfg.bore_diameter_mm + boreCfg.bore_clearance_mm + (extraClearanceMm || 0.0);
    const rNom = Math.max(0.35, Math.min(maxR, 0.5 * dEff));
    const xs = new Float64Array(m);
    const ys = new Float64Array(m);

    for (let i = 0; i < m; i++) {
      const ang = (TWO_PI * i) / m;
      const cosA = Math.cos(ang);
      const sinA = Math.sin(ang);
      let r = rNom;

      if (bt === "d_shaft" || bt === "double_d") {
        const flatDepth = Math.max(0.05 * rNom, Math.min(boreCfg.d_flat_depth_mm, 0.68 * rNom));
        const yFlat = rNom - flatDepth;
        if (bt === "d_shaft") {
          if (sinA > 1e-6) r = Math.min(rNom, yFlat / sinA);
        } else {
          if (Math.abs(sinA) > 1e-6) r = Math.min(rNom, yFlat / Math.abs(sinA));
        }
        xs[i] = r * cosA;
        ys[i] = r * sinA;
      } else if (bt === "hex") {
        const cos30 = Math.cos(Math.PI / 6.0);
        const apothem = Math.min(rNom, maxR * cos30);
        const sec = Math.min(5, Math.floor(ang / (Math.PI / 3.0)));
        const midAng = (sec + 0.5) * (Math.PI / 3.0);
        r = Math.min(maxR, apothem / Math.cos(ang - midAng));
        xs[i] = r * cosA;
        ys[i] = r * sinA;
      } else if (bt === "keyway") {
        const rCirc = Math.min(rNom, 0.90 * maxR);
        const halfW = Math.max(0.15 * rCirc, Math.min(0.5 * boreCfg.keyway_width_mm, 0.62 * rCirc));
        const yCirc = Math.sqrt(Math.max(1e-6, rCirc * rCirc - halfW * halfW));
        const yTop = Math.min(
          Math.sqrt(Math.max(yCirc * yCirc + 1e-5, maxR * maxR - halfW * halfW)),
          rCirc + Math.max(0.15, boreCfg.keyway_depth_mm)
        );
        const t1 = Math.atan2(yCirc, halfW);
        const t2 = Math.atan2(yTop, halfW);
        const t3 = Math.PI - t2;
        const t4 = Math.PI - t1;
        if (ang >= t1 && ang <= t2) {
          xs[i] = halfW;
          ys[i] = Math.min(yTop, Math.max(yCirc, halfW * Math.tan(ang)));
        } else if (ang > t2 && ang < t3) {
          ys[i] = yTop;
          const tA = Math.tan(ang);
          xs[i] = Math.abs(tA) > 1e9 ? 0.0 : Math.max(-halfW, Math.min(halfW, yTop / tA));
        } else if (ang >= t3 && ang <= t4) {
          xs[i] = -halfW;
          ys[i] = Math.min(yTop, Math.max(yCirc, -halfW * Math.tan(ang)));
        } else {
          xs[i] = rCirc * cosA;
          ys[i] = rCirc * sinA;
        }
      } else {
        xs[i] = r * cosA;
        ys[i] = r * sinA;
      }
    }
    return { xs: xs, ys: ys, count: m, rNom: rNom };
  }

  // ==========================================================================
  // 3. Client-Side Engineering Diagnostics & Live 2D Collision / LOA Solver
  // ==========================================================================
  function computeClientAnalysis(p, geom, printer) {
    const betaRad = geom.beta_rad;
    const cosB = Math.cos(betaRad);
    const sinB = Math.sin(betaRad);
    const tanB = Math.tan(betaRad);

    const rb1 = geom.pinion.base_radius_mm;
    const rb2 = geom.gear.base_radius_mm;
    const ra1 = geom.pinion.tip_radius_mm;
    const ra2 = geom.gear.tip_radius_mm;
    const rf1 = geom.pinion.root_radius_mm;
    const rf2 = geom.gear.root_radius_mm;
    const r1 = geom.pinion.pitch_radius_mm;
    const r2 = geom.gear.pitch_radius_mm;
    const a = geom.center_distance_mm;
    const a0 = geom.nominal_center_distance_mm;
    const rw1 = geom.pinion.working_pitch_radius_mm;
    const rw2 = geom.gear.working_pitch_radius_mm;

    const cosAw = Math.max(-0.9999, Math.min(0.9999, (rb1 + rb2) / Math.max(a, 1e-5)));
    const alphaWRad = cosAw >= 0.99985 ? 0.0 : Math.acos(cosAw);
    const sinAw = Math.sin(alphaWRad);
    const tanAw = Math.tan(alphaWRad);

    // Active Line of Action bounds along s (P + s * u_loa)
    const sMinBase = -rw1 * sinAw;
    const sMaxBase = rw2 * sinAw;
    const sEntryTip = rw2 * sinAw - Math.sqrt(Math.max(0.0, ra2 * ra2 - rb2 * rb2));
    const sExitTip = Math.sqrt(Math.max(0.0, ra1 * ra1 - rb1 * rb1)) - rw1 * sinAw;
    const sStart = Math.max(sMinBase, sEntryTip);
    const sEnd = Math.min(sMaxBase, sExitTip);
    const loaLen = Math.max(0.0, sEnd - sStart);

    const pBt = Math.PI * geom.m_t * Math.cos(geom.alpha_t_deg * DEG2RAD);
    const epsAlpha = pBt > 1e-6 ? (loaLen / pBt) : 0.0;
    const effAxialWidth = p.gear_type === "herringbone" ? (0.5 * p.face_width_mm) : p.face_width_mm;
    const epsBeta = p.gear_type === "spur" ? 0.0 : ((effAxialWidth * sinB) / Math.max(1e-6, Math.PI * geom.m_n));
    const epsTotal = epsAlpha + epsBeta;

    // Effective operating backlash & clearances
    const zSum = geom.pinion.teeth + geom.gear.teeth;
    const pTw = TWO_PI * rw1 / geom.pinion.teeth;
    const sW1 = 2.0 * rw1 * Math.max(0.0, geom.pinion.base_half_angle_rad - involuteFn(alphaWRad));
    const sW2 = 2.0 * rw2 * Math.max(0.0, geom.gear.base_half_angle_rad - involuteFn(alphaWRad));
    const effBacklash = (pTw - sW1 - sW2) * cosB;

    const radClr1 = a - (ra2 + rf1);
    const radClr2 = a - (ra1 + rf2);
    const baseInterference = (sEntryTip < sMinBase - 0.03 * geom.m_n) || (sExitTip > sMaxBase + 0.03 * geom.m_n);
    const jammed = (a < geom.min_non_jam_center_distance_mm - 0.004) || (effBacklash < -0.008) || (radClr1 < -0.005) || (radClr2 < -0.005);
    const interference = jammed || baseInterference;
    const minClr = jammed ? 0.0 : Math.max(0.0, Math.min(0.5 * effBacklash, radClr1, radClr2));

    // Kinematics & 3D Forces
    const torque1 = p.input_torque_nm;
    const torque2 = torque1 * geom.ratio;
    const rpm1 = p.sim_rpm;
    const rpm2 = rpm1 / geom.ratio;
    const pitchVel = (TWO_PI * rw1 * rpm1) / 60.0;

    // F_t in Newtons: T1 [N*m] / (r1 [m]) = 1000 * T1 / r1_mm
    const fT = (1000.0 * torque1) / Math.max(1.0, rw1);
    const fR = fT * tanAw;
    const axialBalanced = p.gear_type !== "helical" || geom.beta_deg < 0.1;
    const fA = axialBalanced ? 0.0 : (fT * tanB);

    // Printability
    const ovhDeg = geom.beta_deg;
    const supportsNeeded = ovhDeg > 47.0;
    const sepFootprintX = 2.0 * ra1 + 2.0 * ra2 + 10.0;
    const sepFootprintY = 2.0 * Math.max(ra1, ra2);
    const bedX = Number(printer.bed_x) || 220.0;
    const bedY = Number(printer.bed_y) || 220.0;
    const fitsBed = sepFootprintX <= bedX && sepFootprintY <= bedY;

    const vol1Cm3 = (Math.PI * r1 * r1 * p.face_width_mm) / 1000.0;
    const vol2Cm3 = (Math.PI * r2 * r2 * p.face_width_mm) / 1000.0;
    const totVolCm3 = 0.85 * (vol1Cm3 + vol2Cm3);
    const estWeightG = totVolCm3 * 1.24 * 0.62;
    const estTimeMin = Math.max(8, Math.round(estWeightG * 1.25));
    const lw = Number(printer.line_width_mm) || 0.42;
    const recWalls = Math.max(4, Math.min(6, Math.round((1.8 * geom.m_n) / (2.0 * lw))));

    const issues = [];
    if (jammed) {
      issues.push({
        severity: "critical",
        pt: "TRAVAMENTO MECÂNICO: Distância entre centros Δa muito negativa ou adendo excessivo — dentes colidem!",
        en: "MECHANICAL JAMMING: Center distance Δa too negative or excessive addendum — teeth collide!"
      });
    } else if (interference) {
      issues.push({
        severity: "warn",
        pt: "Interferência de base detectada: ative Auto Correção Anti-Undercut (x) ou aumente o número de dentes.",
        en: "Base-circle interference detected: enable Auto Anti-Undercut Shift (x) or increase tooth count."
      });
    }
    if (geom.pinion.undercut || geom.gear.undercut) {
      issues.push({
        severity: "warn",
        pt: "Adelgaçamento na raiz (Undercut): habilite Auto Correção (x) para reforçar o pé do dente.",
        en: "Root undercut detected: enable Auto Profile Shift (x) to strengthen tooth root."
      });
    }
    if (epsAlpha < 1.15) {
      issues.push({
        severity: "warn",
        pt: "Razão de contato transversal baixa (" + epsAlpha.toFixed(2) + "): aproxime Δa ou aumente o adendo.",
        en: "Low transverse contact ratio (" + epsAlpha.toFixed(2) + "): reduce Δa or increase addendum."
      });
    }
    if (!axialBalanced && fA > 15.0) {
      issues.push({
        severity: "warn",
        pt: "Empuxo axial relevante (" + fA.toFixed(1) + " N): use rolamento axial ou mude para Espinha de Peixe.",
        en: "Significant axial thrust (" + fA.toFixed(1) + " N): use thrust bearing or switch to Herringbone."
      });
    }
    if (supportsNeeded) {
      issues.push({
        severity: "warn",
        pt: "Hélice acima de 47° (" + ovhDeg.toFixed(0) + "°): pode exigir suportes ou camadas finas em FDM.",
        en: "Helix above 47° (" + ovhDeg.toFixed(0) + "°): may require supports or thin layer height in FDM."
      });
    }
    if (!fitsBed) {
      issues.push({
        severity: "critical",
        pt: "Par separado excede a mesa (" + Math.round(bedX) + "×" + Math.round(bedY) + " mm): exporte G1 e G2 individualmente.",
        en: "Separated pair exceeds build plate (" + Math.round(bedX) + "×" + Math.round(bedY) + " mm): export G1/G2 individually."
      });
    }
    if (issues.length === 0) {
      issues.push({
        severity: "ok",
        pt: "Engrenamento livre de interferência com folga saudável para impressão FDM.",
        en: "Interference-free conjugate meshing with healthy FDM printing clearance."
      });
    }

    const status = (jammed || !fitsBed) ? "critical" : (issues.some(function (x) { return x.severity === "warn"; }) ? "warn" : "ok");

    return {
      status: status,
      loa: { alphaWRad: alphaWRad, sStart: sStart, sEnd: sEnd, sMinBase: sMinBase, sMaxBase: sMaxBase, pBt: pBt },
      contact: {
        transverse_ratio: epsAlpha,
        axial_overlap_ratio: epsBeta,
        total_contact_ratio: epsTotal,
        line_of_action_length_mm: loaLen
      },
      fit: {
        effective_backlash_mm: effBacklash,
        radial_clearance_g1_mm: radClr1,
        radial_clearance_g2_mm: radClr2,
        min_tooth_clearance_mm: minClr,
        interference_detected: interference,
        jammed: jammed,
        undercut_g1: geom.pinion.undercut,
        undercut_g2: geom.gear.undercut,
        thin_tip_g1: geom.pinion.tip_thickness_mm < 0.25 * geom.m_n,
        thin_tip_g2: geom.gear.tip_thickness_mm < 0.25 * geom.m_n,
        center_distance_mm: a,
        nominal_center_distance_mm: a0,
        delta_a_mm: p.center_distance_offset_mm
      },
      kinematics: {
        ratio: geom.ratio,
        rpm_g1: rpm1,
        rpm_g2: rpm2,
        pitch_line_velocity_mm_s: pitchVel,
        torque_g1_nm: torque1,
        torque_g2_nm: torque2,
        tangential_force_n: fT,
        radial_force_n: fR,
        axial_force_n: fA,
        axial_thrust_balanced: axialBalanced
      },
      printability: {
        helix_overhang_deg: ovhDeg,
        supports_needed: supportsNeeded,
        fits_bed: fitsBed,
        bed_x_mm: bedX,
        bed_y_mm: bedY,
        pair_footprint_mm: [sepFootprintX, sepFootprintY],
        estimated_volume_cm3: totVolCm3,
        estimated_weight_g: estWeightG,
        estimated_print_time_min: estTimeMin,
        recommended_wall_loops: recWalls
      },
      issues: issues
    };
  }

  // Real-time 2D Meshing Window Collision & Clearance Check at exact current angle theta1
  function checkLive2DMeshCollision(c1, c2, theta1, theta2, a, mN, r1) {
    const cos1 = Math.cos(theta1), sin1 = Math.sin(theta1);
    const cos2 = Math.cos(theta2), sin2 = Math.sin(theta2);
    const xLo = r1 - 3.2 * mN;
    const xHi = r1 + 3.2 * mN;
    const yLim = 3.6 * mN;

    const segs1 = [];
    const n1 = c1.count;
    for (let i = 0; i < n1; i++) {
      const j = (i + 1) % n1;
      const x0 = c1.xs[i] * cos1 - c1.ys[i] * sin1;
      const y0 = c1.xs[i] * sin1 + c1.ys[i] * cos1;
      if (Math.abs(y0) > yLim * 1.4 || x0 < xLo - 2.0 * mN) continue;
      const x1p = c1.xs[j] * cos1 - c1.ys[j] * sin1;
      const y1p = c1.xs[j] * sin1 + c1.ys[j] * cos1;
      if (Math.max(x0, x1p) >= xLo && Math.min(x0, x1p) <= xHi && Math.min(Math.abs(y0), Math.abs(y1p)) <= yLim) {
        segs1.push(x0, y0, x1p, y1p);
      }
    }

    const segs2 = [];
    const n2 = c2.count;
    for (let i = 0; i < n2; i++) {
      const j = (i + 1) % n2;
      const x0 = c2.xs[i] * cos2 - c2.ys[i] * sin2 + a;
      const y0 = c2.xs[i] * sin2 + c2.ys[i] * cos2;
      if (Math.abs(y0) > yLim * 1.4 || x0 > xHi + 2.0 * mN) continue;
      const x1p = c2.xs[j] * cos2 - c2.ys[j] * sin2 + a;
      const y1p = c2.xs[j] * sin2 + c2.ys[j] * cos2;
      if (Math.max(x0, x1p) >= xLo && Math.min(x0, x1p) <= xHi && Math.min(Math.abs(y0), Math.abs(y1p)) <= yLim) {
        segs2.push(x0, y0, x1p, y1p);
      }
    }

    const hitPoints = [];
    let minDistSq = Infinity;
    const cSeg1 = segs1.length >> 2;
    const cSeg2 = segs2.length >> 2;

    for (let i = 0; i < cSeg1; i++) {
      const ax0 = segs1[4 * i], ay0 = segs1[4 * i + 1], ax1 = segs1[4 * i + 2], ay1 = segs1[4 * i + 3];
      const dpx = ax1 - ax0, dpy = ay1 - ay0;
      const lenA2 = Math.max(1e-12, dpx * dpx + dpy * dpy);

      for (let j = 0; j < cSeg2; j++) {
        const bx0 = segs2[4 * j], by0 = segs2[4 * j + 1], bx1 = segs2[4 * j + 2], by1 = segs2[4 * j + 3];
        const dqx = bx1 - bx0, dqy = by1 - by0;
        const denom = dpx * dqy - dpy * dqx;
        if (Math.abs(denom) > 1e-12) {
          const qpx = bx0 - ax0, qpy = by0 - ay0;
          const t = (qpx * dqy - qpy * dqx) / denom;
          const u = (qpx * dpy - qpy * dpx) / denom;
          if (t >= 0.0 && t <= 1.0 && u >= 0.0 && u <= 1.0) {
            minDistSq = 0.0;
            if (hitPoints.length < 24) {
              hitPoints.push([ax0 + t * dpx, ay0 + t * dpy]);
            }
            continue;
          }
        }
        // Point-to-segment distance check
        const lenB2 = Math.max(1e-12, dqx * dqx + dqy * dqy);
        const projB = Math.max(0.0, Math.min(1.0, ((ax0 - bx0) * dqx + (ay0 - by0) * dqy) / lenB2));
        const dxB = ax0 - (bx0 + projB * dqx);
        const dyB = ay0 - (by0 + projB * dqy);
        const d2B = dxB * dxB + dyB * dyB;
        if (d2B < minDistSq) minDistSq = d2B;

        const projA = Math.max(0.0, Math.min(1.0, ((bx0 - ax0) * dpx + (by0 - ay0) * dpy) / lenA2));
        const dxA = bx0 - (ax0 + projA * dpx);
        const dyA = by0 - (ay0 + projA * dpy);
        const d2A = dxA * dxA + dyA * dyA;
        if (d2A < minDistSq) minDistSq = d2A;
      }
    }

    return {
      collided: hitPoints.length > 0,
      minDistMm: Number.isFinite(minDistSq) ? Math.sqrt(minDistSq) : 0.0,
      hitPoints: hitPoints
    };
  }

  // ==========================================================================
  // 4. Translations (PT-BR & EN) & Slider Metadata
  // ==========================================================================
  const I18N = {
    pt: {
      btn_random: "Aleatório",
      tab_gears: "Engrenamento",
      tab_bodies: "Eixos & Cubos",
      tab_export: "Diagnóstico",
      tab_presets: "Presets",
      sec_presets: "Presets Mecânicos",
      btn_save_preset: "+ Salvar",
      btn_ok: "Salvar",
      cat_all: "Todos",
      cat_spur: "Retas/Ind",
      cat_helical: "Helicoidal",
      cat_herringbone: "Espinha V",
      cat_robotics: "Robótica/Fit",
      cat_user: "Meus",
      sec_transmission: "Transmissão & Hélice",
      gt_spur: "Reta (Spur)",
      gt_helical: "Helicoidal",
      gt_herringbone: "Espinha de Peixe",
      lbl_helix_quick: "Ângulo de Hélice Rápido",
      hand_right: "Mão Destra (G1 R / G2 L)",
      hand_left: "Mão Canhota (G1 L / G2 R)",
      btn_swap_teeth: "⇄ Inverter Pinhão / Coroa (Z1 ↔ Z2)",
      sec_tooth_height: "Altura do Dente (Fator × | mm)",
      tp_iso: "ISO Padrão 1.00×",
      tp_stub: "Stub Robusto 0.75×",
      tp_high: "Alto Contato 1.20×",
      lbl_auto_shift: "Auto Correção Anti-Undercut (x)",
      sec_bodies: "Furos, Cubos & Alívio",
      body_pinion: "⚙ Pinhão G1 (Motriz)",
      body_gear: "⚙ Coroa G2 (Movida)",
      lbl_bore_type: "Tipo de Furo / Eixo (G1)",
      lbl_bore_type_g2: "Tipo de Furo / Eixo (G2)",
      bore_none: "Sem Furo (Sólido)",
      bore_round: "Circular Liso",
      bore_d: "Eixo em D (NEMA / Motor)",
      bore_dd: "Duplo D",
      bore_hex: "Sextavado (Hex / Porca)",
      bore_keyway: "Rasgo de Chaveta DIN",
      lbl_hub: "Cubo Saliente Central (Hub)",
      lbl_recess: "Alojamento Rolamento / Rebaixo",
      side_top: "Topo (+Z)",
      side_bottom: "Base (Z=0)",
      side_both: "Ambos os Lados",
      lbl_lightening: "Alívio de Massa do Corpo",
      light_solid: "Corpo Maciço",
      light_web: "Alma Rebaixada (Web)",
      light_holes: "Furos Circulares de Alívio",
      vp_meshed: "⚙ Par Engrenado",
      vp_plater: "🖨 Mesa de Impressão",
      vp_fit_kit: "🧪 Kit de Teste Rápido",
      vp_heatmap: "🔥 Overhang",
      vp_forces: "⚡ Forças 3D",
      vp_wire: "⌗ Malha",
      hud_title: "Cargas & Malha",
      hud_cd: "Centros a (mm)",
      hud_ft: "Tangencial Ft",
      hud_fr: "Radial Fr",
      hud_fa: "Empuxo Axial Fa",
      cam_iso: "Perspectiva",
      cam_top: "Topo (Engrenamento)",
      cam_front: "Frontal (Hélice)",
      cam_reset: "Reset",
      sim_scrub: "Ângulo θ₁",
      sim_delta_a: "Afaste / Aproxime Eixos (Δa):",
      btn_reset_da: "Reset 0.00 mm",
      loupe_title: "🔍 Lupa 2D de Engrenamento & Linha de Pressão",
      jam_alert: "INTERFERÊNCIA / TRAVAMENTO DETECTADO",
      sec_tolerances: "Folgas FDM & Torque Motriz",
      sec_diagnostics: "Diagnóstico de Engrenamento",
      diag_sec_contact: "Razão de Contato & Envolvente",
      dk_eps_a: "Transversal ε_α",
      dk_eps_b: "Recobrimento Axial ε_β",
      dk_eps_g: "Contato Total ε_γ",
      dk_loa: "Linha de Ação",
      diag_sec_fit: "Encaixe, Folga & Cinemática",
      dk_cd: "Distância Centros a",
      dk_clr: "Folga Mín. Dentes",
      dk_t2: "Torque Saída (G2)",
      dk_rpm2: "Rotação Saída / Vel.",
      diag_sec_print: "Impressão Mecânica FDM",
      dk_ovh: "Overhang Hélice",
      dk_walls: "Paredes Sugeridas",
      dk_wgt: "Peso / Tempo Est.",
      dk_bed: "Área na Mesa",
      sec_export_pkg: "Pacote de Saída & Fatiamento",
      lbl_export_target: "O que enviar / exportar:",
      exp_pair: "Par Separado (Pronto p/ Imprimir)",
      exp_pinion: "Apenas Pinhão (G1)",
      exp_gear: "Apenas Coroa (G2)",
      exp_kit: "Kit de Teste Rápido (Setores + Base 2 Pinos + Régua Eixo)",
      exp_full: "Conjunto Completo (Par + Gabaritos)",
      note_exp_pair: "Posiciona Pinhão (G1) e Coroa (G2) separados com margem segura na mesa, prontos para fatiar sem fusão de dentes.",
      note_exp_single: "Exporta individualmente a engrenagem selecionada centralizada na mesa de impressão.",
      note_exp_kit: "Imprime em ~10 min: 2 setores dentados + base gabarito na distância entre centros exata (a) + régua de calibração de eixo!",
      note_exp_full: "Pacote completo na mesa: Par de Engrenagens (G1 + G2) acompanhado da base de teste e régua de furo.",
      lbl_auto_slicer: "Auto-Ajustar Fatiamento Mecânico (4–6 paredes maciças + Gyroid)",
      btn_send_plater: "Enviar para a Mesa do OrcaSlicer",
      btn_exp_3mf: "Exportar .3MF",
      btn_exp_stl: "Exportar .STL",
      status_ok: "ÓTIMO",
      status_warn: "ATENÇÃO",
      status_crit: "CRÍTICO",
      thrust_zero_spur: "Empuxo Axial: 0.0 N (Dentes Retos)",
      thrust_zero_hb: "Empuxo Axial: 0.0 N (Auto-Balanceado V)",
      thrust_helical_fmt: "Empuxo Axial Z: {fa} N (Hélice {b}°)",
      toast_randomized: "Novo par de engrenagens gerado!",
      toast_preset_saved: "Preset mecânico salvo com sucesso!"
    },
    en: {
      btn_random: "Randomize",
      tab_gears: "Meshing",
      tab_bodies: "Shafts & Hubs",
      tab_export: "Diagnostics",
      tab_presets: "Presets",
      sec_presets: "Mechanical Presets",
      btn_save_preset: "+ Save",
      btn_ok: "Save",
      cat_all: "All",
      cat_spur: "Spur/Ind",
      cat_helical: "Helical",
      cat_herringbone: "Herringbone",
      cat_robotics: "Robotics/Fit",
      cat_user: "Saved",
      sec_transmission: "Transmission & Helix",
      gt_spur: "Spur",
      gt_helical: "Helical",
      gt_herringbone: "Herringbone (V)",
      lbl_helix_quick: "Quick Helix Angle",
      hand_right: "Right-Hand (G1 R / G2 L)",
      hand_left: "Left-Hand (G1 L / G2 R)",
      btn_swap_teeth: "⇄ Swap Pinion / Gear (Z1 ↔ Z2)",
      sec_tooth_height: "Tooth Height (Factor × | mm)",
      tp_iso: "ISO Standard 1.00×",
      tp_stub: "Heavy Stub 0.75×",
      tp_high: "High Contact 1.20×",
      lbl_auto_shift: "Auto Anti-Undercut Shift (x)",
      sec_bodies: "Bores, Hubs & Lightening",
      body_pinion: "⚙ Pinion G1 (Driver)",
      body_gear: "⚙ Gear G2 (Driven)",
      lbl_bore_type: "Shaft / Bore Type (G1)",
      lbl_bore_type_g2: "Shaft / Bore Type (G2)",
      bore_none: "No Bore (Solid)",
      bore_round: "Round Shaft",
      bore_d: "D-Shaft (NEMA / Motor)",
      bore_dd: "Double-D Shaft",
      bore_hex: "Hex Bore (Across-Flats)",
      bore_keyway: "DIN Keyway Bore",
      lbl_hub: "Raised Central Hub",
      lbl_recess: "Bearing / Bolt Recess",
      side_top: "Top (+Z)",
      side_bottom: "Bottom (Z=0)",
      side_both: "Both Sides",
      lbl_lightening: "Body Mass Lightening",
      light_solid: "Solid Gear Body",
      light_web: "Recessed Web Pocket",
      light_holes: "Circular Lightening Holes",
      vp_meshed: "⚙ Meshed Pair",
      vp_plater: "🖨 Build Plate",
      vp_fit_kit: "🧪 Quick Fit-Test Kit",
      vp_heatmap: "🔥 Overhang",
      vp_forces: "⚡ 3D Forces",
      vp_wire: "⌗ Wire",
      hud_title: "Loads & Mesh",
      hud_cd: "Center Dist a",
      hud_ft: "Tangential Ft",
      hud_fr: "Radial Fr",
      hud_fa: "Axial Thrust Fa",
      cam_iso: "Perspective",
      cam_top: "Top (Meshing)",
      cam_front: "Front (Helix)",
      cam_reset: "Reset",
      sim_scrub: "Angle θ₁",
      sim_delta_a: "Center-Distance Offset (Δa):",
      btn_reset_da: "Reset 0.00 mm",
      loupe_title: "🔍 2D Tooth-Mesh Loupe & Pressure Line",
      jam_alert: "INTERFERENCE / JAMMING DETECTED",
      sec_tolerances: "FDM Clearances & Input Torque",
      sec_diagnostics: "Meshing & Fit Diagnostics",
      diag_sec_contact: "Contact Ratio & Involute",
      dk_eps_a: "Transverse ε_α",
      dk_eps_b: "Axial Overlap ε_β",
      dk_eps_g: "Total Contact ε_γ",
      dk_loa: "Line of Action",
      diag_sec_fit: "Fit, Clearance & Kinematics",
      dk_cd: "Center Distance a",
      dk_clr: "Min Tooth Clearance",
      dk_t2: "Output Torque (G2)",
      dk_rpm2: "Output Speed",
      diag_sec_print: "Mechanical FDM Printability",
      dk_ovh: "Helix Overhang",
      dk_walls: "Suggested Walls",
      dk_wgt: "Est. Weight / Time",
      dk_bed: "Bed Footprint",
      sec_export_pkg: "Export Package & Slicing",
      lbl_export_target: "Target package:",
      exp_pair: "Separated Pair (Ready to Print)",
      exp_pinion: "Pinion Only (G1)",
      exp_gear: "Driven Gear Only (G2)",
      exp_kit: "Quick Fit-Test Kit (Sectors + 2-Pin Jig + Shaft Gauge)",
      exp_full: "Full Suite (Gear Pair + Calibration Jigs)",
      note_exp_pair: "Places Pinion (G1) and Gear (G2) separated with safe gap on the build plate so teeth never fuse.",
      note_exp_single: "Exports only the selected gear centered on the printer build plate.",
      note_exp_kit: "10-minute calibration print: two 5-tooth sectors + 2-pin center-distance base jig + 4-hole shaft gauge!",
      note_exp_full: "Complete build plate suite: full G1 + G2 gear pair alongside center-distance jig and shaft gauge.",
      lbl_auto_slicer: "Auto-Configure Mechanical Slicing (4–6 solid walls + Gyroid)",
      btn_send_plater: "Send to OrcaSlicer Plater",
      btn_exp_3mf: "Export .3MF",
      btn_exp_stl: "Export .STL",
      status_ok: "OPTIMAL",
      status_warn: "WARNING",
      status_crit: "CRITICAL",
      thrust_zero_spur: "Axial Thrust: 0.0 N (Spur)",
      thrust_zero_hb: "Axial Thrust: 0.0 N (Balanced V)",
      thrust_helical_fmt: "Axial Thrust Z: {fa} N ({b}° Helix)",
      toast_randomized: "Generated printable gear pair!",
      toast_preset_saved: "Mechanical preset saved!"
    }
  };

  const SLIDER_SPECS = [
    { path: "helix_angle_deg", min: 0, max: 60, step: 1, unit: "°", pt: "Ângulo de Hélice (β)", en: "Helix Angle (β)" },
    { path: "pinion.teeth", min: 6, max: 160, step: 1, unit: "Z₁", pt: "Dentes do Pinhão (G1)", en: "Pinion Teeth (G1)" },
    { path: "gear.teeth", min: 6, max: 200, step: 1, unit: "Z₂", pt: "Dentes da Coroa (G2)", en: "Driven Gear Teeth (G2)" },
    { path: "module_mm", min: 0.5, max: 10.0, step: 0.05, unit: "mm", pt: "Módulo Normal (m_n)", en: "Normal Module (m_n)" },
    { path: "pressure_angle_deg", min: 14.5, max: 30.0, step: 0.5, unit: "°", pt: "Ângulo de Pressão (α_n)", en: "Pressure Angle (α_n)" },
    { path: "face_width_mm", min: 2.0, max: 120.0, step: 0.5, unit: "mm", pt: "Largura de Face (b)", en: "Face Width (b)" },

    { path: "addendum_coeff", min: 0.40, max: 1.40, step: 0.02, unit: "×", dualMm: true, pt: "Fator de Adendo (h_a*)", en: "Addendum Coeff (h_a*)" },
    { path: "clearance_coeff", min: 0.10, max: 0.50, step: 0.02, unit: "×", dualMm: true, pt: "Folga de Fundo (c*)", en: "Root Clearance Coeff (c*)" },
    { path: "root_fillet_coeff", min: 0.05, max: 0.45, step: 0.02, unit: "×", dualMm: true, pt: "Raio de Filete Raiz (ρ_f*)", en: "Root Fillet Coeff (ρ_f*)" },
    { path: "tip_chamfer_coeff", min: 0.00, max: 0.25, step: 0.01, unit: "×", dualMm: true, pt: "Quebra de Quina Topo (c_k*)", en: "Tip Chamfer Coeff (c_k*)" },

    { path: "profile_shift_g1", min: -0.50, max: 0.80, step: 0.02, unit: "x₁", pt: "Deslocamento Perfil G1 (x₁)", en: "Profile Shift G1 (x₁)" },
    { path: "profile_shift_g2", min: -0.50, max: 0.80, step: 0.02, unit: "x₂", pt: "Deslocamento Perfil G2 (x₂)", en: "Profile Shift G2 (x₂)" },

    { path: "backlash_mm", min: 0.00, max: 1.00, step: 0.01, unit: "mm", pt: "Backlash / Folga Lateral", en: "Circumferential Backlash" },
    { path: "xy_compensation_mm", min: -0.20, max: 0.30, step: 0.01, unit: "mm", pt: "Compensação Expansão XY", en: "FDM XY Compensation" },
    { path: "elephant_foot_chamfer_mm", min: 0.00, max: 1.50, step: 0.05, unit: "mm", pt: "Chanfro Anti-Pé-de-Elefante", en: "Anti-Elephant-Foot Chamfer" },
    { path: "center_distance_offset_mm", min: -1.50, max: 3.00, step: 0.01, unit: "mm", pt: "Offset Distância Centros (Δa)", en: "Center-Distance Offset (Δa)" },
    { path: "input_torque_nm", min: 0.05, max: 50.0, step: 0.05, unit: "N·m", pt: "Torque no Pinhão (T₁)", en: "Input Torque on G1 (T₁)" },

    { path: "pinion.bore_diameter_mm", min: 1.5, max: 80.0, step: 0.1, unit: "mm", pt: "Diâmetro Nominal Eixo", en: "Nominal Shaft Diameter" },
    { path: "pinion.bore_clearance_mm", min: -0.20, max: 0.80, step: 0.01, unit: "mm", pt: "Folga Diametral Furo", en: "Diametral Bore Clearance" },
    { path: "pinion.d_flat_depth_mm", min: 0.10, max: 8.0, step: 0.05, unit: "mm", pt: "Rebaixo do Chanfro D", en: "D-Flat Depth" },
    { path: "pinion.keyway_width_mm", min: 0.8, max: 20.0, step: 0.1, unit: "mm", pt: "Largura da Chaveta", en: "Keyway Width" },
    { path: "pinion.keyway_depth_mm", min: 0.4, max: 12.0, step: 0.1, unit: "mm", pt: "Profundidade da Chaveta", en: "Keyway Depth" },
    { path: "pinion.hub_diameter_mm", min: 4.0, max: 140.0, step: 0.5, unit: "mm", pt: "Diâmetro do Cubo (G1)", en: "Hub Diameter (G1)" },
    { path: "pinion.hub_height_mm", min: 0.5, max: 50.0, step: 0.5, unit: "mm", pt: "Altura do Cubo (G1)", en: "Hub Height (G1)" },
    { path: "pinion.recess_diameter_mm", min: 4.0, max: 140.0, step: 0.2, unit: "mm", pt: "Diâmetro do Rebaixo (G1)", en: "Recess Diameter (G1)" },
    { path: "pinion.recess_depth_mm", min: 0.5, max: 40.0, step: 0.2, unit: "mm", pt: "Profundidade Rebaixo (G1)", en: "Recess Depth (G1)" },
    { path: "pinion.web_thickness_mm", min: 1.2, max: 40.0, step: 0.2, unit: "mm", pt: "Espessura da Alma (G1)", en: "Web Thickness (G1)" },
    { path: "pinion.lightening_hole_count", min: 3, max: 16, step: 1, unit: "un", pt: "Nº Furos de Alívio (G1)", en: "Lightening Hole Count (G1)" },
    { path: "pinion.lightening_hole_diameter_mm", min: 2.0, max: 60.0, step: 0.5, unit: "mm", pt: "Diâmetro Furos Alívio (G1)", en: "Lightening Hole Ø (G1)" },

    { path: "gear.bore_diameter_mm", min: 1.5, max: 80.0, step: 0.1, unit: "mm", pt: "Diâmetro Nominal Eixo", en: "Nominal Shaft Diameter" },
    { path: "gear.bore_clearance_mm", min: -0.20, max: 0.80, step: 0.01, unit: "mm", pt: "Folga Diametral Furo", en: "Diametral Bore Clearance" },
    { path: "gear.d_flat_depth_mm", min: 0.10, max: 8.0, step: 0.05, unit: "mm", pt: "Rebaixo do Chanfro D", en: "D-Flat Depth" },
    { path: "gear.keyway_width_mm", min: 0.8, max: 20.0, step: 0.1, unit: "mm", pt: "Largura da Chaveta", en: "Keyway Width" },
    { path: "gear.keyway_depth_mm", min: 0.4, max: 12.0, step: 0.1, unit: "mm", pt: "Profundidade da Chaveta", en: "Keyway Depth" },
    { path: "gear.hub_diameter_mm", min: 4.0, max: 160.0, step: 0.5, unit: "mm", pt: "Diâmetro do Cubo (G2)", en: "Hub Diameter (G2)" },
    { path: "gear.hub_height_mm", min: 0.5, max: 50.0, step: 0.5, unit: "mm", pt: "Altura do Cubo (G2)", en: "Hub Height (G2)" },
    { path: "gear.recess_diameter_mm", min: 4.0, max: 160.0, step: 0.2, unit: "mm", pt: "Diâmetro do Rebaixo (G2)", en: "Recess Diameter (G2)" },
    { path: "gear.recess_depth_mm", min: 0.5, max: 40.0, step: 0.2, unit: "mm", pt: "Profundidade Rebaixo (G2)", en: "Recess Depth (G2)" },
    { path: "gear.web_thickness_mm", min: 1.2, max: 40.0, step: 0.2, unit: "mm", pt: "Espessura da Alma (G2)", en: "Web Thickness (G2)" },
    { path: "gear.lightening_hole_count", min: 3, max: 16, step: 1, unit: "un", pt: "Nº Furos de Alívio (G2)", en: "Lightening Hole Count (G2)" },
    { path: "gear.lightening_hole_diameter_mm", min: 2.0, max: 80.0, step: 0.5, unit: "mm", pt: "Diâmetro Furos Alívio (G2)", en: "Lightening Hole Ø (G2)" }
  ];

  // ==========================================================================
  // 5. Application State, Simulation State & Undo/Redo Stack
  // ==========================================================================
  const initCtx = (BOOT_PAYLOAD && BOOT_PAYLOAD.initial_context) ? BOOT_PAYLOAD.initial_context : {};
  const state = {
    mode: BOOT_PAYLOAD.mode === "dock" ? "dock" : "page",
    lang: initCtx.lang === "en" ? "en" : "pt",
    theme: initCtx.theme === "light" ? "light" : "dark",
    printer: Object.assign(
      {
        name: "Generic FDM 220×220",
        bed_x: 220.0,
        bed_y: 220.0,
        max_z: 250.0,
        nozzle_mm: 0.4,
        layer_height_mm: 0.2,
        line_width_mm: 0.42
      },
      initCtx.printer || {}
    ),
    builtinPresets: Array.isArray(initCtx.builtin_presets) && initCtx.builtin_presets.length
      ? initCtx.builtin_presets
      : (Array.isArray(BOOT_PAYLOAD.fallback_presets) ? BOOT_PAYLOAD.fallback_presets : []),
    userPresets: Array.isArray(initCtx.user_presets) ? initCtx.user_presets : [],
    presetFilter: "all",
    activePresetId: "spur_classic_1_2",
    activeBodyTab: "pinion", // "pinion" | "gear"
    vpView: "meshed",        // "meshed" | "plater" | "fit_kit"
    heatmap: false,
    showForces: true,
    wireframe: false,
    crossCutPct: 0,
    crossCutAxis: "z",       // "z" | "y"
    loupeZoom: 1.7,
    loupeCollapsed: false,
    simPlaying: true,
    theta1Rad: 0.0,
    lastFrameMs: 0.0,
    isInteracting: false,
    busyAction: false,
    params: normalizeParams(initCtx.params || BOOT_PAYLOAD.fallback_params || JS_DEFAULT_PARAMS),
    geom: null,
    contourG1: null,
    contourG2: null,
    clientReport: null,
    hostReport: null,
    liveCollision: { collided: false, minDistMm: 0.15, hitPoints: [] },
    undoStack: [],
    redoStack: []
  };

  function tr(key) {
    const dict = I18N[state.lang] || I18N.pt;
    return dict[key] !== undefined ? dict[key] : key;
  }

  function getByPath(obj, path) {
    const parts = path.split(".");
    let cur = obj;
    for (let i = 0; i < parts.length; i++) {
      if (cur == null) return undefined;
      cur = cur[parts[i]];
    }
    return cur;
  }

  function setByPath(obj, path, val) {
    const parts = path.split(".");
    let cur = obj;
    for (let i = 0; i < parts.length - 1; i++) {
      if (cur[parts[i]] == null || typeof cur[parts[i]] !== "object") cur[parts[i]] = {};
      cur = cur[parts[i]];
    }
    cur[parts[parts.length - 1]] = val;
  }

  let dragSnapshot = null;
  function beginUndoGesture() {
    if (!dragSnapshot) dragSnapshot = deepClone(state.params);
  }

  function commitUndoGesture() {
    if (!dragSnapshot) return;
    if (JSON.stringify(dragSnapshot) !== JSON.stringify(state.params)) {
      state.undoStack.push(dragSnapshot);
      if (state.undoStack.length > 50) state.undoStack.shift();
      state.redoStack.length = 0;
      updateUndoButtons();
    }
    dragSnapshot = null;
  }

  function pushUndoSnapshot(beforeParams) {
    state.undoStack.push(deepClone(beforeParams));
    if (state.undoStack.length > 50) state.undoStack.shift();
    state.redoStack.length = 0;
    updateUndoButtons();
  }

  function performUndo() {
    if (!state.undoStack.length) return;
    state.redoStack.push(deepClone(state.params));
    state.params = normalizeParams(state.undoStack.pop());
    state.hostReport = null;
    updateUndoButtons();
    syncControlsFromState();
    rebuildScene(false);
    scheduleHostAnalyze();
  }

  function performRedo() {
    if (!state.redoStack.length) return;
    state.undoStack.push(deepClone(state.params));
    state.params = normalizeParams(state.redoStack.pop());
    state.hostReport = null;
    updateUndoButtons();
    syncControlsFromState();
    rebuildScene(false);
    scheduleHostAnalyze();
  }

  // ==========================================================================
  // 6. OrcaSlicer WebView2 IPC Bridge (`window.orca` / `window.chrome.webview` / `postMessage`)
  // ==========================================================================
  let bridgeReadySent = false;
  let analyzeTimer = null;

  function hasOrcaBridge() {
    if (typeof window === "undefined") return false;
    if (window.orca && typeof window.orca.postMessage === "function") return true;
    if (window.chrome && window.chrome.webview && typeof window.chrome.webview.postMessage === "function") return true;
    return false;
  }

  function sendToHost(payload) {
    if (typeof window === "undefined") return false;
    try {
      if (window.orca && typeof window.orca.postMessage === "function") {
        window.orca.postMessage(payload);
        return true;
      }
      if (window.chrome && window.chrome.webview && typeof window.chrome.webview.postMessage === "function") {
        window.chrome.webview.postMessage(payload);
        return true;
      }
    } catch (err) {
      console.error("Orca WebView2 bridge postMessage error:", err);
    }
    return false;
  }

  function scheduleHostAnalyze() {
    if (analyzeTimer) clearTimeout(analyzeTimer);
    analyzeTimer = setTimeout(function () {
      sendToHost({
        type: "analyze",
        params: deepClone(state.params)
      });
    }, 180);
  }

  function detectHostInjectedTheme() {
    if (typeof window === "undefined" || typeof document === "undefined" || !window.getComputedStyle) return null;
    try {
      const rawBg = String(window.getComputedStyle(document.documentElement).getPropertyValue("--orca-bg") || "").trim();
      if (!rawBg) return null;
      let r = -1, g = -1, b = -1;
      if (rawBg.charAt(0) === "#") {
        const hex = rawBg.slice(1).trim();
        if (hex.length === 3) {
          r = parseInt(hex[0] + hex[0], 16);
          g = parseInt(hex[1] + hex[1], 16);
          b = parseInt(hex[2] + hex[2], 16);
        } else if (hex.length >= 6) {
          r = parseInt(hex.slice(0, 2), 16);
          g = parseInt(hex.slice(2, 4), 16);
          b = parseInt(hex.slice(4, 6), 16);
        }
      } else {
        const m = rawBg.match(/rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/i);
        if (m) {
          r = parseInt(m[1], 10);
          g = parseInt(m[2], 10);
          b = parseInt(m[3], 10);
        }
      }
      if (r >= 0 && g >= 0 && b >= 0 && !isNaN(r) && !isNaN(g) && !isNaN(b)) {
        const lum = 0.2126 * r + 0.7152 * g + 0.0722 * b;
        return lum > 135 ? "light" : "dark";
      }
    } catch (_) {}
    return null;
  }

  function handleHostMessage(rawData) {
    let msg = rawData;
    if (typeof rawData === "string") {
      try {
        msg = JSON.parse(rawData);
      } catch (_) {
        return;
      }
    }
    if (!msg || typeof msg !== "object" || typeof msg.type !== "string") return;

    if (msg.type === "init_state") {
      if (msg.lang === "en" || msg.lang === "pt") state.lang = msg.lang;
      const injectedTheme = detectHostInjectedTheme();
      if (injectedTheme && !msg.theme_explicit) {
        state.theme = injectedTheme;
      } else if (msg.theme === "light" || msg.theme === "dark") {
        state.theme = msg.theme;
      }
      if (msg.printer && typeof msg.printer === "object") {
        state.printer = Object.assign(state.printer, msg.printer);
      }
      if (Array.isArray(msg.builtin_presets) && msg.builtin_presets.length) {
        state.builtinPresets = msg.builtin_presets;
      }
      if (Array.isArray(msg.user_presets)) {
        state.userPresets = msg.user_presets;
      }
      if (msg.params && typeof msg.params === "object") {
        state.params = normalizeParams(msg.params);
      }
      applyThemeAndLanguage();
      renderPresetsGrid();
      syncControlsFromState();
      rebuildBedGeometry();
      rebuildScene(false);
      fitCameraToScene();
      return;
    }

    if (msg.type === "analysis_result" && msg.report) {
      state.hostReport = msg.report;
      updateDiagnosticsUI();
      return;
    }

    if (msg.type === "params_updated" && msg.params) {
      pushUndoSnapshot(state.params);
      state.params = normalizeParams(msg.params);
      state.hostReport = null;
      syncControlsFromState();
      rebuildScene(false);
      scheduleHostAnalyze();
      showToast(tr("toast_randomized"), false);
      return;
    }

    if (msg.type === "presets_updated" && Array.isArray(msg.user_presets)) {
      state.userPresets = msg.user_presets;
      renderPresetsGrid();
      return;
    }

    if (msg.type === "action_result") {
      setActionButtonsBusy(false);
      if (msg.report) {
        state.hostReport = msg.report;
        updateDiagnosticsUI();
      }
      if (msg.message) {
        showToast(msg.message, !msg.ok);
      }
      return;
    }
  }

  function connectOrcaBridge() {
    if (typeof window === "undefined") return;
    window.addEventListener("message", function (ev) {
      if (ev && ev.data) handleHostMessage(ev.data);
    });
    if (window.chrome && window.chrome.webview && typeof window.chrome.webview.addEventListener === "function") {
      window.chrome.webview.addEventListener("message", function (ev) {
        if (ev && ev.data) handleHostMessage(ev.data);
      });
    }
    const tryBind = function () {
      if (bridgeReadySent) return;
      if (window.orca && typeof window.orca.onMessage === "function") {
        bridgeReadySent = true;
        window.orca.onMessage(handleHostMessage);
        sendToHost({ type: "ready", mode: state.mode });
      } else if (window.chrome && window.chrome.webview && typeof window.chrome.webview.postMessage === "function") {
        bridgeReadySent = true;
        sendToHost({ type: "ready", mode: state.mode });
      }
    };
    tryBind();
    if (!bridgeReadySent) {
      setTimeout(tryBind, 80);
      setTimeout(tryBind, 300);
    }
  }

  // ==========================================================================
  // 7. 3D Mesh Builders (Pinion, Gear, Bores, Hubs, Recesses, Lightening & Fit Kit)
  // ==========================================================================
  function createCollector() {
    return {
      pos: [],
      nrm: [],
      ovh: [],
      idx: [],
      wire: [],
      vCount: 0,
      addV: function (x, y, z, nx, ny, nz, ovhDeg) {
        const id = this.vCount++;
        this.pos.push(x, y, z);
        this.nrm.push(nx, ny, nz);
        this.ovh.push(ovhDeg);
        return id;
      },
      addTri: function (a, b, c) {
        this.idx.push(a, b, c);
      },
      addWire: function (x1, y1, z1, x2, y2, z2) {
        this.wire.push(x1, y1, z1, x2, y2, z2);
      }
    };
  }

  function raySectorDistance(hx, hy, dirX, dirY, halfAngle, outerRadius) {
    const b = 2.0 * (hx * dirX + hy * dirY);
    const c = hx * hx + hy * hy - outerRadius * outerRadius;
    const disc = Math.max(0.0, b * b - 4.0 * c);
    let bestT = 0.5 * (-b + Math.sqrt(disc));
    if (halfAngle < Math.PI - 1e-4) {
      const angles = [halfAngle, -halfAngle];
      for (let k = 0; k < 2; k++) {
        const rx = Math.cos(angles[k]);
        const ry = Math.sin(angles[k]);
        const det = dirX * ry - dirY * rx;
        if (Math.abs(det) > 1e-8) {
          const tRay = (ry * (-hx) - rx * (-hy)) / det;
          const sRay = (dirX * (-hy) - dirY * (-hx)) / det;
          if (tRay > 1e-5 && sRay >= -1e-5 && tRay < bestT) bestT = tRay;
        }
      }
    }
    return Math.max(bestT, 0.1);
  }

  function appendAnnulusCap(col, rInPtsX, rInPtsY, rOut, zVal, facingUp) {
    const n = rInPtsX.length;
    const nz = facingUp ? 1.0 : -1.0;
    const inIds = new Int32Array(n);
    const outIds = new Int32Array(n);
    for (let i = 0; i < n; i++) {
      const ang = (TWO_PI * i) / n;
      inIds[i] = col.addV(rInPtsX[i], rInPtsY[i], zVal, 0, 0, nz, 0.0);
      outIds[i] = col.addV(rOut * Math.cos(ang), rOut * Math.sin(ang), zVal, 0, 0, nz, 0.0);
    }
    for (let i = 0; i < n; i++) {
      const j = (i + 1) % n;
      if (facingUp) {
        col.addTri(inIds[i], outIds[i], outIds[j]);
        col.addTri(inIds[i], outIds[j], inIds[j]);
      } else {
        col.addTri(inIds[i], outIds[j], outIds[i]);
        col.addTri(inIds[i], inIds[j], outIds[j]);
      }
    }
  }

  function appendCircleStepWall(col, radius, z0, z1, segs, outward) {
    if (Math.abs(z1 - z0) < 1e-4) return;
    const r0 = new Int32Array(segs);
    const r1 = new Int32Array(segs);
    const sgn = outward ? 1.0 : -1.0;
    for (let i = 0; i < segs; i++) {
      const a = (TWO_PI * i) / segs;
      const c = Math.cos(a), s = Math.sin(a);
      r0[i] = col.addV(radius * c, radius * s, z0, sgn * c, sgn * s, 0, 0);
      r1[i] = col.addV(radius * c, radius * s, z1, sgn * c, sgn * s, 0, 0);
    }
    const zUp = z1 > z0;
    const flip = outward ? zUp : !zUp;
    for (let i = 0; i < segs; i++) {
      const j = (i + 1) % segs;
      if (flip) {
        col.addTri(r0[i], r0[j], r1[j]);
        col.addTri(r0[i], r1[j], r1[i]);
      } else {
        col.addTri(r0[i], r1[j], r0[j]);
        col.addTri(r0[i], r1[i], r1[j]);
      }
    }
  }

  function appendPerforatedWebAnnulus(col, rIn, rOut, zBot, zTop, holeCount, holeDiam) {
    const nHoles = Math.max(3, Math.min(18, holeCount | 0));
    const midR = 0.5 * (rIn + rOut);
    const radialHalf = 0.5 * (rOut - rIn);
    const maxChordHalf = midR * Math.sin(Math.PI / nHoles) * 0.72;
    const hr = Math.max(0.8, Math.min(0.5 * holeDiam, radialHalf - 0.8, maxChordHalf));
    const holeSegs = 20;
    const halfSector = Math.PI / nHoles;

    for (let k = 0; k < nHoles; k++) {
      const rot = (TWO_PI * k) / nHoles;
      const cosR = Math.cos(rot), sinR = Math.sin(rot);
      const botHole = [], botBnd = [], topHole = [], topBnd = [];
      const tunBot = [], tunTop = [];

      for (let s = 0; s < holeSegs; s++) {
        const aL = (TWO_PI * s) / holeSegs;
        const dx = Math.cos(aL), dy = Math.sin(aL);
        let dBnd = raySectorDistance(midR, 0.0, dx, dy, halfSector, rOut);

        // Intersect ray with inner circle rIn if pointing inward
        const bIn = 2.0 * midR * dx;
        const cIn = midR * midR - rIn * rIn;
        const discIn = bIn * bIn - 4.0 * cIn;
        if (discIn > 0.0) {
          const tIn = 0.5 * (-bIn - Math.sqrt(discIn));
          if (tIn > 1e-4 && tIn < dBnd) dBnd = tIn;
        }
        dBnd = Math.max(hr + 0.15, dBnd);

        const lxH = midR + hr * dx, lyH = hr * dy;
        const lxB = midR + dBnd * dx, lyB = dBnd * dy;
        const wxH = lxH * cosR - lyH * sinR, wyH = lxH * sinR + lyH * cosR;
        const wxB = lxB * cosR - lyB * sinR, wyB = lxB * sinR + lyB * cosR;

        botHole.push(col.addV(wxH, wyH, zBot, 0, 0, -1, 0));
        botBnd.push(col.addV(wxB, wyB, zBot, 0, 0, -1, 0));
        topHole.push(col.addV(wxH, wyH, zTop, 0, 0, 1, 0));
        topBnd.push(col.addV(wxB, wyB, zTop, 0, 0, 1, 0));

        const nx = -(dx * cosR - dy * sinR);
        const ny = -(dx * sinR + dy * cosR);
        tunBot.push(col.addV(wxH, wyH, zBot, nx, ny, 0, 0));
        tunTop.push(col.addV(wxH, wyH, zTop, nx, ny, 0, 0));
      }

      for (let s = 0; s < holeSegs; s++) {
        const j = (s + 1) % holeSegs;
        col.addTri(botHole[s], botBnd[j], botBnd[s]);
        col.addTri(botHole[s], botHole[j], botBnd[j]);
        col.addTri(topHole[s], topBnd[s], topBnd[j]);
        col.addTri(topHole[s], topBnd[j], topHole[j]);
        col.addTri(tunBot[s], tunTop[s], tunTop[j]);
        col.addTri(tunBot[s], tunTop[j], tunBot[j]);
      }
    }
  }

  function buildGear3DMeshData(p, geom, which, fast) {
    const col = createCollector();
    const g = which === "gear" ? geom.gear : geom.pinion;
    const bodyCfg = which === "gear" ? p.gear : p.pinion;
    const b = p.face_width_mm;
    const samplesFlank = fast ? 5 : 8;

    const baseContour = buildGear2DContour(p, geom, which, samplesFlank, 0.0);
    const chamf = Math.max(0.0, Math.min(p.elephant_foot_chamfer_mm, 0.22 * b));
    const chamfContour = chamf > 0.02
      ? buildGear2DContour(p, geom, which, samplesFlank, chamf)
      : baseContour;

    const interiorSlices = p.gear_type === "spur"
      ? 2
      : (fast ? Math.max(12, Math.round(b * 1.3)) : Math.max(22, Math.round(b * 2.2)));

    const zLevels = [];
    const zContours = [];
    if (chamf > 0.02) {
      zLevels.push(0.0);
      zContours.push(chamfContour);
      for (let i = 0; i <= interiorSlices; i++) {
        const t = i / interiorSlices;
        const z = chamf + t * (b - 2.0 * chamf);
        zLevels.push(z);
        zContours.push(baseContour);
      }
      zLevels.push(b);
      zContours.push(chamfContour);
    } else {
      for (let i = 0; i <= interiorSlices; i++) {
        zLevels.push((i / interiorSlices) * b);
        zContours.push(baseContour);
      }
    }

    const nz = zLevels.length;
    const nt = baseContour.count;
    const ringX = new Array(nz);
    const ringY = new Array(nz);

    for (let i = 0; i < nz; i++) {
      const z = zLevels[i];
      const psi = helixTwistAngleRad(z, b, g.pitch_radius_mm, geom.beta_deg, g.helix_hand, p.gear_type);
      const cosP = Math.cos(psi), sinP = Math.sin(psi);
      const src = zContours[i];
      const rx = new Float32Array(nt);
      const ry = new Float32Array(nt);
      for (let j = 0; j < nt; j++) {
        rx[j] = src.xs[j] * cosP - src.ys[j] * sinP;
        ry[j] = src.xs[j] * sinP + src.ys[j] * cosP;
      }
      ringX[i] = rx;
      ringY[i] = ry;
    }

    // Build outer gear tooth wall with exact helical & chamfer normals + overhang
    const wallRingIds = new Array(nz);
    for (let i = 0; i < nz; i++) {
      const ids = new Int32Array(nt);
      const i0 = Math.max(0, i - 1);
      const i1 = Math.min(nz - 1, i + 1);
      const dz = Math.max(1e-5, zLevels[i1] - zLevels[i0]);
      const z = zLevels[i];

      for (let j = 0; j < nt; j++) {
        const jp = (j + nt - 1) % nt;
        const jn = (j + 1) % nt;
        const tx = ringX[i][jn] - ringX[i][jp];
        const ty = ringY[i][jn] - ringY[i][jp];
        const ux = ringX[i1][j] - ringX[i0][j];
        const uy = ringY[i1][j] - ringY[i0][j];

        // Outward normal = T_ring x T_up
        let nx = ty * dz;
        let ny = -tx * dz;
        let nzVal = tx * uy - ty * ux;
        const nLen = Math.hypot(nx, ny, nzVal) || 1.0;
        nx /= nLen; ny /= nLen; nzVal /= nLen;

        let ovhDeg = 0.0;
        if (z > 0.03 && nzVal < -1e-4) {
          ovhDeg = Math.asin(Math.min(1.0, -nzVal)) * RAD2DEG;
        }
        ids[j] = col.addV(ringX[i][j], ringY[i][j], z, nx, ny, nzVal, ovhDeg);
      }
      wallRingIds[i] = ids;
    }

    for (let i = 0; i < nz - 1; i++) {
      const r0 = wallRingIds[i], r1 = wallRingIds[i + 1];
      for (let j = 0; j < nt; j++) {
        const jn = (j + 1) % nt;
        col.addTri(r0[j], r0[jn], r1[jn]);
        col.addTri(r0[j], r1[jn], r1[j]);
      }
    }

    // Sample clean wireframe lines on top, mid, and bottom tooth contours
    const wireSlices = [0, Math.floor(nz * 0.5), nz - 1];
    for (let ws = 0; ws < wireSlices.length; ws++) {
      const si = wireSlices[ws];
      const z = zLevels[si];
      for (let j = 0; j < nt; j++) {
        const jn = (j + 1) % nt;
        col.addWire(ringX[si][j], ringY[si][j], z, ringX[si][jn], ringY[si][jn], z);
      }
    }

    // Rim inner circle inside root radius
    const rSafeRim = Math.max(1.2, chamfContour.rf - Math.max(0.9, 0.45 * geom.m_n));
    const capSegs = 64;

    // Stitch outer tooth contour at z=0 and z=b cleanly inward to circular rim `rSafeRim`
    const stitchContourToCircle = function (rx, ry, rInner, zVal, facingUp) {
      const nzDir = facingUp ? 1.0 : -1.0;
      const outIds = new Int32Array(nt);
      const inIds = new Int32Array(nt);
      for (let j = 0; j < nt; j++) {
        const ang = Math.atan2(ry[j], rx[j]);
        outIds[j] = col.addV(rx[j], ry[j], zVal, 0, 0, nzDir, 0);
        inIds[j] = col.addV(rInner * Math.cos(ang), rInner * Math.sin(ang), zVal, 0, 0, nzDir, 0);
      }
      for (let j = 0; j < nt; j++) {
        const jn = (j + 1) % nt;
        if (facingUp) {
          col.addTri(inIds[j], outIds[j], outIds[jn]);
          col.addTri(inIds[j], outIds[jn], inIds[jn]);
        } else {
          col.addTri(inIds[j], outIds[jn], outIds[j]);
          col.addTri(inIds[j], inIds[jn], outIds[jn]);
        }
      }
    };
    stitchContourToCircle(ringX[0], ringY[0], rSafeRim, 0.0, false);
    stitchContourToCircle(ringX[nz - 1], ringY[nz - 1], rSafeRim, b, true);

    // Bore contour inside safe radius
    const maxBoreR = Math.max(0.6, rSafeRim - 1.0);
    const bore = buildBore2DContour(bodyCfg, maxBoreR, capSegs, 0.0);
    const rBoreOuter = bore
      ? Math.min(rSafeRim - 0.6, Math.max(bore.rNom, 0.5 * bodyCfg.bore_diameter_mm) + (bodyCfg.bore_type === "keyway" ? bodyCfg.keyway_depth_mm : 0.0) + 0.8)
      : 0.0;

    // Determine concentric radial zones from rCoreOut -> rSafeRim
    let zTopInner = b;
    let zBotInner = 0.0;
    let rInnerCore = Math.min(rSafeRim, Math.max(rBoreOuter, 1.2));

    const hasHub = Boolean(bodyCfg.hub_enabled) && (rSafeRim > rBoreOuter + 1.2);
    const hasRecess = Boolean(bodyCfg.recess_enabled) && (rSafeRim > rBoreOuter + 1.2);
    const rHub = hasHub ? Math.max(rInnerCore + 0.6, Math.min(rSafeRim - 0.3, 0.5 * bodyCfg.hub_diameter_mm)) : rInnerCore;
    const rRecess = hasRecess ? Math.max(rInnerCore + 0.6, Math.min(rSafeRim - 0.3, 0.5 * bodyCfg.recess_diameter_mm)) : rInnerCore;

    let zFeatureTop = b;
    let zFeatureBot = 0.0;
    let rFeature = rInnerCore;

    if (hasRecess) {
      rFeature = rRecess;
      const maxDepth = Math.max(0.4, 0.42 * b);
      const dep = Math.min(bodyCfg.recess_depth_mm, maxDepth);
      if (bodyCfg.recess_side === "top" || bodyCfg.recess_side === "both") zFeatureTop = b - dep;
      if (bodyCfg.recess_side === "bottom" || bodyCfg.recess_side === "both") zFeatureBot = dep;
    } else if (hasHub) {
      rFeature = rHub;
      zFeatureTop = b + bodyCfg.hub_height_mm;
    }
    zTopInner = zFeatureTop;
    zBotInner = zFeatureBot;

    // Inner bore tunnel OR solid center disk
    if (bore) {
      const bBot = new Int32Array(capSegs);
      const bTop = new Int32Array(capSegs);
      for (let i = 0; i < capSegs; i++) {
        const ip = (i + capSegs - 1) % capSegs;
        const inx = (i + 1) % capSegs;
        const tx = bore.xs[inx] - bore.xs[ip];
        const ty = bore.ys[inx] - bore.ys[ip];
        const tl = Math.hypot(tx, ty) || 1.0;
        // Bore wall faces inward toward origin: (-ty, tx) for CCW contour
        const nx = -ty / tl, ny = tx / tl;
        bBot[i] = col.addV(bore.xs[i], bore.ys[i], zBotInner, nx, ny, 0, 0);
        bTop[i] = col.addV(bore.xs[i], bore.ys[i], zTopInner, nx, ny, 0, 0);
      }
      for (let i = 0; i < capSegs; i++) {
        const j = (i + 1) % capSegs;
        col.addTri(bBot[i], bTop[i], bTop[j]);
        col.addTri(bBot[i], bTop[j], bBot[j]);
      }
      appendAnnulusCap(col, bore.xs, bore.ys, rFeature, zTopInner, true);
      appendAnnulusCap(col, bore.xs, bore.ys, rFeature, zBotInner, false);
    } else {
      const cTop = col.addV(0, 0, zTopInner, 0, 0, 1, 0);
      const cBot = col.addV(0, 0, zBotInner, 0, 0, -1, 0);
      const rTop = new Int32Array(capSegs);
      const rBot = new Int32Array(capSegs);
      for (let i = 0; i < capSegs; i++) {
        const a = (TWO_PI * i) / capSegs;
        rTop[i] = col.addV(rFeature * Math.cos(a), rFeature * Math.sin(a), zTopInner, 0, 0, 1, 0);
        rBot[i] = col.addV(rFeature * Math.cos(a), rFeature * Math.sin(a), zBotInner, 0, 0, -1, 0);
      }
      for (let i = 0; i < capSegs; i++) {
        const j = (i + 1) % capSegs;
        col.addTri(cTop, rTop[i], rTop[j]);
        col.addTri(cBot, rBot[j], rBot[i]);
      }
    }

    // Vertical step wall at rFeature if Hub or Recess changed Z
    if (Math.abs(zFeatureTop - b) > 1e-4) {
      appendCircleStepWall(col, rFeature, b, zFeatureTop, capSegs, zFeatureTop > b);
    }
    if (Math.abs(zFeatureBot - 0.0) > 1e-4) {
      // Bottom recess ceiling overhang = 90 deg if recessed on bottom
      appendCircleStepWall(col, rFeature, 0.0, zFeatureBot, capSegs, false);
    }

    // Body region between rFeature and rSafeRim: Solid, Web Recess, or Lightening Holes
    const spanRadial = rSafeRim - rFeature;
    const circlePts = function (rad) {
      const xs = new Float64Array(capSegs), ys = new Float64Array(capSegs);
      for (let i = 0; i < capSegs; i++) {
        const a = (TWO_PI * i) / capSegs;
        xs[i] = rad * Math.cos(a);
        ys[i] = rad * Math.sin(a);
      }
      return { xs: xs, ys: ys };
    };

    if (bodyCfg.lightening_mode === "web_recess" && spanRadial > 3.0) {
      const rWebIn = rFeature + 0.8;
      const rWebOut = rSafeRim - 0.8;
      const webH = Math.max(1.2, Math.min(b - 0.8, bodyCfg.web_thickness_mm));
      const zWebBot = 0.5 * (b - webH);
      const zWebTop = b - zWebBot;

      const cFeat = circlePts(rFeature);
      appendAnnulusCap(col, cFeat.xs, cFeat.ys, rWebIn, b, true);
      appendAnnulusCap(col, cFeat.xs, cFeat.ys, rWebIn, 0.0, false);

      appendCircleStepWall(col, rWebIn, zWebTop, b, capSegs, true);
      appendCircleStepWall(col, rWebIn, zWebBot, 0.0, capSegs, true);

      const cWebIn = circlePts(rWebIn);
      appendAnnulusCap(col, cWebIn.xs, cWebIn.ys, rWebOut, zWebTop, true);
      appendAnnulusCap(col, cWebIn.xs, cWebIn.ys, rWebOut, zWebBot, false);

      appendCircleStepWall(col, rWebOut, zWebTop, b, capSegs, false);
      appendCircleStepWall(col, rWebOut, zWebBot, 0.0, capSegs, false);

      const cWebOut = circlePts(rWebOut);
      appendAnnulusCap(col, cWebOut.xs, cWebOut.ys, rSafeRim, b, true);
      appendAnnulusCap(col, cWebOut.xs, cWebOut.ys, rSafeRim, 0.0, false);
    } else if (bodyCfg.lightening_mode === "lightening_holes" && spanRadial > 3.6) {
      const rHoleIn = rFeature + 0.6;
      const rHoleOut = rSafeRim - 0.6;
      const cFeat = circlePts(rFeature);
      appendAnnulusCap(col, cFeat.xs, cFeat.ys, rHoleIn, b, true);
      appendAnnulusCap(col, cFeat.xs, cFeat.ys, rHoleIn, 0.0, false);

      appendPerforatedWebAnnulus(
        col,
        rHoleIn,
        rHoleOut,
        0.0,
        b,
        bodyCfg.lightening_hole_count,
        bodyCfg.lightening_hole_diameter_mm
      );

      const cHoleOut = circlePts(rHoleOut);
      appendAnnulusCap(col, cHoleOut.xs, cHoleOut.ys, rSafeRim, b, true);
      appendAnnulusCap(col, cHoleOut.xs, cHoleOut.ys, rSafeRim, 0.0, false);
    } else if (spanRadial > 1e-4) {
      const cFeat = circlePts(rFeature);
      appendAnnulusCap(col, cFeat.xs, cFeat.ys, rSafeRim, b, true);
      appendAnnulusCap(col, cFeat.xs, cFeat.ys, rSafeRim, 0.0, false);
    }

    return col;
  }

  // Fit-Test Kit 3D Preview Builders (Jig Base + 2 Pins, 5-Tooth Sectors, 4-Hole Bore Gauge)
  function buildFitKitSectorMesh(p, geom, which) {
    const g = which === "gear" ? geom.gear : geom.pinion;
    const zTeeth = g.teeth;
    const bKit = Math.min(p.face_width_mm, 8.0);
    const minRootD = 2.0 * Math.min(geom.pinion.root_radius_mm, geom.gear.root_radius_mm);
    const dPinHole = Math.max(4.0, Math.min(8.0, 0.45 * minRootD));

    if (zTeeth <= 9) {
      const pClone = deepClone(p);
      pClone.face_width_mm = bKit;
      const bObj = which === "gear" ? pClone.gear : pClone.pinion;
      bObj.bore_type = "round";
      bObj.bore_diameter_mm = dPinHole;
      bObj.bore_clearance_mm = 0.0;
      bObj.hub_enabled = false;
      bObj.recess_enabled = false;
      bObj.lightening_mode = "solid";
      return buildGear3DMeshData(pClone, geom, which, true);
    }

    const col = createCollector();
    const tpl = buildSingleToothPolarTemplate(p, geom, which, 6, 0.0);
    const nKeep = Math.min(5, zTeeth);
    const kStart = -Math.floor(nKeep / 2);
    const kEnd = kStart + nKeep - 1;
    const centerBaseAng = which === "gear" ? Math.PI : 0.0;

    const arcPhi = [];
    const arcR = [];
    for (let k = kStart; k <= kEnd; k++) {
      const off = centerBaseAng + (TWO_PI * k) / zTeeth;
      for (let j = 0; j < tpl.phi.length; j++) {
        arcPhi.push(off + tpl.phi[j]);
        arcR.push(tpl.rad[j]);
      }
    }

    const rRingInner = 0.5 * dPinHole;
    const rRingOuter = Math.max(rRingInner + 2.4, Math.min(tpl.rf - 0.5, rRingInner + 4.5));
    const phiFirst = arcPhi[0];
    const phiLast = arcPhi[arcPhi.length - 1];

    // Closed outer loop of sector wedge + hub ring
    const polyBaseX = [];
    const polyBaseY = [];
    const polyIsTeeth = [];
    for (let i = 0; i < arcPhi.length; i++) {
      polyBaseX.push(arcR[i] * Math.cos(arcPhi[i]));
      polyBaseY.push(arcR[i] * Math.sin(arcPhi[i]));
      polyIsTeeth.push(true);
    }
    const backSteps = 28;
    const backSpan = TWO_PI - (phiLast - phiFirst);
    for (let s = 0; s <= backSteps; s++) {
      const ang = phiLast + (s / backSteps) * backSpan;
      polyBaseX.push(rRingOuter * Math.cos(ang));
      polyBaseY.push(rRingOuter * Math.sin(ang));
      polyIsTeeth.push(false);
    }

    const nLoop = polyBaseX.length;
    const nz = p.gear_type === "spur" ? 2 : 14;
    const ringsIds = new Array(nz);
    const ringWX = new Array(nz);
    const ringWY = new Array(nz);

    for (let i = 0; i < nz; i++) {
      const z = (i / (nz - 1)) * bKit;
      const psi = helixTwistAngleRad(z, bKit, g.pitch_radius_mm, geom.beta_deg, g.helix_hand, p.gear_type);
      const cp = Math.cos(psi), sp = Math.sin(psi);
      const wx = new Float32Array(nLoop);
      const wy = new Float32Array(nLoop);
      for (let j = 0; j < nLoop; j++) {
        if (polyIsTeeth[j]) {
          wx[j] = polyBaseX[j] * cp - polyBaseY[j] * sp;
          wy[j] = polyBaseX[j] * sp + polyBaseY[j] * cp;
        } else {
          wx[j] = polyBaseX[j];
          wy[j] = polyBaseY[j];
        }
      }
      ringWX[i] = wx;
      ringWY[i] = wy;
    }

    for (let i = 0; i < nz; i++) {
      const z = (i / (nz - 1)) * bKit;
      const ids = new Int32Array(nLoop);
      for (let j = 0; j < nLoop; j++) {
        const jp = (j + nLoop - 1) % nLoop;
        const jn = (j + 1) % nLoop;
        const tx = ringWX[i][jn] - ringWX[i][jp];
        const ty = ringWY[i][jn] - ringWY[i][jp];
        const tl = Math.hypot(tx, ty) || 1.0;
        ids[j] = col.addV(ringWX[i][j], ringWY[i][j], z, ty / tl, -tx / tl, 0, 0);
      }
      ringsIds[i] = ids;
    }
    for (let i = 0; i < nz - 1; i++) {
      for (let j = 0; j < nLoop; j++) {
        const jn = (j + 1) % nLoop;
        col.addTri(ringsIds[i][j], ringsIds[i][jn], ringsIds[i + 1][jn]);
        col.addTri(ringsIds[i][j], ringsIds[i + 1][jn], ringsIds[i + 1][j]);
      }
    }

    // Inner pin hole tunnel + top/bottom caps
    const holeBot = new Int32Array(nLoop);
    const holeTop = new Int32Array(nLoop);
    const capBotIn = new Int32Array(nLoop), capBotOut = new Int32Array(nLoop);
    const capTopIn = new Int32Array(nLoop), capTopOut = new Int32Array(nLoop);

    for (let j = 0; j < nLoop; j++) {
      const angB = Math.atan2(ringWY[0][j], ringWX[0][j]);
      const angT = Math.atan2(ringWY[nz - 1][j], ringWX[nz - 1][j]);
      const ixB = rRingInner * Math.cos(angB), iyB = rRingInner * Math.sin(angB);
      const ixT = rRingInner * Math.cos(angT), iyT = rRingInner * Math.sin(angT);

      const aHole = (TWO_PI * j) / nLoop;
      const ch = Math.cos(aHole), sh = Math.sin(aHole);
      holeBot[j] = col.addV(rRingInner * ch, rRingInner * sh, 0.0, -ch, -sh, 0, 0);
      holeTop[j] = col.addV(rRingInner * ch, rRingInner * sh, bKit, -ch, -sh, 0, 0);

      capBotIn[j] = col.addV(ixB, iyB, 0.0, 0, 0, -1, 0);
      capBotOut[j] = col.addV(ringWX[0][j], ringWY[0][j], 0.0, 0, 0, -1, 0);
      capTopIn[j] = col.addV(ixT, iyT, bKit, 0, 0, 1, 0);
      capTopOut[j] = col.addV(ringWX[nz - 1][j], ringWY[nz - 1][j], bKit, 0, 0, 1, 0);
    }
    for (let j = 0; j < nLoop; j++) {
      const jn = (j + 1) % nLoop;
      col.addTri(holeBot[j], holeTop[j], holeTop[jn]);
      col.addTri(holeBot[j], holeTop[jn], holeBot[jn]);
      col.addTri(capBotIn[j], capBotOut[jn], capBotOut[j]);
      col.addTri(capBotIn[j], capBotIn[jn], capBotOut[jn]);
      col.addTri(capTopIn[j], capTopOut[j], capTopOut[jn]);
      col.addTri(capTopIn[j], capTopOut[jn], capTopIn[jn]);
    }

    return col;
  }

  function buildFitKitJigAndGaugeMeshes(p, geom) {
    const a = geom.center_distance_mm;
    const minRootD = 2.0 * Math.min(geom.pinion.root_radius_mm, geom.gear.root_radius_mm);
    const dPin = Math.max(4.0, Math.min(8.0, 0.45 * minRootD)) - 0.22;
    const rPin = 0.5 * dPin;
    const bKit = Math.min(p.face_width_mm, 8.0);
    const rPad = Math.max(rPin + 5.5, 9.5);
    const baseH = 3.0;
    const pinTopZ = baseH + bKit + 1.5;

    // 1. 2-Pin Rounded Stadium Jig Base
    const jigCol = createCollector();
    const nArc = 24;
    const stadX = [], stadY = [];
    for (let i = 0; i <= nArc; i++) {
      const ang = -0.5 * Math.PI + (Math.PI * i) / nArc;
      stadX.push(0.5 * a + rPad * Math.cos(ang));
      stadY.push(rPad * Math.sin(ang));
    }
    for (let i = 0; i <= nArc; i++) {
      const ang = 0.5 * Math.PI + (Math.PI * i) / nArc;
      stadX.push(-0.5 * a + rPad * Math.cos(ang));
      stadY.push(rPad * Math.sin(ang));
    }
    const nS = stadX.length;
    const bIds = new Int32Array(nS), tIds = new Int32Array(nS);
    const cBot = jigCol.addV(0, 0, 0, 0, 0, -1, 0);
    const cTop = jigCol.addV(0, 0, baseH, 0, 0, 1, 0);
    const cbRing = new Int32Array(nS), ctRing = new Int32Array(nS);

    for (let i = 0; i < nS; i++) {
      const ip = (i + nS - 1) % nS, inx = (i + 1) % nS;
      const tx = stadX[inx] - stadX[ip], ty = stadY[inx] - stadY[ip];
      const tl = Math.hypot(tx, ty) || 1.0;
      bIds[i] = jigCol.addV(stadX[i], stadY[i], 0, ty / tl, -tx / tl, 0, 0);
      tIds[i] = jigCol.addV(stadX[i], stadY[i], baseH, ty / tl, -tx / tl, 0, 0);
      cbRing[i] = jigCol.addV(stadX[i], stadY[i], 0, 0, 0, -1, 0);
      ctRing[i] = jigCol.addV(stadX[i], stadY[i], baseH, 0, 0, 1, 0);
    }
    for (let i = 0; i < nS; i++) {
      const j = (i + 1) % nS;
      jigCol.addTri(bIds[i], bIds[j], tIds[j]);
      jigCol.addTri(bIds[i], tIds[j], tIds[i]);
      jigCol.addTri(cBot, cbRing[j], cbRing[i]);
      jigCol.addTri(cTop, ctRing[i], ctRing[j]);
    }

    // Add 2 vertical pins at (-a/2, 0) and (+a/2, 0) with 0.6mm top chamfer
    const pinCenters = [-0.5 * a, 0.5 * a];
    const pSegs = 28;
    for (let pk = 0; pk < 2; pk++) {
      const px = pinCenters[pk];
      const r0 = new Int32Array(pSegs), r1 = new Int32Array(pSegs), r2 = new Int32Array(pSegs);
      const capC = jigCol.addV(px, 0, pinTopZ, 0, 0, 1, 0);
      const capR = new Int32Array(pSegs);
      const rChamfTop = Math.max(0.5, rPin - 0.6);
      for (let s = 0; s < pSegs; s++) {
        const ang = (TWO_PI * s) / pSegs;
        const cs = Math.cos(ang), sn = Math.sin(ang);
        r0[s] = jigCol.addV(px + rPin * cs, rPin * sn, baseH, cs, sn, 0, 0);
        r1[s] = jigCol.addV(px + rPin * cs, rPin * sn, pinTopZ - 0.6, cs, sn, 0.3, 0);
        r2[s] = jigCol.addV(px + rChamfTop * cs, rChamfTop * sn, pinTopZ, 0.7 * cs, 0.7 * sn, 0.7, 0);
        capR[s] = jigCol.addV(px + rChamfTop * cs, rChamfTop * sn, pinTopZ, 0, 0, 1, 0);
      }
      for (let s = 0; s < pSegs; s++) {
        const j = (s + 1) % pSegs;
        jigCol.addTri(r0[s], r0[j], r1[j]);
        jigCol.addTri(r0[s], r1[j], r1[s]);
        jigCol.addTri(r1[s], r1[j], r2[j]);
        jigCol.addTri(r1[s], r2[j], r2[s]);
        jigCol.addTri(capC, capR[s], capR[j]);
      }
    }

    // 2. 4-Hole Bore Calibration Strip Gauge with V-Notch Markers
    const gaugeCol = createCollector();
    const bCfg = deepClone(p.pinion);
    if (bCfg.bore_type === "none") bCfg.bore_type = "round";
    const holeD = Math.max(2.0, Math.min(18.0, bCfg.bore_diameter_mm));
    const pitchX = holeD + 6.5;
    const halfW = 2.0 * pitchX + 3.0;
    const halfD = 0.5 * holeD + 4.5;
    const gH = 5.0;
    const deltas = [-0.05, 0.0, 0.05, 0.10];

    for (let k = 0; k < 4; k++) {
      const cx = (k - 1.5) * pitchX;
      const xL = cx - 0.5 * pitchX + (k === 0 ? -1.5 : 0.0);
      const xR = cx + 0.5 * pitchX + (k === 3 ? 1.5 : 0.0);
      const holePoly = buildBore2DContour(bCfg, 0.5 * holeD + 1.8, 32, deltas[k]);
      const hN = holePoly.count;

      const botH = new Int32Array(hN), botB = new Int32Array(hN);
      const topH = new Int32Array(hN), topB = new Int32Array(hN);
      const tunB = new Int32Array(hN), tunT = new Int32Array(hN);

      for (let s = 0; s < hN; s++) {
        const aL = (TWO_PI * s) / hN;
        const dx = Math.cos(aL), dy = Math.sin(aL);
        let tBox = Infinity;
        if (dx > 1e-6) tBox = Math.min(tBox, (xR - cx) / dx);
        if (dx < -1e-6) tBox = Math.min(tBox, (xL - cx) / dx);
        if (dy > 1e-6) tBox = Math.min(tBox, halfD / dy);
        if (dy < -1e-6) {
          // Add subtle V-notch marker(s) on front -Y edge for hole index (k+1)
          let yFront = -halfD;
          const bxTest = cx + (yFront / dy) * dx;
          for (let m = 0; m <= k; m++) {
            const notchX = cx + (m - 0.5 * k) * 1.8;
            const distN = Math.abs(bxTest - notchX);
            if (distN < 0.65) yFront += (0.65 - distN) * 0.9;
          }
          tBox = Math.min(tBox, yFront / dy);
        }

        const hx = cx + holePoly.xs[s], hy = holePoly.ys[s];
        const bx = cx + tBox * dx, by = tBox * dy;
        botH[s] = gaugeCol.addV(hx, hy, 0, 0, 0, -1, 0);
        botB[s] = gaugeCol.addV(bx, by, 0, 0, 0, -1, 0);
        topH[s] = gaugeCol.addV(hx, hy, gH, 0, 0, 1, 0);
        topB[s] = gaugeCol.addV(bx, by, gH, 0, 0, 1, 0);
        tunB[s] = gaugeCol.addV(hx, hy, 0, -dx, -dy, 0, 0);
        tunT[s] = gaugeCol.addV(hx, hy, gH, -dx, -dy, 0, 0);

        // Outer box side walls where ray hits strip exterior
        const sn = (s + 1) % hN;
        const aLn = (TWO_PI * sn) / hN;
        const dxn = Math.cos(aLn), dyn = Math.sin(aLn);
        let tBoxN = Infinity;
        if (dxn > 1e-6) tBoxN = Math.min(tBoxN, (xR - cx) / dxn);
        if (dxn < -1e-6) tBoxN = Math.min(tBoxN, (xL - cx) / dxn);
        if (dyn > 1e-6) tBoxN = Math.min(tBoxN, halfD / dyn);
        if (dyn < -1e-6) {
          let yFrontN = -halfD;
          const bxTestN = cx + (yFrontN / dyn) * dxn;
          for (let m = 0; m <= k; m++) {
            const notchX = cx + (m - 0.5 * k) * 1.8;
            const distN = Math.abs(bxTestN - notchX);
            if (distN < 0.65) yFrontN += (0.65 - distN) * 0.9;
          }
          tBoxN = Math.min(tBoxN, yFrontN / dyn);
        }
        const bxN = cx + tBoxN * dxn, byN = tBoxN * dyn;
        const isExtWall =
          (Math.abs(by - halfD) < 0.05 && Math.abs(byN - halfD) < 0.05) ||
          (by < -halfD + 0.9 && byN < -halfD + 0.9) ||
          (k === 0 && Math.abs(bx - xL) < 0.05 && Math.abs(bxN - xL) < 0.05) ||
          (k === 3 && Math.abs(bx - xR) < 0.05 && Math.abs(bxN - xR) < 0.05);
        if (isExtWall) {
          const etx = bxN - bx, ety = byN - by;
          const etl = Math.hypot(etx, ety) || 1.0;
          const w0 = gaugeCol.addV(bx, by, 0, ety / etl, -etx / etl, 0, 0);
          const w1 = gaugeCol.addV(bxN, byN, 0, ety / etl, -etx / etl, 0, 0);
          const w2 = gaugeCol.addV(bxN, byN, gH, ety / etl, -etx / etl, 0, 0);
          const w3 = gaugeCol.addV(bx, by, gH, ety / etl, -etx / etl, 0, 0);
          gaugeCol.addTri(w0, w1, w2);
          gaugeCol.addTri(w0, w2, w3);
        }
      }

      for (let s = 0; s < hN; s++) {
        const j = (s + 1) % hN;
        gaugeCol.addTri(botH[s], botB[j], botB[s]);
        gaugeCol.addTri(botH[s], botH[j], botB[j]);
        gaugeCol.addTri(topH[s], topB[s], topB[j]);
        gaugeCol.addTri(topH[s], topB[j], topH[j]);
        gaugeCol.addTri(tunB[s], tunT[s], tunT[j]);
        gaugeCol.addTri(tunB[s], tunT[j], tunB[j]);
      }
    }

    return { jig: jigCol, gauge: gaugeCol, rPad: rPad, stripHalfW: halfW, stripHalfD: halfD };
  }

  // ==========================================================================
  // 8. WebGL2 3D Viewport Engine (Rigid-Body Instanced Transforms + 3D Force Vectors)
  // ==========================================================================
  let gl = null;
  let isWebGL2 = false;
  let meshProg = null;
  let lineProg = null;
  let bedBuffer = null;
  let bedVertCount = 0;
  let dynLineBuffer = null;
  const gpuParts = {};

  const camera = {
    yaw: -0.72,
    pitch: 0.56,
    distance: 155.0,
    target: [0.0, 0.0, 6.0]
  };

  function mat4Identity() {
    const m = new Float32Array(16);
    m[0] = 1; m[5] = 1; m[10] = 1; m[15] = 1;
    return m;
  }

  function mat4Multiply(a, b) {
    const out = new Float32Array(16);
    for (let col = 0; col < 4; col++) {
      const b0 = b[col * 4], b1 = b[col * 4 + 1], b2 = b[col * 4 + 2], b3 = b[col * 4 + 3];
      out[col * 4]     = a[0] * b0 + a[4] * b1 + a[8]  * b2 + a[12] * b3;
      out[col * 4 + 1] = a[1] * b0 + a[5] * b1 + a[9]  * b2 + a[13] * b3;
      out[col * 4 + 2] = a[2] * b0 + a[6] * b1 + a[10] * b2 + a[14] * b3;
      out[col * 4 + 3] = a[3] * b0 + a[7] * b1 + a[11] * b2 + a[15] * b3;
    }
    return out;
  }

  function mat4TranslateRotateZ(tx, ty, tz, rotRad) {
    const c = Math.cos(rotRad), s = Math.sin(rotRad);
    const m = mat4Identity();
    m[0] = c;  m[4] = -s; m[12] = tx;
    m[1] = s;  m[5] = c;  m[13] = ty;
    m[14] = tz;
    return m;
  }

  function mat4Perspective(fovyRad, aspect, near, far) {
    const f = 1.0 / Math.tan(0.5 * fovyRad);
    const nf = 1.0 / (near - far);
    const out = new Float32Array(16);
    out[0] = f / Math.max(aspect, 0.05);
    out[5] = f;
    out[10] = (far + near) * nf;
    out[11] = -1.0;
    out[14] = (2.0 * far * near) * nf;
    return out;
  }

  function mat4LookAtZUp(eye, center) {
    let fx = center[0] - eye[0], fy = center[1] - eye[1], fz = center[2] - eye[2];
    const fl = Math.hypot(fx, fy, fz) || 1.0;
    fx /= fl; fy /= fl; fz /= fl;

    let upX = 0.0, upY = 0.0, upZ = 1.0;
    if (Math.abs(fz) > 0.998) { upY = 1.0; upZ = 0.0; }

    let sx = fy * upZ - fz * upY;
    let sy = fz * upX - fx * upZ;
    let sz = fx * upY - fy * upX;
    const sl = Math.hypot(sx, sy, sz) || 1.0;
    sx /= sl; sy /= sl; sz /= sl;

    const ux = sy * fz - sz * fy;
    const uy = sz * fx - sx * fz;
    const uz = sx * fy - sy * fx;

    const out = mat4Identity();
    out[0] = sx;  out[4] = sy;  out[8]  = sz;  out[12] = -(sx * eye[0] + sy * eye[1] + sz * eye[2]);
    out[1] = ux;  out[5] = uy;  out[9]  = uz;  out[13] = -(ux * eye[0] + uy * eye[1] + uz * eye[2]);
    out[2] = -fx; out[6] = -fy; out[10] = -fz; out[14] = (fx * eye[0] + fy * eye[1] + fz * eye[2]);
    return out;
  }

  function compileProgram(glCtx, vsSrc, fsSrc) {
    const vs = glCtx.createShader(glCtx.VERTEX_SHADER);
    glCtx.shaderSource(vs, vsSrc);
    glCtx.compileShader(vs);
    if (!glCtx.getShaderParameter(vs, glCtx.COMPILE_STATUS)) return null;
    const fs = glCtx.createShader(glCtx.FRAGMENT_SHADER);
    glCtx.shaderSource(fs, fsSrc);
    glCtx.compileShader(fs);
    if (!glCtx.getShaderParameter(fs, glCtx.COMPILE_STATUS)) return null;
    const prog = glCtx.createProgram();
    glCtx.attachShader(prog, vs);
    glCtx.attachShader(prog, fs);
    glCtx.linkProgram(prog);
    if (!glCtx.getProgramParameter(prog, glCtx.LINK_STATUS)) return null;
    return prog;
  }

  function initWebGLViewport() {
    const canvas = document.getElementById("gl-canvas");
    if (!canvas || !canvas.getContext) return;

    gl = canvas.getContext("webgl2", { antialias: true, alpha: false, depth: true });
    if (gl) {
      isWebGL2 = true;
    } else {
      gl = canvas.getContext("webgl", { antialias: true, alpha: false, depth: true });
      isWebGL2 = false;
      if (gl) gl.getExtension("OES_element_index_uint");
    }
    if (!gl) return;

    const vsMesh300 = `#version 300 es
      precision highp float;
      in vec3 a_pos;
      in vec3 a_nrm;
      in float a_ovh;
      uniform mat4 u_vp;
      uniform mat4 u_model;
      out vec3 v_pos;
      out vec3 v_nrm;
      out float v_ovh;
      void main() {
        vec4 wp = u_model * vec4(a_pos, 1.0);
        v_pos = wp.xyz;
        v_nrm = mat3(u_model) * a_nrm;
        v_ovh = a_ovh;
        gl_Position = u_vp * wp;
      }
    `;

    const fsMesh300 = `#version 300 es
      precision highp float;
      in vec3 v_pos;
      in vec3 v_nrm;
      in float v_ovh;
      uniform vec3 u_eye;
      uniform vec3 u_albedo;
      uniform float u_roughness;
      uniform float u_metallic;
      uniform float u_heatmap;
      uniform float u_jamPulse;
      uniform float u_clipMode;
      uniform float u_clipVal;
      out vec4 outColor;

      vec3 heatmapColor(float deg) {
        vec3 safeA = vec3(0.04, 0.78, 0.44);
        vec3 safeB = vec3(0.18, 0.86, 0.42);
        vec3 warn  = vec3(1.00, 0.69, 0.02);
        vec3 crit  = vec3(0.98, 0.20, 0.16);
        if (deg <= 45.0) return mix(safeA, safeB, clamp(deg / 45.0, 0.0, 1.0));
        if (deg <= 55.0) return mix(warn, crit, (deg - 45.0) / 10.0);
        return crit;
      }

      void main() {
        if (u_clipMode > 0.5 && u_clipMode < 1.5 && v_pos.z > u_clipVal) discard;
        if (u_clipMode > 1.5 && v_pos.y < u_clipVal) discard;

        vec3 N = normalize(v_nrm);
        bool backFace = !gl_FrontFacing;
        if (backFace) N = -N;

        vec3 V = normalize(u_eye - v_pos);
        vec3 albedo = u_heatmap > 0.5 ? heatmapColor(v_ovh) : u_albedo;
        if (u_jamPulse > 0.01) {
          albedo = mix(albedo, vec3(0.98, 0.20, 0.22), u_jamPulse * 0.42);
        }
        if (backFace && u_clipMode > 0.5) {
          albedo = mix(albedo, vec3(1.0, 0.72, 0.24), 0.55);
        }

        float layerSheen = 0.988 + 0.012 * sin(v_pos.z * 31.4159);
        albedo *= layerSheen;

        vec3 L1 = normalize(vec3(-0.48, -0.62, 0.62));
        vec3 L2 = normalize(vec3(0.66, -0.22, 0.48));
        vec3 L3 = normalize(vec3(0.08, 0.84, 0.36));

        float d1 = max(dot(N, L1), 0.0);
        float d2 = max(dot(N, L2), 0.0);
        float d3 = max(dot(N, L3), 0.0);

        vec3 H1 = normalize(L1 + V);
        float shininess = mix(92.0, 18.0, u_roughness);
        float spec = pow(max(dot(N, H1), 0.0), shininess) * mix(0.28, 0.85, 1.0 - u_roughness);

        float hemi = 0.5 + 0.5 * N.z;
        vec3 ambient = mix(vec3(0.15, 0.17, 0.22), vec3(0.35, 0.38, 0.44), hemi);
        float rim = pow(1.0 - max(dot(N, V), 0.0), 3.0) * 0.22;

        vec3 specTint = mix(vec3(1.0), albedo, u_metallic);
        vec3 col = albedo * (ambient + 0.78 * d1 + 0.32 * d2 + 0.22 * d3)
                 + specTint * spec
                 + vec3(0.55, 0.84, 0.88) * rim;
        outColor = vec4(pow(clamp(col, 0.0, 1.0), vec3(0.93)), 1.0);
      }
    `;

    const vsLine300 = `#version 300 es
      precision highp float;
      in vec3 a_pos;
      uniform mat4 u_mvp;
      void main() { gl_Position = u_mvp * vec4(a_pos, 1.0); }
    `;

    const fsLine300 = `#version 300 es
      precision highp float;
      uniform vec4 u_color;
      out vec4 outColor;
      void main() { outColor = u_color; }
    `;

    const vsMesh100 = `
      precision highp float;
      attribute vec3 a_pos;
      attribute vec3 a_nrm;
      attribute float a_ovh;
      uniform mat4 u_vp;
      uniform mat4 u_model;
      varying vec3 v_pos;
      varying vec3 v_nrm;
      varying float v_ovh;
      void main() {
        vec4 wp = u_model * vec4(a_pos, 1.0);
        v_pos = wp.xyz;
        v_nrm = mat3(u_model) * a_nrm;
        v_ovh = a_ovh;
        gl_Position = u_vp * wp;
      }
    `;

    const fsMesh100 = `
      precision highp float;
      varying vec3 v_pos;
      varying vec3 v_nrm;
      varying float v_ovh;
      uniform vec3 u_eye;
      uniform vec3 u_albedo;
      uniform float u_heatmap;
      uniform float u_jamPulse;
      uniform float u_clipMode;
      uniform float u_clipVal;
      vec3 heatmapColor(float deg) {
        if (deg <= 45.0) return vec3(0.08, 0.80, 0.44);
        if (deg <= 55.0) return vec3(1.00, 0.68, 0.02);
        return vec3(0.98, 0.20, 0.16);
      }
      void main() {
        if (u_clipMode > 0.5 && u_clipMode < 1.5 && v_pos.z > u_clipVal) discard;
        if (u_clipMode > 1.5 && v_pos.y < u_clipVal) discard;
        vec3 N = normalize(v_nrm);
        if (!gl_FrontFacing) N = -N;
        vec3 V = normalize(u_eye - v_pos);
        vec3 alb = u_heatmap > 0.5 ? heatmapColor(v_ovh) : u_albedo;
        if (u_jamPulse > 0.01) alb = mix(alb, vec3(0.98, 0.20, 0.22), u_jamPulse * 0.42);
        vec3 L1 = normalize(vec3(-0.48, -0.62, 0.62));
        float diff = max(dot(N, L1), 0.0);
        vec3 H = normalize(L1 + V);
        float spec = pow(max(dot(N, H), 0.0), 42.0) * 0.38;
        gl_FragColor = vec4(alb * (0.32 + 0.76 * diff) + vec3(spec), 1.0);
      }
    `;

    const vsLine100 = `
      precision highp float;
      attribute vec3 a_pos;
      uniform mat4 u_mvp;
      void main() { gl_Position = u_mvp * vec4(a_pos, 1.0); }
    `;

    const fsLine100 = `
      precision highp float;
      uniform vec4 u_color;
      void main() { gl_FragColor = u_color; }
    `;

    meshProg = compileProgram(gl, isWebGL2 ? vsMesh300 : vsMesh100, isWebGL2 ? fsMesh300 : fsMesh100);
    lineProg = compileProgram(gl, isWebGL2 ? vsLine300 : vsLine100, isWebGL2 ? fsLine300 : fsLine100);
    bedBuffer = gl.createBuffer();
    dynLineBuffer = gl.createBuffer();

    rebuildBedGeometry();
    bindViewportEvents(canvas);
  }

  function ensurePartGPU(key) {
    if (!gpuParts[key] && gl) {
      gpuParts[key] = {
        pos: gl.createBuffer(),
        nrm: gl.createBuffer(),
        ovh: gl.createBuffer(),
        idx: gl.createBuffer(),
        wire: gl.createBuffer(),
        indexCount: 0,
        indexType: 0,
        wireCount: 0
      };
    }
    return gpuParts[key];
  }

  function uploadCollectorToPart(key, col) {
    if (!gl) return;
    const part = ensurePartGPU(key);
    const usage = state.isInteracting ? gl.DYNAMIC_DRAW : gl.STATIC_DRAW;

    const posArr = new Float32Array(col.pos);
    const nrmArr = new Float32Array(col.nrm);
    const ovhArr = new Float32Array(col.ovh);
    const wireArr = new Float32Array(col.wire);

    gl.bindBuffer(gl.ARRAY_BUFFER, part.pos);
    gl.bufferData(gl.ARRAY_BUFFER, posArr, usage);
    gl.bindBuffer(gl.ARRAY_BUFFER, part.nrm);
    gl.bufferData(gl.ARRAY_BUFFER, nrmArr, usage);
    gl.bindBuffer(gl.ARRAY_BUFFER, part.ovh);
    gl.bufferData(gl.ARRAY_BUFFER, ovhArr, usage);

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, part.idx);
    if (isWebGL2 || posArr.length / 3 > 65530) {
      gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint32Array(col.idx), usage);
      part.indexType = gl.UNSIGNED_INT;
    } else {
      gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(col.idx), usage);
      part.indexType = gl.UNSIGNED_SHORT;
    }
    part.indexCount = col.idx.length;

    gl.bindBuffer(gl.ARRAY_BUFFER, part.wire);
    gl.bufferData(gl.ARRAY_BUFFER, wireArr, usage);
    part.wireCount = wireArr.length / 3;
  }

  function rebuildBedGeometry() {
    if (!gl || !bedBuffer) return;
    const bx = Math.max(80, Number(state.printer.bed_x) || 220);
    const by = Math.max(80, Number(state.printer.bed_y) || 220);
    const hx = 0.5 * bx, hy = 0.5 * by;
    const verts = [];
    const step = 20;
    for (let x = -Math.floor(hx / step) * step; x <= hx + 0.01; x += step) {
      verts.push(x, -hy, -0.06, x, hy, -0.06);
    }
    for (let y = -Math.floor(hy / step) * step; y <= hy + 0.01; y += step) {
      verts.push(-hx, y, -0.06, hx, y, -0.06);
    }
    verts.push(
      -hx, -hy, 0.02, hx, -hy, 0.02,
      hx, -hy, 0.02, hx, hy, 0.02,
      hx, hy, 0.02, -hx, hy, 0.02,
      -hx, hy, 0.02, -hx, -hy, 0.02,
      -18, -hy - 3.5, 0.02, 18, -hy - 3.5, 0.02
    );
    const arr = new Float32Array(verts);
    bedVertCount = arr.length / 3;
    gl.bindBuffer(gl.ARRAY_BUFFER, bedBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, arr, gl.STATIC_DRAW);
  }

  function append3DArrowLines(arr, ox, oy, oz, dx, dy, dz, lengthMm) {
    if (lengthMm < 0.8) return;
    const dl = Math.hypot(dx, dy, dz) || 1.0;
    const ux = dx / dl, uy = dy / dl, uz = dz / dl;
    const ex = ox + ux * lengthMm, ey = oy + uy * lengthMm, ez = oz + uz * lengthMm;
    arr.push(ox, oy, oz, ex, ey, ez);

    // Build two perpendicular wing vectors for crisp 3D arrowhead
    let px = -uy, py = ux, pz = 0.0;
    if (Math.hypot(px, py) < 0.15) { px = 1.0; py = 0.0; pz = 0.0; }
    const pl = Math.hypot(px, py, pz) || 1.0;
    px /= pl; py /= pl; pz /= pl;
    const qx = uy * pz - uz * py, qy = uz * px - ux * pz, qz = ux * py - uy * px;

    const headLen = Math.min(4.8, 0.26 * lengthMm);
    const headRad = 0.45 * headLen;
    const bx = ex - ux * headLen, by = ey - uy * headLen, bz = ez - uz * headLen;
    arr.push(
      ex, ey, ez, bx + px * headRad, by + py * headRad, bz + pz * headRad,
      ex, ey, ez, bx - px * headRad, by - py * headRad, bz - pz * headRad,
      ex, ey, ez, bx + qx * headRad, by + qy * headRad, bz + qz * headRad,
      ex, ey, ez, bx - qx * headRad, by - qy * headRad, bz - qz * headRad
    );
  }

  function drawDynamicLines(vpMat, coords, r, g, b, a) {
    if (!gl || !lineProg || !coords.length) return;
    const arr = new Float32Array(coords);
    gl.useProgram(lineProg);
    gl.uniformMatrix4fv(gl.getUniformLocation(lineProg, "u_mvp"), false, vpMat);
    gl.uniform4f(gl.getUniformLocation(lineProg, "u_color"), r, g, b, a);
    const loc = gl.getAttribLocation(lineProg, "a_pos");
    gl.bindBuffer(gl.ARRAY_BUFFER, dynLineBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, arr, gl.DYNAMIC_DRAW);
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 3, gl.FLOAT, false, 0, 0);
    gl.drawArrays(gl.LINES, 0, arr.length / 3);
  }

  function drawPartInstance(vpMat, eye, partKey, modelMat, albedo, rough, metal, jamPulse) {
    const part = gpuParts[partKey];
    if (!part || part.indexCount <= 0) return;

    gl.useProgram(meshProg);
    gl.uniformMatrix4fv(gl.getUniformLocation(meshProg, "u_vp"), false, vpMat);
    gl.uniformMatrix4fv(gl.getUniformLocation(meshProg, "u_model"), false, modelMat);
    gl.uniform3fv(gl.getUniformLocation(meshProg, "u_eye"), eye);
    gl.uniform3fv(gl.getUniformLocation(meshProg, "u_albedo"), albedo);
    gl.uniform1f(gl.getUniformLocation(meshProg, "u_roughness"), rough);
    gl.uniform1f(gl.getUniformLocation(meshProg, "u_metallic"), metal);
    gl.uniform1f(gl.getUniformLocation(meshProg, "u_heatmap"), state.heatmap ? 1.0 : 0.0);
    gl.uniform1f(gl.getUniformLocation(meshProg, "u_jamPulse"), jamPulse);

    const maxH = state.params.face_width_mm + Math.max(
      state.params.pinion.hub_enabled ? state.params.pinion.hub_height_mm : 0,
      state.params.gear.hub_enabled ? state.params.gear.hub_height_mm : 0
    ) + 2.0;
    const maxY = Math.max(state.geom.pinion.tip_radius_mm, state.geom.gear.tip_radius_mm) + 15.0;

    let clipMode = 0.0;
    let clipVal = 9999.0;
    if (state.crossCutPct > 0) {
      if (state.crossCutAxis === "z") {
        clipMode = 1.0;
        clipVal = maxH * (1.0 - (state.crossCutPct / 105.0));
      } else {
        clipMode = 2.0;
        clipVal = maxY * (1.0 - 2.0 * (state.crossCutPct / 100.0));
      }
    }
    gl.uniform1f(gl.getUniformLocation(meshProg, "u_clipMode"), clipMode);
    gl.uniform1f(gl.getUniformLocation(meshProg, "u_clipVal"), clipVal);

    const locPos = gl.getAttribLocation(meshProg, "a_pos");
    const locNrm = gl.getAttribLocation(meshProg, "a_nrm");
    const locOvh = gl.getAttribLocation(meshProg, "a_ovh");

    gl.bindBuffer(gl.ARRAY_BUFFER, part.pos);
    gl.enableVertexAttribArray(locPos);
    gl.vertexAttribPointer(locPos, 3, gl.FLOAT, false, 0, 0);

    if (locNrm >= 0) {
      gl.bindBuffer(gl.ARRAY_BUFFER, part.nrm);
      gl.enableVertexAttribArray(locNrm);
      gl.vertexAttribPointer(locNrm, 3, gl.FLOAT, false, 0, 0);
    }
    if (locOvh >= 0) {
      gl.bindBuffer(gl.ARRAY_BUFFER, part.ovh);
      gl.enableVertexAttribArray(locOvh);
      gl.vertexAttribPointer(locOvh, 1, gl.FLOAT, false, 0, 0);
    }

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, part.idx);
    gl.drawElements(gl.TRIANGLES, part.indexCount, part.indexType, 0);

    if (state.wireframe && part.wireCount > 0 && state.crossCutPct === 0) {
      const mvp = mat4Multiply(vpMat, modelMat);
      gl.useProgram(lineProg);
      gl.uniformMatrix4fv(gl.getUniformLocation(lineProg, "u_mvp"), false, mvp);
      gl.uniform4f(gl.getUniformLocation(lineProg, "u_color"), 0.0, 0.0, 0.0, 0.35);
      const locL = gl.getAttribLocation(lineProg, "a_pos");
      gl.bindBuffer(gl.ARRAY_BUFFER, part.wire);
      gl.enableVertexAttribArray(locL);
      gl.vertexAttribPointer(locL, 3, gl.FLOAT, false, 0, 0);
      gl.drawArrays(gl.LINES, 0, part.wireCount);
    }
  }

  function renderWebGLFrame(nowMs) {
    if (!gl || !meshProg || !lineProg || !state.geom) return;
    const canvas = gl.canvas;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const w = Math.max(1, Math.floor((canvas.clientWidth || 640) * dpr));
    const h = Math.max(1, Math.floor((canvas.clientHeight || 360) * dpr));
    if (canvas.width !== w || canvas.height !== h) {
      canvas.width = w;
      canvas.height = h;
    }

    gl.viewport(0, 0, w, h);
    gl.enable(gl.DEPTH_TEST);
    gl.disable(gl.CULL_FACE);

    if (state.theme === "light") gl.clearColor(0.84, 0.88, 0.93, 1.0);
    else gl.clearColor(0.095, 0.11, 0.135, 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    const cosP = Math.cos(camera.pitch);
    const eye = [
      camera.target[0] + camera.distance * cosP * Math.cos(camera.yaw),
      camera.target[1] + camera.distance * cosP * Math.sin(camera.yaw),
      camera.target[2] + camera.distance * Math.sin(camera.pitch)
    ];

    const proj = mat4Perspective(38.0 * DEG2RAD, w / h, 2.0, 2600.0);
    const view = mat4LookAtZUp(eye, camera.target);
    const vp = mat4Multiply(proj, view);

    // 1. Draw Printer Build Plate Grid
    if (bedVertCount > 0) {
      gl.useProgram(lineProg);
      gl.uniformMatrix4fv(gl.getUniformLocation(lineProg, "u_mvp"), false, vp);
      const fits = state.clientReport ? state.clientReport.printability.fits_bed : true;
      if (!fits) gl.uniform4f(gl.getUniformLocation(lineProg, "u_color"), 0.98, 0.26, 0.26, 0.82);
      else if (state.theme === "light") gl.uniform4f(gl.getUniformLocation(lineProg, "u_color"), 0.34, 0.44, 0.54, 0.45);
      else gl.uniform4f(gl.getUniformLocation(lineProg, "u_color"), 0.0, 0.72, 0.62, 0.30);

      const locL = gl.getAttribLocation(lineProg, "a_pos");
      gl.bindBuffer(gl.ARRAY_BUFFER, bedBuffer);
      gl.enableVertexAttribArray(locL);
      gl.vertexAttribPointer(locL, 3, gl.FLOAT, false, 0, 0);
      gl.drawArrays(gl.LINES, 0, bedVertCount);
    }

    const g = state.geom;
    const p = state.params;
    const a = g.center_distance_mm;
    const ra1 = g.pinion.tip_radius_mm;
    const ra2 = g.gear.tip_radius_mm;
    const theta1 = state.theta1Rad;
    const theta2 = g.mesh_phase_g2_rad - theta1 * (g.pinion.teeth / g.gear.teeth);

    const isJammed = Boolean((state.clientReport && state.clientReport.fit.jammed) || state.liveCollision.collided);
    const jamPulse = isJammed ? (0.45 + 0.55 * Math.abs(Math.sin((nowMs || 0) * 0.007))) : 0.0;

    // Distinct CAD engineering colors: Pinion G1 = Orca Teal (#00bfa5), Gear G2 = Precision Steel Blue (#4f9cf9)
    const colG1 = [0.02, 0.74, 0.64];
    const colG2 = [0.31, 0.61, 0.96];
    const colJig = [0.38, 0.43, 0.50];
    const colGauge = [0.85, 0.62, 0.16];

    if (state.vpView === "meshed") {
      // Center pair bounding box on build plate
      const x1 = -0.5 * (a + ra2 - ra1);
      const x2 = x1 + a;

      // Subtle mechanical judder when jammed & playing
      const judder = (isJammed && state.simPlaying) ? (0.015 * Math.sin((nowMs || 0) * 0.06)) : 0.0;

      const m1 = mat4TranslateRotateZ(x1, 0.0, 0.0, theta1 + judder);
      const m2 = mat4TranslateRotateZ(x2, 0.0, 0.0, theta2 - judder);

      drawPartInstance(vp, eye, "pinion", m1, colG1, 0.28, 0.35, jamPulse);
      drawPartInstance(vp, eye, "gear", m2, colG2, 0.30, 0.42, jamPulse);

      // 3D Force Vector Arrows (Ft, Fr, Fa) at the Pitch Contact Point!
      if (state.showForces && state.clientReport) {
        const kin = state.clientReport.kinematics;
        const px = x1 + g.pinion.working_pitch_radius_mm;
        const py = 0.0;
        const pz = 0.5 * p.face_width_mm;
        const dirSgn = p.sim_direction === "cw" ? -1.0 : 1.0;

        const baseScale = Math.max(10.0, Math.min(34.0, 0.42 * (ra1 + ra2)));
        const ftLen = baseScale;
        const frLen = Math.max(4.0, ftLen * Math.tan(state.clientReport.loa.alphaWRad));

        const ftLines = [];
        append3DArrowLines(ftLines, px, py, pz, 0.0, dirSgn, 0.0, ftLen);
        drawDynamicLines(vp, ftLines, 0.05, 0.92, 0.65, 1.0); // Emerald Ft

        const frLines = [];
        append3DArrowLines(frLines, px, py, pz, 1.0, 0.0, 0.0, frLen);
        drawDynamicLines(vp, frLines, 1.0, 0.72, 0.12, 1.0); // Gold Fr

        if (p.gear_type === "helical" && g.beta_deg > 0.2) {
          const faLen = Math.min(42.0, ftLen * Math.tan(g.beta_rad));
          const handSgn = p.helix_hand === "right" ? 1.0 : -1.0;
          const faLines = [];
          append3DArrowLines(faLines, px, py, pz, 0.0, 0.0, dirSgn * handSgn, faLen);
          drawDynamicLines(vp, faLines, 0.98, 0.32, 0.58, 1.0); // Magenta Axial Thrust Fa!
        } else if (p.gear_type === "herringbone" && g.beta_deg > 0.2) {
          // Balanced opposing V-thrust arrows canceling at mid-plane z = b/2!
          const halfZ = 0.46 * p.face_width_mm;
          const hbLines = [];
          append3DArrowLines(hbLines, px, py + 2.5, p.face_width_mm + 4.0, 0.0, 0.0, -1.0, Math.max(4.5, halfZ * 0.75));
          append3DArrowLines(hbLines, px, py + 2.5, -4.0, 0.0, 0.0, 1.0, Math.max(4.5, halfZ * 0.75));
          drawDynamicLines(vp, hbLines, 0.20, 0.90, 0.48, 0.95); // Balanced green opposing arrows
        }
      }
    } else if (state.vpView === "fit_kit") {
      // Interactive 4-piece Fit-Test Kit mounted on 2-pin jig + Bore Gauge in front!
      const osc = Math.sin(theta1 * 2.0) * (1.25 / Math.max(6, g.pinion.teeth)) * Math.PI;
      const oscG2 = g.mesh_phase_g2_rad - osc * (g.pinion.teeth / g.gear.teeth);
      const jigY = 10.0;
      const gaugeY = -18.0;

      drawPartInstance(vp, eye, "jig_base", mat4TranslateRotateZ(0.0, jigY, 0.0, 0.0), colJig, 0.45, 0.25, 0.0);
      drawPartInstance(vp, eye, "sector_pinion", mat4TranslateRotateZ(-0.5 * a, jigY, 3.05, osc), colG1, 0.28, 0.35, jamPulse);
      drawPartInstance(vp, eye, "sector_gear", mat4TranslateRotateZ(0.5 * a, jigY, 3.05, oscG2), colG2, 0.30, 0.42, jamPulse);
      drawPartInstance(vp, eye, "bore_gauge", mat4TranslateRotateZ(0.0, gaugeY, 0.0, 0.0), colGauge, 0.38, 0.22, 0.0);
    } else {
      // "plater" view: shows exact print-ready separated layout matching `export_target`
      const target = p.export_target;
      const gap = 8.0;
      if (target === "pinion_only") {
        drawPartInstance(vp, eye, "pinion", mat4TranslateRotateZ(0, 0, 0, 0), colG1, 0.28, 0.35, 0);
      } else if (target === "gear_only") {
        drawPartInstance(vp, eye, "gear", mat4TranslateRotateZ(0, 0, 0, 0), colG2, 0.30, 0.42, 0);
      } else if (target === "fit_test_kit") {
        drawPartInstance(vp, eye, "jig_base", mat4TranslateRotateZ(0, 22, 0, 0), colJig, 0.45, 0.25, 0);
        drawPartInstance(vp, eye, "sector_pinion", mat4TranslateRotateZ(-26, -12, 0, 0), colG1, 0.28, 0.35, 0);
        drawPartInstance(vp, eye, "sector_gear", mat4TranslateRotateZ(26, -12, 0, 0), colG2, 0.30, 0.42, 0);
        drawPartInstance(vp, eye, "bore_gauge", mat4TranslateRotateZ(0, -44, 0, 0), colGauge, 0.38, 0.22, 0);
      } else if (target === "full_suite") {
        const totW = 2 * ra1 + gap + 2 * ra2;
        const x1 = -0.5 * totW + ra1;
        const x2 = 0.5 * totW - ra2;
        const yOff = Math.max(ra1, ra2) * 0.45 + 12.0;
        drawPartInstance(vp, eye, "pinion", mat4TranslateRotateZ(x1, yOff, 0, 0), colG1, 0.28, 0.35, 0);
        drawPartInstance(vp, eye, "gear", mat4TranslateRotateZ(x2, yOff, 0, 0), colG2, 0.30, 0.42, 0);
        drawPartInstance(vp, eye, "jig_base", mat4TranslateRotateZ(-28, -yOff - 14, 0, 0), colJig, 0.45, 0.25, 0);
        drawPartInstance(vp, eye, "bore_gauge", mat4TranslateRotateZ(36, -yOff - 14, 0, 0), colGauge, 0.38, 0.22, 0);
      } else {
        // pair_separated
        const totW = 2 * ra1 + gap + 2 * ra2;
        const x1 = -0.5 * totW + ra1;
        const x2 = 0.5 * totW - ra2;
        drawPartInstance(vp, eye, "pinion", mat4TranslateRotateZ(x1, 0, 0, 0), colG1, 0.28, 0.35, 0);
        drawPartInstance(vp, eye, "gear", mat4TranslateRotateZ(x2, 0, 0, 0), colG2, 0.30, 0.42, 0);
      }
    }
  }

  function fitCameraToScene() {
    if (!state.geom) return;
    const ra1 = state.geom.pinion.tip_radius_mm;
    const ra2 = state.geom.gear.tip_radius_mm;
    const a = state.geom.center_distance_mm;
    const b = state.params.face_width_mm;
    const spanXY = Math.max(a + ra1 + ra2, 55.0);
    camera.target = [0.0, 0.0, b * 0.45];
    camera.distance = Math.max(85.0, Math.min(950.0, spanXY * 1.65 + b * 1.2));
    requestRender();
  }

  function bindViewportEvents(canvas) {
    let dragging = false;
    let panMode = false;
    let lastX = 0, lastY = 0;

    canvas.addEventListener("contextmenu", function (e) { e.preventDefault(); });
    canvas.addEventListener("pointerdown", function (e) {
      dragging = true;
      panMode = (e.button === 1 || e.button === 2 || e.shiftKey);
      lastX = e.clientX;
      lastY = e.clientY;
      canvas.setPointerCapture?.(e.pointerId);
    });
    canvas.addEventListener("pointermove", function (e) {
      if (!dragging) return;
      const dx = e.clientX - lastX;
      const dy = e.clientY - lastY;
      lastX = e.clientX;
      lastY = e.clientY;

      if (panMode) {
        const panScale = camera.distance * 0.0014;
        const rx = -Math.sin(camera.yaw), ry = Math.cos(camera.yaw);
        camera.target[0] -= dx * rx * panScale;
        camera.target[1] -= dx * ry * panScale;
        camera.target[2] += dy * panScale;
      } else {
        camera.yaw -= dx * 0.0085;
        camera.pitch = Math.max(-1.48, Math.min(1.48, camera.pitch + dy * 0.0075));
      }
      requestRender();
    });
    const endDrag = function (e) {
      dragging = false;
      canvas.releasePointerCapture?.(e.pointerId);
    };
    canvas.addEventListener("pointerup", endDrag);
    canvas.addEventListener("pointercancel", endDrag);

    canvas.addEventListener("wheel", function (e) {
      e.preventDefault();
      camera.distance = Math.max(35.0, Math.min(1200.0, camera.distance * Math.exp(e.deltaY * 0.0011)));
      requestRender();
    }, { passive: false });

    canvas.addEventListener("dblclick", fitCameraToScene);

    if (typeof ResizeObserver !== "undefined") {
      const ro = new ResizeObserver(function () {
        requestRender();
        draw2DLoupe(performance.now());
      });
      ro.observe(canvas);
    }
  }

  // ==========================================================================
  // 9. Synchronized High-DPI 2D Tooth-Mesh Loupe (`#loupe-canvas`)
  // ==========================================================================
  function draw2DLoupe(nowMs) {
    if (state.loupeCollapsed) return;
    const canvas = document.getElementById("loupe-canvas");
    if (!canvas || !canvas.getContext || !state.geom || !state.contourG1 || !state.contourG2) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const w = canvas.clientWidth || 640;
    const h = canvas.clientHeight || 168;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const cw = Math.max(1, Math.floor(w * dpr));
    const ch = Math.max(1, Math.floor(h * dpr));
    if (canvas.width !== cw || canvas.height !== ch) {
      canvas.width = cw;
      canvas.height = ch;
    }

    const g = state.geom;
    const p = state.params;
    const rep = state.clientReport;
    const a = g.center_distance_mm;
    const rw1 = g.pinion.working_pitch_radius_mm;
    const rw2 = g.gear.working_pitch_radius_mm;
    const rb1 = g.pinion.base_radius_mm;
    const rb2 = g.gear.base_radius_mm;

    const theta1 = state.theta1Rad;
    const theta2 = g.mesh_phase_g2_rad - theta1 * (g.pinion.teeth / g.gear.teeth);

    // Live exact 2D meshing window collision & clearance check
    state.liveCollision = checkLive2DMeshCollision(
      state.contourG1,
      state.contourG2,
      theta1,
      theta2,
      a,
      g.m_n,
      g.pinion.pitch_radius_mm
    );
    const isJammed = Boolean(state.liveCollision.collided || (rep && rep.fit.jammed));
    const jamBadge = document.getElementById("loupe-jam-badge");
    if (jamBadge) jamBadge.classList.toggle("visible", isJammed);

    ctx.save();
    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, w, h);

    const isLight = state.theme === "light";
    ctx.fillStyle = isLight ? "#f4f7fb" : "#14171d";
    ctx.fillRect(0, 0, w, h);

    // Coordinate transform centered right on the working Pitch Point P = (rw1, 0)!
    const cxScreen = w * 0.44;
    const cyScreen = h * 0.52;
    const viewWindowMm = Math.max(4.5 * g.m_n, 7.0) / state.loupeZoom;
    const pxPerMm = (h * 0.45) / viewWindowMm;

    const toSX = function (wx) { return cxScreen + (wx - rw1) * pxPerMm; };
    const toSY = function (wy) { return cyScreen - wy * pxPerMm; };

    // Subtle engineering grid in mm around pitch point
    const gridStepMm = g.m_n >= 2.0 ? 2.0 : 1.0;
    ctx.strokeStyle = isLight ? "rgba(60, 80, 110, 0.09)" : "rgba(255, 255, 255, 0.05)";
    ctx.lineWidth = 1;
    const spanXMm = (w / pxPerMm) * 0.65;
    for (let gx = Math.floor((rw1 - spanXMm) / gridStepMm) * gridStepMm; gx <= rw1 + spanXMm; gx += gridStepMm) {
      const sx = toSX(gx);
      ctx.beginPath(); ctx.moveTo(sx, 0); ctx.lineTo(sx, h); ctx.stroke();
    }
    for (let gy = -Math.ceil(viewWindowMm * 1.4 / gridStepMm) * gridStepMm; gy <= viewWindowMm * 1.4; gy += gridStepMm) {
      const sy = toSY(gy);
      ctx.beginPath(); ctx.moveTo(0, sy); ctx.lineTo(w, sy); ctx.stroke();
    }

    // Centerline O1 -> O2
    ctx.save();
    ctx.strokeStyle = isLight ? "rgba(80, 100, 125, 0.25)" : "rgba(255, 255, 255, 0.14)";
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(0, cyScreen);
    ctx.lineTo(w, cyScreen);
    ctx.stroke();
    ctx.restore();

    // Draw Gear 1 (Teal) and Gear 2 (Steel Blue) exact 2D involute contours
    const drawContour = function (c, ox, rotRad, fillCol, strokeCol) {
      const cs = Math.cos(rotRad), sn = Math.sin(rotRad);
      ctx.beginPath();
      for (let i = 0; i < c.count; i++) {
        const wx = ox + c.xs[i] * cs - c.ys[i] * sn;
        const wy = c.xs[i] * sn + c.ys[i] * cs;
        const sx = toSX(wx), sy = toSY(wy);
        if (i === 0) ctx.moveTo(sx, sy);
        else ctx.lineTo(sx, sy);
      }
      ctx.closePath();
      ctx.fillStyle = fillCol;
      ctx.fill();
      ctx.strokeStyle = strokeCol;
      ctx.lineWidth = 1.7;
      ctx.stroke();
    };

    drawContour(
      state.contourG1,
      0.0,
      theta1,
      isJammed ? "rgba(255, 65, 65, 0.22)" : (isLight ? "rgba(0, 150, 136, 0.22)" : "rgba(0, 191, 165, 0.24)"),
      isJammed ? "#ff5252" : (isLight ? "#00796b" : "#00bfa5")
    );

    drawContour(
      state.contourG2,
      a,
      theta2,
      isJammed ? "rgba(255, 90, 65, 0.20)" : (isLight ? "rgba(37, 99, 235, 0.18)" : "rgba(79, 156, 249, 0.22)"),
      isJammed ? "#ff6e40" : (isLight ? "#1d4ed8" : "#4f9cf9")
    );

    // Dashed Working Pitch Circles (rw1, rw2) & Dotted Base Circles (rb1, rb2)
    const drawCircleArc = function (ox, rad, dash, color) {
      ctx.save();
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.1;
      ctx.setLineDash(dash);
      ctx.beginPath();
      ctx.arc(toSX(ox), toSY(0), rad * pxPerMm, 0, TWO_PI);
      ctx.stroke();
      ctx.restore();
    };
    drawCircleArc(0.0, rw1, [5, 4], isLight ? "rgba(0, 137, 123, 0.65)" : "rgba(0, 229, 195, 0.55)");
    drawCircleArc(a, rw2, [5, 4], isLight ? "rgba(37, 99, 235, 0.65)" : "rgba(110, 178, 255, 0.55)");
    drawCircleArc(0.0, rb1, [2, 3], isLight ? "rgba(0, 105, 92, 0.42)" : "rgba(0, 191, 165, 0.35)");
    drawCircleArc(a, rb2, [2, 3], isLight ? "rgba(30, 64, 175, 0.42)" : "rgba(79, 156, 249, 0.35)");

    // Tilted Pressure Line of Action & Live Moving Contact Points!
    if (rep && rep.loa) {
      const loa = rep.loa;
      const dirSign = p.sim_direction === "cw" ? -1.0 : 1.0;
      // Driving line of action unit vector u = (dirSign * sinAw, cosAw) or (-sinAw, -cosAw)
      // Check: when G1 rotates CW (theta1 decreasing, teeth move -Y at pitch point), G1 upper flank pushes -Y on G2:
      // Normal along LOA has tangent direction u = (sinAw, -cosAw) for CW and (sinAw, +cosAw) for CCW!
      const ux = Math.sin(loa.alphaWRad);
      const uy = dirSign * Math.cos(loa.alphaWRad);

      // Extended reference pressure line
      const ext = Math.max(loa.sEnd - loa.sStart, 3.0 * g.m_n) * 0.95;
      ctx.save();
      ctx.strokeStyle = isLight ? "rgba(217, 119, 6, 0.36)" : "rgba(255, 193, 7, 0.30)";
      ctx.setLineDash([3, 3]);
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(toSX(rw1 - ext * ux), toSY(-ext * uy));
      ctx.lineTo(toSX(rw1 + ext * ux), toSY(ext * uy));
      ctx.stroke();
      ctx.restore();

      // Active Contact Segment [sStart, sEnd]
      if (loa.sEnd > loa.sStart + 1e-4) {
        const sx0 = toSX(rw1 + loa.sStart * ux), sy0 = toSY(loa.sStart * uy);
        const sx1 = toSX(rw1 + loa.sEnd * ux), sy1 = toSY(loa.sEnd * uy);

        ctx.strokeStyle = isLight ? "#d97706" : "#ffc107";
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.moveTo(sx0, sy0);
        ctx.lineTo(sx1, sy1);
        ctx.stroke();

        // Entry & Exit limit ticks
        ctx.fillStyle = isLight ? "#d97706" : "#ffd54f";
        ctx.beginPath(); ctx.arc(sx0, sy0, 3.0, 0, TWO_PI); ctx.fill();
        ctx.beginPath(); ctx.arc(sx1, sy1, 3.0, 0, TWO_PI); ctx.fill();

        // Live Moving Contact Dots sliding along the Pressure Line of Action in exact phase!
        const pBt = loa.pBt;
        if (pBt > 1e-4 && !isJammed) {
          // Exact involute contact position along LOA for tooth k:
          // On G1, flank is at theta1 + k*(2*pi/Z1) +/- psiB1. Contact roll distance from T1 = rb1 * rollAngle
          const sBaseRef = -rw1 * Math.sin(loa.alphaWRad);
          const flankPhase = dirSign > 0
            ? (theta1 + g.pinion.base_half_angle_rad)
            : (-theta1 + g.pinion.base_half_angle_rad);
          const sPhase = rb1 * flankPhase + sBaseRef;

          const kMin = Math.floor((loa.sStart - sPhase) / pBt) - 1;
          const kMax = Math.ceil((loa.sEnd - sPhase) / pBt) + 1;
          for (let k = kMin; k <= kMax; k++) {
            const sVal = sPhase + k * pBt;
            if (sVal >= loa.sStart - 0.02 && sVal <= loa.sEnd + 0.02) {
              const cxPt = toSX(rw1 + sVal * ux);
              const cyPt = toSY(sVal * uy);
              ctx.beginPath();
              ctx.arc(cxPt, cyPt, 4.8, 0, TWO_PI);
              ctx.fillStyle = "#00e676";
              ctx.fill();
              ctx.lineWidth = 1.6;
              ctx.strokeStyle = "#ffffff";
              ctx.stroke();
            }
          }
        }
      }
    }

    // Pitch Point Crosshair P
    const pxS = toSX(rw1), pyS = toSY(0.0);
    ctx.strokeStyle = isLight ? "#111827" : "#ffffff";
    ctx.lineWidth = 1.3;
    ctx.beginPath();
    ctx.moveTo(pxS - 5, pyS); ctx.lineTo(pxS + 5, pyS);
    ctx.moveTo(pxS, pyS - 5); ctx.lineTo(pxS, pyS + 5);
    ctx.stroke();

    // Pulsing Red Collision Zone Highlights if Jammed / Overlapping!
    if (isJammed) {
      const pulseR = 7.0 + 4.5 * Math.abs(Math.sin((nowMs || 0) * 0.008));
      const pts = state.liveCollision.hitPoints.length
        ? state.liveCollision.hitPoints
        : [[rw1, 0.0]];
      for (let i = 0; i < pts.length; i++) {
        const hx = toSX(pts[i][0]), hy = toSY(pts[i][1]);
        ctx.beginPath();
        ctx.arc(hx, hy, pulseR, 0, TWO_PI);
        ctx.fillStyle = "rgba(255, 35, 35, 0.34)";
        ctx.fill();
        ctx.beginPath();
        ctx.arc(hx, hy, 3.6, 0, TWO_PI);
        ctx.fillStyle = "#ff1744";
        ctx.fill();
      }
    }

    // Right-Side Live Engineering Readout Card inside 2D Loupe
    if (rep && w >= 360) {
      const boxW = 178;
      const boxH = h - 16;
      const bx = w - boxW - 8;
      const by = 8;
      ctx.fillStyle = isLight ? "rgba(255, 255, 255, 0.88)" : "rgba(22, 25, 32, 0.86)";
      ctx.strokeStyle = isJammed ? "#ff5252" : (isLight ? "#cbd5e1" : "#323846");
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.roundRect ? ctx.roundRect(bx, by, boxW, boxH, 6) : ctx.rect(bx, by, boxW, boxH);
      ctx.fill();
      ctx.stroke();

      const lblCol = isLight ? "#64748b" : "#8b96a8";
      const valCol = isLight ? "#0f172a" : "#eef2f7";
      const rows = [
        [state.lang === "en" ? "Ratio" : "Relação", "1 : " + g.ratio.toFixed(2) + " (" + g.pinion.teeth + ":" + g.gear.teeth + ")"],
        [state.lang === "en" ? "Out Speed" : "Saída G2", rep.kinematics.rpm_g2.toFixed(1) + " RPM"],
        [state.lang === "en" ? "Contact ε_γ" : "Contato ε_γ", rep.contact.total_contact_ratio.toFixed(2) + " (εα " + rep.contact.transverse_ratio.toFixed(2) + ")"],
        [state.lang === "en" ? "Clearance" : "Folga Mín.", (isJammed ? "0.000 COLISÃO" : state.liveCollision.minDistMm.toFixed(3) + " mm")]
      ];

      const rowStep = Math.max(22, Math.floor((boxH - 10) / rows.length));
      ctx.font = "600 10px Segoe UI, sans-serif";
      for (let r = 0; r < rows.length; r++) {
        const ry = by + 16 + r * rowStep;
        ctx.fillStyle = lblCol;
        ctx.fillText(rows[r][0], bx + 8, ry);
        ctx.fillStyle = (r === 3 && isJammed) ? "#ff5252" : (r === 3 ? "#00c853" : valCol);
        ctx.font = "700 10.5px Consolas, monospace";
        const tw = ctx.measureText(rows[r][1]).width;
        ctx.fillText(rows[r][1], bx + boxW - tw - 8, ry);
        ctx.font = "600 10px Segoe UI, sans-serif";
      }
    }

    ctx.restore();
  }

  // ==========================================================================
  // 10. Animation Loop (60 FPS Micro-Simulation + Degree Scrubbing)
  // ==========================================================================
  let rafId = 0;

  function updateAngleReadoutsOnly() {
    let deg = ((state.theta1Rad * RAD2DEG) % 360.0 + 360.0) % 360.0;
    if (deg >= 359.95) deg = 0.0;
    const inp = document.getElementById("inp-sim-angle");
    const lbl = document.getElementById("lbl-sim-angle");
    if (inp && document.activeElement !== inp) inp.value = deg.toFixed(1);
    if (lbl) lbl.textContent = deg.toFixed(1) + "°";
  }

  function stepAnimation(nowMs) {
    rafId = 0;
    if (!state.lastFrameMs) state.lastFrameMs = nowMs;
    const dtSec = Math.min(0.08, Math.max(0.0, (nowMs - state.lastFrameMs) / 1000.0));
    state.lastFrameMs = nowMs;

    if (state.simPlaying) {
      const dirSign = state.params.sim_direction === "cw" ? -1.0 : 1.0;
      const omegaRadSec = (state.params.sim_rpm * TWO_PI) / 60.0;
      state.theta1Rad = (state.theta1Rad + dirSign * omegaRadSec * dtSec) % TWO_PI;
      if (state.theta1Rad < 0) state.theta1Rad += TWO_PI;
      updateAngleReadoutsOnly();
    }

    renderWebGLFrame(nowMs);
    draw2DLoupe(nowMs);

    const isJammed = Boolean((state.clientReport && state.clientReport.fit.jammed) || state.liveCollision.collided);
    if (state.simPlaying || isJammed) {
      requestRender();
    }
  }

  function requestRender() {
    if (rafId || typeof requestAnimationFrame === "undefined") return;
    rafId = requestAnimationFrame(stepAnimation);
  }

  // ==========================================================================
  // 11. Scene Rebuild, Dual Badges, Presets & Diagnostics Sync
  // ==========================================================================
  function recomputeKinematicsAndLoupeOnly() {
    state.geom = computeGearPairGeometry(state.params);
    state.clientReport = computeClientAnalysis(state.params, state.geom, state.printer);
    updateDerivedBadges();
    updateDiagnosticsUI();
    requestRender();
  }

  function rebuildScene(fastInteractive) {
    const p = state.params;
    const fast = Boolean(fastInteractive);
    state.geom = computeGearPairGeometry(p);
    state.contourG1 = buildGear2DContour(p, state.geom, "pinion", 12, 0.0);
    state.contourG2 = buildGear2DContour(p, state.geom, "gear", 12, 0.0);
    state.clientReport = computeClientAnalysis(p, state.geom, state.printer);

    if (gl) {
      uploadCollectorToPart("pinion", buildGear3DMeshData(p, state.geom, "pinion", fast));
      uploadCollectorToPart("gear", buildGear3DMeshData(p, state.geom, "gear", fast));

      if (state.vpView === "fit_kit" || (state.vpView === "plater" && (p.export_target === "fit_test_kit" || p.export_target === "full_suite"))) {
        uploadCollectorToPart("sector_pinion", buildFitKitSectorMesh(p, state.geom, "pinion"));
        uploadCollectorToPart("sector_gear", buildFitKitSectorMesh(p, state.geom, "gear"));
        const jg = buildFitKitJigAndGaugeMeshes(p, state.geom);
        uploadCollectorToPart("jig_base", jg.jig);
        uploadCollectorToPart("bore_gauge", jg.gauge);
      }
    }

    updateDerivedBadges();
    updateDiagnosticsUI();
    requestRender();
  }

  const sliderRefs = {};

  function buildSliderWidgets() {
    for (let i = 0; i < SLIDER_SPECS.length; i++) {
      const spec = SLIDER_SPECS[i];
      const host = document.querySelector('[data-slider="' + spec.path + '"]');
      if (!host) continue;

      const decs = spec.step < 0.05 ? 2 : (spec.step < 1 ? 1 : 0);
      const initVal = getByPath(state.params, spec.path);
      const dualHtml = spec.dualMm
        ? '<span class="dual-mm-badge" data-dual-badge="' + spec.path + '">0.00 mm</span>'
        : "";

      host.className = "ctrl-row";
      host.innerHTML =
        '<div class="ctrl-top">' +
          '<span class="ctrl-label" data-spec-label="' + spec.path + '">' + (state.lang === "en" ? spec.en : spec.pt) + '</span>' +
          '<div class="ctrl-val-wrap">' +
            dualHtml +
            '<input class="ctrl-num" type="number" min="' + spec.min + '" max="' + spec.max + '" step="' + spec.step + '" value="' + Number(initVal).toFixed(decs) + '" />' +
            '<span class="ctrl-unit">' + spec.unit + '</span>' +
          '</div>' +
        '</div>' +
        '<input class="orca-slider" type="range" min="' + spec.min + '" max="' + spec.max + '" step="' + spec.step + '" value="' + initVal + '" />';

      const rangeEl = host.querySelector('input[type="range"]');
      const numEl = host.querySelector('input[type="number"]');
      const labelEl = host.querySelector("[data-spec-label]");
      const dualEl = host.querySelector("[data-dual-badge]");

      sliderRefs[spec.path] = { spec: spec, rangeEl: rangeEl, numEl: numEl, labelEl: labelEl, dualEl: dualEl, decs: decs };

      const applyParamEdit = function (rawVal, isLiveDrag) {
        if (spec.path === "helix_angle_deg" && rawVal > 0.5 && state.params.gear_type === "spur") {
          state.params.gear_type = "helical";
        }
        setByPath(state.params, spec.path, rawVal);
        state.params = normalizeParams(state.params);
        state.hostReport = null;
        const normV = getByPath(state.params, spec.path);
        if (numEl && document.activeElement !== numEl) numEl.value = Number(normV).toFixed(decs);
        if (rangeEl && document.activeElement !== rangeEl) rangeEl.value = String(normV);

        // Fast rigid-body update when only center_distance_offset_mm or input_torque_nm changes!
        if (spec.path === "center_distance_offset_mm" || spec.path === "input_torque_nm") {
          recomputeKinematicsAndLoupeOnly();
        } else {
          rebuildScene(isLiveDrag);
        }
      };

      if (rangeEl) {
        rangeEl.addEventListener("pointerdown", function () {
          beginUndoGesture();
          state.isInteracting = true;
        });
        rangeEl.addEventListener("input", function () {
          applyParamEdit(Number(rangeEl.value), true);
        });
        const finishRange = function () {
          if (!state.isInteracting) return;
          state.isInteracting = false;
          commitUndoGesture();
          rebuildScene(false);
          scheduleHostAnalyze();
        };
        rangeEl.addEventListener("pointerup", finishRange);
        rangeEl.addEventListener("change", finishRange);
      }

      if (numEl) {
        numEl.addEventListener("change", function () {
          const before = deepClone(state.params);
          applyParamEdit(Number(numEl.value), false);
          numEl.value = Number(getByPath(state.params, spec.path)).toFixed(decs);
          pushUndoSnapshot(before);
          scheduleHostAnalyze();
        });
      }
    }
  }

  function syncSlidersOnly() {
    const paths = Object.keys(sliderRefs);
    for (let i = 0; i < paths.length; i++) {
      const ref = sliderRefs[paths[i]];
      const v = getByPath(state.params, paths[i]);
      if (v === undefined) continue;
      if (ref.rangeEl) ref.rangeEl.value = String(v);
      if (ref.numEl) ref.numEl.value = Number(v).toFixed(ref.decs);
    }
  }

  function updateDerivedBadges() {
    const p = state.params;
    const g = state.geom || computeGearPairGeometry(p);
    const mN = p.module_mm;

    // 1. Dual Tooth-Height Badges (`Factor × | Real mm`) + Total Tooth Height `h = (2*h_a* + c*) * m_n`
    const dualKeys = ["addendum_coeff", "clearance_coeff", "root_fillet_coeff", "tip_chamfer_coeff"];
    for (let i = 0; i < dualKeys.length; i++) {
      const k = dualKeys[i];
      const ref = sliderRefs[k];
      if (ref && ref.dualEl) {
        const factor = Number(p[k]);
        const realMm = factor * mN;
        ref.dualEl.textContent = factor.toFixed(2) + "× (" + realMm.toFixed(2) + " mm)";
      }
    }
    const totalToothMm = (2.0 * p.addendum_coeff + p.clearance_coeff) * mN;
    const hBadge = document.getElementById("badge-total-tooth-h");
    if (hBadge) hBadge.textContent = "h = " + totalToothMm.toFixed(2) + " mm";

    const tpBtns = document.querySelectorAll("[data-tooth-preset]");
    for (let i = 0; i < tpBtns.length; i++) {
      const kind = tpBtns[i].getAttribute("data-tooth-preset");
      const match =
        (kind === "iso" && Math.abs(p.addendum_coeff - 1.00) < 0.02) ||
        (kind === "stub" && Math.abs(p.addendum_coeff - 0.75) < 0.02) ||
        (kind === "high" && Math.abs(p.addendum_coeff - 1.20) < 0.02);
      tpBtns[i].classList.toggle("active", match);
    }

    // 2. Ratio, Gear Type, Helix Pills & Hand
    const ratioBadge = document.getElementById("badge-ratio");
    if (ratioBadge) {
      ratioBadge.textContent = "1 : " + g.ratio.toFixed(2) + " (" + p.pinion.teeth + ":" + p.gear.teeth + ")";
    }

    const gtBtns = document.querySelectorAll("[data-gear-type]");
    for (let i = 0; i < gtBtns.length; i++) {
      gtBtns[i].classList.toggle("active", gtBtns[i].getAttribute("data-gear-type") === p.gear_type);
    }

    const effBeta = effectiveHelixAngleDeg(p);
    const effBadge = document.getElementById("badge-eff-helix");
    if (effBadge) {
      effBadge.textContent = "β_eff " + effBeta.toFixed(1) + "°";
    }

    const hPills = document.querySelectorAll("[data-helix-pill]");
    for (let i = 0; i < hPills.length; i++) {
      const hv = Number(hPills[i].getAttribute("data-helix-pill"));
      const isAct = (hv === 0 && effBeta < 0.2) || (hv > 0 && p.gear_type !== "spur" && Math.abs(p.helix_angle_deg - hv) < 0.4);
      hPills[i].classList.toggle("active", isAct);
    }

    const handBtns = document.querySelectorAll("[data-helix-hand]");
    for (let i = 0; i < handBtns.length; i++) {
      handBtns[i].classList.toggle("active", handBtns[i].getAttribute("data-helix-hand") === p.helix_hand);
    }

    const modPills = document.querySelectorAll("[data-mod-pill]");
    for (let i = 0; i < modPills.length; i++) {
      const mv = Number(modPills[i].getAttribute("data-mod-pill"));
      modPills[i].classList.toggle("active", Math.abs(p.module_mm - mv) < 0.02);
    }

    // 3. Effective Profile Shifts Readout
    const shiftNote = document.getElementById("badge-eff-shifts");
    if (shiftNote) {
      const fmtS = function (v) { return (v >= 0 ? "+" : "") + v.toFixed(2); };
      shiftNote.textContent = "x₁ efetivo: " + fmtS(g.x1) + " · x₂ efetivo: " + fmtS(g.x2) +
        (g.pinion.undercut || g.gear.undercut ? " ⚠ Undercut" : " ✓ Sem Undercut");
    }

    // 4. Body Pane Visibility & Conditional Bore / Hub / Recess / Lightening Controls
    const isG1 = state.activeBodyTab === "pinion";
    const tabG1 = document.getElementById("btn-body-tab-pinion");
    const tabG2 = document.getElementById("btn-body-tab-gear");
    const paneG1 = document.getElementById("body-pane-pinion");
    const paneG2 = document.getElementById("body-pane-gear");
    if (tabG1) tabG1.classList.toggle("active", isG1);
    if (tabG2) tabG2.classList.toggle("active-g2", !isG1);
    if (paneG1) paneG1.style.display = isG1 ? "flex" : "none";
    if (paneG2) paneG2.style.display = isG1 ? "none" : "flex";

    const syncBodySubBoxes = function (who) {
      const b = p[who];
      const boreDims = document.getElementById("box-" + who + "-bore-dims");
      const dflat = document.getElementById("box-" + who + "-dflat");
      const kw = document.getElementById("box-" + who + "-keyway");
      const hub = document.getElementById("box-" + who + "-hub");
      const rec = document.getElementById("box-" + who + "-recess");
      const web = document.getElementById("box-" + who + "-web");
      const holes = document.getElementById("box-" + who + "-holes");

      if (boreDims) boreDims.style.display = b.bore_type === "none" ? "none" : "flex";
      if (dflat) dflat.style.display = (b.bore_type === "d_shaft" || b.bore_type === "double_d") ? "flex" : "none";
      if (kw) kw.style.display = b.bore_type === "keyway" ? "flex" : "none";
      if (hub) hub.style.display = b.hub_enabled ? "flex" : "none";
      if (rec) rec.style.display = b.recess_enabled ? "flex" : "none";
      if (web) web.style.display = b.lightening_mode === "web_recess" ? "flex" : "none";
      if (holes) holes.style.display = b.lightening_mode === "lightening_holes" ? "flex" : "none";
    };
    syncBodySubBoxes("pinion");
    syncBodySubBoxes("gear");

    // 5. Simulation Transport & Live Delta_a Bar Sync
    const playBtn = document.getElementById("btn-sim-play");
    if (playBtn) {
      playBtn.textContent = state.simPlaying
        ? (state.lang === "en" ? "⏸ Pause" : "⏸ Pausar")
        : (state.lang === "en" ? "▶ Play" : "▶ Girar");
    }
    const dirBtn = document.getElementById("btn-sim-dir");
    if (dirBtn) {
      dirBtn.textContent = p.sim_direction === "cw" ? "CW ↻" : "CCW ↺";
    }
    const rpmInp = document.getElementById("inp-sim-rpm");
    const rpmLbl = document.getElementById("lbl-sim-rpm");
    if (rpmInp && document.activeElement !== rpmInp) rpmInp.value = String(Math.round(p.sim_rpm));
    if (rpmLbl) rpmLbl.textContent = Math.round(p.sim_rpm) + " rpm";

    const daInp = document.getElementById("inp-sim-delta-a");
    const daLbl = document.getElementById("lbl-sim-delta-a");
    if (daInp && document.activeElement !== daInp) {
      daInp.value = String(Math.max(-1.0, Math.min(2.0, p.center_distance_offset_mm)));
    }
    if (daLbl) {
      const da = p.center_distance_offset_mm;
      daLbl.textContent = (da >= 0 ? "+" : "") + da.toFixed(2) + " mm";
      daLbl.style.color = da < -0.15 ? "var(--status-crit)" : "";
    }

    // 6. Export Target Helper Note
    const expNote = document.getElementById("export-target-note");
    if (expNote) {
      if (p.export_target === "fit_test_kit") expNote.textContent = tr("note_exp_kit");
      else if (p.export_target === "full_suite") expNote.textContent = tr("note_exp_full");
      else if (p.export_target === "pair_separated") expNote.textContent = tr("note_exp_pair");
      else expNote.textContent = tr("note_exp_single");
    }
  }

  function updateDiagnosticsUI() {
    const cRep = state.clientReport;
    if (!cRep) return;
    // Prefer host Python `analysis_result` when idle & fresh; fallback seamlessly to live JS solver while dragging!
    const rep = (!state.isInteracting && state.hostReport && state.hostReport.contact) ? state.hostReport : cRep;
    const contact = rep.contact || cRep.contact;
    const fit = rep.fit || cRep.fit;
    const kin = rep.kinematics || cRep.kinematics;
    const prt = rep.printability || cRep.printability;
    const isJammed = Boolean(fit.jammed || cRep.fit.jammed || state.liveCollision.collided);
    const status = isJammed ? "critical" : (rep.status || cRep.status || "ok");

    const setTxt = function (id, txt, color) {
      const el = document.getElementById(id);
      if (el) {
        el.textContent = txt;
        el.style.color = color || "";
      }
    };

    // Viewport Right HUD
    const hudPill = document.getElementById("hud-status-pill");
    const diagPill = document.getElementById("diag-status-pill");
    const cls = status === "critical" ? "crit" : (status === "warn" ? "warn" : "ok");
    const stText = status === "critical" ? tr("status_crit") : (status === "warn" ? tr("status_warn") : tr("status_ok"));
    if (hudPill) { hudPill.className = "hud-status-pill " + cls; hudPill.textContent = stText; }
    if (diagPill) { diagPill.className = "hud-status-pill " + cls; diagPill.textContent = stText; }

    setTxt("hud-cd", Number(fit.center_distance_mm).toFixed(2) + " mm");
    setTxt("hud-ft", Number(kin.tangential_force_n).toFixed(1) + " N");
    setTxt("hud-fr", Number(kin.radial_force_n).toFixed(1) + " N");
    const faVal = Number(kin.axial_force_n || 0);
    setTxt("hud-fa", faVal.toFixed(1) + " N", faVal > 0.5 ? "#f59e0b" : "var(--status-ok)");

    const thrustNote = document.getElementById("hud-thrust-note");
    if (thrustNote) {
      const balanced = Boolean(kin.axial_thrust_balanced);
      thrustNote.classList.toggle("axial-active", !balanced && faVal > 0.1);
      if (state.params.gear_type === "spur" || state.geom.beta_deg < 0.1) {
        thrustNote.textContent = tr("thrust_zero_spur");
      } else if (state.params.gear_type === "herringbone") {
        thrustNote.textContent = tr("thrust_zero_hb");
      } else {
        thrustNote.textContent = tr("thrust_helical_fmt")
          .replace("{fa}", faVal.toFixed(1))
          .replace("{b}", state.geom.beta_deg.toFixed(0));
      }
    }

    // Right Column Diagnostics Grid
    setTxt("dv-eps-a", Number(contact.transverse_ratio).toFixed(2), contact.transverse_ratio < 1.15 ? "var(--status-warn)" : "");
    setTxt("dv-eps-b", Number(contact.axial_overlap_ratio).toFixed(2));
    setTxt("dv-eps-g", Number(contact.total_contact_ratio).toFixed(2), "var(--orca-accent-hover)");
    setTxt("dv-loa", Number(contact.line_of_action_length_mm).toFixed(2) + " mm");

    const da = state.params.center_distance_offset_mm;
    setTxt("dv-cd", Number(fit.center_distance_mm).toFixed(2) + " (" + (da >= 0 ? "+" : "") + da.toFixed(2) + ")");
    const clrVal = isJammed ? 0.0 : Number(fit.min_tooth_clearance_mm);
    setTxt("dv-clr", isJammed ? "0.00 (COLISÃO)" : clrVal.toFixed(3) + " mm", isJammed ? "var(--status-crit)" : "var(--status-ok)");
    setTxt("dv-t2", Number(kin.torque_g2_nm).toFixed(2) + " N·m");
    setTxt("dv-rpm2", Number(kin.rpm_g2).toFixed(1) + " rpm · " + Number(kin.pitch_line_velocity_mm_s).toFixed(0) + " mm/s");

    const ovh = Number(prt.helix_overhang_deg || 0);
    setTxt("dv-ovh", ovh.toFixed(0) + "° " + (prt.supports_needed ? "⚠ Suporte" : "✓ Livre"), prt.supports_needed ? "var(--status-warn)" : "var(--status-ok)");
    setTxt("dv-walls", String(prt.recommended_wall_loops || 4) + " loops + Gyroid");
    setTxt("dv-wgt", "~" + Math.max(1, Math.round(prt.estimated_weight_g || 20)) + " g · " + Math.max(5, Math.round(prt.estimated_print_time_min || 25)) + " min");
    const fp = Array.isArray(prt.pair_footprint_mm) ? prt.pair_footprint_mm : [100, 60];
    setTxt("dv-bed", Math.round(fp[0]) + "×" + Math.round(fp[1]) + " mm", prt.fits_bed === false ? "var(--status-crit)" : "");

    // Issues List
    const issuesEl = document.getElementById("diag-issues-list");
    if (issuesEl) {
      issuesEl.innerHTML = "";
      const list = Array.isArray(rep.issues) && rep.issues.length ? rep.issues : cRep.issues;
      for (let i = 0; i < list.length; i++) {
        const it = list[i];
        const div = document.createElement("div");
        if (typeof it === "string") {
          div.className = "issue-item warn";
          div.textContent = it;
        } else {
          const sev = String(it.severity || "ok").toLowerCase();
          div.className = "issue-item " + (sev === "critical" || sev === "crit" ? "critical" : (sev === "warn" || sev === "warning" ? "warn" : "ok"));
          div.textContent = state.lang === "en" ? (it.en || it.message_en || it.pt || "") : (it.pt || it.message_pt || it.en || "");
        }
        issuesEl.appendChild(div);
      }
    }
  }

  function syncControlsFromState() {
    const p = state.params;
    const setVal = function (id, v) {
      const el = document.getElementById(id);
      if (el) el.value = v;
    };
    const setChk = function (id, v) {
      const el = document.getElementById(id);
      if (el) el.checked = Boolean(v);
    };

    setVal("inp-gear-name", p.name);
    setChk("chk-auto-shift", p.auto_profile_shift);
    setChk("chk-auto-slicer", p.auto_configure_slicer);
    setVal("sel-export-target", p.export_target);

    setVal("sel-pinion-bore-type", p.pinion.bore_type);
    setChk("chk-pinion-hub", p.pinion.hub_enabled);
    setChk("chk-pinion-recess", p.pinion.recess_enabled);
    setVal("sel-pinion-recess-side", p.pinion.recess_side);
    setVal("sel-pinion-lightening", p.pinion.lightening_mode);

    setVal("sel-gear-bore-type", p.gear.bore_type);
    setChk("chk-gear-hub", p.gear.hub_enabled);
    setChk("chk-gear-recess", p.gear.recess_enabled);
    setVal("sel-gear-recess-side", p.gear.recess_side);
    setVal("sel-gear-lightening", p.gear.lightening_mode);

    syncSlidersOnly();
    updateDerivedBadges();
  }

  function makePresetMiniSvg(presetParams) {
    const p = normalizeParams(presetParams);
    const gt = p.gear_type;
    let slash = "";
    if (gt === "helical") {
      slash = '<line x1="8" y1="21" x2="14" y2="11" stroke="#00bfa5" stroke-width="1.5"/>';
    } else if (gt === "herringbone") {
      slash = '<polyline points="8,21 12,16 8,11" fill="none" stroke="#f59e0b" stroke-width="1.4"/>';
    }
    return '<svg width="32" height="32" viewBox="0 0 32 32">' +
      '<circle cx="11" cy="16" r="7.5" fill="rgba(0,191,165,0.18)" stroke="#00bfa5" stroke-width="1.6" stroke-dasharray="2.5 1.5"/>' +
      '<circle cx="22.5" cy="16" r="5.5" fill="rgba(79,156,249,0.18)" stroke="#4f9cf9" stroke-width="1.5" stroke-dasharray="2.2 1.4"/>' +
      slash +
      '</svg>';
  }

  function matchesPresetCategory(item, filterCat) {
    if (filterCat === "all") return true;
    if (filterCat === "user") return Boolean(item._isUser);
    const cat = String(item.category || "").toLowerCase();
    const gt = item.params && item.params.gear_type ? item.params.gear_type : "";
    if (filterCat === "spur_ind") return gt === "spur" || cat.includes("ind") || cat.includes("stand") || cat.includes("prec");
    if (filterCat === "helical") return gt === "helical" || cat === "helical";
    if (filterCat === "herringbone") return gt === "herringbone" || cat === "herringbone";
    if (filterCat === "robotics_cal") return cat.includes("robot") || cat.includes("cal") || (item.params && item.params.export_target === "fit_test_kit");
    return true;
  }

  function renderPresetsGrid() {
    const gridEl = document.getElementById("presets-grid");
    if (!gridEl) return;
    gridEl.innerHTML = "";

    const combined = [];
    for (let i = 0; i < state.userPresets.length; i++) {
      combined.push(Object.assign({}, state.userPresets[i], { _isUser: true }));
    }
    for (let i = 0; i < state.builtinPresets.length; i++) {
      combined.push(Object.assign({}, state.builtinPresets[i], { _isUser: false }));
    }

    for (let i = 0; i < combined.length; i++) {
      const item = combined[i];
      if (!matchesPresetCategory(item, state.presetFilter)) continue;

      const card = document.createElement("div");
      card.className = "preset-card" + (item.id === state.activePresetId ? " active" : "");

      const title = state.lang === "en"
        ? (item.name_en || item.title_en || item.name || item.name_pt || "Preset")
        : (item.name_pt || item.title_pt || item.name || item.name_en || "Preset");
      const desc = state.lang === "en"
        ? (item.desc_en || item.description_en || item.category || "")
        : (item.desc_pt || item.description_pt || item.category || "");

      card.innerHTML =
        '<div class="preset-thumb">' + makePresetMiniSvg(item.params || {}) + '</div>' +
        '<div class="preset-meta">' +
          '<div class="preset-name"></div>' +
          '<div class="preset-sub"></div>' +
        '</div>';

      const nmEl = card.querySelector(".preset-name");
      const sbEl = card.querySelector(".preset-sub");
      if (nmEl) nmEl.textContent = title;
      if (sbEl) sbEl.textContent = desc;
      card.title = title + (desc ? " — " + desc : "");

      if (item._isUser) {
        const delBtn = document.createElement("button");
        delBtn.className = "preset-del-btn";
        delBtn.textContent = "×";
        delBtn.title = "Delete";
        delBtn.addEventListener("click", function (ev) {
          ev.stopPropagation();
          if (!sendToHost({ type: "preset_delete", id: item.id })) {
            state.userPresets = state.userPresets.filter(function (u) { return u.id !== item.id; });
            renderPresetsGrid();
          }
        });
        card.appendChild(delBtn);
      }

      card.addEventListener("click", function () {
        pushUndoSnapshot(state.params);
        state.activePresetId = item.id;
        state.params = normalizeParams(item.params);
        if (title) state.params.name = title.slice(0, 80);
        state.hostReport = null;

        // If calibration preset selected, showcase the 3D Fit-Test Kit automatically!
        if (state.params.export_target === "fit_test_kit") {
          setViewportMode("fit_kit");
        } else if (state.vpView === "fit_kit") {
          setViewportMode("meshed");
        }

        renderPresetsGrid();
        syncControlsFromState();
        rebuildScene(false);
        fitCameraToScene();
        scheduleHostAnalyze();
      });

      gridEl.appendChild(card);
    }
  }

  function setViewportMode(nextMode) {
    state.vpView = nextMode;
    const btns = document.querySelectorAll("[data-vp-view]");
    for (let i = 0; i < btns.length; i++) {
      btns[i].classList.toggle("active", btns[i].getAttribute("data-vp-view") === nextMode);
    }
    rebuildScene(false);
    fitCameraToScene();
  }

  function applyThemeAndLanguage() {
    if (typeof document === "undefined") return;
    document.documentElement.setAttribute("data-theme", state.theme);
    document.documentElement.setAttribute("lang", state.lang);
    if (document.body) document.body.setAttribute("data-mode", state.mode);

    const langBtn = document.getElementById("btn-lang");
    if (langBtn) langBtn.textContent = state.lang.toUpperCase();
    const themeBtn = document.getElementById("btn-theme");
    if (themeBtn) themeBtn.textContent = state.theme === "dark" ? "☾" : "☀";

    const printerText = document.getElementById("printer-pill-text");
    if (printerText) {
      const pr = state.printer;
      printerText.textContent =
        (pr.name || "Printer") + " · " +
        Math.round(pr.bed_x || 220) + "×" +
        Math.round(pr.bed_y || 220) + "×" +
        Math.round(pr.max_z || 250) + " mm · " +
        Number(pr.nozzle_mm || 0.4).toFixed(1) + "mm";
    }

    const nodes = document.querySelectorAll("[data-i18n]");
    for (let i = 0; i < nodes.length; i++) {
      const k = nodes[i].getAttribute("data-i18n");
      if (k) nodes[i].textContent = tr(k);
    }

    const paths = Object.keys(sliderRefs);
    for (let i = 0; i < paths.length; i++) {
      const ref = sliderRefs[paths[i]];
      if (ref.labelEl) ref.labelEl.textContent = state.lang === "en" ? ref.spec.en : ref.spec.pt;
    }

    updateDerivedBadges();
    renderPresetsGrid();
    updateDiagnosticsUI();
    requestRender();
  }

  function updateUndoButtons() {
    const u = document.getElementById("btn-undo");
    const r = document.getElementById("btn-redo");
    if (u) u.disabled = state.undoStack.length === 0;
    if (r) r.disabled = state.redoStack.length === 0;
  }

  function setActionButtonsBusy(busy) {
    state.busyAction = busy;
    const btns = document.querySelectorAll("[data-action]");
    for (let i = 0; i < btns.length; i++) btns[i].disabled = busy;
  }

  let toastTimer = null;
  function showToast(text, isError) {
    const el = document.getElementById("toast-banner");
    if (!el) return;
    el.textContent = text;
    el.classList.toggle("error", Boolean(isError));
    el.classList.add("visible");
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      el.classList.remove("visible");
    }, 3600);
  }

  function localPrintableRandomize(seedNum) {
    let s = (seedNum || Date.now()) >>> 0;
    const rand = function () {
      s = (Math.imul(s ^ (s >>> 15), 2246822519) + 3266489917) >>> 0;
      return (s >>> 0) / 4294967295.0;
    };
    const pick = function (arr) { return arr[Math.floor(rand() * arr.length)]; };
    const p = deepClone(state.params);
    p.gear_type = pick(["spur", "helical", "herringbone"]);
    p.helix_angle_deg = p.gear_type === "spur" ? 30.0 : pick([20, 25, 30, 35, 45]);
    p.module_mm = pick([1.25, 1.5, 1.75, 2.0, 2.5]);
    p.face_width_mm = pick([10, 12, 14, 16]);
    p.addendum_coeff = pick([0.85, 1.0, 1.0, 1.15]);
    p.center_distance_offset_mm = 0.0;
    p.auto_profile_shift = true;
    p.pinion.teeth = Math.floor(10 + rand() * 14);
    p.gear.teeth = Math.min(64, Math.round(p.pinion.teeth * pick([1.5, 2.0, 2.5, 3.0, 3.5])));
    p.pinion.bore_type = pick(["d_shaft", "round", "hex"]);
    p.gear.bore_type = pick(["round", "hex", "keyway"]);
    p.gear.lightening_mode = p.gear.teeth >= 26 ? "lightening_holes" : "solid";
    return normalizeParams(p);
  }

  function sanitizeExportStem(name) {
    const clean = String(name || "engrenagens").replace(/[^\w\-. ]+/g, "").trim().replace(/\s+/g, "_");
    return clean || "engrenagens";
  }

  // ==========================================================================
  // 12. UI Event Wiring & Boot
  // ==========================================================================
  function bindUIControls() {
    const on = function (id, evt, fn) {
      const el = document.getElementById(id);
      if (el) el.addEventListener(evt, fn);
    };

    on("inp-gear-name", "change", function (e) {
      state.params.name = String(e.target.value || "").trim().slice(0, 80) || "Par Engrenagens";
    });

    on("btn-undo", "click", performUndo);
    on("btn-redo", "click", performRedo);

    on("btn-randomize", "click", function () {
      const seed = Math.floor(Math.random() * 99999) + 1;
      if (!sendToHost({ type: "randomize", seed: seed, params: deepClone(state.params) })) {
        pushUndoSnapshot(state.params);
        state.params = localPrintableRandomize(seed);
        state.hostReport = null;
        syncControlsFromState();
        rebuildScene(false);
        fitCameraToScene();
        showToast(tr("toast_randomized"), false);
      }
    });

    on("btn-reset", "click", function () {
      pushUndoSnapshot(state.params);
      state.params = normalizeParams(JS_DEFAULT_PARAMS);
      state.hostReport = null;
      state.crossCutPct = 0;
      state.vpView = "meshed";
      const cutEl = document.getElementById("inp-cross-cut");
      const cutLbl = document.getElementById("lbl-cross-cut");
      if (cutEl) cutEl.value = "0";
      if (cutLbl) cutLbl.textContent = "Off";
      syncControlsFromState();
      setViewportMode("meshed");
      scheduleHostAnalyze();
    });

    on("btn-lang", "click", function () {
      state.lang = state.lang === "pt" ? "en" : "pt";
      applyThemeAndLanguage();
    });

    on("btn-theme", "click", function () {
      state.theme = state.theme === "dark" ? "light" : "dark";
      applyThemeAndLanguage();
    });

    // Dock Mode Tabs
    const tabBtns = document.querySelectorAll(".dock-tab-btn");
    for (let i = 0; i < tabBtns.length; i++) {
      tabBtns[i].addEventListener("click", function () {
        const tab = tabBtns[i].getAttribute("data-tab") || "gears";
        if (document.body) document.body.setAttribute("data-dock-tab", tab);
        for (let k = 0; k < tabBtns.length; k++) {
          tabBtns[k].classList.toggle("active", tabBtns[k] === tabBtns[i]);
        }
        requestRender();
      });
    }

    // Presets Save & Filter Chips
    on("btn-toggle-save-preset", "click", function () {
      const bar = document.getElementById("save-preset-bar");
      const inp = document.getElementById("inp-save-preset-name");
      if (bar) {
        const open = !bar.classList.contains("open");
        bar.classList.toggle("open", open);
        if (open && inp) {
          inp.value = state.params.name || "Meu Redutor";
          inp.focus?.();
        }
      }
    });

    on("btn-confirm-save-preset", "click", function () {
      const inp = document.getElementById("inp-save-preset-name");
      const bar = document.getElementById("save-preset-bar");
      const name = String(inp && inp.value ? inp.value : state.params.name || "Meu Redutor").trim() || "Meu Redutor";
      state.params.name = name.slice(0, 80);
      const nmMain = document.getElementById("inp-gear-name");
      if (nmMain) nmMain.value = state.params.name;

      if (!sendToHost({ type: "preset_save", name: state.params.name, params: deepClone(state.params) })) {
        state.userPresets.push({
          id: "local_" + Date.now(),
          name: state.params.name,
          name_pt: state.params.name,
          name_en: state.params.name,
          category: "user",
          params: deepClone(state.params)
        });
        renderPresetsGrid();
      }
      if (bar) bar.classList.remove("open");
      showToast(tr("toast_preset_saved"), false);
    });

    const filterChips = document.querySelectorAll("#preset-filters .filter-chip");
    for (let i = 0; i < filterChips.length; i++) {
      filterChips[i].addEventListener("click", function () {
        state.presetFilter = filterChips[i].getAttribute("data-cat") || "all";
        for (let k = 0; k < filterChips.length; k++) {
          filterChips[k].classList.toggle("active", filterChips[k] === filterChips[i]);
        }
        renderPresetsGrid();
      });
    }

    // Gear Type Buttons (`spur`, `helical`, `herringbone`)
    const gtBtns = document.querySelectorAll("[data-gear-type]");
    for (let i = 0; i < gtBtns.length; i++) {
      gtBtns[i].addEventListener("click", function () {
        const gt = gtBtns[i].getAttribute("data-gear-type");
        if (!gt || state.params.gear_type === gt) return;
        pushUndoSnapshot(state.params);
        state.params.gear_type = gt;
        if (gt !== "spur" && state.params.helix_angle_deg < 1.0) {
          state.params.helix_angle_deg = 30.0;
        }
        state.hostReport = null;
        syncControlsFromState();
        rebuildScene(false);
        scheduleHostAnalyze();
      });
    }

    // Helix Quick Pills (`0°`, `15°`, `30°`, `45°` — 1-click switches `spur` -> `helical` for 15/30/45!)
    const hPills = document.querySelectorAll("[data-helix-pill]");
    for (let i = 0; i < hPills.length; i++) {
      hPills[i].addEventListener("click", function () {
        const deg = Number(hPills[i].getAttribute("data-helix-pill"));
        pushUndoSnapshot(state.params);
        if (deg <= 0.0) {
          state.params.gear_type = "spur";
          state.params.helix_angle_deg = 0.0;
        } else {
          if (state.params.gear_type === "spur") {
            state.params.gear_type = "helical";
          }
          state.params.helix_angle_deg = deg;
        }
        state.hostReport = null;
        syncControlsFromState();
        rebuildScene(false);
        scheduleHostAnalyze();
      });
    }

    // Helix Hand (`right` / `left`)
    const handBtns = document.querySelectorAll("[data-helix-hand]");
    for (let i = 0; i < handBtns.length; i++) {
      handBtns[i].addEventListener("click", function () {
        const hh = handBtns[i].getAttribute("data-helix-hand");
        if (!hh || state.params.helix_hand === hh) return;
        pushUndoSnapshot(state.params);
        state.params.helix_hand = hh;
        state.hostReport = null;
        syncControlsFromState();
        rebuildScene(false);
        scheduleHostAnalyze();
      });
    }

    // Swap Z1 <-> Z2
    on("btn-swap-teeth", "click", function () {
      pushUndoSnapshot(state.params);
      const t1 = state.params.pinion.teeth;
      state.params.pinion.teeth = state.params.gear.teeth;
      state.params.gear.teeth = t1;
      state.hostReport = null;
      syncControlsFromState();
      rebuildScene(false);
      fitCameraToScene();
      scheduleHostAnalyze();
    });

    // Quick Module Pills
    const modPills = document.querySelectorAll("[data-mod-pill]");
    for (let i = 0; i < modPills.length; i++) {
      modPills[i].addEventListener("click", function () {
        const mv = Number(modPills[i].getAttribute("data-mod-pill"));
        pushUndoSnapshot(state.params);
        state.params.module_mm = mv;
        state.hostReport = null;
        syncControlsFromState();
        rebuildScene(false);
        fitCameraToScene();
        scheduleHostAnalyze();
      });
    }

    // Dual Tooth-Height Quick Presets (`ISO 1.00×`, `Stub 0.75×`, `High Contact 1.20×`)
    const tpBtns = document.querySelectorAll("[data-tooth-preset]");
    for (let i = 0; i < tpBtns.length; i++) {
      tpBtns[i].addEventListener("click", function () {
        const kind = tpBtns[i].getAttribute("data-tooth-preset");
        pushUndoSnapshot(state.params);
        if (kind === "stub") {
          state.params.addendum_coeff = 0.75;
          state.params.clearance_coeff = 0.25;
          state.params.root_fillet_coeff = 0.38;
          state.params.tip_chamfer_coeff = 0.05;
        } else if (kind === "high") {
          state.params.addendum_coeff = 1.20;
          state.params.clearance_coeff = 0.30;
          state.params.root_fillet_coeff = 0.26;
          state.params.tip_chamfer_coeff = 0.06;
        } else {
          state.params.addendum_coeff = 1.00;
          state.params.clearance_coeff = 0.25;
          state.params.root_fillet_coeff = 0.30;
          state.params.tip_chamfer_coeff = 0.06;
        }
        state.hostReport = null;
        syncControlsFromState();
        rebuildScene(false);
        scheduleHostAnalyze();
      });
    }

    on("chk-auto-shift", "change", function (e) {
      pushUndoSnapshot(state.params);
      state.params.auto_profile_shift = Boolean(e.target.checked);
      state.hostReport = null;
      rebuildScene(false);
      scheduleHostAnalyze();
    });

    // Pinion G1 vs Gear G2 Body Tabs & Controls
    on("btn-body-tab-pinion", "click", function () {
      state.activeBodyTab = "pinion";
      updateDerivedBadges();
    });
    on("btn-body-tab-gear", "click", function () {
      state.activeBodyTab = "gear";
      updateDerivedBadges();
    });

    const bindBodyControls = function (who) {
      on("sel-" + who + "-bore-type", "change", function (e) {
        pushUndoSnapshot(state.params);
        state.params[who].bore_type = e.target.value;
        state.params = normalizeParams(state.params);
        state.hostReport = null;
        updateDerivedBadges();
        rebuildScene(false);
        scheduleHostAnalyze();
      });
      on("chk-" + who + "-hub", "change", function (e) {
        pushUndoSnapshot(state.params);
        state.params[who].hub_enabled = Boolean(e.target.checked);
        updateDerivedBadges();
        rebuildScene(false);
        scheduleHostAnalyze();
      });
      on("chk-" + who + "-recess", "change", function (e) {
        pushUndoSnapshot(state.params);
        state.params[who].recess_enabled = Boolean(e.target.checked);
        updateDerivedBadges();
        rebuildScene(false);
        scheduleHostAnalyze();
      });
      on("sel-" + who + "-recess-side", "change", function (e) {
        pushUndoSnapshot(state.params);
        state.params[who].recess_side = e.target.value;
        rebuildScene(false);
        scheduleHostAnalyze();
      });
      on("sel-" + who + "-lightening", "change", function (e) {
        pushUndoSnapshot(state.params);
        state.params[who].lightening_mode = e.target.value;
        updateDerivedBadges();
        rebuildScene(false);
        scheduleHostAnalyze();
      });
    };
    bindBodyControls("pinion");
    bindBodyControls("gear");

    on("btn-608-gear", "click", function () {
      pushUndoSnapshot(state.params);
      state.params.gear.bore_type = "round";
      state.params.gear.bore_diameter_mm = 8.0;
      state.params.gear.recess_enabled = true;
      state.params.gear.recess_diameter_mm = 22.2;
      state.params.gear.recess_depth_mm = Math.min(7.0, Math.max(2.0, state.params.face_width_mm - 2.0));
      syncControlsFromState();
      rebuildScene(false);
      scheduleHostAnalyze();
    });

    // Viewport Toolbar Controls
    const vpBtns = document.querySelectorAll("[data-vp-view]");
    for (let i = 0; i < vpBtns.length; i++) {
      vpBtns[i].addEventListener("click", function () {
        setViewportMode(vpBtns[i].getAttribute("data-vp-view") || "meshed");
      });
    }

    on("btn-vp-heatmap", "click", function () {
      state.heatmap = !state.heatmap;
      const b = document.getElementById("btn-vp-heatmap");
      const leg = document.getElementById("heatmap-legend");
      if (b) b.classList.toggle("active", state.heatmap);
      if (leg) leg.classList.toggle("visible", state.heatmap);
      requestRender();
    });

    on("btn-vp-forces", "click", function () {
      state.showForces = !state.showForces;
      const b = document.getElementById("btn-vp-forces");
      if (b) b.classList.toggle("active", state.showForces);
      requestRender();
    });

    on("btn-vp-wire", "click", function () {
      state.wireframe = !state.wireframe;
      const b = document.getElementById("btn-vp-wire");
      if (b) b.classList.toggle("active", state.wireframe);
      requestRender();
    });

    // Camera Presets (`Perspectiva`, `Topo (Engrenamento)`, `Frontal (Hélice)`, `Reset`)
    const camBtns = document.querySelectorAll("[data-cam]");
    for (let i = 0; i < camBtns.length; i++) {
      camBtns[i].addEventListener("click", function () {
        const kind = camBtns[i].getAttribute("data-cam");
        if (kind === "iso") { camera.yaw = -0.72; camera.pitch = 0.56; fitCameraToScene(); }
        else if (kind === "top") { camera.yaw = -Math.PI * 0.5; camera.pitch = 1.47; fitCameraToScene(); }
        else if (kind === "front") { camera.yaw = -Math.PI * 0.5; camera.pitch = 0.08; fitCameraToScene(); }
        else if (kind === "reset") { camera.yaw = -0.72; camera.pitch = 0.56; fitCameraToScene(); }
      });
    }

    // Z / Y Cross-Section Clipping Bar
    on("lbl-cut-axis", "click", function () {
      state.crossCutAxis = state.crossCutAxis === "z" ? "y" : "z";
      const lbl = document.getElementById("lbl-cut-axis");
      if (lbl) lbl.textContent = state.crossCutAxis === "z" ? "✂ Corte Z" : "✂ Corte Y";
      requestRender();
    });

    on("inp-cross-cut", "input", function (e) {
      state.crossCutPct = clampInt(e.target.value, 0, 0, 100);
      const lbl = document.getElementById("lbl-cross-cut");
      if (lbl) lbl.textContent = state.crossCutPct === 0 ? "Off" : (state.crossCutPct + "%");
      requestRender();
    });

    on("btn-cut-half", "click", function () {
      state.crossCutPct = state.crossCutPct === 50 ? 0 : 50;
      const inp = document.getElementById("inp-cross-cut");
      const lbl = document.getElementById("lbl-cross-cut");
      if (inp) inp.value = String(state.crossCutPct);
      if (lbl) lbl.textContent = state.crossCutPct === 0 ? "Off" : "50%";
      requestRender();
    });

    // Micro-Simulation Transport Controls
    on("btn-sim-play", "click", function () {
      state.simPlaying = !state.simPlaying;
      state.lastFrameMs = 0;
      updateDerivedBadges();
      requestRender();
    });

    on("btn-sim-dir", "click", function () {
      state.params.sim_direction = state.params.sim_direction === "cw" ? "ccw" : "cw";
      updateDerivedBadges();
      requestRender();
    });

    on("inp-sim-rpm", "input", function (e) {
      state.params.sim_rpm = clampFloat(e.target.value, 24.0, 1.0, 300.0);
      recomputeKinematicsAndLoupeOnly();
    });
    on("inp-sim-rpm", "change", scheduleHostAnalyze);

    // Manual Degree Scrub Slider & Precision Step Buttons (`-1°`, `-0.2°`, `+0.2°`, `+1°`)
    on("inp-sim-angle", "input", function (e) {
      state.simPlaying = false;
      const deg = clampFloat(e.target.value, 0.0, 0.0, 360.0);
      state.theta1Rad = deg * DEG2RAD;
      updateAngleReadoutsOnly();
      updateDerivedBadges();
      requestRender();
    });

    const stepBtns = document.querySelectorAll("[data-angle-step]");
    for (let i = 0; i < stepBtns.length; i++) {
      stepBtns[i].addEventListener("click", function () {
        state.simPlaying = false;
        const deltaDeg = Number(stepBtns[i].getAttribute("data-angle-step") || 0);
        state.theta1Rad = ((state.theta1Rad + deltaDeg * DEG2RAD) % TWO_PI + TWO_PI) % TWO_PI;
        updateAngleReadoutsOnly();
        updateDerivedBadges();
        requestRender();
      });
    }

    // Live Center-Distance Offset (Delta_a) Slider in Simulation Bar!
    const simDa = document.getElementById("inp-sim-delta-a");
    if (simDa) {
      simDa.addEventListener("pointerdown", beginUndoGesture);
      simDa.addEventListener("input", function (e) {
        state.params.center_distance_offset_mm = clampFloat(e.target.value, 0.0, -1.0, 2.0);
        state.hostReport = null;
        syncSlidersOnly();
        recomputeKinematicsAndLoupeOnly();
      });
      const finishDa = function () {
        commitUndoGesture();
        scheduleHostAnalyze();
      };
      simDa.addEventListener("pointerup", finishDa);
      simDa.addEventListener("change", finishDa);
    }

    on("btn-sim-delta-reset", "click", function () {
      if (Math.abs(state.params.center_distance_offset_mm) < 1e-5) return;
      pushUndoSnapshot(state.params);
      state.params.center_distance_offset_mm = 0.0;
      state.hostReport = null;
      syncSlidersOnly();
      recomputeKinematicsAndLoupeOnly();
      scheduleHostAnalyze();
    });

    // 2D Loupe Zoom & Collapse
    const zoomBtns = document.querySelectorAll("[data-loupe-zoom]");
    for (let i = 0; i < zoomBtns.length; i++) {
      zoomBtns[i].addEventListener("click", function () {
        state.loupeZoom = Number(zoomBtns[i].getAttribute("data-loupe-zoom") || 1.7);
        requestRender();
      });
    }

    on("btn-loupe-collapse", "click", function () {
      state.loupeCollapsed = !state.loupeCollapsed;
      const panel = document.getElementById("loupe-panel");
      const btn = document.getElementById("btn-loupe-collapse");
      if (panel) panel.classList.toggle("collapsed", state.loupeCollapsed);
      if (btn) btn.textContent = state.loupeCollapsed ? "▴" : "▾";
      requestRender();
    });

    // Export Target & Mechanical Slicer Auto-Config
    on("sel-export-target", "change", function (e) {
      state.params.export_target = toChoice(e.target.value, "pair_separated", VALID_EXPORT_TARGETS);
      if (state.params.export_target === "fit_test_kit") {
        setViewportMode("fit_kit");
      } else if (state.vpView === "plater") {
        rebuildScene(false);
      }
      updateDerivedBadges();
    });

    on("chk-auto-slicer", "change", function (e) {
      state.params.auto_configure_slicer = Boolean(e.target.checked);
    });

    // Primary OrcaSlicer Plater & Export Actions
    const actionBtns = document.querySelectorAll("[data-action]");
    for (let i = 0; i < actionBtns.length; i++) {
      actionBtns[i].addEventListener("click", function () {
        const act = actionBtns[i].getAttribute("data-action");
        if (act === "send_to_plater") {
          setActionButtonsBusy(true);
          if (!sendToHost({
            type: "send_to_plater",
            export_target: state.params.export_target,
            params: deepClone(state.params)
          })) {
            setActionButtonsBusy(false);
            showToast("OrcaSlicer host bridge not connected (Standalone Preview).", true);
          }
        } else if (act === "export_3mf" || act === "export_stl") {
          const fmt = act === "export_3mf" ? "3mf" : "stl";
          const fname = sanitizeExportStem(state.params.name) + "." + fmt;
          setActionButtonsBusy(true);
          if (!sendToHost({
            type: "export_file",
            format: fmt,
            export_target: state.params.export_target,
            params: deepClone(state.params),
            filename: fname
          })) {
            setActionButtonsBusy(false);
            showToast("OrcaSlicer host bridge not connected (Standalone Preview).", true);
          }
        } else if (act === "open_folder") {
          sendToHost({ type: "open_exports_folder" });
        }
      });
    }

    // Global Keyboard Shortcuts: Space = Play/Pause, Ctrl+Z = Undo, Ctrl+Y / Ctrl+Shift+Z = Redo
    document.addEventListener("keydown", function (e) {
      const tag = (e.target && e.target.tagName) ? String(e.target.tagName).toUpperCase() : "";
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
      if (e.code === "Space") {
        e.preventDefault();
        state.simPlaying = !state.simPlaying;
        state.lastFrameMs = 0;
        updateDerivedBadges();
        requestRender();
      } else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "z") {
        e.preventDefault();
        if (e.shiftKey) performRedo();
        else performUndo();
      } else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "y") {
        e.preventDefault();
        performRedo();
      }
    });
  }

  function bootStudioUI() {
    if (typeof document === "undefined" || !document.getElementById) return;
    const hostTheme = detectHostInjectedTheme();
    if (hostTheme) state.theme = hostTheme;
    buildSliderWidgets();
    initWebGLViewport();
    bindUIControls();
    applyThemeAndLanguage();
    syncControlsFromState();
    rebuildScene(false);
    fitCameraToScene();
    connectOrcaBridge();
  }

  bootStudioUI();
})();
</script>
</body>
</html>
"""


def get_studio_html(mode: str = "page", initial_context: dict[str, Any] | None = None) -> str:
    """Return the complete 100% offline self-contained Orca Gear Studio HTML5/WebGL2 application.

    Args:
        mode: `"page"` for the wide 3-column OrcaSlicer tab, or `"dock"` for the
            compact right-side docked panel beside OrcaSlicer's 3D Plater.
        initial_context: Optional initial state dictionary (`lang`, `theme`,
            `printer`, `builtin_presets`, `user_presets`, `params`, `export_dir`).
    """
    norm_mode = "dock" if str(mode or "").strip().lower() == "dock" else "page"
    ctx: dict[str, Any] = copy.deepcopy(initial_context) if isinstance(initial_context, dict) else {}

    lang_raw = str(ctx.get("lang") or "pt").strip().lower()
    norm_lang = "en" if lang_raw.startswith("en") else "pt"

    theme_raw = str(ctx.get("theme") or "dark").strip().lower()
    norm_theme = "light" if theme_raw == "light" else "dark"

    fallback_params = copy.deepcopy(DEFAULT_PARAMS) if isinstance(DEFAULT_PARAMS, dict) else None
    fallback_presets = copy.deepcopy(BUILTIN_PRESETS) if isinstance(BUILTIN_PRESETS, list) else []

    boot_payload: dict[str, Any] = {
        "mode": norm_mode,
        "initial_context": ctx,
        "fallback_params": fallback_params,
        "fallback_presets": fallback_presets,
    }

    html = _STUDIO_UI_HTML_TEMPLATE
    html = html.replace("__INITIAL_LANG__", norm_lang)
    html = html.replace("__INITIAL_THEME__", norm_theme)
    html = html.replace("__INITIAL_MODE__", norm_mode)
    html = html.replace("__ORCA_GEAR_STUDIO_BOOT_JSON__", _studio_ui_safe_json(boot_payload))
    return html

# ===========================================================================
# MODULE: gear_studio.plugin_main
# ===========================================================================

pass  # [bundled] hoisted __future__ import

from collections.abc import Sequence
import copy
import ctypes
import json
import locale
import os
import re
import sys
import threading
import time
import types
from pathlib import Path
from typing import Any, Callable

# Intra-package imports (stripped cleanly when bundled into single-file PEP 723 script)
if "normalize_params" not in globals():
    pass  # [bundled] resolved intra-package import
    pass  # [bundled] resolved intra-package import
    pass  # [bundled] resolved intra-package import
    pass  # [bundled] resolved intra-package import
    pass  # [bundled] resolved intra-package import
    pass  # [bundled] resolved intra-package import
    pass  # [bundled] resolved intra-package import


# ---------------------------------------------------------------------------
# OrcaSlicer `orca` Native Binding Import (with standalone fallback stub)
# ---------------------------------------------------------------------------


def _build_fallback_orca_module() -> types.ModuleType:
    """Create a lightweight stand-in when imported outside OrcaSlicer."""
    mod = types.ModuleType("orca")
    mod._registered_capabilities = []
    mod._requested_permissions = {}
    mod._plugin_cls = None

    class PythonPluginBase:
        def __init__(self) -> None:
            self._stored_config: str = "{}"

        def get_name(self) -> str:
            return ""

        def on_load(self) -> None:
            pass

        def on_unload(self) -> None:
            pass

        def has_config_ui(self) -> bool:
            return False

        def get_config_ui(self) -> str:
            return ""

        def get_default_config(self) -> dict[str, Any]:
            return {}

        def get_config(self) -> str:
            return self._stored_config

        def get_config_version(self) -> str:
            return "1.2.0"

        def save_config(self, config: str) -> bool:
            self._stored_config = str(config or "{}")
            return True

    class BasePlugin:
        def __init__(self) -> None:
            pass

        def register_capabilities(self) -> None:
            pass

    class PagesPluginCapabilityBase(PythonPluginBase):
        def get_ui(self) -> str:
            return ""

        def get_icon(self) -> str:
            return ""

        def on_message(self, data: Any) -> None:
            pass

        def post_message(self, data: Any) -> None:
            pass

    class ScriptPluginCapabilityBase(PythonPluginBase):
        def execute(self) -> Any:
            return None

    class PluginResult:
        Success = 0
        Skipped = 1
        RecoverableError = 2
        FatalError = 3

    class ExecutionResult:
        def __init__(self, status: int = 0, message: str = "", data: str = "") -> None:
            self.status = status
            self.message = message
            self.data = data

        @classmethod
        def success(cls, message: str = "", data: str = "") -> "ExecutionResult":
            return cls(PluginResult.Success, message, data)

        @classmethod
        def skipped(cls, message: str = "") -> "ExecutionResult":
            return cls(PluginResult.Skipped, message, "")

        @classmethod
        def failure(cls, status: int, message: str, data: str = "") -> "ExecutionResult":
            return cls(status, message, data)

    def plugin_decorator(cls: type) -> type:
        mod._plugin_cls = cls
        return cls

    def register_capability(cap_cls: type) -> None:
        mod._registered_capabilities.append(cap_cls)

    def request_permissions(**kwargs: Any) -> None:
        mod._requested_permissions.update(kwargs)

    pages_mod = types.ModuleType("orca.pages")
    pages_mod.PagesPluginCapabilityBase = PagesPluginCapabilityBase

    script_mod = types.ModuleType("orca.script")
    script_mod.ScriptPluginCapabilityBase = ScriptPluginCapabilityBase

    plugin_sub = types.ModuleType("orca.plugin")
    plugin_sub.storage = lambda: str(Path(__file__).resolve().parent)

    class NotificationLevel:
        RegularNotificationLevel = 0
        HintNotificationLevel = 1
        ProgressBarNotificationLevel = 2
        PrintInfoNotificationLevel = 3
        PrintInfoShortNotificationLevel = 4
        ImportantNotificationLevel = 5
        WarningNotificationLevel = 6
        SeriousWarningNotificationLevel = 7
        ErrorNotificationLevel = 8

    host_mod = types.ModuleType("orca.host")
    host_mod.app_language = lambda: "pt_BR"
    host_mod.app_info = lambda: {"version": "2.5.1", "language": "pt_BR"}
    host_mod.preset_bundle = lambda: None
    host_mod.plater = lambda: None
    host_mod.model = lambda: None
    host_mod.selected_printer = lambda: None
    host_mod.plugin = plugin_sub
    host_mod.ui = types.SimpleNamespace(
        NotificationLevel=NotificationLevel,
        create_dock_panel=None,
        create_window=None,
        push_notification=None,
        message=None,
    )
    host_mod.preset = types.SimpleNamespace(
        process=None,
        printer=None,
        filament=None,
    )

    mod.base = BasePlugin
    mod.PythonPluginBase = PythonPluginBase
    mod.PluginResult = PluginResult
    mod.ExecutionResult = ExecutionResult
    mod.plugin = plugin_decorator
    mod.register_capability = register_capability
    mod.request_permissions = request_permissions
    mod.pages = pages_mod
    mod.script = script_mod
    mod.host = host_mod

    return mod


try:
    import orca  # type: ignore[import-not-found]
except ImportError:
    orca = _build_fallback_orca_module()


PLUGIN_SLUG = "orca_gear_generator"
WM_COPYDATA = 0x004A
SMTO_ABORTIFHUNG = 0x0002
ORCA_OTHER_INSTANCE_DWDATA = 1

ICON_SVG_CONTENT: str = """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32" fill="none">
  <defs>
    <linearGradient id="orcaGearMain" x1="3" y1="5" x2="22" y2="27" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#26e6c8"/>
      <stop offset="55%" stop-color="#00bfa5"/>
      <stop offset="100%" stop-color="#00a896"/>
    </linearGradient>
    <linearGradient id="orcaGearPinion" x1="17" y1="3" x2="30" y2="17" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#64ffda"/>
      <stop offset="100%" stop-color="#00bfa5"/>
    </linearGradient>
  </defs>
  <!-- Driven Gear G2 (8 involute teeth centered at 11.5, 19.0) -->
  <path d="M10.4 9.6L12.6 9.6L13.1 11.7L14.7 12.4L16.5 11.2L18.1 12.8L16.9 14.6L17.6 16.2L19.7 16.7L19.7 18.9L17.6 19.4L16.9 21.0L18.1 22.8L16.5 24.4L14.7 23.2L13.1 23.9L12.6 26.0L10.4 26.0L9.9 23.9L8.3 23.2L6.5 24.4L4.9 22.8L6.1 21.0L5.4 19.4L3.3 18.9L3.3 16.7L5.4 16.2L6.1 14.6L4.9 12.8L6.5 11.2L8.3 12.4L9.9 11.7Z"
        transform="translate(0 1.8)"
        fill="url(#orcaGearMain)" fill-opacity="0.22"
        stroke="url(#orcaGearMain)" stroke-width="1.55" stroke-linejoin="round"/>
  <circle cx="11.5" cy="19.6" r="3.1" stroke="#00bfa5" stroke-width="1.45"/>
  <circle cx="11.5" cy="19.6" r="5.3" stroke="#00a896" stroke-width="0.9" stroke-dasharray="2 1.6" opacity="0.75"/>

  <!-- Meshed Pinion G1 (6 involute teeth centered at 22.4, 10.2, phase-interleaved with G2) -->
  <path d="M21.5 3.6L23.3 3.6L23.8 5.4L25.1 6.1L26.9 5.3L27.8 6.9L26.5 8.2L26.5 9.8L28.1 10.7L27.2 12.3L25.4 11.8L24.1 12.6L23.8 14.5L22.0 14.5L21.5 12.7L20.2 12.0L18.4 12.8L17.5 11.2L18.8 9.9L18.8 8.3L17.2 7.4L18.1 5.8L19.9 6.3L21.2 5.5Z"
        transform="translate(0.5 0.9)"
        fill="url(#orcaGearPinion)" fill-opacity="0.26"
        stroke="url(#orcaGearPinion)" stroke-width="1.45" stroke-linejoin="round"/>
  <path d="M21.5 10.0A1.9 1.9 0 1 0 24.3 10.0L24.3 9.2L21.5 9.2Z"
        stroke="#64ffda" stroke-width="1.25" stroke-linejoin="round"/>
</svg>
"""


# ---------------------------------------------------------------------------
# Cross-Platform Environment, Storage & In-Process Plater IPC (Win32 + macOS)
# ---------------------------------------------------------------------------

_MACOS_PENDING_DISPATCH_CBS: list[Any] = []


def _is_native_orca_host() -> bool:
    """Return True only when running inside the real C++ pybind11 OrcaSlicer host."""
    base_cls = getattr(orca, "base", None)
    return base_cls is not None and type(base_cls).__name__ == "pybind11_type"


def _is_mock_callable(obj: Any) -> bool:
    """Detect unittest.mock objects without importing unittest.mock eagerly."""
    cls_mod = getattr(type(obj), "__module__", "")
    return cls_mod.startswith("unittest.mock")


def _orca_user_config_root(platform_name: str | None = None) -> Path:
    """Return OrcaSlicer's user configuration directory on Windows, macOS, and Linux."""
    plat = platform_name or sys.platform
    if plat == "win32":
        appdata = os.environ.get("APPDATA", "").strip()
        if appdata:
            return Path(appdata) / "OrcaSlicer"
        return Path.home() / "AppData" / "Roaming" / "OrcaSlicer"
    if plat == "darwin":
        return Path.home() / "Library" / "Application Support" / "OrcaSlicer"
    xdg = os.environ.get("XDG_CONFIG_HOME", "").strip()
    base = Path(xdg) if xdg else (Path.home() / ".config")
    return base / "OrcaSlicer"


def _default_installed_plugin_dir() -> Path:
    return _orca_user_config_root() / "orca_plugins" / PLUGIN_SLUG


def _default_plugin_data_dir() -> Path:
    return _orca_user_config_root() / "orca_plugins" / "plugin_data" / PLUGIN_SLUG


def _resolve_storage_dir() -> Path:
    """Resolve current plugin storage folder safely (inside or outside callbacks)."""
    # 1. Try orca.plugin.storage() or orca.host.plugin.storage()
    for holder in (getattr(orca, "plugin", None), getattr(getattr(orca, "host", None), "plugin", None)):
        storage_fn = getattr(holder, "storage", None)
        if callable(storage_fn):
            try:
                raw = storage_fn()
                if isinstance(raw, (str, os.PathLike)) and str(raw).strip():
                    return Path(raw)
            except Exception:
                pass

    # 2. In native OrcaSlicer, prefer `plugin_data/orca_gear_generator`
    if _is_native_orca_host():
        data_dir = _default_plugin_data_dir()
        try:
            data_dir.mkdir(parents=True, exist_ok=True)
            return data_dir
        except Exception:
            pass

    # 3. Fallback to __file__ parent if available
    try:
        here = Path(__file__).resolve().parent
        if here.exists():
            return here
    except Exception:
        pass

    return _default_installed_plugin_dir()


def _format_other_instance_payload(file_paths: Sequence[str | Path]) -> str:
    """Format Win32 `WM_COPYDATA` payload matching `OrcaSlicer.dll` `unescape_strings_cstyle`.

    Produces `"orca-slicer.exe";"<resolved_path_1>";...` where every token escapes
    `\\` -> `\\\\`, `"` -> `\\"`, `\\r` -> `\\r`, `\\n` -> `\\n`, wrapped in double quotes and
    joined by `;` with NO trailing `;` (`OtherInstanceMessageHandler::handle_message` skips `args[0]`).
    """
    resolved_files = [str(Path(p).resolve()) for p in file_paths if str(p).strip()]
    if not resolved_files:
        raise ValueError("file_paths must contain at least one model path")

    tokens = ["orca-slicer.exe", *resolved_files]
    escaped: list[str] = []
    for tok in tokens:
        s = (
            tok.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\r", "\\r")
            .replace("\n", "\\n")
        )
        escaped.append(f'"{s}"')
    return ";".join(escaped)


def _find_orca_mainframe_hwnd(target_pid: int | None = None) -> int | None:
    """Locate OrcaSlicer's `MainFrame` `wxWindowNR` `HWND` in `target_pid` (`os.getpid()` by default).

    Prefers `wxWindowNR` windows marked with OrcaSlicer's `Instance_Hash_Minor` or
    `Instance_Hash_Major` properties, falling back to a visible top-level `wxWindowNR` of that PID.
    """
    if sys.platform != "win32":
        return None

    from ctypes import wintypes

    pid = int(target_pid) if target_pid is not None else os.getpid()
    user32 = ctypes.windll.user32

    WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

    enum_windows = user32.EnumWindows
    if not _is_mock_callable(enum_windows):
        enum_windows.argtypes = [WNDENUMPROC, wintypes.LPARAM]
        enum_windows.restype = wintypes.BOOL

    get_pid = user32.GetWindowThreadProcessId
    if not _is_mock_callable(get_pid):
        get_pid.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
        get_pid.restype = wintypes.DWORD

    get_class = user32.GetClassNameW
    if not _is_mock_callable(get_class):
        get_class.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
        get_class.restype = ctypes.c_int

    get_prop = user32.GetPropW
    if not _is_mock_callable(get_prop):
        get_prop.argtypes = [wintypes.HWND, wintypes.LPCWSTR]
        get_prop.restype = wintypes.HANDLE

    is_visible = user32.IsWindowVisible
    if not _is_mock_callable(is_visible):
        is_visible.argtypes = [wintypes.HWND]
        is_visible.restype = wintypes.BOOL

    get_parent = user32.GetParent
    if not _is_mock_callable(get_parent):
        get_parent.argtypes = [wintypes.HWND]
        get_parent.restype = wintypes.HWND

    hash_visible: list[int] = []
    hash_any: list[int] = []
    fallback_visible: list[int] = []

    def _enum_cb(hwnd: int, _lparam: int) -> bool:
        if not hwnd:
            return True
        win_pid = wintypes.DWORD(0)
        get_pid(hwnd, ctypes.byref(win_pid))
        if int(win_pid.value) != pid:
            return True

        cls_buf = ctypes.create_unicode_buffer(64)
        cls_len = get_class(hwnd, cls_buf, 64)
        if cls_len <= 0 or cls_buf.value != "wxWindowNR":
            return True

        minor = get_prop(hwnd, "Instance_Hash_Minor")
        major = get_prop(hwnd, "Instance_Hash_Major")
        vis = bool(is_visible(hwnd))
        hwnd_int = int(hwnd)

        if bool(minor) or bool(major):
            if vis:
                hash_visible.append(hwnd_int)
            else:
                hash_any.append(hwnd_int)
        elif vis and not get_parent(hwnd):
            fallback_visible.append(hwnd_int)
        return True

    cb_ref = WNDENUMPROC(_enum_cb)
    enum_windows(cb_ref, 0)

    if hash_visible:
        return hash_visible[0]
    if hash_any:
        return hash_any[0]
    if fallback_visible:
        return fallback_visible[0]
    return None


class _COPYDATASTRUCT(ctypes.Structure):
    _fields_ = [
        ("dwData", ctypes.c_size_t),
        ("cbData", ctypes.c_uint32),
        ("lpData", ctypes.c_void_p),
    ]


def _dispatch_copydata_to_hwnd(
    hwnd: int,
    payload_str: str,
    timeout_ms: int = 5000,
) -> tuple[bool, str]:
    """Send UTF-16LE `WM_COPYDATA` (`dwData = 1`) to `hwnd` via `SendMessageTimeoutW` (`0x0002`)."""
    if not hwnd or int(hwnd) <= 0:
        return (False, "OrcaSlicer MainFrame HWND not found")
    if not payload_str:
        return (False, "Empty WM_COPYDATA payload")
    if sys.platform != "win32":
        return (False, "WM_COPYDATA requires win32")

    from ctypes import wintypes

    wchar_buf = ctypes.create_unicode_buffer(payload_str)
    cds = _COPYDATASTRUCT(
        dwData=ORCA_OTHER_INSTANCE_DWDATA,
        cbData=ctypes.sizeof(wchar_buf),
        lpData=ctypes.cast(wchar_buf, ctypes.c_void_p),
    )
    result = ctypes.c_size_t(0)

    user32 = ctypes.windll.user32
    send_msg = user32.SendMessageTimeoutW
    if not _is_mock_callable(send_msg):
        send_msg.argtypes = [
            wintypes.HWND,
            wintypes.UINT,
            wintypes.WPARAM,
            ctypes.c_void_p,
            wintypes.UINT,
            wintypes.UINT,
            ctypes.POINTER(ctypes.c_size_t),
        ]
        send_msg.restype = ctypes.c_size_t

    ret = send_msg(
        int(hwnd),
        WM_COPYDATA,
        0,
        ctypes.byref(cds),
        SMTO_ABORTIFHUNG,
        max(100, int(timeout_ms)),
        ctypes.byref(result),
    )
    if not ret:
        err = ctypes.windll.kernel32.GetLastError()
        return (False, f"SendMessageTimeoutW failed (GetLastError={err})")
    return (True, "ok")


class _MacDispatchQueueS(ctypes.Structure):
    pass


def _load_macos_objc_and_gcd() -> tuple[Any, Any]:
    """Load Objective-C runtime (`libobjc`) and GCD (`libSystem`) on macOS (`arm64` & `x86_64`)."""
    for fw in (
        "/System/Library/Frameworks/Foundation.framework/Foundation",
        "/System/Library/Frameworks/AppKit.framework/AppKit",
    ):
        try:
            ctypes.CDLL(fw)
        except OSError:
            pass

    objc = None
    for cand in ("/usr/lib/libobjc.A.dylib", "libobjc.A.dylib", "libobjc.dylib"):
        try:
            objc = ctypes.CDLL(cand)
            break
        except OSError:
            continue
    if objc is None:
        raise RuntimeError("Could not load macOS libobjc.A.dylib")

    libsystem = None
    for cand in ("/usr/lib/libSystem.B.dylib", "libSystem.B.dylib", "libSystem.dylib"):
        try:
            libsystem = ctypes.CDLL(cand)
            break
        except OSError:
            continue
    if libsystem is None:
        raise RuntimeError("Could not load macOS libSystem.B.dylib")

    if not _is_mock_callable(objc.objc_getClass):
        objc.objc_getClass.argtypes = [ctypes.c_char_p]
        objc.objc_getClass.restype = ctypes.c_void_p
    if not _is_mock_callable(objc.sel_registerName):
        objc.sel_registerName.argtypes = [ctypes.c_char_p]
        objc.sel_registerName.restype = ctypes.c_void_p

    return objc, libsystem


def _resolve_macos_app_bundle_path() -> str | None:
    """Find running `.app` bundle path on macOS from `sys.executable` or `/Applications`."""
    try:
        exe_resolved = Path(sys.executable).resolve()
        for parent in exe_resolved.parents:
            if parent.suffix.lower() == ".app" and parent.is_dir():
                return str(parent)
    except Exception:
        pass

    for cand in (
        Path("/Applications/OrcaSlicer.app"),
        Path.home() / "Applications" / "OrcaSlicer.app",
    ):
        try:
            if cand.is_dir():
                return str(cand)
        except Exception:
            continue
    return None


def _dispatch_macos_open_files(
    file_paths: Sequence[str | Path],
    timeout_ms: int = 5000,
) -> tuple[bool, str]:
    """Send model files in-process to OrcaSlicer's Cocoa `wxAppController` on macOS (`darwin`).

    Marshals onto the Cocoa main queue (`_dispatch_main_q`) using ARM64-safe typed `CFUNCTYPE`
    wrappers around `objc_msgSend`, invoking `[NSApp.delegate application:NSApp openFiles:paths]`
    (`GUI_App::MacOpenFiles` -> `Plater::load_files`), with `NSWorkspace` fallback if needed.
    Requires ZERO external `subprocess` permissions.
    """
    if sys.platform != "darwin":
        return (False, "Cocoa openFiles dispatch requires darwin")

    resolved_files = [str(Path(p).resolve()) for p in file_paths if str(p).strip()]
    if not resolved_files:
        return (False, "Empty file_paths for macOS Plater dispatch")

    try:
        objc, libsystem = _load_macos_objc_and_gcd()
    except Exception as exc:
        return (False, f"macOS Objective-C load error: {exc}")

    msg_addr = ctypes.cast(objc.objc_msgSend, ctypes.c_void_p).value
    if not msg_addr:
        return (False, "objc_msgSend address unavailable")

    # Non-variadic ARM64 & x86_64 ABI-safe Objective-C message wrappers
    msg_id0 = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(msg_addr)
    msg_void0 = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)(msg_addr)
    msg_id_cstr = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p)(msg_addr)
    msg_id_id = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(msg_addr)
    msg_void_id = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(msg_addr)
    msg_bool_sel = ctypes.CFUNCTYPE(ctypes.c_byte, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(msg_addr)
    msg_bool_id_id = ctypes.CFUNCTYPE(
        ctypes.c_byte, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p
    )(msg_addr)
    msg_void_id_id = ctypes.CFUNCTYPE(
        None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p
    )(msg_addr)
    msg_open_urls = ctypes.CFUNCTYPE(
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_ulong,
        ctypes.c_void_p,
        ctypes.c_void_p,
    )(msg_addr)

    cls_pool = objc.objc_getClass(b"NSAutoreleasePool")
    cls_app = objc.objc_getClass(b"NSApplication")
    cls_str = objc.objc_getClass(b"NSString")
    cls_url = objc.objc_getClass(b"NSURL")
    cls_arr = objc.objc_getClass(b"NSMutableArray")
    cls_ws = objc.objc_getClass(b"NSWorkspace")
    cls_bundle = objc.objc_getClass(b"NSBundle")

    sel_alloc = objc.sel_registerName(b"alloc")
    sel_init = objc.sel_registerName(b"init")
    sel_drain = objc.sel_registerName(b"drain")
    sel_shared_app = objc.sel_registerName(b"sharedApplication")
    sel_delegate = objc.sel_registerName(b"delegate")
    sel_responds = objc.sel_registerName(b"respondsToSelector:")
    sel_open_files = objc.sel_registerName(b"application:openFiles:")
    sel_open_file = objc.sel_registerName(b"application:openFile:")
    sel_str_utf8 = objc.sel_registerName(b"stringWithUTF8String:")
    sel_file_url = objc.sel_registerName(b"fileURLWithPath:")
    sel_array = objc.sel_registerName(b"array")
    sel_add_obj = objc.sel_registerName(b"addObject:")
    sel_shared_ws = objc.sel_registerName(b"sharedWorkspace")
    sel_main_bundle = objc.sel_registerName(b"mainBundle")
    sel_bundle_url = objc.sel_registerName(b"bundleURL")
    sel_open_urls = objc.sel_registerName(
        b"openURLs:withApplicationAtURL:options:configuration:error:"
    )

    done_evt = threading.Event()
    result_box: dict[str, Any] = {"ok": False, "msg": "macOS main-queue callback pending"}

    DISPATCH_FN = ctypes.CFUNCTYPE(None, ctypes.c_void_p)

    def _run_on_cocoa_main(_ctx: int) -> None:
        pool = msg_id0(msg_id0(cls_pool, sel_alloc), sel_init) if cls_pool else None
        try:
            ns_paths = msg_id0(cls_arr, sel_array)
            ns_urls = msg_id0(cls_arr, sel_array)
            for fp in resolved_files:
                ns_s = msg_id_cstr(cls_str, sel_str_utf8, fp.encode("utf-8"))
                if ns_s:
                    msg_void_id(ns_paths, sel_add_obj, ns_s)
                    if cls_url:
                        ns_u = msg_id_id(cls_url, sel_file_url, ns_s)
                        if ns_u:
                            msg_void_id(ns_urls, sel_add_obj, ns_u)

            ns_app = msg_id0(cls_app, sel_shared_app) if cls_app else None
            delegate = msg_id0(ns_app, sel_delegate) if ns_app else None

            if delegate and bool(msg_bool_sel(delegate, sel_responds, sel_open_files)):
                msg_void_id_id(delegate, sel_open_files, ns_app, ns_paths)
                result_box["ok"] = True
                result_box["msg"] = "ok (NSApp.delegate application:openFiles:)"
                return

            if delegate and bool(msg_bool_sel(delegate, sel_responds, sel_open_file)):
                all_ok = True
                for fp in resolved_files:
                    ns_s = msg_id_cstr(cls_str, sel_str_utf8, fp.encode("utf-8"))
                    if not bool(msg_bool_id_id(delegate, sel_open_file, ns_app, ns_s)):
                        all_ok = False
                if all_ok:
                    result_box["ok"] = True
                    result_box["msg"] = "ok (NSApp.delegate application:openFile:)"
                    return

            # Fallback to NSWorkspace openURLs with running bundle URL
            ws = msg_id0(cls_ws, sel_shared_ws) if cls_ws else None
            app_url = None
            if cls_bundle:
                mb = msg_id0(cls_bundle, sel_main_bundle)
                if mb:
                    app_url = msg_id0(mb, sel_bundle_url)
            if not app_url:
                app_path = _resolve_macos_app_bundle_path()
                if app_path and cls_url:
                    ns_app_s = msg_id_cstr(cls_str, sel_str_utf8, app_path.encode("utf-8"))
                    app_url = msg_id_id(cls_url, sel_file_url, ns_app_s)
            if ws and app_url and ns_urls:
                run_app = msg_open_urls(ws, sel_open_urls, ns_urls, app_url, 0, None, None)
                if run_app:
                    result_box["ok"] = True
                    result_box["msg"] = "ok (NSWorkspace openURLs)"
                    return

            result_box["ok"] = False
            result_box["msg"] = "No Cocoa openFiles delegate or NSWorkspace target responded"
        except Exception as inner_exc:
            result_box["ok"] = False
            result_box["msg"] = f"Cocoa main-queue exception: {inner_exc}"
        finally:
            if pool:
                try:
                    msg_void0(pool, sel_drain)
                except Exception:
                    pass
            done_evt.set()

    c_cb = DISPATCH_FN(_run_on_cocoa_main)
    _MACOS_PENDING_DISPATCH_CBS.append(c_cb)

    try:
        main_q = ctypes.cast(
            ctypes.byref(_MacDispatchQueueS.in_dll(libsystem, "_dispatch_main_q")),
            ctypes.c_void_p,
        )
        dispatch_async_f = libsystem.dispatch_async_f
        if not _is_mock_callable(dispatch_async_f):
            dispatch_async_f.argtypes = [ctypes.c_void_p, ctypes.c_void_p, DISPATCH_FN]
            dispatch_async_f.restype = None
        dispatch_async_f(main_q, None, c_cb)
    except Exception as exc:
        if c_cb in _MACOS_PENDING_DISPATCH_CBS:
            _MACOS_PENDING_DISPATCH_CBS.remove(c_cb)
        return (False, f"dispatch_async_f failed: {exc}")

    finished = done_evt.wait(timeout=max(0.2, float(timeout_ms) / 1000.0))
    if finished and c_cb in _MACOS_PENDING_DISPATCH_CBS:
        _MACOS_PENDING_DISPATCH_CBS.remove(c_cb)

    if not finished:
        return (False, "Timed out waiting for Cocoa main-queue openFiles")
    return (bool(result_box["ok"]), str(result_box["msg"]))


def _open_folder_native(folder_path: Path) -> bool:
    """Open `folder_path` in Explorer (Windows) or Finder (macOS) without `subprocess`."""
    resolved = str(Path(folder_path).resolve())
    if sys.platform == "win32":
        startfile_fn = getattr(os, "startfile", None)
        if callable(startfile_fn):
            startfile_fn(resolved)
            return True
        return False

    if sys.platform == "darwin":
        objc, _ = _load_macos_objc_and_gcd()
        msg_addr = ctypes.cast(objc.objc_msgSend, ctypes.c_void_p).value
        if not msg_addr:
            return False
        msg_id0 = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(msg_addr)
        msg_id_cstr = ctypes.CFUNCTYPE(
            ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p
        )(msg_addr)
        msg_id_id = ctypes.CFUNCTYPE(
            ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p
        )(msg_addr)
        msg_bool_id = ctypes.CFUNCTYPE(
            ctypes.c_byte, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p
        )(msg_addr)

        cls_str = objc.objc_getClass(b"NSString")
        cls_url = objc.objc_getClass(b"NSURL")
        cls_ws = objc.objc_getClass(b"NSWorkspace")
        sel_str_utf8 = objc.sel_registerName(b"stringWithUTF8String:")
        sel_file_url = objc.sel_registerName(b"fileURLWithPath:")
        sel_shared_ws = objc.sel_registerName(b"sharedWorkspace")
        sel_open_url = objc.sel_registerName(b"openURL:")

        ns_s = msg_id_cstr(cls_str, sel_str_utf8, resolved.encode("utf-8"))
        ns_u = msg_id_id(cls_url, sel_file_url, ns_s) if ns_s else None
        ws = msg_id0(cls_ws, sel_shared_ws) if cls_ws else None
        if ws and ns_u:
            return bool(msg_bool_id(ws, sel_open_url, ns_u))
        return False

    return False


def _dispatch_files_to_plater(
    file_paths: Sequence[str | Path],
    timeout_ms: int = 5000,
) -> tuple[bool, str, int | None]:
    """Cross-platform in-process Plater file loader for Windows (`win32`) and macOS (`darwin`)."""
    if sys.platform == "win32":
        copydata_payload = _format_other_instance_payload(file_paths)
        hwnd = _find_orca_mainframe_hwnd()
        ok, msg = _dispatch_copydata_to_hwnd(hwnd or 0, copydata_payload, timeout_ms=timeout_ms)
        return (ok, msg, hwnd)

    if sys.platform == "darwin":
        ok, msg = _dispatch_macos_open_files(file_paths, timeout_ms=timeout_ms)
        return (ok, msg, None)

    return (False, f"Unsupported platform for in-process Plater IPC: {sys.platform}", None)


def _slugify_filename(name: str, fallback: str = "engrenagens") -> str:
    """Slugify filename while scrubbing OrcaSlicer `PluginAuditManager` denied path keywords
    (`secret`, `cert`, `conf` — which C++ `is_denied_path_keyword` blocks case-insensitively).
    """
    cleaned = re.sub(r"[^\w\-. ]+", "", str(name or "").strip(), flags=re.ASCII)
    cleaned = re.sub(r"\s+", "_", cleaned).strip("._-")
    cleaned = re.sub(r"secret", "secr", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"cert", "crt", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"conf", "cfg", cleaned, flags=re.IGNORECASE)
    if not cleaned:
        return fallback
    return cleaned[:64]


def _extract_first_float(val: Any, default: float) -> float:
    if val is None:
        return default
    if isinstance(val, (int, float)) and not isinstance(val, bool):
        f = float(val)
        return f if f == f else default
    if isinstance(val, (list, tuple)):
        for item in val:
            res = _extract_first_float(item, float("nan"))
            if res == res:
                return res
        return default
    s = str(val).strip()
    if not s:
        return default
    m = re.search(r"[-+]?\d*\.?\d+", s)
    if not m:
        return default
    try:
        return float(m.group(0))
    except ValueError:
        return default


def _parse_printable_area(raw: Any, default_x: float = 220.0, default_y: float = 220.0) -> tuple[float, float]:
    """Parse OrcaSlicer `printable_area` into `(bed_x_mm, bed_y_mm)`."""
    if raw is None:
        return (default_x, default_y)

    xs: list[float] = []
    ys: list[float] = []

    tokens: list[Any]
    if isinstance(raw, str):
        s = raw.strip()
        if s.startswith("["):
            try:
                parsed = json.loads(s)
                tokens = parsed if isinstance(parsed, list) else [s]
            except Exception:
                tokens = re.split(r"[;,]+", s)
        else:
            tokens = re.split(r"[;,]+", s)
    elif isinstance(raw, (list, tuple)):
        tokens = list(raw)
    else:
        return (default_x, default_y)

    for tok in tokens:
        if isinstance(tok, (list, tuple)) and len(tok) >= 2:
            try:
                xs.append(float(tok[0]))
                ys.append(float(tok[1]))
            except (TypeError, ValueError):
                continue
        elif isinstance(tok, str):
            m = re.search(r"([-+]?\d*\.?\d+)\s*[xX:]\s*([-+]?\d*\.?\d+)", tok)
            if m:
                try:
                    xs.append(float(m.group(1)))
                    ys.append(float(m.group(2)))
                except ValueError:
                    continue

    if len(xs) >= 2 and len(ys) >= 2:
        dx = max(xs) - min(xs)
        dy = max(ys) - min(ys)
        if dx >= 30.0 and dy >= 30.0:
            return (round(dx, 2), round(dy, 2))

    return (default_x, default_y)


def _parse_line_width(raw: Any, nozzle_mm: float) -> float:
    default_lw = round(nozzle_mm * 1.05, 2)
    if raw is None:
        return default_lw
    if isinstance(raw, (list, tuple)):
        return _parse_line_width(raw[0] if raw else None, nozzle_mm)
    s = str(raw).strip()
    if not s:
        return default_lw
    if s.endswith("%"):
        pct = _extract_first_float(s[:-1], 0.0)
        if pct > 10.0:
            return round(max(0.2, min(2.5, nozzle_mm * (pct / 100.0))), 3)
        return default_lw
    val = _extract_first_float(s, 0.0)
    if val <= 0.05:
        return default_lw
    return round(max(0.2, min(2.5, val)), 3)


def _extract_preset_name(obj: Any, fallback: str = "") -> str:
    if obj is None:
        return fallback
    if isinstance(obj, str):
        return obj.strip() or fallback
    if isinstance(obj, dict):
        for k in ("name", "preset_name", "id"):
            v = obj.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
        return fallback
    for attr in ("name", "preset_name"):
        try:
            val = getattr(obj, attr, None)
            if callable(val):
                val = val()
            if isinstance(val, str) and val.strip():
                return val.strip()
        except Exception:
            continue
    return fallback


def _bundle_get_value(bundle: Any, key: str) -> Any:
    if bundle is None:
        return None
    for method_name in ("full_config_value", "config_value", "get"):
        fn = getattr(bundle, method_name, None)
        if callable(fn):
            try:
                val = fn(key)
                if val is not None and val != "":
                    return val
            except Exception:
                continue
    return None


def _detect_language(app_info: dict[str, Any]) -> str:
    raw = str(app_info.get("language") or app_info.get("lang") or "").strip().lower()
    if raw.startswith("en"):
        return "en"
    if raw.startswith("pt"):
        return "pt"
    if raw:
        return "en" if not raw.startswith("pt") else "pt"
    try:
        loc = (locale.getlocale()[0] or "").lower()
        if loc.startswith("en"):
            return "en"
        if loc.startswith("pt"):
            return "pt"
    except Exception:
        pass
    return "pt"


def _detect_theme(app_info: dict[str, Any]) -> str:
    theme_raw = str(app_info.get("theme") or app_info.get("color_mode") or "").strip().lower()
    if theme_raw == "light":
        return "light"
    if theme_raw == "dark":
        return "dark"
    if app_info.get("dark_mode") is False:
        return "light"
    return "dark"


def _make_execution_result_success(message: str) -> Any:
    exec_cls = getattr(orca, "ExecutionResult", None)
    if exec_cls is not None:
        success_fn = getattr(exec_cls, "success", None)
        if callable(success_fn):
            try:
                return success_fn(message)
            except TypeError:
                return success_fn(message, "")
        try:
            ok_code = getattr(getattr(orca, "PluginResult", None), "Success", 0)
            return exec_cls(ok_code, message, "")
        except Exception:
            pass
    return {"status": "Success", "message": message}


# ---------------------------------------------------------------------------
# Shared Gear Studio Session & Message Router
# ---------------------------------------------------------------------------


class GearStudioController:
    """Coordinates live OrcaSlicer host reading, gear mesh generation, exports, and Plater IPC."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._current_params: dict[str, Any] = normalize_params(DEFAULT_PARAMS)
        self._listeners: list[Callable[[dict[str, Any]], None]] = []
        self._last_plater_worker: threading.Thread | None = None
        self._last_plater_outcome: dict[str, Any] = {}

    @property
    def current_params(self) -> dict[str, Any]:
        with self._lock:
            return copy.deepcopy(self._current_params)

    def set_current_params(self, raw: dict[str, Any] | None) -> dict[str, Any]:
        norm = normalize_params(raw)
        with self._lock:
            self._current_params = norm
            return copy.deepcopy(norm)

    def get_presets_dir(self) -> Path:
        base = _resolve_storage_dir()
        target = base / "presets"
        try:
            target.mkdir(parents=True, exist_ok=True)
            return target
        except Exception:
            return base

    def get_export_dir(self) -> Path:
        base = _resolve_storage_dir()
        target = base / "exports"
        try:
            target.mkdir(parents=True, exist_ok=True)
            return target
        except Exception:
            fallback = Path.home() / "Documents" / "OrcaGearStudio"
            try:
                fallback.mkdir(parents=True, exist_ok=True)
                return fallback
            except Exception:
                return base

    def read_host_context(self) -> dict[str, Any]:
        """Defensively inspect `orca.host.app_language()` and `orca.host.preset_bundle()`."""
        app_info: dict[str, Any] = {}
        host = getattr(orca, "host", None)
        if host is not None:
            # Official OrcaSlicer API Reference (`orca.host.app_language()`)
            app_lang_fn = getattr(host, "app_language", None)
            if callable(app_lang_fn):
                try:
                    raw_lang = app_lang_fn()
                    if isinstance(raw_lang, str) and raw_lang.strip():
                        app_info["language"] = raw_lang.strip()
                except Exception:
                    pass

            app_info_fn = getattr(host, "app_info", None)
            if callable(app_info_fn):
                try:
                    info = app_info_fn()
                    if isinstance(info, dict):
                        for k, v in info.items():
                            app_info.setdefault(k, v)
                except Exception:
                    pass

        lang = _detect_language(app_info)
        theme = _detect_theme(app_info)
        theme_explicit = bool(
            app_info.get("theme") or app_info.get("color_mode") or ("dark_mode" in app_info)
        )
        orca_version = str(app_info.get("version") or "2.5.1")

        bundle = None
        if host is not None:
            bundle_fn = getattr(host, "preset_bundle", None)
            if callable(bundle_fn):
                try:
                    bundle = bundle_fn()
                except Exception:
                    bundle = None

        printer_name = "Generic FDM 220x220"
        process_name = "0.20mm Standard"
        filament_name = "Generic PLA"

        if bundle is not None:
            for m in ("current_printer_preset",):
                fn = getattr(bundle, m, None)
                if callable(fn):
                    try:
                        printer_name = _extract_preset_name(fn(), printer_name)
                    except Exception:
                        pass

            for m in ("current_print_preset", "current_process_preset"):
                fn = getattr(bundle, m, None)
                if callable(fn):
                    try:
                        got = _extract_preset_name(fn(), "")
                        if got:
                            process_name = got
                            break
                    except Exception:
                        pass

            for m in ("current_filament_preset_names", "current_filament_presets"):
                fn = getattr(bundle, m, None)
                if callable(fn):
                    try:
                        fils = fn()
                        if isinstance(fils, (list, tuple)) and fils:
                            got = _extract_preset_name(fils[0], "")
                            if got:
                                filament_name = got
                                break
                    except Exception:
                        pass

            if printer_name == "Generic FDM 220x220":
                p_id = _bundle_get_value(bundle, "printer_settings_id")
                if isinstance(p_id, str) and p_id.strip():
                    printer_name = p_id.strip()

        bed_x, bed_y = _parse_printable_area(
            _bundle_get_value(bundle, "printable_area"),
            default_x=220.0,
            default_y=220.0,
        )
        max_z = max(
            50.0,
            min(1000.0, _extract_first_float(_bundle_get_value(bundle, "printable_height"), 250.0)),
        )
        nozzle_mm = max(
            0.15,
            min(2.0, _extract_first_float(_bundle_get_value(bundle, "nozzle_diameter"), 0.4)),
        )
        layer_height_mm = max(
            0.04,
            min(1.2, _extract_first_float(_bundle_get_value(bundle, "layer_height"), 0.2)),
        )
        line_width_mm = _parse_line_width(
            _bundle_get_value(bundle, "outer_wall_line_width"),
            nozzle_mm=nozzle_mm,
        )

        return {
            "lang": lang,
            "theme": theme,
            "theme_explicit": theme_explicit,
            "orca_version": orca_version,
            "printer_name": printer_name,
            "process_name": process_name,
            "filament_name": filament_name,
            "bed_x": float(bed_x),
            "bed_y": float(bed_y),
            "max_z": float(max_z),
            "nozzle_mm": float(nozzle_mm),
            "layer_height_mm": float(layer_height_mm),
            "line_width_mm": float(line_width_mm),
        }

    def read_full_host_config_snapshot(self, host_ctx: dict[str, Any] | None = None) -> dict[str, Any]:
        """Collect full resolved `project_settings` snapshot from `preset_bundle()` for `.3mf` export."""
        ctx = dict(host_ctx) if host_ctx is not None else self.read_host_context()
        project_settings: dict[str, Any] = {}

        host = getattr(orca, "host", None)
        bundle = None
        if host is not None:
            bundle_fn = getattr(host, "preset_bundle", None)
            if callable(bundle_fn):
                try:
                    bundle = bundle_fn()
                except Exception:
                    bundle = None

        if bundle is not None:
            keys_fn = getattr(bundle, "full_config_keys", None)
            val_fn = getattr(bundle, "full_config_value", None) or getattr(bundle, "config_value", None)
            if callable(keys_fn) and callable(val_fn):
                try:
                    keys = keys_fn()
                    if isinstance(keys, (list, tuple, set)):
                        for k in keys:
                            ks = str(k)
                            if not ks:
                                continue
                            try:
                                v = val_fn(ks)
                                if v is not None:
                                    project_settings[ks] = v
                            except Exception:
                                continue
                except Exception:
                    pass

        ctx["project_settings"] = project_settings
        return ctx

    def build_initial_context(self, mode: str = "page") -> dict[str, Any]:
        host_ctx = self.read_host_context()
        presets_dir = self.get_presets_dir()
        export_dir = self.get_export_dir()
        params = self.current_params
        return {
            "mode": mode,
            "lang": host_ctx["lang"],
            "theme": host_ctx["theme"],
            "theme_explicit": host_ctx.get("theme_explicit", False),
            "printer": {
                "name": host_ctx["printer_name"],
                "process_name": host_ctx["process_name"],
                "filament_name": host_ctx["filament_name"],
                "orca_version": host_ctx["orca_version"],
                "bed_x": host_ctx["bed_x"],
                "bed_y": host_ctx["bed_y"],
                "max_z": host_ctx["max_z"],
                "nozzle_mm": host_ctx["nozzle_mm"],
                "layer_height_mm": host_ctx["layer_height_mm"],
                "line_width_mm": host_ctx["line_width_mm"],
            },
            "builtin_presets": BUILTIN_PRESETS,
            "user_presets": load_user_presets(presets_dir),
            "params": params,
            "export_dir": str(export_dir),
        }

    def _compute_process_preset_updates(
        self,
        params: dict[str, Any],
        host_ctx: dict[str, Any],
    ) -> dict[str, str]:
        """Build mechanical process preset key/value strings for `orca.host.preset.process.begin_update()`."""
        lw = max(0.20, float(host_ctx.get("line_width_mm", 0.42)))
        module_mm = max(0.5, float(params.get("module_mm", 2.0)))
        wall_loops = max(4, min(6, int(round((1.8 * module_mm) / (2.0 * lw)))))

        return {
            "spiral_mode": "0",
            "spiral_mode_smooth": "0",
            "wall_loops": str(wall_loops),
            "top_shell_layers": "5",
            "bottom_shell_layers": "5",
            "sparse_infill_density": "35%",
            "sparse_infill_pattern": "gyroid",
            "elefant_foot_compensation": "0.15",
        }

    def _apply_process_presets(self, updates: dict[str, str]) -> dict[str, Any]:
        """Apply process preset changes on the calling background worker thread.

        NEVER call `orca.host.preset.process.begin_update()` on the wxWidgets UI thread!
        """
        outcome: dict[str, Any] = {"applied": False, "error": None}
        if not updates:
            return outcome
        try:
            host = getattr(orca, "host", None)
            preset_ns = getattr(host, "preset", None) if host is not None else None
            process_ed = getattr(preset_ns, "process", None) if preset_ns is not None else None
            begin_fn = getattr(process_ed, "begin_update", None) if process_ed is not None else None
            if not callable(begin_fn):
                return outcome

            tx = begin_fn()
            if tx is None:
                return outcome

            staged_any = False
            for key, val in updates.items():
                try:
                    tx.set(str(key), str(val))
                    staged_any = True
                except Exception:
                    continue

            if staged_any:
                commit_fn = getattr(tx, "commit", None)
                if callable(commit_fn):
                    commit_fn()
                outcome["applied"] = True
        except Exception as exc:
            outcome["error"] = str(exc)
        return outcome

    def _apply_process_presets_async(
        self,
        updates: dict[str, str],
        delay_sec: float = 0.0,
    ) -> tuple[threading.Thread, dict[str, Any]]:
        """Apply process preset changes strictly on a background daemon thread."""
        outcome: dict[str, Any] = {"applied": False, "error": None}

        def _worker() -> None:
            if delay_sec > 0.0:
                time.sleep(delay_sec)
            res = self._apply_process_presets(updates)
            outcome.update(res)

        thread = threading.Thread(
            target=_worker,
            name="OrcaGearStudio-PresetUpdater",
            daemon=True,
        )
        thread.start()
        return thread, outcome

    def _write_stl_resilient(self, directory: Path, stem: str, mesh: Any, header: str) -> Path:
        target = directory / f"{stem}.stl"
        try:
            return Path(write_binary_stl(target, mesh, header_name=header))
        except PermissionError:
            alt = directory / f"{stem}_{int(time.time() * 1000)}.stl"
            return Path(write_binary_stl(alt, mesh, header_name=header))

    def _notify_host_toast(self, text: str, warning: bool = False) -> None:
        """Show a 3D Plater notification via `orca.host.ui.push_notification(level, text)`."""
        host = getattr(orca, "host", None)
        ui = getattr(host, "ui", None) if host is not None else None
        push_fn = getattr(ui, "push_notification", None) if ui is not None else None
        if not callable(push_fn):
            return

        lvl_enum = getattr(ui, "NotificationLevel", None)
        level_val: Any = None
        if lvl_enum is not None:
            attr_name = "WarningNotificationLevel" if warning else "RegularNotificationLevel"
            level_val = getattr(lvl_enum, attr_name, None)

        try:
            if level_val is not None:
                push_fn(level_val, text)
            else:
                push_fn(0, text)
        except TypeError:
            try:
                push_fn(text)
            except Exception:
                pass
        except Exception:
            pass

    def _run_pair_analysis(
        self,
        params: dict[str, Any],
        host_ctx: dict[str, Any],
        resolution: str = "low",
        prebuilt_meshes: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if prebuilt_meshes is not None and "pinion" in prebuilt_meshes and "gear" in prebuilt_meshes:
            pair_meshes = prebuilt_meshes
        else:
            pinion_mesh = generate_gear_mesh(params, which="pinion", resolution=resolution)
            gear_mesh = generate_gear_mesh(params, which="gear", resolution=resolution)
            pair_meshes = {"pinion": pinion_mesh, "gear": gear_mesh}
        return analyze_gear_pair(params, host_context=host_ctx, meshes=pair_meshes)

    def handle_message(
        self,
        raw_data: Any,
        send_fn: Callable[[dict[str, Any]], None],
        default_mode: str = "page",
    ) -> None:
        """Process incoming WebView2 bridge payload and send responses via `send_fn`."""
        try:
            msg = json.loads(raw_data) if isinstance(raw_data, str) else raw_data
        except Exception as exc:
            send_fn(
                {
                    "type": "action_result",
                    "ok": False,
                    "action": "parse_error",
                    "message": f"Invalid JSON message: {exc}",
                    "paths": [],
                }
            )
            return

        if not isinstance(msg, dict):
            return

        msg_type = str(msg.get("type") or "").strip()

        try:
            if msg_type == "ready":
                mode = str(msg.get("mode") or default_mode)
                init_ctx = self.build_initial_context(mode=mode)
                host_ctx = self.read_host_context()
                params = init_ctx["params"]
                report = self._run_pair_analysis(params, host_ctx, resolution="low")

                send_fn({"type": "init_state", **init_ctx})
                send_fn({"type": "analysis_result", "report": report})
                return

            if msg_type == "analyze":
                params = self.set_current_params(msg.get("params") or self.current_params)
                host_ctx = self.read_host_context()
                report = self._run_pair_analysis(params, host_ctx, resolution="low")
                send_fn({"type": "analysis_result", "report": report})
                return

            if msg_type == "randomize":
                raw_seed = msg.get("seed")
                seed_val: int | None = None
                if raw_seed is not None and raw_seed != "":
                    try:
                        seed_val = int(raw_seed)
                    except (TypeError, ValueError):
                        seed_val = None
                base_params = normalize_params(msg.get("params") or self.current_params)
                randomized = generate_random_printable_params(seed=seed_val, current_params=base_params)
                params = self.set_current_params(randomized)
                send_fn(
                    {
                        "type": "params_updated",
                        "params": params,
                        "source": "randomize",
                    }
                )
                return

            if msg_type == "preset_save":
                params = self.set_current_params(msg.get("params") or self.current_params)
                preset_name = str(msg.get("name") or params.get("name") or "Meu Par").strip() or "Meu Par"
                preset_id = msg.get("id") or msg.get("preset_id")
                preset_id_str = str(preset_id).strip() if preset_id else None
                user_presets = save_user_preset(
                    self.get_presets_dir(),
                    name=preset_name,
                    params=params,
                    preset_id=preset_id_str,
                )
                send_fn(
                    {
                        "type": "presets_updated",
                        "user_presets": user_presets,
                    }
                )
                return

            if msg_type == "preset_delete":
                preset_id = str(msg.get("id") or msg.get("preset_id") or "").strip()
                user_presets = delete_user_preset(self.get_presets_dir(), preset_id=preset_id)
                send_fn(
                    {
                        "type": "presets_updated",
                        "user_presets": user_presets,
                    }
                )
                return

            if msg_type == "export_file":
                incoming_params = copy.deepcopy(msg.get("params") or self.current_params)
                if isinstance(msg.get("export_target"), str) and str(msg.get("export_target")).strip():
                    incoming_params["export_target"] = str(msg.get("export_target")).strip()
                params = self.set_current_params(incoming_params)

                fmt = str(msg.get("format") or "3mf").strip().lower().lstrip(".")
                if fmt not in ("3mf", "stl"):
                    fmt = "3mf"
                export_target = str(msg.get("export_target") or params.get("export_target") or "pair_separated").strip()

                # Capture host snapshots & plugin storage folder on the UI thread (inside callback scope)
                host_ctx = self.read_host_context()
                lang = host_ctx["lang"]
                export_dir = self.get_export_dir()
                host_cfg = self.read_full_host_config_snapshot(host_ctx) if fmt == "3mf" else None

                raw_filename = str(msg.get("filename") or "").strip()
                if raw_filename:
                    base_stem = _slugify_filename(Path(raw_filename).stem, fallback="engrenagens")
                else:
                    base_stem = _slugify_filename(params.get("name", "engrenagens"), fallback="engrenagens")

                native_host = _is_native_orca_host()

                def _export_bg_worker() -> None:
                    try:
                        target_items = collect_target_meshes(params, target=export_target, lang=lang)
                        prebuilt_pair: dict[str, Any] | None = None
                        if export_target in ("pair_separated", "full_suite") and len(target_items) >= 2:
                            prebuilt_pair = {"pinion": target_items[0][1], "gear": target_items[1][1]}
                        report = self._run_pair_analysis(
                            params, host_ctx, resolution="low", prebuilt_meshes=prebuilt_pair
                        )

                        paths: list[str] = []
                        if fmt == "3mf":
                            target_3mf = export_dir / f"{base_stem}.3mf"
                            items_3mf = [(item_name, item_mesh, None) for item_name, item_mesh in target_items]
                            written_3mf = Path(write_orca_3mf(target_3mf, items_3mf, params, host_config=host_cfg))
                            paths.append(str(written_3mf))
                        else:
                            if len(target_items) == 1:
                                item_name, item_mesh = target_items[0]
                                stl_path = self._write_stl_resilient(
                                    export_dir,
                                    base_stem,
                                    item_mesh,
                                    header=f"OrcaGearStudio:{item_name}",
                                )
                                paths.append(str(stl_path))
                            else:
                                for item_name, item_mesh in target_items:
                                    item_slug = _slugify_filename(item_name, fallback="item")
                                    stl_path = self._write_stl_resilient(
                                        export_dir,
                                        f"{base_stem}_{item_slug}",
                                        item_mesh,
                                        header=f"OrcaGearStudio:{item_name}",
                                    )
                                    paths.append(str(stl_path))

                        ok_msg = (
                            f"Exportado com sucesso ({len(paths)} arquivo(s)): {Path(paths[0]).name}"
                            if lang == "pt"
                            else f"Exported successfully ({len(paths)} file(s)): {Path(paths[0]).name}"
                        )
                        self._notify_host_toast(ok_msg)
                        send_fn(
                            {
                                "type": "action_result",
                                "ok": True,
                                "action": "export_file",
                                "format": fmt,
                                "export_target": export_target,
                                "path": paths[0],
                                "paths": paths,
                                "message": ok_msg,
                                "report": report,
                            }
                        )
                    except Exception as bg_exc:
                        send_fn(
                            {
                                "type": "action_result",
                                "ok": False,
                                "action": "export_file",
                                "message": str(bg_exc),
                                "paths": [],
                            }
                        )

                exp_worker = threading.Thread(
                    target=_export_bg_worker,
                    name="OrcaGearStudio-ExportWorker",
                    daemon=True,
                )
                exp_worker.start()
                if not native_host:
                    exp_worker.join(timeout=8.0)
                return

            if msg_type == "send_to_plater":
                incoming_params = copy.deepcopy(msg.get("params") or self.current_params)
                if isinstance(msg.get("export_target"), str) and str(msg.get("export_target")).strip():
                    incoming_params["export_target"] = str(msg.get("export_target")).strip()
                params = self.set_current_params(incoming_params)

                export_target = str(msg.get("export_target") or params.get("export_target") or "pair_separated").strip()
                auto_cfg = bool(params.get("auto_configure_slicer", True))

                # Capture host context & plugin storage folder on the UI thread before spawning worker
                host_ctx = self.read_host_context()
                lang = host_ctx["lang"]
                export_dir = self.get_export_dir()
                base_stem = _slugify_filename(params.get("name", "engrenagens"), fallback="engrenagens")

                updates: dict[str, str] = {}
                if auto_cfg:
                    updates = self._compute_process_preset_updates(params=params, host_ctx=host_ctx)

                native_host = _is_native_orca_host()
                process_ed = getattr(
                    getattr(getattr(orca, "host", None), "preset", None),
                    "process",
                    None,
                )
                has_begin_update = bool(auto_cfg and hasattr(process_ed, "begin_update"))

                ipc_delay = 0.06 if native_host else 0.01
                preset_delay = 0.45 if native_host else 0.01
                dispatch_outcome: dict[str, Any] = {
                    "ipc_ok": False,
                    "ipc_message": "",
                    "hwnd": None,
                    "platform": sys.platform,
                    "thread_id": None,
                    "preset_applied": False,
                    "preset_error": None,
                }
                self._last_plater_outcome = dispatch_outcome

                def _plater_bg_worker() -> None:
                    try:
                        dispatch_outcome["thread_id"] = threading.get_ident()
                        target_items = collect_target_meshes(params, target=export_target, lang=lang)
                        prebuilt_pair_plater: dict[str, Any] | None = None
                        if export_target in ("pair_separated", "full_suite") and len(target_items) >= 2:
                            prebuilt_pair_plater = {"pinion": target_items[0][1], "gear": target_items[1][1]}
                        report = self._run_pair_analysis(
                            params, host_ctx, resolution="low", prebuilt_meshes=prebuilt_pair_plater
                        )

                        stl_paths: list[str] = []
                        for item_name, item_mesh in target_items:
                            item_slug = _slugify_filename(item_name, fallback="peca")
                            stl_file = self._write_stl_resilient(
                                export_dir,
                                f"{base_stem}_{item_slug}_plater",
                                item_mesh,
                                header=f"OrcaGearStudio:{item_name}",
                            )
                            stl_paths.append(str(stl_file))

                        if ipc_delay > 0.0:
                            time.sleep(ipc_delay)

                        ipc_ok, ipc_msg, hwnd = _dispatch_files_to_plater(stl_paths)
                        dispatch_outcome["hwnd"] = hwnd
                        dispatch_outcome["ipc_ok"] = ipc_ok
                        dispatch_outcome["ipc_message"] = ipc_msg

                        if auto_cfg and updates:
                            if preset_delay > 0.0:
                                time.sleep(preset_delay)
                            preset_res = self._apply_process_presets(updates)
                            dispatch_outcome["preset_applied"] = bool(preset_res.get("applied", False))
                            dispatch_outcome["preset_error"] = preset_res.get("error")

                        slicer_configured = (
                            bool(dispatch_outcome.get("preset_applied", False))
                            if not native_host
                            else bool(dispatch_outcome.get("preset_applied", False) or has_begin_update)
                        )
                        msg_text = (
                            f"Enviado para a mesa do OrcaSlicer ({len(stl_paths)} peça(s))."
                            if lang == "pt"
                            else f"Sent to OrcaSlicer Plater ({len(stl_paths)} part(s))."
                        )
                        self._notify_host_toast(msg_text)
                        send_fn(
                            {
                                "type": "action_result",
                                "ok": True,
                                "action": "send_to_plater",
                                "export_target": export_target,
                                "path": stl_paths[0],
                                "paths": stl_paths,
                                "message": msg_text,
                                "report": report,
                                "slicer_configured": slicer_configured,
                            }
                        )
                    except Exception as bg_exc:
                        send_fn(
                            {
                                "type": "action_result",
                                "ok": False,
                                "action": "send_to_plater",
                                "message": str(bg_exc),
                                "paths": [],
                            }
                        )

                worker = threading.Thread(
                    target=_plater_bg_worker,
                    name="OrcaGearStudio-PlaterDispatch",
                    daemon=True,
                )
                self._last_plater_worker = worker
                worker.start()

                if not native_host:
                    # Safe to join in standalone/test harness; NEVER join on native wxWidgets UI thread!
                    worker.join(timeout=8.0)
                return

            if msg_type == "open_exports_folder":
                export_dir = self.get_export_dir()
                lang = self.read_host_context()["lang"]
                startfile_fn = getattr(os, "startfile", None)
                if _is_native_orca_host() or _is_mock_callable(startfile_fn) or _is_mock_callable(_open_folder_native):
                    try:
                        _open_folder_native(export_dir)
                    except Exception:
                        pass

                msg_text = (
                    f"Pasta de exportação: {export_dir}"
                    if lang == "pt"
                    else f"Exports folder: {export_dir}"
                )
                send_fn(
                    {
                        "type": "action_result",
                        "ok": True,
                        "action": "open_exports_folder",
                        "path": str(export_dir),
                        "paths": [str(export_dir)],
                        "message": msg_text,
                    }
                )
                return

            send_fn(
                {
                    "type": "action_result",
                    "ok": False,
                    "action": msg_type or "unknown",
                    "message": f"Unsupported message type: {msg_type!r}",
                    "paths": [],
                }
            )
        except Exception as exc:
            send_fn(
                {
                    "type": "action_result",
                    "ok": False,
                    "action": msg_type or "error",
                    "message": str(exc),
                    "paths": [],
                }
            )


_SHARED_CONTROLLER = GearStudioController()


# ---------------------------------------------------------------------------
# OrcaSlicer Plugin Capabilities (Top-Bar Page + Docked Side Panel)
# ---------------------------------------------------------------------------


class GearStudioPageCapability(orca.pages.PagesPluginCapabilityBase):
    """Full-screen top-bar tab (`Gerador de Engrenagens`) beside Prepare / Preview / Device."""

    def __init__(self, controller: GearStudioController | None = None) -> None:
        super().__init__()
        self._controller = controller or _SHARED_CONTROLLER

    def get_name(self) -> str:
        return "Gerador de Engrenagens"

    def get_default_config(self) -> dict[str, Any]:
        return {
            "default_gear_type": "spur",
            "default_module_mm": 2.0,
            "default_export_target": "pair_separated",
            "auto_configure_slicer": True,
        }

    def get_icon(self) -> str:
        storage_dir = _resolve_storage_dir()
        existing_candidates: list[Path] = []
        try:
            existing_candidates.append(Path(__file__).resolve().parent / "icon.svg")
        except Exception:
            pass
        existing_candidates.extend(
            [
                storage_dir / "icon.svg",
                _default_installed_plugin_dir() / "icon.svg",
            ]
        )
        for cand in existing_candidates:
            try:
                if cand.is_file() and cand.stat().st_size > 0:
                    return str(cand)
            except Exception:
                continue

        # Auto-materialize embedded `icon.svg` when user side-loaded only `orca_gear_generator.py`
        write_targets: list[Path] = [
            storage_dir / "icon.svg",
            _default_plugin_data_dir() / "icon.svg",
        ]
        try:
            write_targets.append(Path(__file__).resolve().parent / "icon.svg")
        except Exception:
            pass
        write_targets.append(Path.home() / "Documents" / "OrcaGearStudio" / "icon.svg")

        seen_dirs: set[str] = set()
        for target in write_targets:
            key = str(target)
            if key in seen_dirs:
                continue
            seen_dirs.add(key)
            try:
                target.parent.mkdir(parents=True, exist_ok=True)
                with open(target, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(ICON_SVG_CONTENT)
                if target.is_file() and target.stat().st_size > 0:
                    return str(target)
            except Exception:
                continue
        return ""

    def get_ui(self) -> str:
        initial_ctx = self._controller.build_initial_context(mode="page")
        return get_studio_html(mode="page", initial_context=initial_ctx)

    def post_message(self, data: Any) -> None:
        super_post = getattr(super(), "post_message", None)
        if callable(super_post):
            super_post(data)

    def on_message(self, data: Any) -> None:
        self._controller.handle_message(
            raw_data=data,
            send_fn=self.post_message,
            default_mode="page",
        )


class GearStudioDockCapability(orca.script.ScriptPluginCapabilityBase):
    """Opens/shows a docked right-hand Gear Studio panel directly beside the 3D Plater."""

    _active_panel: Any = None
    _panel_lock = threading.RLock()

    def __init__(self, controller: GearStudioController | None = None) -> None:
        super().__init__()
        self._controller = controller or _SHARED_CONTROLLER

    def get_name(self) -> str:
        return "Orca Gear Studio - Painel Lateral"

    def get_default_config(self) -> dict[str, Any]:
        return {
            "default_export_target": "pair_separated",
            "auto_configure_slicer": True,
            "dock_side": "right",
        }

    def get_ui(self) -> str:
        initial_ctx = self._controller.build_initial_context(mode="dock")
        return get_studio_html(mode="dock", initial_context=initial_ctx)

    def _post_to_panel(self, payload: dict[str, Any]) -> None:
        with self._panel_lock:
            panel = GearStudioDockCapability._active_panel
        if panel is None:
            return
        try:
            is_open_fn = getattr(panel, "is_open", None)
            if callable(is_open_fn) and not is_open_fn():
                return
            post_fn = getattr(panel, "post", None)
            if callable(post_fn):
                post_fn(payload)
        except Exception:
            pass

    def _on_panel_message(self, data: Any) -> None:
        self._controller.handle_message(
            raw_data=data,
            send_fn=self._post_to_panel,
            default_mode="dock",
        )

    def _on_panel_close(self) -> None:
        with self._panel_lock:
            GearStudioDockCapability._active_panel = None

    def on_message(self, data: Any) -> None:
        """Direct message entry point for testing or programmatic invocation."""
        self._on_panel_message(data)

    def execute(self) -> Any:
        """Invoked on OrcaSlicer's background Script worker thread."""
        with self._panel_lock:
            existing = GearStudioDockCapability._active_panel

        if existing is not None:
            try:
                is_open_fn = getattr(existing, "is_open", None)
                if not callable(is_open_fn) or is_open_fn():
                    show_fn = getattr(existing, "show", None)
                    if callable(show_fn):
                        show_fn()
                    init_ctx = self._controller.build_initial_context(mode="dock")
                    self._post_to_panel({"type": "init_state", **init_ctx})
                    return _make_execution_result_success("Painel lateral Orca Gear Studio exibido.")
            except Exception:
                with self._panel_lock:
                    GearStudioDockCapability._active_panel = None

        html = self.get_ui()
        host = getattr(orca, "host", None)
        ui = getattr(host, "ui", None) if host is not None else None
        create_dock_fn = getattr(ui, "create_dock_panel", None) if ui is not None else None

        if callable(create_dock_fn):
            panel = create_dock_fn(
                html,
                title="Orca Gear Studio",
                width=430,
                height=800,
                on_message=self._on_panel_message,
                on_close=self._on_panel_close,
                dock="right",
            )
            with self._panel_lock:
                GearStudioDockCapability._active_panel = panel
            if panel is not None:
                show_fn = getattr(panel, "show", None)
                if callable(show_fn):
                    try:
                        show_fn()
                    except Exception:
                        pass
            return _make_execution_result_success("Painel lateral Orca Gear Studio aberto.")

        create_win_fn = getattr(ui, "create_window", None) if ui is not None else None
        if callable(create_win_fn):
            panel = create_win_fn(
                html,
                title="Orca Gear Studio",
                width=450,
                height=820,
                on_message=self._on_panel_message,
                on_close=self._on_panel_close,
            )
            with self._panel_lock:
                GearStudioDockCapability._active_panel = panel
            return _make_execution_result_success("Janela Orca Gear Studio aberta.")

        return _make_execution_result_success("Orca Gear Studio pronto.")


# ---------------------------------------------------------------------------
# Single `@orca.plugin` Entry Point Class
# ---------------------------------------------------------------------------


@orca.plugin
class OrcaGearStudioPlugin(orca.base):
    """OrcaSlicer 2.5.1+ Native Plugin Entry Point for Orca Gear Studio."""

    def __init__(self) -> None:
        super().__init__()

    def register_capabilities(self) -> None:
        """Declare required plugin permissions and register Page + Script Dock capabilities.

        Per OrcaSlicer's `Plugin Audit Hook` specification:
        - `data_dir()` (`orca_plugins` and `orca.host.plugin.storage()`) is already a global
          read+write Allowed Root requiring zero `fs_read`/`fs_readwrite` prompts.
        - `has_permission` uses exact string equality (glob wildcards like `/*` are invalid).
        - `threading=True` declares the fixed `"thread"` audit target once up front.
        """
        req_fn = getattr(orca, "request_permissions", None)
        if callable(req_fn):
            req_fn(threading=True)

        orca.register_capability(GearStudioPageCapability)
        orca.register_capability(GearStudioDockCapability)
