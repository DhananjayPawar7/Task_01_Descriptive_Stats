#!/usr/bin/env python3
"""Task 1 - equivalent descriptive statistics using Pandas.

Usage:
    python pandas_stats.py data/facebook_political_ads.csv
    python pandas_stats.py data/facebook_political_ads.csv --output pandas_results.json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd

MISSING_TOKENS = {"", "na", "n/a", "null", "none", "nan", "missing"}


def cleaned_strings(series: pd.Series) -> pd.Series:
    s = series.astype("string").str.strip()
    return s.mask(s.str.lower().isin(MISSING_TOKENS))


def numeric_candidate(series: pd.Series) -> pd.Series:
    s = cleaned_strings(series)
    s = s.str.replace(",", "", regex=False)
    s = s.str.replace("$", "", regex=False)
    s = s.str.replace("%", "", regex=False)
    s = s.str.replace(r"^\((.*)\)$", r"-\1", regex=True)
    return pd.to_numeric(s, errors="coerce")


def infer_column_type(series: pd.Series, threshold: float = 0.90) -> str:
    s = cleaned_strings(series)
    nonmissing = s.dropna()
    if nonmissing.empty:
        return "empty"
    nums = numeric_candidate(series)
    numeric_share = nums.notna().sum() / len(nonmissing)
    return "numeric" if numeric_share >= threshold else "categorical"


def analyze(path: Path) -> dict:
    # Read as strings first so type inference follows the same explicit rules as
    # the pure-Python implementation instead of silently relying on Pandas dtype inference.
    df = pd.read_csv(path, dtype="string", keep_default_na=False, encoding="utf-8-sig")

    result = {
        "file": path.name,
        "row_count": int(df.shape[0]),
        "column_count": int(df.shape[1]),
        "columns": {},
        "missing_values": {},
        "inferred_types": {},
    }

    for column in df.columns:
        s = cleaned_strings(df[column])
        missing = int(s.isna().sum())
        inferred = infer_column_type(df[column])
        result["missing_values"][column] = missing
        result["inferred_types"][column] = inferred

        if inferred == "numeric":
            nums = numeric_candidate(df[column]).dropna()
            result["columns"][column] = {
                "type": "numeric",
                "count": int(nums.count()),
                "mean": float(nums.mean()) if len(nums) else None,
                "min": float(nums.min()) if len(nums) else None,
                "max": float(nums.max()) if len(nums) else None,
                "std": float(nums.std(ddof=1)) if len(nums) > 1 else (0.0 if len(nums) == 1 else None),
                "median": float(nums.median()) if len(nums) else None,
            }
        elif inferred == "empty":
            result["columns"][column] = {"type": "empty", "count": 0}
        else:
            nonmissing = s.dropna()
            counts = nonmissing.value_counts(dropna=True)
            top5 = counts.head(5)
            mode = None if counts.empty else str(counts.index[0])
            mode_freq = 0 if counts.empty else int(counts.iloc[0])
            result["columns"][column] = {
                "type": "categorical",
                "count": int(nonmissing.count()),
                "unique": int(nonmissing.nunique(dropna=True)),
                "mode": mode,
                "mode_frequency": mode_freq,
                "top_5": [
                    {"value": str(value), "frequency": int(freq)}
                    for value, freq in top5.items()
                ],
            }

    return result, df


def fmt(value: object) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, float):
        return f"{value:,.4f}"
    return str(value)


def print_report(result: dict, df: pd.DataFrame) -> None:
    print("=" * 72)
    print("PANDAS DESCRIPTIVE STATISTICS")
    print("=" * 72)
    print(f"File: {result['file']}")
    print(f"Shape: {df.shape}")
    print("\nRaw string dtypes used for controlled inference:")
    print(df.dtypes)
    print("\nDataFrame info:")
    df.info()

    print("\nMissing values and inferred types")
    print("-" * 72)
    for column in result["columns"]:
        print(
            f"{column}: missing={result['missing_values'][column]}, "
            f"type={result['inferred_types'][column]}"
        )

    print("\nPandas describe(include='all') on the raw imported frame")
    print("-" * 72)
    print(df.describe(include="all").transpose().to_string())

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

    result, df = analyze(args.csv_file)
    print_report(result, df)

    if args.output:
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nJSON results written to {args.output}")


if __name__ == "__main__":
    main()
