#!/usr/bin/env python3
"""Task 1 - descriptive statistics using only the Python standard library.

Usage:
    python pure_python_stats.py data/facebook_political_ads.csv
    python pure_python_stats.py data/facebook_political_ads.csv --output pure_python_results.json
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import statistics
from collections import Counter
from pathlib import Path
from typing import Iterable, Optional

MISSING_TOKENS = {"", "na", "n/a", "null", "none", "nan", "missing"}


def clean_text(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()


def is_missing(value: object) -> bool:
    return clean_text(value).lower() in MISSING_TOKENS


def parse_number(value: object) -> Optional[float]:
    """Parse common numeric strings while leaving genuinely non-numeric text alone."""
    text = clean_text(value)
    if is_missing(text):
        return None

    # Remove common formatting while preserving signs/decimals/scientific notation.
    normalized = text.replace(",", "").replace("$", "").replace("%", "")
    normalized = re.sub(r"^\((.*)\)$", r"-\1", normalized)
    try:
        return float(normalized)
    except ValueError:
        return None


def infer_column_type(values: Iterable[object], threshold: float = 0.90) -> str:
    nonmissing = [v for v in values if not is_missing(v)]
    if not nonmissing:
        return "empty"
    numeric = sum(parse_number(v) is not None for v in nonmissing)
    return "numeric" if numeric / len(nonmissing) >= threshold else "categorical"


def compute_numeric_stats(values: Iterable[object]) -> dict:
    nums = [n for v in values if (n := parse_number(v)) is not None]
    if not nums:
        return {
            "count": 0,
            "mean": None,
            "min": None,
            "max": None,
            "std": None,
            "median": None,
        }

    return {
        "count": len(nums),
        "mean": sum(nums) / len(nums),
        "min": min(nums),
        "max": max(nums),
        # Match Pandas' default sample standard deviation (ddof=1).
        "std": statistics.stdev(nums) if len(nums) > 1 else 0.0,
        "median": statistics.median(nums),
    }


def compute_categorical_stats(values: Iterable[object]) -> dict:
    cleaned = [clean_text(v) for v in values if not is_missing(v)]
    counts = Counter(cleaned)
    most_common = counts.most_common(5)
    mode_value, mode_frequency = (most_common[0] if most_common else (None, 0))

    return {
        "count": len(cleaned),
        "unique": len(counts),
        "mode": mode_value,
        "mode_frequency": mode_frequency,
        "top_5": [{"value": value, "frequency": freq} for value, freq in most_common],
    }


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header row.")
        rows = list(reader)
        return list(reader.fieldnames), rows


def analyze(path: Path) -> dict:
    columns, rows = load_csv(path)

    result = {
        "file": path.name,
        "row_count": len(rows),
        "column_count": len(columns),
        "columns": {},
        "missing_values": {},
        "inferred_types": {},
    }

    for column in columns:
        values = [row.get(column, "") for row in rows]
        missing = sum(is_missing(v) for v in values)
        inferred = infer_column_type(values)

        result["missing_values"][column] = missing
        result["inferred_types"][column] = inferred

        if inferred == "numeric":
            result["columns"][column] = {
                "type": "numeric",
                **compute_numeric_stats(values),
            }
        elif inferred == "empty":
            result["columns"][column] = {
                "type": "empty",
                "count": 0,
            }
        else:
            result["columns"][column] = {
                "type": "categorical",
                **compute_categorical_stats(values),
            }

    return result


def fmt(value: object) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, float):
        return f"{value:,.4f}"
    return str(value)


def print_report(result: dict) -> None:
    print("=" * 72)
    print("PURE PYTHON DESCRIPTIVE STATISTICS")
    print("=" * 72)
    print(f"File: {result['file']}")
    print(f"Rows: {result['row_count']:,}")
    print(f"Columns: {result['column_count']:,}\n")

    print("Missing values and inferred types")
    print("-" * 72)
    for column in result["columns"]:
        print(
            f"{column}: missing={result['missing_values'][column]}, "
            f"type={result['inferred_types'][column]}"
        )

    for column, stats in result["columns"].items():
        print("\n" + column)
        print("-" * len(column))
        if stats["type"] == "numeric":
            for key in ("count", "mean", "min", "max", "std", "median"):
                print(f"{key:>8}: {fmt(stats[key])}")
        elif stats["type"] == "categorical":
            print(f"   count: {stats['count']}")
            print(f"  unique: {stats['unique']}")
            print(f"    mode: {stats['mode']!r}")
            print(f"mode freq: {stats['mode_frequency']}")
            print("   top 5:")
            for item in stats["top_5"]:
                print(f"      {item['frequency']:>6}  {item['value']!r}")
        else:
            print("Column is entirely missing/empty.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path, help="Path to the CSV dataset")
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()

    if not args.csv_file.exists():
        raise SystemExit(f"Dataset not found: {args.csv_file}")

    result = analyze(args.csv_file)
    print_report(result)

    if args.output:
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nJSON results written to {args.output}")


if __name__ == "__main__":
    main()
