#!/usr/bin/env python3
"""Compare JSON outputs from pure_python_stats.py and pandas_stats.py."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def close(a, b, tol=1e-9):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol)
    return a == b


def compare(a, b, path="root", diffs=None):
    if diffs is None:
        diffs = []
    if isinstance(a, dict) and isinstance(b, dict):
        for key in sorted(set(a) | set(b)):
            if key not in a or key not in b:
                diffs.append(f"{path}.{key}: key missing from one result")
            else:
                compare(a[key], b[key], f"{path}.{key}", diffs)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            diffs.append(f"{path}: list lengths differ ({len(a)} vs {len(b)})")
        else:
            for i, (x, y) in enumerate(zip(a, b)):
                compare(x, y, f"{path}[{i}]", diffs)
    elif not close(a, b):
        diffs.append(f"{path}: {a!r} != {b!r}")
    return diffs


def main():
    p = argparse.ArgumentParser()
    p.add_argument("pure_json", type=Path)
    p.add_argument("pandas_json", type=Path)
    args = p.parse_args()

    pure = json.loads(args.pure_json.read_text(encoding="utf-8"))
    pandas = json.loads(args.pandas_json.read_text(encoding="utf-8"))
    diffs = compare(pure, pandas)
    if diffs:
        print("Results differ:")
        for d in diffs:
            print(" -", d)
        raise SystemExit(1)
    print("PASS: Pure Python and Pandas results agree.")


if __name__ == "__main__":
    main()
