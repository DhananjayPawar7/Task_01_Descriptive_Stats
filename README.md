# Task 01 — Descriptive Statistics with and without Pandas

## Project description

This project implements the same descriptive-statistics workflow two independent ways:

1. `pure_python_stats.py` uses only the Python standard library (`csv`, `statistics`, `collections`, etc.).
2. `pandas_stats.py` reproduces the analysis with Pandas.

The goal is not only to calculate statistics, but to understand the assumptions behind type inference, missing-value handling, numeric conversion, and summary statistics. The assignment requires the two approaches to arrive at the same statistical truths.

## Dataset

The assignment document names a Google Drive source called **2024 Facebook Political Ads**, but the document itself does not contain a direct downloadable file URL. To keep this submission reproducible rather than inventing data, the completed analysis uses a public Meta Ad Library-derived 2024 election dataset from the project **Election Facebook's Ad Metrics 2024: Trump vs. Harris**.

Public source references:

- Zenodo record: https://doi.org/10.5281/zenodo.14718708
- GitHub source project: https://github.com/VNonTOP-DE/AD-Tech-Analytic-Project
- Analysis file used here: `6state trump data.csv`

The file contains 377 rows from six states and 10 fields describing campaign-ad delivery, creative information, byline, processed impressions, processed spend, and performance.

**Important:** the dataset itself is intentionally **not included** in this repository, in accordance with the assignment instructions. Download it from the source project and place it locally in a `data/` directory.

Recommended local layout:

```text
Task_01_Descriptive_Stats/
├── data/
│   └── 6state trump data.csv   # local only; do not commit
├── pure_python_stats.py
├── pandas_stats.py
├── compare_results.py
├── FINDINGS.md
├── COMPARISON.md
├── RESULTS_SUMMARY.md
├── requirements.txt
└── README.md
```

## Environment setup

Python 3.10+ is recommended.

Create and activate a virtual environment if desired, then install the only third-party dependency:

```bash
pip install -r requirements.txt
```

## Run the pure-Python analysis

```bash
python pure_python_stats.py "data/6state trump data.csv"
```

To save machine-readable results:

```bash
python pure_python_stats.py "data/6state trump data.csv" --output pure_python_results.json
```

The pure-Python script computes:

- total row count and column count;
- missing values for every column;
- inferred data type for every column;
- numeric count, mean, min, max, sample standard deviation, and median;
- categorical non-null count, unique count, mode/frequency, and top five values.

## Run the Pandas analysis

```bash
python pandas_stats.py "data/6state trump data.csv"
```

To save equivalent machine-readable results:

```bash
python pandas_stats.py "data/6state trump data.csv" --output pandas_results.json
```

The Pandas script also displays `shape`, `dtypes`, `info()`, and `describe(include='all')`, then calculates normalized statistics using the same explicit cleaning rules as the manual implementation.

## Verify that both approaches agree

After generating both JSON result files:

```bash
python compare_results.py pure_python_results.json pandas_results.json
```

Expected output:

```text
PASS: Pure Python and Pandas results agree.
```

## Summary of findings

The analyzed public extract contains **377 rows and 10 columns**. Three fields are numeric: processed impressions, processed spend, and performance. The impression and spend distributions are highly right-skewed: mean impressions are about 562,368 compared with a median of about 108,498, while mean processed spend is about 18,165 compared with a median of 3,098.

Missingness is limited mainly to text fields: 2 missing creative bodies, 16 missing creative link descriptions, and 2 missing link titles. The core numeric fields are complete.

Geographically, Pennsylvania has the most rows (90) and the largest processed spend total (about 1.96 million), closely followed by Michigan (about 1.85 million). The byline distribution is also concentrated, with `DONALD J. TRUMP FOR PRESIDENT 2024, INC.` accounting for most rows and most processed spend in this specific extract.

See [`FINDINGS.md`](FINDINGS.md) for the full narrative and [`RESULTS_SUMMARY.md`](RESULTS_SUMMARY.md) for the principal statistics.

## Comparison of the two approaches

The results agree when both implementations use the same rules. The manual version makes assumptions about missingness, type inference, numeric parsing, and standard deviation explicit. Pandas makes the same analysis much shorter and easier to extend but can hide those choices behind automatic inference and convenience methods.

See [`COMPARISON.md`](COMPARISON.md) for the full reflection.

## Reproducibility notes

- The dataset path is supplied as a command-line argument; there are no hard-coded local paths.
- The dataset is not stored in this repository.
- Both scripts use UTF-8 with BOM support (`utf-8-sig`) to handle common CSV exports.
- Both scripts apply the same missing-token set and numeric-cleaning logic.
- Both scripts use sample standard deviation (`ddof=1`).
- `compare_results.py` provides a direct automated equality check between the two JSON outputs.

## Repository contents

| File | Purpose |
|---|---|
| `pure_python_stats.py` | Standard-library-only descriptive statistics |
| `pandas_stats.py` | Equivalent Pandas analysis |
| `compare_results.py` | Verifies both output files agree |
| `FINDINGS.md` | 1–2 page narrative analysis |
| `COMPARISON.md` | Reflection comparing approaches |
| `RESULTS_SUMMARY.md` | Key computed statistics |
| `requirements.txt` | Pandas dependency |
| `README.md` | Project instructions and overview |

## Scope limitation

This public extract is narrower than all political advertising on Meta during the 2024 election and should not be generalized beyond the dataset. If the exact instructor-provided Google Drive CSV becomes available, the same two scripts can be run against it by changing only the command-line file path; the dataset-specific findings should then be regenerated from that exact file.
