"""Curated built-in mechanical gear presets, user preset storage, and smart printable randomizer."""

from __future__ import annotations

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
    "sim_rpm": 1.0,
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

    out["sim_rpm"] = _presets_clamp_float(out.get("sim_rpm"), 1.0, 10.0, 1.0)
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
        from .schema import DEFAULT_PARAMS, normalize_params
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
