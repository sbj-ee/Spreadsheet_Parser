# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains small, self-contained Python examples for reading every
sheet of an Excel workbook and exporting the data to Polars, SQLite, CSV,
Parquet, or JSON.

## Dependencies

Python 3.9+ (the code uses `dict[str, ...]` hints; developed and tested on 3.14).
Runtime deps are in `requirements.txt`; `requirements-dev.txt` adds pytest.

- **polars** - DataFrame library for data manipulation
- **pandas** - Used for Excel file reading (ExcelFile, read_excel) and SQLite export (`to_sql`)
- **numpy** - Numerical operations (warnings are suppressed)
- **sqlalchemy** - Database connectivity for SQLite export
- **openpyxl** - The engine pandas uses to read `.xlsx` files
- **pyarrow** - Required by `pl.from_pandas` for non-trivial dtypes, and for Parquet export

## Architecture

Shared logic lives in **spreadsheet_utils.py**:
- `suppress_numpy_warnings()` - silences the spurious numpy/pandas warnings raised while reading Excel
- `load_sheets_pandas(path)` - returns `dict[str, pandas.DataFrame]`, one entry per sheet
- `load_sheets(path)` - returns `dict[str, polars.DataFrame]`, one entry per sheet
- `sanitize_name(name)` - turns a sheet name into a table/file identifier: strips surrounding whitespace and replaces spaces with underscores; other characters are left as-is

The numbered example scripts each demonstrate one export target, import from
`spreadsheet_utils`, and expose a `main(...)` function that the tests call directly:

1. **example1.py** - Load all sheets into a dict of Polars DataFrames and print it (all rows)
2. **example2.py** - Export each sheet to a SQLite table via pandas `to_sql(if_exists="replace")`
3. **example3.py** - Export each sheet to a separate CSV file (creates the output dir, overwrites files)
4. **example4.py** - Export each sheet to a separate Parquet file (creates the output dir, overwrites files)
5. **example5.py** - Concatenate all sheets into one DataFrame with a `source_sheet` column, using a `diagonal_relaxed` concat (columns matched by name, gaps filled with nulls)
6. **example6.py** - Export the whole workbook to one JSON object keyed by sheet name; non-JSON values such as dates are serialized with `str()`

`example.xlsx` is the bundled sample workbook with three sheets: `Sales` (4 rows),
`Inventory` (3 rows) and `Employees` (3 rows).

## Running Scripts

Each example takes the workbook path (and where relevant an output path) as
command-line arguments, defaulting to `example.xlsx`. Relative output paths are
resolved against the current directory:

```bash
python example1.py file.xlsx                   # stdout
python example2.py file.xlsx output.db         # default output.db
python example3.py file.xlsx csv_output        # default csv_output/
python example4.py file.xlsx parquet_output    # default parquet_output/
python example5.py file.xlsx                   # stdout
python example6.py file.xlsx output.json       # default output.json
```

Generated outputs (`*.db`, `*.json`, `csv_output/`, `parquet_output/`) are gitignored.

## Testing

```bash
pip install -r requirements-dev.txt
pytest
```

`tests/test_examples.py` covers the shared helpers and each example's `main()`.
It does not use `example.xlsx`: the `sample_xlsx` fixture in the root
`conftest.py` generates a two-sheet workbook (`Sales North`, `Inventory`) in a
temp directory. The root-level `conftest.py` also puts the repo root on
`sys.path` so the examples import cleanly.

Keep `README.md` in sync when changing example behaviour.
