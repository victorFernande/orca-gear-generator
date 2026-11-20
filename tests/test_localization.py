"""Language persistence and packaging invariants independent of native Orca UI."""
from __future__ import annotations

import ast
import gc
import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from gear_studio.locale_catalog import SUPPORTED_LANGUAGES, TRANSLATION_CATALOG, normalize_language, translate_message
from gear_studio import plugin_main
from gear_studio.studio_ui import _STUDIO_UI_HTML_TEMPLATE, get_studio_html


class LocalizationTests(unittest.TestCase):
    def test_known_host_messages_preserve_numbers_paths_and_user_text(self):
        # Completeness is a regression promise for these authored catalogs only.
        # Future data-only languages are explicitly allowed to be partial.
        for code in ("es", "it", "fr", "de", "ja"):
            text = translate_message("Exported successfully (2 file(s)): My custom 日本語.stl", code)
            self.assertNotIn("Exported successfully", text)
            self.assertIn("My custom 日本語.stl", text)
            self.assertIn("2", text)
            self.assertEqual(translate_message("Unknown error with custom text", code), "Unknown error with custom text")
    def test_locale_variants_and_unsupported_fallback(self):
        for code in SUPPORTED_LANGUAGES:
            self.assertEqual(normalize_language(code.upper().replace("-", "_")), code)
            self.assertEqual(normalize_language(code + "-!unavailable"), code)
            self.assertEqual(normalize_language(code + ".UTF-8"), code)
            self.assertEqual(plugin_main._detect_language({"language": code.upper().replace("-", "_")}), code)
        self.assertEqual(normalize_language(None), "pt")
        self.assertEqual(normalize_language("!unsupported"), "en")
        self.assertEqual(plugin_main._detect_language({"language": "!unsupported"}), "en")

    def test_all_core_keys_specs_and_builtins_have_translations(self):
        source = _STUDIO_UI_HTML_TEMPLATE
        english = source.split("    en: {", 1)[1].split("\n    }", 1)[0]
        phrases = set(re.findall(r'^\s+\w+: "(.*)"[,\n]', english, re.M))
        phrases.update(re.findall(r'\ben: "([^"\n]+)"', source.split("const SLIDER_SPECS =", 1)[1].split("\n  ];", 1)[0]))
        from gear_studio.presets_catalog import BUILTIN_PRESETS
        for preset in BUILTIN_PRESETS:
            phrases.update((preset["name_en"], preset["desc_en"]))
        for code in ("es", "it", "fr", "de", "ja"):
            missing = phrases - TRANSLATION_CATALOG[code].keys()
            self.assertEqual(missing, set(), (code, missing))
            for source, translated in TRANSLATION_CATALOG[code].items():
                self.assertTrue(translated)
                self.assertEqual(sorted(re.findall(r"\{\w+\}", source)), sorted(re.findall(r"\{\w+\}", translated)))

    def test_manual_preference_survives_host_and_reopen_and_notifies_two_views(self):
        with tempfile.TemporaryDirectory() as td, patch.object(plugin_main, "_resolve_storage_dir", return_value=Path(td)):
            controller = plugin_main.GearStudioController()
            page_messages, dock_messages = [], []
            def page(message): page_messages.append(message)
            def dock(message): dock_messages.append(message)
            # Unsupported messages register the sinks without expensive analysis.
            controller.handle_message({"type": "test_subscribe"}, page)
            controller.handle_message({"type": "test_subscribe"}, dock, default_mode="dock")
            controller.handle_message({"type": "ui_preferences", "lang": "it"}, page)
            self.assertEqual(page_messages[-1]["lang"], "it")
            self.assertEqual(page_messages[-1]["language_revision"], 1)
            self.assertEqual(dock_messages[-1], page_messages[-1])
            self.assertEqual(json.loads((Path(td)/"ui_preferences.json").read_text())["lang"], "it")
            with patch.object(plugin_main.orca.host, "app_language", return_value="de_DE"):
                self.assertEqual(controller.read_host_context()["lang"], "it")
                self.assertTrue(controller.read_host_context()["lang_explicit"])
                reopened = plugin_main.GearStudioController()
                self.assertEqual(reopened.read_host_context()["lang"], "it")
            self.assertEqual(len(controller._listeners), 2)
            replacement = []
            controller.handle_message({"type": "test_subscribe"}, replacement.append)
            controller.handle_message({"type": "ui_preferences", "lang": "ja"}, replacement.append)
            self.assertEqual(replacement[-1]["lang"], "ja")
            self.assertEqual(dock_messages[-1]["lang"], "ja")
            self.assertEqual(len(controller._listeners), 2)

    def test_storage_is_loaded_only_inside_host_callback(self):
        with tempfile.TemporaryDirectory() as td, patch.object(plugin_main, "_resolve_storage_dir", return_value=Path(td)) as resolve:
            (Path(td)/"ui_preferences.json").write_text('{"lang":"fr"}',encoding="utf-8")
            controller = plugin_main.GearStudioController()
            resolve.assert_not_called()
            self.assertEqual(controller.read_host_context()["lang"], "fr")
            resolve.assert_called_once()

    def test_page_and_dock_include_script_safe_offline_catalog(self):
        for mode in ("page", "dock"):
            for code in SUPPORTED_LANGUAGES:
                html = get_studio_html(mode, {"lang": code.upper().replace("-", "_")})
                self.assertIn(f'<html lang="{code}"', html)
                self.assertIn('id="lang-select"', html)
                self.assertIn('日本語', html)
                self.assertNotRegex(html, r'<script[^>]+src=')
                self.assertIn('"locales":', html)

    def test_packed_template_is_exact_and_bridge_stays_readable(self):
        spec=importlib.util.spec_from_file_location("gear_build_test", ROOT/"scripts/build_and_install.py")
        build=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(build)
        bundle=build.build_bundle()
        text=bundle.read_text(encoding="utf-8")
        self.assertIn("class GearStudioController", text)
        self.assertIn("# version = \"1.4.0\"", text)
        tree=ast.parse(text)
        assignment=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="_STUDIO_UI_HTML_TEMPLATE" for t in n.targets))
        import base64, zlib
        namespace={"_gear_ui_b64":base64, "_gear_ui_zlib":zlib}
        restored=eval(compile(ast.Expression(assignment.value),"template-check","eval"),namespace)
        self.assertEqual(restored,_STUDIO_UI_HTML_TEMPLATE)
        packed = next(n.value for n in ast.walk(assignment.value) if isinstance(n, ast.Constant) and isinstance(n.value, bytes))
        self.assertLess(len(packed), len(_STUDIO_UI_HTML_TEMPLATE.encode("utf-8")))


if __name__ == "__main__":
    unittest.main()
