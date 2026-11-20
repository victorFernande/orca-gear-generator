"""Measure fresh bundle imports; report medians without a native-Orca timing claim."""
from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--samples", type=int, default=7)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    code = """import importlib.util,json,sys,time
p=sys.argv[1]
t=time.perf_counter()
s=importlib.util.spec_from_file_location('orca_gear_measure',p)
m=importlib.util.module_from_spec(s)
sys.modules[s.name]=m
s.loader.exec_module(m)
print(json.dumps({'import_ms':(time.perf_counter()-t)*1000}))
"""
    samples = []
    for _ in range(args.samples):
        result = subprocess.run([sys.executable, "-B", "-W", "error", "-c", code,
                                 str(args.bundle.resolve())], check=True, capture_output=True, text=True)
        samples.append(json.loads(result.stdout.strip().splitlines()[-1])["import_ms"])
    report = {"method": "sequential fresh Python subprocess imports including NumPy; no OS cache flush",
              "samples": samples, "median_ms": statistics.median(samples),
              "bundle_bytes": args.bundle.stat().st_size, "python": sys.version.split()[0]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
