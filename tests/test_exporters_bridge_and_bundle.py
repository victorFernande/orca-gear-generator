"""Comprehensive tests for binary STL, multi-object OrcaSlicer 3MF archives, presets CRUD,
GearStudioPageCapability & GearStudioDockCapability HTML/JS/WebView2 IPC round-trips,
and PEP 723 single-file bundling (`build_bundle()` + `verify_bundle_smoke()`).
"""

from __future__ import annotations

import sys

# CRITICAL: Never emit __pycache__ / .pyc next to any plugin bundle!
sys.dont_write_bytecode = True

import asyncio
import copy
import importlib.util
import json
import math
import re
import shutil
import struct
import subprocess
import tempfile
import threading
import time
import tomllib
import types
import unittest
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Any
from unittest import mock

import os

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROJECT_SRC = PROJECT_ROOT / "src"
BUILD_SCRIPT = PROJECT_ROOT / "scripts" / "build_and_install.py"
_CP_TAG = f"cp{sys.version_info.major}{sys.version_info.minor}"
if sys.platform == "win32":
    _ORCA_BASE = Path(os.environ.get("APPDATA") or (Path.home() / "AppData" / "Roaming")) / "OrcaSlicer"
elif sys.platform == "darwin":
    _ORCA_BASE = Path.home() / "Library" / "Application Support" / "OrcaSlicer"
else:
    _ORCA_BASE = Path(os.environ.get("XDG_CONFIG_HOME") or (Path.home() / ".config")) / "OrcaSlicer"
INSTALLED_DIR = _ORCA_BASE / "orca_plugins" / "orca_gear_generator"

for _cand in (_ORCA_BASE / "python" / "packages" / _CP_TAG, _ORCA_BASE / "python" / "packages" / "cp312", PROJECT_SRC):
    _ps = str(_cand)
    if _cand.exists() and _ps not in sys.path:
        sys.path.insert(0, _ps)

import numpy as np

from gear_studio.exporters import write_binary_stl, write_orca_3mf
from gear_studio.mesh_generator import collect_target_meshes, generate_gear_mesh
from gear_studio.presets_catalog import (
    BUILTIN_PRESETS,
    delete_user_preset,
    generate_random_printable_params,
    load_user_presets,
    save_user_preset,
)
from gear_studio.schema import DEFAULT_PARAMS, normalize_params


def _strip_ns(tag: str) -> str:
    return tag.split("}", 1)[1] if "}" in tag else tag


def _extract_pep723_block(source: str) -> dict[str, Any]:
    match = re.search(
        r"(?m)^# /// script[ \t]*\r?\n((?:^#(?: .*|[ \t]*)\r?\n)+)^# ///[ \t]*$",
        source,
    )
    if not match:
        raise ValueError("Missing valid PEP 723 `# /// script ... # ///` metadata block")
    lines: list[str] = []
    for raw_line in match.group(1).splitlines():
        if raw_line.startswith("# "):
            lines.append(raw_line[2:])
        elif raw_line.startswith("#"):
            lines.append(raw_line[1:])
    return tomllib.loads("\n".join(lines))


def _extract_script_blocks(html: str) -> list[str]:
    return re.findall(r"<script\b[^>]*>(.*?)</script>", html, flags=re.DOTALL | re.IGNORECASE)


class MockOrcaHostHarness:
    """Faithful mock of OrcaSlicer 2.5.1 C++ pybind11 `orca` module hierarchy."""

    def __init__(self, storage_dir: Path) -> None:
        self.storage_dir = storage_dir
        self.main_thread_id = threading.get_ident()
        self.plugin_classes: list[type] = []
        self.registered_capabilities: list[type] = []
        self.requested_permissions: list[dict[str, Any]] = []
        self.posted_page_messages: list[dict[str, Any]] = []
        self.dock_panels: list[Any] = []
        self.windows: list[Any] = []
        self.notifications: list[tuple[Any, Any]] = []
        self.process_transactions: list[dict[str, Any]] = []
        self.tx_event = threading.Event()
        self._saved_configs: dict[str, str] = {}

        self.preset_values: dict[str, Any] = {
            "printer_settings_id": "Bambu Lab X1 Carbon 0.4 nozzle",
            "filament_settings_id": ["Generic PETG @System"],
            "print_settings_id": "0.20mm Standard @BBL X1C",
            "printable_area": ["0x0", "220x0", "220x220", "0x220"],
            "printable_height": "250",
            "nozzle_diameter": ["0.4"],
            "layer_height": "0.2",
            "outer_wall_line_width": "0.42",
            "spiral_mode": "1",
            "wall_loops": "2",
            "bottom_shell_layers": "3",
            "top_shell_layers": "3",
            "sparse_infill_density": "15%",
        }

    def build_modules(self) -> dict[str, types.ModuleType]:
        harness = self

        orca_mod = types.ModuleType("orca")
        pages_mod = types.ModuleType("orca.pages")
        script_mod = types.ModuleType("orca.script")
        host_mod = types.ModuleType("orca.host")
        host_ui_mod = types.ModuleType("orca.host.ui")
        host_preset_mod = types.ModuleType("orca.host.preset")
        plugin_mod = types.ModuleType("orca.plugin")

        class PluginType:
            Pages = "Pages"
            Script = "Script"
            Unknown = "Unknown"

        class PluginResult:
            Success = "Success"
            Skipped = "Skipped"
            RecoverableError = "RecoverableError"
            FatalError = "FatalError"

        class ExecutionResult:
            def __init__(self, status: str = PluginResult.Success, message: str = "", data: str = "") -> None:
                self.status = status
                self.message = message
                self.data = data

            @staticmethod
            def success(message: str = "", data: str = "") -> ExecutionResult:
                return ExecutionResult(PluginResult.Success, message, data)

            @staticmethod
            def failure(status: str = PluginResult.RecoverableError, message: str = "", data: str = "") -> ExecutionResult:
                return ExecutionResult(status, message, data)

        class OrcaBase:
            def __init__(self) -> None:
                pass

            def register_capabilities(self) -> None:
                pass

        def plugin_decorator(cls: type) -> type:
            harness.plugin_classes.append(cls)
            return cls

        def register_capability(cap_cls: type) -> None:
            harness.registered_capabilities.append(cap_cls)

        def request_permissions(**kwargs: Any) -> None:
            harness.requested_permissions.append(dict(kwargs))

        class PythonPluginBase:
            def get_name(self) -> str:
                raise NotImplementedError

            def get_type(self) -> str:
                return PluginType.Unknown

            def on_load(self) -> None:
                pass

            def on_unload(self) -> None:
                pass

            def get_config(self) -> str:
                return harness._saved_configs.get(self.__class__.__name__, "{}")

            def save_config(self, config_json: str) -> bool:
                harness._saved_configs[self.__class__.__name__] = str(config_json)
                return True

        class PagesPluginCapabilityBase(PythonPluginBase):
            def get_type(self) -> str:
                return PluginType.Pages

            def get_ui(self) -> str:
                raise NotImplementedError

            def get_icon(self) -> str:
                return ""

            def on_message(self, data: Any) -> None:
                pass

            def post_message(self, data: Any) -> None:
                serialized = json.loads(json.dumps(data))
                harness.posted_page_messages.append(serialized)

        class ScriptPluginCapabilityBase(PythonPluginBase):
            def get_type(self) -> str:
                return PluginType.Script

            def execute(self) -> Any:
                raise NotImplementedError

        class ReadOnlyModel:
            id = 1
            object_count = 0
            max_z = 0.0
            material_count = 1
            current_plate_index = 0

            def objects(self) -> list[Any]:
                return []

        class ReadOnlyPlater:
            model = ReadOnlyModel()
            is_project_dirty = False
            is_presets_dirty = False
            project_path = ""

        class MockPresetBundle:
            def current_print_preset(self) -> str:
                return "0.20mm Standard @BBL X1C"

            def current_printer_preset(self) -> str:
                return "Bambu Lab X1 Carbon 0.4 nozzle"

            def current_filament_presets(self) -> list[str]:
                return ["Generic PETG @System"]

            def full_config_keys(self) -> list[str]:
                return list(harness.preset_values.keys())

            def full_config_value(self, key: str) -> Any:
                val = harness.preset_values.get(key, "")
                return val[0] if isinstance(val, list) and len(val) == 1 else val

            def config_value(self, key: str) -> Any:
                return self.full_config_value(key)

        class MockPresetUpdateResult:
            def __init__(self, ok: bool = True, message: str = "") -> None:
                self.ok = ok
                self.success = ok
                self.message = message

            def __bool__(self) -> bool:
                return self.ok

        class MockPresetTransaction:
            def __init__(self, preset_name: str, thread_id: int) -> None:
                self.preset_name = preset_name
                self.thread_id = thread_id
                self.updates: dict[str, str] = {}
                self.committed = False

            def set(self, key: str, value: str) -> MockPresetTransaction:
                self.updates[str(key)] = str(value)
                return self

            def commit(self) -> MockPresetUpdateResult:
                self.committed = True
                for k, v in self.updates.items():
                    harness.preset_values[k] = v
                harness.process_transactions.append(
                    {
                        "preset_name": self.preset_name,
                        "thread_id": self.thread_id,
                        "on_ui_thread": (self.thread_id == harness.main_thread_id),
                        "updates": dict(self.updates),
                    }
                )
                harness.tx_event.set()
                return MockPresetUpdateResult(True)

            def __enter__(self) -> MockPresetTransaction:
                return self

            def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
                if exc_type is None and not self.committed:
                    self.commit()
                return False

        class MockPresetEditor:
            def update(self, key: str, value: str) -> MockPresetUpdateResult:
                tid = threading.get_ident()
                harness.preset_values[str(key)] = str(value)
                harness.process_transactions.append(
                    {
                        "preset_name": "",
                        "thread_id": tid,
                        "on_ui_thread": (tid == harness.main_thread_id),
                        "updates": {str(key): str(value)},
                    }
                )
                harness.tx_event.set()
                return MockPresetUpdateResult(True)

            def begin_update(self, preset_name: str = "") -> MockPresetTransaction:
                return MockPresetTransaction(preset_name, threading.get_ident())

        class MockDockPanel:
            def __init__(
                self,
                html: str,
                title: str = "OrcaSlicer",
                width: int = 420,
                height: int = 780,
                on_message: Any = None,
                on_close: Any = None,
                dock: str = "right",
            ) -> None:
                self.html = html
                self.title = title
                self.width = width
                self.height = height
                self.on_message = on_message
                self.on_close = on_close
                self.dock = dock
                self._open = True
                self.posted: list[dict[str, Any]] = []

            def post(self, data: Any) -> None:
                self.posted.append(json.loads(json.dumps(data)))

            def post_message(self, data: Any) -> None:
                self.post(data)

            def show(self) -> None:
                self._open = True

            def hide(self) -> None:
                self._open = False

            def close(self) -> None:
                self._open = False
                if callable(self.on_close):
                    self.on_close()

            def is_open(self) -> bool:
                return self._open

        def create_dock_panel(
            html: str,
            title: str = "OrcaSlicer",
            width: int = 420,
            height: int = 780,
            on_message: Any = None,
            on_close: Any = None,
            dock: str = "right",
        ) -> MockDockPanel:
            panel = MockDockPanel(html, title, width, height, on_message, on_close, dock)
            harness.dock_panels.append(panel)
            return panel

        def create_window(
            html: str,
            title: str = "OrcaSlicer",
            width: int = 900,
            height: int = 720,
            on_message: Any = None,
            on_close: Any = None,
            style: int = 0,
            on_submit: Any = None,
        ) -> MockDockPanel:
            win = MockDockPanel(html, title, width, height, on_message, on_close, "window")
            harness.windows.append(win)
            return win

        def storage_fn() -> str:
            harness.storage_dir.mkdir(parents=True, exist_ok=True)
            return str(harness.storage_dir)

        plugin_mod.storage = storage_fn

        host_ui_mod.create_dock_panel = create_dock_panel
        host_ui_mod.create_window = create_window
        host_ui_mod.push_notification = lambda *a, **kw: harness.notifications.append((a, kw))
        host_ui_mod.message = lambda *a, **kw: "ok"
        host_ui_mod.WINDOW_MODELESS = 0

        host_preset_mod.process = MockPresetEditor()
        host_preset_mod.printer = MockPresetEditor()
        host_preset_mod.filament = MockPresetEditor()

        host_mod.plater = lambda: ReadOnlyPlater()
        host_mod.model = lambda: ReadOnlyModel()
        host_mod.preset_bundle = lambda: MockPresetBundle()
        host_mod.preset = host_preset_mod
        host_mod.ui = host_ui_mod
        host_mod.plugin = plugin_mod
        host_mod.app_info = lambda: {
            "version": "2.5.1",
            "orca_version": "2.5.1",
            "language": "pt_BR",
            "theme": "dark",
        }
        host_mod.gl_info = lambda: {"version": "4.6.0", "renderer": "MockGPU"}
        host_mod.selected_printer = lambda: "Bambu Lab X1 Carbon 0.4 nozzle"

        pages_mod.PagesPluginCapabilityBase = PagesPluginCapabilityBase
        script_mod.ScriptPluginCapabilityBase = ScriptPluginCapabilityBase

        orca_mod.base = OrcaBase
        orca_mod.plugin = plugin_decorator
        orca_mod.register_capability = register_capability
        orca_mod.request_permissions = request_permissions
        orca_mod.PythonPluginBase = PythonPluginBase
        orca_mod.PluginType = PluginType
        orca_mod.PluginResult = PluginResult
        orca_mod.ExecutionResult = ExecutionResult
        orca_mod.pages = pages_mod
        orca_mod.script = script_mod
        orca_mod.host = host_mod
        orca_mod.plugin_storage = plugin_mod

        return {
            "orca": orca_mod,
            "orca.pages": pages_mod,
            "orca.script": script_mod,
            "orca.host": host_mod,
            "orca.host.ui": host_ui_mod,
            "orca.host.preset": host_preset_mod,
            "orca.plugin": plugin_mod,
        }


class TestExportersBridgeAndBundle(unittest.TestCase):
    """Validate STL/3MF exporters, presets CRUD, WebView2 Studio bridge, and PEP 723 bundler."""

    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(prefix="orca_gear_qa_")
        self.tmp_path = Path(self._tmpdir.name)
        self.harness = MockOrcaHostHarness(self.tmp_path / "plugin_storage")
        self._mock_mods = self.harness.build_modules()
        self._saved_sys_mods = {k: sys.modules.get(k) for k in self._mock_mods}
        sys.modules.update(self._mock_mods)

    def tearDown(self) -> None:
        for k, orig in self._saved_sys_mods.items():
            if orig is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = orig
        sys.modules.pop("_qa_loaded_orca_gear_bundle", None)
        sys.modules.pop("_qa_gear_build_script", None)
        self._tmpdir.cleanup()

    def _load_build_script(self) -> types.ModuleType:
        self.assertTrue(BUILD_SCRIPT.is_file(), f"Missing build script at {BUILD_SCRIPT}")
        spec = importlib.util.spec_from_file_location("_qa_gear_build_script", str(BUILD_SCRIPT))
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        sys.modules["_qa_gear_build_script"] = mod
        spec.loader.exec_module(mod)
        return mod

    def _exec_bundle_in_mock_orca(self, bundle_path: Path) -> types.ModuleType:
        source = bundle_path.read_text(encoding="utf-8")
        mod = types.ModuleType("_qa_loaded_orca_gear_bundle")
        mod.__file__ = str(bundle_path)
        code = compile(source, str(bundle_path), "exec")
        exec(code, mod.__dict__)
        sys.modules["_qa_loaded_orca_gear_bundle"] = mod
        return mod

    def test_01_write_binary_stl_header_size_and_triangle_count(self) -> None:
        params = normalize_params(
            {
                "gear_type": "helical",
                "helix_angle_deg": 45.0,
                "module_mm": 2.0,
                "face_width_mm": 10.0,
                "pinion": {"teeth": 14, "bore_type": "d_shaft", "bore_diameter_mm": 5.0},
            }
        )
        mesh = generate_gear_mesh(params, which="pinion", resolution="low")
        n_faces = int(mesh.triangles.shape[0])

        stl_path = self.tmp_path / "pinion_helical_45.stl"
        ret = write_binary_stl(stl_path, mesh, header_name="OrcaGearQA")
        self.assertEqual(Path(ret).resolve(), stl_path.resolve())
        self.assertTrue(stl_path.is_file())

        raw = stl_path.read_bytes()
        expected_size = 84 + 50 * n_faces
        self.assertEqual(
            len(raw),
            expected_size,
            f"Binary STL byte count {len(raw)} != 84 + 50*{n_faces} ({expected_size})",
        )
        self.assertIn(b"OrcaGearQA", raw[:80])

        (tri_count,) = struct.unpack("<I", raw[80:84])
        self.assertEqual(tri_count, n_faces)

        stl_dtype = np.dtype(
            [
                ("normal", "<f4", (3,)),
                ("v0", "<f4", (3,)),
                ("v1", "<f4", (3,)),
                ("v2", "<f4", (3,)),
                ("attr", "<u2"),
            ]
        )
        records = np.frombuffer(raw, dtype=stl_dtype, offset=84)
        self.assertEqual(len(records), n_faces)
        self.assertTrue(np.all(np.isfinite(records["normal"])))
        self.assertTrue(np.all(np.isfinite(records["v0"])))
        self.assertTrue(np.all(np.isfinite(records["v1"])))
        self.assertTrue(np.all(np.isfinite(records["v2"])))

        expected_tris = mesh.vertices[mesh.triangles]
        np.testing.assert_allclose(records["v0"], expected_tris[:, 0], atol=1e-5)
        np.testing.assert_allclose(records["v1"], expected_tris[:, 1], atol=1e-5)
        np.testing.assert_allclose(records["v2"], expected_tris[:, 2], atol=1e-5)

    def _validate_3mf_archive(
        self,
        archive_path: Path,
        expected_item_count: int,
        bed_x: float = 220.0,
        bed_y: float = 220.0,
    ) -> dict[str, Any]:
        self.assertTrue(archive_path.is_file())
        self.assertTrue(zipfile.is_zipfile(archive_path))

        with zipfile.ZipFile(archive_path, "r") as zf:
            self.assertIsNone(zf.testzip(), "Corrupted ZIP entry in .3mf")
            names = set(zf.namelist())
            required = {
                "[Content_Types].xml",
                "_rels/.rels",
                "3D/3dmodel.model",
                "Metadata/model_settings.config",
                "Metadata/project_settings.config",
            }
            self.assertTrue(required.issubset(names), f"Missing 3MF members: {required - names}")

            # Parse 3D/3dmodel.model (plus sub-object .model files if present)
            obj_bounds_local: dict[str, tuple[float, float, float, float, float]] = {}
            for member in names:
                if member.endswith(".model"):
                    m_root = ET.fromstring(zf.read(member))
                    for obj_el in m_root.iter():
                        if _strip_ns(obj_el.tag) == "object":
                            oid = obj_el.attrib.get("id", "")
                            xs: list[float] = []
                            ys: list[float] = []
                            zs: list[float] = []
                            for sub_el in obj_el.iter():
                                if _strip_ns(sub_el.tag) == "vertex":
                                    xs.append(float(sub_el.attrib["x"]))
                                    ys.append(float(sub_el.attrib["y"]))
                                    zs.append(float(sub_el.attrib["z"]))
                            if xs:
                                obj_bounds_local[oid] = (min(xs), max(xs), min(ys), max(ys), min(zs))

            model_root = ET.fromstring(zf.read("3D/3dmodel.model"))
            self.assertEqual(_strip_ns(model_root.tag), "model")
            self.assertEqual(model_root.attrib.get("unit"), "millimeter")

            build_items = [el for el in model_root.iter() if _strip_ns(el.tag) == "item"]
            self.assertEqual(len(build_items), expected_item_count)

            # Compute world XY AABB for every build item and assert zero pairwise overlap & bed fit
            world_aabbs: list[tuple[float, float, float, float]] = []
            for item_el in build_items:
                oid = item_el.attrib["objectid"]
                tf = [float(v) for v in item_el.attrib["transform"].split()]
                self.assertEqual(len(tf), 12)
                tx, ty, tz = tf[9], tf[10], tf[11]
                self.assertIn(oid, obj_bounds_local)
                xmin, xmax, ymin, ymax, zmin = obj_bounds_local[oid]
                self.assertAlmostEqual(zmin + tz, 0.0, delta=1e-2)
                wx0, wx1 = xmin + tx, xmax + tx
                wy0, wy1 = ymin + ty, ymax + ty
                self.assertGreaterEqual(wx0, -1.0, f"Object {oid} out of left bed bound: {wx0:.2f}")
                self.assertLessEqual(wx1, bed_x + 1.0, f"Object {oid} out of right bed bound: {wx1:.2f}")
                self.assertGreaterEqual(wy0, -1.0, f"Object {oid} out of front bed bound: {wy0:.2f}")
                self.assertLessEqual(wy1, bed_y + 1.0, f"Object {oid} out of back bed bound: {wy1:.2f}")
                world_aabbs.append((wx0, wx1, wy0, wy1))

            for i in range(len(world_aabbs)):
                ax0, ax1, ay0, ay1 = world_aabbs[i]
                for j in range(i + 1, len(world_aabbs)):
                    bx0, bx1, by0, by1 = world_aabbs[j]
                    overlap_x = min(ax1, bx1) - max(ax0, bx0)
                    overlap_y = min(ay1, by1) - max(ay0, by0)
                    self.assertFalse(
                        overlap_x > 0.0 and overlap_y > 0.0,
                        f"3MF items {i} and {j} overlap on XY bed: {world_aabbs[i]} vs {world_aabbs[j]}",
                    )

            ms_root = ET.fromstring(zf.read("Metadata/model_settings.config"))
            self.assertEqual(_strip_ns(ms_root.tag), "config")

            proj_cfg = json.loads(zf.read("Metadata/project_settings.config").decode("utf-8"))
            self.assertIsInstance(proj_cfg, dict)
            return proj_cfg

    def test_02_write_orca_3mf_pair_separated_and_fit_test_kit(self) -> None:
        params = normalize_params(
            {
                "name": "Redutor Helicoidal QA",
                "gear_type": "helical",
                "helix_angle_deg": 45.0,
                "module_mm": 2.0,
                "face_width_mm": 10.0,
                "auto_configure_slicer": True,
                "pinion": {"teeth": 14, "bore_type": "d_shaft", "bore_diameter_mm": 5.0},
                "gear": {"teeth": 28, "bore_type": "round", "bore_diameter_mm": 8.0},
            }
        )
        host_cfg = {
            "bed_x": 220.0,
            "bed_y": 220.0,
            "project_settings": {
                "printer_settings_id": "Bambu Lab X1 Carbon 0.4 nozzle",
                "spiral_mode": "1",
            },
        }

        # 1. pair_separated -> 2 objects
        pair_items = collect_target_meshes(params, target="pair_separated")
        self.assertEqual(len(pair_items), 2)
        pair_3mf = self.tmp_path / "pair_separated.3mf"
        write_orca_3mf(pair_3mf, pair_items, params, host_config=host_cfg)
        proj_pair = self._validate_3mf_archive(pair_3mf, expected_item_count=2)
        self.assertEqual(proj_pair.get("spiral_mode"), "0")
        self.assertGreaterEqual(int(proj_pair.get("wall_loops", "0")), 4)

        # 2. fit_test_kit -> 4 objects without XY overlap + mechanical slicer settings
        kit_items = collect_target_meshes(params, target="fit_test_kit")
        self.assertEqual(len(kit_items), 4)
        kit_3mf = self.tmp_path / "fit_test_kit.3mf"
        write_orca_3mf(kit_3mf, kit_items, params, host_config=host_cfg)
        proj_kit = self._validate_3mf_archive(kit_3mf, expected_item_count=4)
        self.assertEqual(proj_kit.get("spiral_mode"), "0")
        self.assertGreaterEqual(int(proj_kit.get("wall_loops", "0")), 4)

    def test_03_presets_catalog_crud_and_randomizer(self) -> None:
        self.assertEqual(len(BUILTIN_PRESETS), 12)
        seen_ids: set[str] = set()
        for preset in BUILTIN_PRESETS:
            pid = preset["id"]
            self.assertNotIn(pid, seen_ids)
            seen_ids.add(pid)
            self.assertIsInstance(preset.get("params"), dict)
            norm = normalize_params(preset["params"])
            self.assertIn(norm["gear_type"], ("spur", "helical", "herringbone"))

        presets_dir = self.tmp_path / "user_presets"
        self.assertEqual(load_user_presets(presets_dir), [])
        saved = save_user_preset(presets_dir, "Meu Redutor 1:3", normalize_params({"pinion": {"teeth": 15}, "gear": {"teeth": 45}}))
        self.assertEqual(len(saved), 1)
        pid = saved[0]["id"]
        self.assertEqual(len(load_user_presets(presets_dir)), 1)
        after_del = delete_user_preset(presets_dir, pid)
        self.assertEqual(after_del, [])

        r1 = generate_random_printable_params(seed=42, current_params=DEFAULT_PARAMS)
        r2 = generate_random_printable_params(seed=42, current_params=DEFAULT_PARAMS)
        self.assertEqual(r1, r2)
        r3 = generate_random_printable_params(seed=99, current_params=DEFAULT_PARAMS)
        self.assertNotEqual(r1, r3)

    def test_04_build_bundle_pep723_and_verify_bundle_smoke(self) -> None:
        build_mod = self._load_build_script()
        bundle_path = Path(build_mod.build_bundle())
        self.assertTrue(bundle_path.is_file(), f"Bundle was not written at {bundle_path}")
        self.assertEqual(bundle_path.name, "orca_gear_generator.py")

        source = bundle_path.read_text(encoding="utf-8")
        meta = _extract_pep723_block(source)
        self.assertIn("requires-python", meta)
        self.assertIn("dependencies", meta)
        self.assertTrue(any("numpy" in str(dep).lower() for dep in meta["dependencies"]))

        plugin_meta = meta.get("tool", {}).get("orcaslicer", {}).get("plugin", {})
        self.assertNotIn("type", plugin_meta)
        self.assertEqual(plugin_meta.get("name"), "Orca Gear Studio")
        self.assertTrue(bool(plugin_meta.get("description")))
        self.assertTrue(bool(plugin_meta.get("author")))
        self.assertEqual(plugin_meta.get("version"), "1.3.0")

        # Run official smoke check from build_and_install.py (temporarily clear mock orca so smoke uses its own orca fallback)
        saved_orca = {k: sys.modules.pop(k) for k in list(sys.modules) if k == "orca" or k.startswith("orca.")}
        try:
            build_mod.verify_bundle_smoke(bundle_path)
        finally:
            sys.modules.update(saved_orca)

        # If already installed in %APPDATA%, assert strict single-.py + zero __pycache__ rule
        if INSTALLED_DIR.is_dir():
            py_files = [p for p in INSTALLED_DIR.rglob("*.py") if p.is_file()]
            pyc_files = [p for p in INSTALLED_DIR.rglob("*.pyc") if p.is_file()]
            pycache_dirs = [p for p in INSTALLED_DIR.rglob("__pycache__") if p.is_dir()]
            self.assertEqual([p.name for p in py_files], ["orca_gear_generator.py"])
            self.assertEqual(pyc_files, [])
            self.assertEqual(pycache_dirs, [])

    def test_05_capabilities_html_js_and_full_webview2_roundtrips(self) -> None:
        build_mod = self._load_build_script()
        bundle_path = Path(build_mod.build_bundle())
        mod = self._exec_bundle_in_mock_orca(bundle_path)

        self.assertEqual(len(self.harness.plugin_classes), 1)
        plugin_cls = self.harness.plugin_classes[0]
        plugin_inst = plugin_cls()
        plugin_inst.register_capabilities()

        # Verify permissions requested (official OrcaSlicer Audit Hook rules: threading=True,
        # zero external process permissions, and NO invalid `/*` wildcard path strings!)
        merged_perms: dict[str, Any] = {}
        for p in self.harness.requested_permissions:
            merged_perms.update(p)
        self.assertTrue(bool(merged_perms.get("threading")))
        self.assertNotIn("process", merged_perms)
        for fs_key in ("fs_read", "fs_readwrite"):
            for entry in merged_perms.get(fs_key, []):
                self.assertNotIn("*", str(entry), f"Forbidden wildcard in {fs_key}: {entry}")

        # Verify denied-path-keyword sanitization (`secret`, `cert`, `conf`) in _slugify_filename
        scrubbed = mod._slugify_filename("Config Secret Certificado Par")
        self.assertNotIn("conf", scrubbed.lower())
        self.assertNotIn("secret", scrubbed.lower())
        self.assertNotIn("cert", scrubbed.lower())

        page_cap = mod.GearStudioPageCapability()
        dock_cap = mod.GearStudioDockCapability()
        page_cap.on_load()
        dock_cap.on_load()

        # Capability names must be unique and never contain ';' (OrcaSlicer preset separator rule)
        self.assertNotIn(";", page_cap.get_name())
        self.assertNotIn(";", dock_cap.get_name())
        self.assertNotEqual(page_cap.get_name(), dock_cap.get_name())
        self.assertIsInstance(page_cap.get_default_config(), dict)
        self.assertIsInstance(dock_cap.get_default_config(), dict)

        self.assertEqual(page_cap.get_name(), "Gerador de Engrenagens")
        self.assertEqual(dock_cap.get_name(), "Orca Gear Studio - Painel Lateral")

        html_page = page_cap.get_ui()
        html_dock = dock_cap.get_ui() if hasattr(dock_cap, "get_ui") else mod.get_studio_html(mode="dock")

        node_bin = shutil.which("node")
        for mode_name, html in (("page", html_page), ("dock", html_dock)):
            with self.subTest(ui_mode=mode_name):
                self.assertIsInstance(html, str)
                self.assertGreater(len(html), 8000)
                self.assertIn("<html", html.lower())
                self.assertIn("webgl2", html.lower())
                self.assertIn("postMessage", html)
                self.assertIn("onMessage", html)

                # Zero external CDN links
                ext_scripts = re.findall(r"<script\b[^>]+src=[\"']https?://[^\"']+[\"']", html, flags=re.I)
                ext_links = re.findall(r"<link\b[^>]+href=[\"']https?://[^\"']+[\"']", html, flags=re.I)
                self.assertEqual(ext_scripts, [])
                self.assertEqual(ext_links, [])

                scripts = _extract_script_blocks(html)
                self.assertGreaterEqual(len(scripts), 1)
                if node_bin:
                    for s_idx, js_code in enumerate(scripts):
                        js_file = self.tmp_path / f"gear_ui_{mode_name}_{s_idx}.js"
                        js_file.write_text(js_code, encoding="utf-8")
                        proc = subprocess.run(
                            [node_bin, "--check", str(js_file)],
                            capture_output=True,
                            text=True,
                            timeout=15,
                        )
                        self.assertEqual(
                            proc.returncode,
                            0,
                            f"JS syntax error in {mode_name} script[{s_idx}]:\n{proc.stderr}",
                        )

        def send_and_collect(payload: dict[str, Any] | str, expected_types: set[str], timeout: float = 6.0) -> list[dict[str, Any]]:
            start_idx = len(self.harness.posted_page_messages)
            page_cap.on_message(payload)
            deadline = time.monotonic() + timeout
            while time.monotonic() < deadline:
                batch = self.harness.posted_page_messages[start_idx:]
                seen = {m.get("type") for m in batch if isinstance(m, dict)}
                if expected_types.issubset(seen):
                    return batch
                time.sleep(0.03)
            return self.harness.posted_page_messages[start_idx:]

        # 1. `ready` roundtrip
        ready_msgs = send_and_collect(
            json.dumps({"type": "ready", "mode": "page"}),
            {"init_state", "analysis_result"},
        )
        init_msg = [m for m in ready_msgs if m.get("type") == "init_state"][0]
        self.assertEqual(len(init_msg.get("builtin_presets", [])), 12)
        self.assertIsInstance(init_msg.get("params"), dict)
        init_rep = [m for m in ready_msgs if m.get("type") == "analysis_result"][0]["report"]
        self.assertIsInstance(init_rep, dict)

        # 2. `analyze` roundtrip
        test_params = normalize_params(
            {
                "name": "Bridge Helical 45",
                "gear_type": "helical",
                "helix_angle_deg": 45.0,
                "module_mm": 2.0,
                "face_width_mm": 10.0,
                "auto_configure_slicer": True,
                "export_target": "pair_separated",
                "pinion": {"teeth": 14, "bore_type": "d_shaft", "bore_diameter_mm": 5.0},
                "gear": {"teeth": 28, "bore_type": "round", "bore_diameter_mm": 8.0, "lightening_mode": "solid"},
            }
        )
        an_msgs = send_and_collect({"type": "analyze", "params": test_params}, {"analysis_result"})
        an_rep = [m for m in an_msgs if m.get("type") == "analysis_result"][0]["report"]
        self.assertIn("status", an_rep)

        # 3. `randomize` roundtrip
        rnd_msgs = send_and_collect(
            json.dumps({"type": "randomize", "seed": 123, "params": test_params}),
            {"params_updated"},
        )
        rnd_msg = [m for m in rnd_msgs if m.get("type") == "params_updated"][0]
        self.assertIsInstance(rnd_msg.get("params"), dict)

        # 4. `preset_save` & `preset_delete` roundtrips
        save_msgs = send_and_collect(
            json.dumps({"type": "preset_save", "name": "Bridge Preset QA", "params": test_params}),
            {"presets_updated"},
        )
        user_list = [m for m in save_msgs if m.get("type") == "presets_updated"][0]["user_presets"]
        self.assertEqual(len(user_list), 1)
        saved_id = user_list[0]["id"]

        del_msgs = send_and_collect(
            json.dumps({"type": "preset_delete", "id": saved_id}),
            {"presets_updated"},
        )
        after_del = [m for m in del_msgs if m.get("type") == "presets_updated"][0]["user_presets"]
        self.assertEqual(len(after_del), 0)

        # 5. `export_file` STL & 3MF roundtrips
        exp_stl_msgs = send_and_collect(
            json.dumps(
                {
                    "type": "export_file",
                    "format": "stl",
                    "export_target": "pair_separated",
                    "params": test_params,
                }
            ),
            {"action_result"},
        )
        stl_res = [m for m in exp_stl_msgs if m.get("type") == "action_result"][0]
        self.assertTrue(stl_res.get("ok"), f"STL export_file failed: {stl_res}")
        stl_paths = stl_res.get("paths") or ([stl_res["path"]] if "path" in stl_res else [])
        self.assertEqual(len(stl_paths), 2)
        for sp in stl_paths:
            self.assertTrue(Path(sp).is_file())

        exp_3mf_msgs = send_and_collect(
            json.dumps(
                {
                    "type": "export_file",
                    "format": "3mf",
                    "export_target": "fit_test_kit",
                    "params": test_params,
                }
            ),
            {"action_result"},
        )
        mf_res = [m for m in exp_3mf_msgs if m.get("type") == "action_result"][0]
        self.assertTrue(mf_res.get("ok"), f"3MF export_file failed: {mf_res}")
        mf_paths = mf_res.get("paths") or ([mf_res["path"]] if "path" in mf_res else [])
        self.assertEqual(len(mf_paths), 1)
        self._validate_3mf_archive(Path(mf_paths[0]), expected_item_count=4)

        # 6. `send_to_plater` cross-platform in-process IPC (Win32 WM_COPYDATA + macOS Cocoa) & off-UI-thread preset update
        self.harness.process_transactions.clear()
        self.harness.tx_event.clear()

        with (
            mock.patch.object(mod, "_find_orca_mainframe_hwnd", return_value=0x123456) as mock_hwnd,
            mock.patch.object(mod, "_dispatch_copydata_to_hwnd", return_value=(True, "ok")) as mock_copydata,
            mock.patch.object(mod.sys, "platform", "win32"),
        ):
            plater_msgs = send_and_collect(
                json.dumps(
                    {
                        "type": "send_to_plater",
                        "export_target": "pair_separated",
                        "params": test_params,
                    }
                ),
                {"action_result"},
                timeout=8.0,
            )
            plater_res = [m for m in plater_msgs if m.get("type") == "action_result"][0]
            self.assertTrue(plater_res.get("ok"), f"send_to_plater failed: {plater_res}")
            self.assertGreaterEqual(mock_hwnd.call_count, 1)
            self.assertGreaterEqual(mock_copydata.call_count, 1)

            dispatched_hwnd, dispatched_payload = mock_copydata.call_args_list[0][0][:2]
            self.assertEqual(dispatched_hwnd, 0x123456)
            self.assertTrue(
                dispatched_payload.startswith('"orca-slicer.exe";'),
                f"WM_COPYDATA payload must start with '\"orca-slicer.exe\";', got: {dispatched_payload!r}",
            )
            self.assertFalse(dispatched_payload.endswith(";"))

            sent_files = plater_res.get("paths") or []
            self.assertEqual(len(sent_files), 2)
            for sf in sent_files:
                self.assertTrue(Path(sf).is_file(), f"Missing exported plater file: {sf}")

            # Verify async mechanical slicer preset update occurred off the UI thread
            self.harness.tx_event.wait(timeout=4.0)
            self.assertGreaterEqual(
                len(self.harness.process_transactions),
                1,
                "Expected async mechanical preset update via orca.host.preset.process",
            )
            merged_tx: dict[str, str] = {}
            for tx in self.harness.process_transactions:
                self.assertFalse(
                    tx["on_ui_thread"],
                    "CRITICAL DEADLOCK BUG: preset.process update called synchronously on UI thread!",
                )
                merged_tx.update(tx["updates"])

            self.assertEqual(merged_tx.get("spiral_mode"), "0")
            self.assertGreaterEqual(int(merged_tx.get("wall_loops", "0")), 4)

        # 6b. Verify macOS (`darwin`) path resolution & Cocoa Plater dispatch routing
        mac_root = mod._orca_user_config_root("darwin")
        self.assertEqual(mac_root, Path.home() / "Library" / "Application Support" / "OrcaSlicer")
        self.assertEqual(
            build_mod.get_install_dir("darwin"),
            Path.home() / "Library" / "Application Support" / "OrcaSlicer" / "orca_plugins" / "orca_gear_generator",
        )

        with (
            mock.patch.object(mod.sys, "platform", "darwin"),
            mock.patch.object(
                mod,
                "_dispatch_macos_open_files",
                return_value=(True, "ok (NSApp.delegate application:openFiles:)"),
            ) as mock_mac_open,
        ):
            mac_msgs = send_and_collect(
                json.dumps(
                    {
                        "type": "send_to_plater",
                        "export_target": "pinion_only",
                        "params": test_params,
                    }
                ),
                {"action_result"},
                timeout=8.0,
            )
            mac_res = [m for m in mac_msgs if m.get("type") == "action_result"][0]
            self.assertTrue(mac_res.get("ok"), f"macOS send_to_plater failed: {mac_res}")
            self.assertEqual(mock_mac_open.call_count, 1)
            mac_sent_files = mock_mac_open.call_args_list[0][0][0]
            self.assertEqual(len(mac_sent_files), 1)
            self.assertTrue(Path(mac_sent_files[0]).is_file())

        # 7. Dock panel execution & message roundtrip
        exec_res = dock_cap.execute()
        if asyncio.iscoroutine(exec_res):
            asyncio.run(exec_res)
        self.assertEqual(len(self.harness.dock_panels), 1)
        dock_panel = self.harness.dock_panels[0]
        self.assertEqual(dock_panel.dock, "right")
        self.assertTrue(callable(dock_panel.on_message))
        dock_panel.on_message({"type": "ready", "mode": "dock"})
        dock_msg_types = {m.get("type") for m in dock_panel.posted if isinstance(m, dict)}
        self.assertIn("init_state", dock_msg_types)
        self.assertIn("analysis_result", dock_msg_types)


if __name__ == "__main__":
    unittest.main(verbosity=2)
