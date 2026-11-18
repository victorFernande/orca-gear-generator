"""Unified parameter schema and validation for Orca Gear Studio."""

from __future__ import annotations

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
    "sim_rpm": 1.0,
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
        "sim_rpm": _to_float(src.get("sim_rpm"), d["sim_rpm"], 1.0, 10.0),
        "sim_direction": _to_choice(src.get("sim_direction"), d["sim_direction"], VALID_SIM_DIRECTIONS),
        "export_target": _to_choice(src.get("export_target"), d["export_target"], VALID_EXPORT_TARGETS),
        "auto_configure_slicer": _to_bool(
            src.get("auto_configure_slicer"), d["auto_configure_slicer"]
        ),
    }
