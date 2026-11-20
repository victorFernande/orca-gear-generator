"""Create isolated test pages; no native OrcaSlicer or user storage is accessed."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from gear_studio.schema import DEFAULT_PARAMS
from gear_studio.studio_ui import get_studio_html
from gear_studio.locale_catalog import SUPPORTED_LANGUAGES


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args=parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    records=[]
    for mode in ("page", "dock"):
        for theme in ("light", "dark"):
            for code in SUPPORTED_LANGUAGES:
                name=f"{mode}-{theme}-{code}.html"
                context={"lang":code,"theme":theme,"params":DEFAULT_PARAMS,
                         "user_presets":[{"id":"mine", "name":"Save", "name_en":"Save", "name_pt":"Save", "params":DEFAULT_PARAMS}]}
                (args.output/name).write_text(get_studio_html(mode,context),encoding="utf-8")
                records.append({"file":name,"mode":mode,"theme":theme,"lang":code})
    (args.output/"pages.json").write_text(json.dumps(records),encoding="utf-8")


if __name__ == "__main__": main()
