"""Adapt discovered, independently packaged offline language catalogs to the Gear UI."""
from __future__ import annotations
import re
from .language_packs import load_language_packs, resolve_language, language_pack_payload

LANGUAGE_PACKS, LANGUAGE_PACK_ERRORS = load_language_packs()
SUPPORTED_LANGUAGES = tuple(LANGUAGE_PACKS)
LANGUAGE_NAMES = tuple(pack["native_name"] for pack in LANGUAGE_PACKS.values())
TRANSLATION_CATALOG = {code: pack["translations"] for code, pack in LANGUAGE_PACKS.items()}
LANGUAGE_METADATA = language_pack_payload(LANGUAGE_PACKS)


def normalize_language(value: object, default: str = "pt") -> str:
    return resolve_language(value, LANGUAGE_PACKS, default)


def translate_message(text: str, language: str) -> str:
    """Localize known host messages, preserving captured paths and filenames verbatim."""
    catalog = TRANSLATION_CATALOG.get(normalize_language(language), {})
    if text in catalog:
        return catalog[text]
    for source, target in catalog.items():
        pieces = re.split(r"(\{[a-z][a-z0-9_]*\})", source)
        names = [piece for piece in pieces if re.fullmatch(r"\{[a-z][a-z0-9_]*\}", piece)]
        if not names:
            continue
        pattern = "".join("(.+?)" if piece in names else re.escape(piece) for piece in pieces)
        match = re.fullmatch(pattern, text)
        if match:
            for name, value in zip(names, match.groups(), strict=True):
                target = target.replace(name, value)
            return target
    return text
