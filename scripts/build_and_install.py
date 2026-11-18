#!/usr/bin/env python3
"""Single-file PEP 723 bundler and local installer for Orca Gear Studio.

Compiles all modules under `src/gear_studio/` into a self-contained single-file
OrcaSlicer 2.5.1+ plugin (`dist/orca_gear_generator.py`) and deploys ONLY
`orca_gear_generator.py` + `icon.svg` into:
`%APPDATA%\\OrcaSlicer\\orca_plugins\\orca_gear_generator\\`
"""

from __future__ import annotations

import ast
import base64
import hashlib
import io
import os
import re
import shutil
import sys
import tempfile
import tokenize
import tomllib
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PKG_DIR = PROJECT_ROOT / "src" / "gear_studio"
DIST_DIR = PROJECT_ROOT / "dist"
DIST_BUNDLE_PATH = DIST_DIR / "orca_gear_generator.py"
ICON_SRC_PATH = SRC_PKG_DIR / "icon.svg"

MODULE_ORDER: list[str] = [
    "schema.py",
    "involute_math.py",
    "fit_and_kinematics.py",
    "mesh_generator.py",
    "presets_catalog.py",
    "exporters.py",
    "studio_ui.py",
    "plugin_main.py",
]

PEP723_HEADER = """\
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
"""

PLUGIN_VERSION = "1.2.0"
PRESERVED_SIDE_FILES: frozenset[str] = frozenset(
    {
        "orca_gear_generator.py",
        "icon.svg",
        ".install_state.json",
        "install_state.json",
    }
)


def get_orca_base_dir(platform_name: str | None = None) -> Path:
    """Resolve OrcaSlicer user directory across Windows (`win32`), macOS (`darwin`), and Linux."""
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


def get_install_dir(platform_name: str | None = None) -> Path:
    return get_orca_base_dir(platform_name) / "orca_plugins" / "orca_gear_generator"


def extract_pep723_toml(source: str) -> dict:
    """Parse and validate PEP 723 `# /// script ... # ///` block using stdlib `tomllib`."""
    in_block = False
    toml_lines: list[str] = []
    for line in source.splitlines():
        stripped = line.strip()
        if not in_block:
            if stripped == "# /// script":
                in_block = True
            continue
        if stripped == "# ///":
            break
        if line.startswith("# "):
            toml_lines.append(line[2:])
        elif line.startswith("#"):
            toml_lines.append(line[1:])
        else:
            raise ValueError(f"Invalid non-comment line inside PEP 723 header: {line!r}")
    else:
        raise ValueError("Missing closing `# ///` for PEP 723 script block.")

    return tomllib.loads("\n".join(toml_lines))


def _collect_top_level_private_defs(tree: ast.Module) -> tuple[set[str], set[str]]:
    """Return `(private_top_defs, class_attr_names)` for collision analysis."""
    privates: set[str] = set()
    class_attrs: set[str] = set()

    def _record_target(target: ast.AST) -> None:
        if isinstance(target, ast.Name):
            nm = target.id
            if nm.startswith("_") and not (nm.startswith("__") and nm.endswith("__")):
                privates.add(nm)
        elif isinstance(target, (ast.Tuple, ast.List)):
            for elt in target.elts:
                _record_target(elt)

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            nm = node.name
            if nm.startswith("_") and not (nm.startswith("__") and nm.endswith("__")):
                privates.add(nm)
            if isinstance(node, ast.ClassDef):
                for sub in node.body:
                    if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        class_attrs.add(sub.name)
                    elif isinstance(sub, ast.Assign):
                        for t in sub.targets:
                            if isinstance(t, ast.Name):
                                class_attrs.add(t.id)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                _record_target(t)
        elif isinstance(node, ast.AnnAssign) and node.target is not None:
            _record_target(node.target)

    return privates, class_attrs


def _rename_colliding_privates(source: str, mod_stem: str, to_rename: set[str]) -> str:
    """Token-safely prefix colliding module-private helper names without touching strings/JS."""
    if not to_rename:
        return source

    tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    rewritten: list[tokenize.TokenInfo] = []
    prev_significant_str = ""

    for tok in tokens:
        if tok.type == tokenize.NAME and tok.string in to_rename and prev_significant_str != ".":
            tok = tok._replace(string=f"_{mod_stem}{tok.string}")
        rewritten.append(tok)
        if tok.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT):
            prev_significant_str = tok.string

    return tokenize.untokenize(rewritten)


def _strip_internal_imports(source: str) -> tuple[str, set[str]]:
    """Strip `from __future__` and intra-package `gear_studio` imports via AST line spans."""
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    future_features: set[str] = set()

    replacements: list[tuple[int, int, str]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            mod_name = node.module or ""
            is_future = node.level == 0 and mod_name == "__future__"
            is_internal = node.level >= 1 or mod_name == "gear_studio" or mod_name.startswith("gear_studio.")

            if not (is_future or is_internal):
                continue

            start_line = node.lineno
            end_line = node.end_lineno or node.lineno
            first_line = lines[start_line - 1]
            indent_match = re.match(r"^[ \t]*", first_line)
            indent = indent_match.group(0) if indent_match else ""

            if is_future:
                for alias in node.names:
                    future_features.add(alias.name)
                repl = f"{indent}pass  # [bundled] hoisted __future__ import\n"
                replacements.append((start_line, end_line, repl))
                continue

            stmts: list[str] = []
            if node.level >= 1 and not mod_name:
                stmts.append(f"{indent}import sys as _orca_bundle_sys\n")
                for alias in node.names:
                    bound_name = alias.asname or alias.name
                    stmts.append(f"{indent}{bound_name} = _orca_bundle_sys.modules[__name__]\n")
            else:
                for alias in node.names:
                    if alias.name == "*":
                        continue
                    if alias.asname and alias.asname != alias.name:
                        stmts.append(f"{indent}{alias.asname} = {alias.name}\n")
                if not stmts:
                    stmts.append(f"{indent}pass  # [bundled] resolved intra-package import\n")

            replacements.append((start_line, end_line, "".join(stmts)))

        elif isinstance(node, ast.Import):
            internal_aliases = [
                a for a in node.names if a.name == "gear_studio" or a.name.startswith("gear_studio.")
            ]
            if not internal_aliases:
                continue
            start_line = node.lineno
            end_line = node.end_lineno or node.lineno
            first_line = lines[start_line - 1]
            indent_match = re.match(r"^[ \t]*", first_line)
            indent = indent_match.group(0) if indent_match else ""

            stmts = [f"{indent}import sys as _orca_bundle_sys\n"]
            for alias in node.names:
                if alias.name == "gear_studio" or alias.name.startswith("gear_studio."):
                    bound = alias.asname or alias.name.split(".")[0]
                    stmts.append(f"{indent}{bound} = _orca_bundle_sys.modules[__name__]\n")
                else:
                    as_part = f" as {alias.asname}" if alias.asname else ""
                    stmts.append(f"{indent}import {alias.name}{as_part}\n")
            replacements.append((start_line, end_line, "".join(stmts)))

    replacements.sort(key=lambda item: (item[0], -item[1]), reverse=True)
    applied_ranges: list[tuple[int, int]] = []
    for start_line, end_line, repl_text in replacements:
        if any(not (end_line < s or start_line > e) for s, e in applied_ranges):
            continue
        lines[start_line - 1 : end_line] = [repl_text]
        applied_ranges.append((start_line, end_line))

    return "".join(lines), future_features


def build_bundle() -> Path:
    """Compile all `src/gear_studio/*.py` modules into `dist/orca_gear_generator.py`."""
    missing = [m for m in MODULE_ORDER if not (SRC_PKG_DIR / m).is_file()]
    if missing:
        raise FileNotFoundError(f"Missing required source module(s) in {SRC_PKG_DIR}: {missing}")

    raw_sources: dict[str, str] = {}
    private_defs_by_mod: dict[str, set[str]] = {}
    class_attrs_by_mod: dict[str, set[str]] = {}
    def_counts: dict[str, int] = {}

    for mod_file in MODULE_ORDER:
        src = (SRC_PKG_DIR / mod_file).read_text(encoding="utf-8")
        raw_sources[mod_file] = src
        tree = ast.parse(src, filename=mod_file)
        privs, cls_attrs = _collect_top_level_private_defs(tree)
        private_defs_by_mod[mod_file] = privs
        class_attrs_by_mod[mod_file] = cls_attrs
        for nm in privs:
            def_counts[nm] = def_counts.get(nm, 0) + 1

    colliding_privates = {nm for nm, count in def_counts.items() if count > 1}

    all_future_features: set[str] = {"annotations"}
    sections: list[str] = []

    for mod_file in MODULE_ORDER:
        mod_stem = Path(mod_file).stem
        src = raw_sources[mod_file]
        rename_set = (private_defs_by_mod[mod_file] & colliding_privates) - class_attrs_by_mod[mod_file]
        if rename_set:
            src = _rename_colliding_privates(src, mod_stem, rename_set)

        transformed, fut = _strip_internal_imports(src)
        all_future_features.update(fut)

        banner = (
            f"\n# {'=' * 75}\n"
            f"# MODULE: gear_studio.{mod_stem}\n"
            f"# {'=' * 75}\n\n"
        )
        sections.append(banner + transformed.rstrip() + "\n")

    future_stmt = f"from __future__ import {', '.join(sorted(all_future_features))}\n"
    module_bootstrap = (
        "import sys as _orca_init_sys\n"
        "import types as _orca_init_types\n"
        "if __name__ not in _orca_init_sys.modules:\n"
        "    _orca_init_sys.modules[__name__] = _orca_init_types.ModuleType(__name__)\n"
    )
    bundled_code = (
        PEP723_HEADER
        + "\n"
        + future_stmt
        + "\n"
        + module_bootstrap
        + "".join(sections)
    )

    meta = extract_pep723_toml(bundled_code)
    plugin_meta = meta.get("tool", {}).get("orcaslicer", {}).get("plugin", {})
    allowed_plugin_keys = {"name", "description", "author", "version"}
    extra_keys = set(plugin_meta.keys()) - allowed_plugin_keys
    if extra_keys:
        raise RuntimeError(f"Non-canonical [tool.orcaslicer.plugin] keys found: {extra_keys}")
    if not plugin_meta.get("name"):
        raise RuntimeError("PEP 723 header is missing [tool.orcaslicer.plugin].name")
    if not meta.get("dependencies"):
        raise RuntimeError("PEP 723 header is missing dependencies")

    if ICON_SRC_PATH.is_file():
        icon_disk = ICON_SRC_PATH.read_text(encoding="utf-8").strip()
        if icon_disk not in raw_sources["plugin_main.py"]:
            raise RuntimeError("Embedded ICON_SVG_CONTENT in plugin_main.py is out of sync with src/gear_studio/icon.svg")

    compile(bundled_code, str(DIST_BUNDLE_PATH), "exec")

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    with open(DIST_BUNDLE_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(bundled_code)

    return DIST_BUNDLE_PATH


def build_wheel() -> Path:
    """Build a standards-compliant pure-Python universal wheel (`py3-none-any.whl`) in `dist/`
    for OrcaCloud / GitHub Releases (`read_wheel_plugin_metadata` compatible).
    """
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    whl_name = f"orca_gear_generator-{PLUGIN_VERSION}-py3-none-any.whl"
    whl_path = DIST_DIR / whl_name
    dist_info = f"orca_gear_generator-{PLUGIN_VERSION}.dist-info"

    readme_text = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8") if (PROJECT_ROOT / "README.md").is_file() else ""
    metadata_content = (
        "Metadata-Version: 2.1\n"
        "Name: orca-gear-generator\n"
        f"Version: {PLUGIN_VERSION}\n"
        "Summary: Estudio parametrico 3D de engrenagens com simulacao de giro, testes de encaixe e envio direto para a mesa\n"
        "Author: Orca Gear Studio\n"
        "License: MIT\n"
        "Requires-Python: >=3.12\n"
        "Requires-Dist: numpy>=1.26\n"
        "Description-Content-Type: text/markdown\n\n"
        + readme_text
    )
    wheel_content = (
        "Wheel-Version: 1.0\n"
        "Generator: orca-gear-studio-bundler\n"
        "Root-Is-Purelib: true\n"
        "Tag: py3-none-any\n"
    )
    top_level_content = "gear_studio\n"

    entries: list[tuple[str, bytes]] = []
    pkg_files = ["__init__.py", *MODULE_ORDER, "icon.svg"]
    for fname in pkg_files:
        fpath = SRC_PKG_DIR / fname
        if fpath.is_file():
            entries.append((f"gear_studio/{fname}", fpath.read_bytes()))

    if (PROJECT_ROOT / "LICENSE").is_file():
        entries.append((f"{dist_info}/LICENSE", (PROJECT_ROOT / "LICENSE").read_bytes()))
    entries.append((f"{dist_info}/METADATA", metadata_content.encode("utf-8")))
    entries.append((f"{dist_info}/WHEEL", wheel_content.encode("utf-8")))
    entries.append((f"{dist_info}/top_level.txt", top_level_content.encode("utf-8")))

    record_lines: list[str] = []
    for arc_path, data in entries:
        digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode("ascii")
        record_lines.append(f"{arc_path},sha256={digest},{len(data)}")
    record_lines.append(f"{dist_info}/RECORD,,")
    entries.append((f"{dist_info}/RECORD", ("\n".join(record_lines) + "\n").encode("utf-8")))

    with zipfile.ZipFile(whl_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for arc_path, data in entries:
            zf.writestr(arc_path, data)

    return whl_path


def install_plugin(bundle_path: Path) -> Path:
    """Install `orca_gear_generator.py` and `icon.svg` into OrcaSlicer's `orca_plugins`,
    preserving OrcaSlicer's `.install_state.json` / `install_state.json` untouched.
    """
    install_dir = get_install_dir()
    install_dir.mkdir(parents=True, exist_ok=True)

    # Remove any stale .py, .pyc, .pyo, .whl files or __pycache__ directories while
    # strictly preserving `.install_state.json` / `install_state.json` and `icon.svg`.
    for item in list(install_dir.iterdir()):
        if item.name in PRESERVED_SIDE_FILES:
            continue
        if item.is_dir() and item.name == "__pycache__":
            shutil.rmtree(item, ignore_errors=True)
        elif item.is_file() and item.suffix.lower() in {".py", ".pyc", ".pyo", ".whl"}:
            item.unlink()

    for cache_dir in list(install_dir.rglob("__pycache__")):
        shutil.rmtree(cache_dir, ignore_errors=True)

    dest_py = install_dir / "orca_gear_generator.py"
    shutil.copyfile(bundle_path, dest_py)

    if ICON_SRC_PATH.is_file():
        shutil.copyfile(ICON_SRC_PATH, install_dir / "icon.svg")

    # Enforce strict OrcaSlicer.dll v2.5.1 directory invariants
    py_files = list(install_dir.glob("*.py"))
    whl_files = list(install_dir.glob("*.whl"))
    pyc_files = [*install_dir.rglob("*.pyc"), *install_dir.rglob("*.pyo")]
    pycache_dirs = list(install_dir.rglob("__pycache__"))

    if len(py_files) != 1 or py_files[0].name != "orca_gear_generator.py":
        raise RuntimeError(f"Expected strictly 1 .py file in {install_dir}, found: {py_files}")
    if whl_files:
        raise RuntimeError(f"Found forbidden .whl file(s) in {install_dir}: {whl_files}")
    if pyc_files:
        raise RuntimeError(f"Found forbidden bytecode file(s) in {install_dir}: {pyc_files}")
    if pycache_dirs:
        raise RuntimeError(f"Found forbidden __pycache__ in {install_dir}: {pycache_dirs}")

    return install_dir


def verify_bundle_smoke(bundle_path: Path) -> None:
    """Load the generated bundle from `dist/` with a mock `orca` host to verify registration & UI."""
    import importlib.util

    meta = extract_pep723_toml(bundle_path.read_text(encoding="utf-8"))
    plugin_meta = meta.get("tool", {}).get("orcaslicer", {}).get("plugin", {})
    if plugin_meta.get("version") != PLUGIN_VERSION:
        raise RuntimeError(
            f"Expected PEP 723 plugin version {PLUGIN_VERSION!r}, got {plugin_meta.get('version')!r}"
        )

    cp_tag = f"cp{sys.version_info.major}{sys.version_info.minor}"
    pkgs_root = get_orca_base_dir() / "python" / "packages"
    for cand_pkg in (pkgs_root / cp_tag, pkgs_root / "cp312"):
        if cand_pkg.is_dir() and str(cand_pkg) not in sys.path:
            sys.path.insert(0, str(cand_pkg))

    sys.dont_write_bytecode = True

    with tempfile.TemporaryDirectory(prefix="orca_gear_smoke_") as tmp_dir:
        standalone_dir = Path(tmp_dir) / "standalone_only_py"
        standalone_dir.mkdir(parents=True, exist_ok=True)
        standalone_py = standalone_dir / "orca_gear_generator.py"
        shutil.copyfile(bundle_path, standalone_py)

        storage_only_dir = Path(tmp_dir) / "plugin_storage"
        storage_only_dir.mkdir(parents=True, exist_ok=True)

        spec = importlib.util.spec_from_file_location("orca_gear_generator_smoke", str(standalone_py))
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Could not create module spec for {standalone_py}")

        mod = importlib.util.module_from_spec(spec)
        sys.modules["orca_gear_generator_smoke"] = mod
        try:
            spec.loader.exec_module(mod)

            plugin_instance = mod.OrcaGearStudioPlugin()
            plugin_instance.register_capabilities()

            perms = getattr(mod.orca, "_requested_permissions", {})
            assert "process" not in perms, f"Unexpected process permission requested: {perms}"
            assert bool(perms.get("threading")), f"Missing threading=True permission: {perms}"

            sample_stl = Path(tmp_dir) / "gear_smoke.stl"
            sample_stl.write_bytes(b"smoke")
            payload = mod._format_other_instance_payload([sample_stl])
            assert payload.startswith('"orca-slicer.exe";'), f"Bad WM_COPYDATA prefix: {payload!r}"
            assert not payload.endswith(";"), f"Forbidden trailing semicolon in payload: {payload!r}"

            page_cap = mod.GearStudioPageCapability()
            dock_cap = mod.GearStudioDockCapability()
            assert page_cap.get_name() == "Gerador de Engrenagens"
            assert dock_cap.get_name() == "Orca Gear Studio - Painel Lateral"

            mod.orca.host.plugin.storage = lambda: str(storage_only_dir)
            icon_path = page_cap.get_icon()
            assert icon_path and Path(icon_path).is_file(), f"Icon auto-materialization failed: {icon_path!r}"

            html_page = page_cap.get_ui()
            html_dock = dock_cap.get_ui()
            assert "<html" in html_page.lower() and len(html_page) > 1000
            assert "<html" in html_dock.lower() and len(html_dock) > 1000

            outbox: list[dict] = []
            page_cap.post_message = lambda payload: outbox.append(payload)  # type: ignore[method-assign]
            page_cap.on_message('{"type": "ready", "mode": "page"}')
            assert len(outbox) >= 2
            assert outbox[0]["type"] == "init_state"
            assert outbox[1]["type"] == "analysis_result"
        finally:
            sys.modules.pop("orca_gear_generator_smoke", None)


def main() -> int:
    print("[1/4] Bundling src/gear_studio/*.py -> dist/orca_gear_generator.py ...")
    bundle_path = build_bundle()
    size_kb = bundle_path.stat().st_size / 1024.0
    print(f"      Built {bundle_path} ({size_kb:.1f} KB)")

    print("[2/4] Building universal wheel -> dist/orca_gear_generator-*.whl ...")
    whl_path = build_wheel()
    whl_kb = whl_path.stat().st_size / 1024.0
    print(f"      Built {whl_path} ({whl_kb:.1f} KB)")

    print("[3/4] Running smoke verification on dist/orca_gear_generator.py ...")
    verify_bundle_smoke(bundle_path)
    print("      Smoke check passed (PEP 723, @orca.plugin, Page + Dock UI, ready/analysis bridge).")

    print("[4/4] Installing into OrcaSlicer local plugins directory ...")
    install_dir = install_plugin(bundle_path)
    installed_entries = sorted(p.name for p in install_dir.iterdir())
    print(f"      Installed to: {install_dir}")
    print(f"      Directory contents: {installed_entries}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
