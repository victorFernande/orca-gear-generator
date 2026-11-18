"""Orca Gear Studio — Parametric 3D Involute Gear Pair, Kinematics & Fit-Test Engine."""

from __future__ import annotations

import importlib
from typing import Any

from .schema import (
    DEFAULT_PARAMS,
    SCHEMA_VERSION,
    VALID_BORE_TYPES,
    VALID_EXPORT_TARGETS,
    VALID_GEAR_TYPES,
    VALID_HELIX_HANDS,
    VALID_LIGHTENING_MODES,
    VALID_RECESS_SIDES,
    VALID_SIM_DIRECTIONS,
    effective_helix_angle_deg,
    normalize_gear_body,
    normalize_params,
)
from .involute_math import (
    build_bore_2d_contour,
    build_gear_2d_contour,
    compute_gear_pair_geometry,
    helix_twist_angle_rad,
    inverse_involute_fn,
    involute_fn,
)
from .fit_and_kinematics import (
    analyze_gear_pair,
    evaluate_meshed_2d_clearance,
)
from .plugin_main import (
    GearStudioController,
    GearStudioDockCapability,
    GearStudioPageCapability,
    OrcaGearStudioPlugin,
)

__version__ = "1.2.0"

_LAZY_SIBLING_EXPORTS: dict[str, tuple[str, str]] = {
    "MeshData": (".mesh_generator", "MeshData"),
    "generate_gear_mesh": (".mesh_generator", "generate_gear_mesh"),
    "generate_fit_test_kit": (".mesh_generator", "generate_fit_test_kit"),
    "collect_target_meshes": (".mesh_generator", "collect_target_meshes"),
    "BUILTIN_PRESETS": (".presets_catalog", "BUILTIN_PRESETS"),
    "generate_random_printable_params": (".presets_catalog", "generate_random_printable_params"),
    "write_binary_stl": (".exporters", "write_binary_stl"),
    "write_orca_3mf": (".exporters", "write_orca_3mf"),
}


def __getattr__(name: str) -> Any:
    if name in _LAZY_SIBLING_EXPORTS:
        mod_rel, attr_name = _LAZY_SIBLING_EXPORTS[name]
        mod = importlib.import_module(mod_rel, __name__)
        val = getattr(mod, attr_name)
        globals()[name] = val
        return val
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "__version__",
    "SCHEMA_VERSION",
    "DEFAULT_PARAMS",
    "VALID_GEAR_TYPES",
    "VALID_HELIX_HANDS",
    "VALID_BORE_TYPES",
    "VALID_RECESS_SIDES",
    "VALID_LIGHTENING_MODES",
    "VALID_SIM_DIRECTIONS",
    "VALID_EXPORT_TARGETS",
    "normalize_gear_body",
    "normalize_params",
    "effective_helix_angle_deg",
    "involute_fn",
    "inverse_involute_fn",
    "compute_gear_pair_geometry",
    "helix_twist_angle_rad",
    "build_gear_2d_contour",
    "build_bore_2d_contour",
    "evaluate_meshed_2d_clearance",
    "analyze_gear_pair",
    "MeshData",
    "generate_gear_mesh",
    "generate_fit_test_kit",
    "collect_target_meshes",
    "BUILTIN_PRESETS",
    "generate_random_printable_params",
    "write_binary_stl",
    "write_orca_3mf",
    "GearStudioController",
    "GearStudioPageCapability",
    "GearStudioDockCapability",
    "OrcaGearStudioPlugin",
]
