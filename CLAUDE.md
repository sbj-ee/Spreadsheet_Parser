# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains Python scripts for parsing Excel spreadsheets and loading them into different data formats. The primary use case is converting multi-sheet Excel workbooks into either Polars DataFrames or SQLite databases.

## Dependencies

The project uses these key libraries:
- **polars** - DataFrame library for data manipulation
- **pandas** - Used for Excel file reading (ExcelFile, read_excel)
- **numpy** - Numerical operations (warnings are suppressed)
- **sqlalchemy** - Database connectivity for SQLite export
- **pyarrow** - Required by `pl.from_pandas` for non-trivial dtypes, and for Parquet export

## Architecture

Shared logic lives in **spreadsheet_utils.py**:
- `suppress_numpy_warnings()` - silences the spurious numpy/pandas warnings raised while reading Excel
- `load_sheets_pandas(path)` - returns `dict[str, pandas.DataFrame]`, one entry per sheet
- `load_sheets(path)` - returns `dict[str, polars.DataFrame]`, one entry per sheet
- `sanitize_name(name)` - turns a sheet name into a safe table/file identifier (strips, replaces spaces)

The numbered example scripts each demonstrate one export target and import from
`spreadsheet_utils`:

1. **example1.py** - Load all sheets into a dict of Polars DataFrames
2. **example2.py** - Export each sheet to a SQLite table (one table per sheet)
3. **example3.py** - Export each sheet to a separate CSV file
4. **example4.py** - Export each sheet to a separate Parquet file
5. **example5.py** - Concatenate all sheets into one DataFrame (tagged by source sheet via diagonal concat)
6. **example6.py** - Export the whole workbook to a single JSON file

## Running Scripts

Each example takes the workbook path (and where relevant an output path) as
command-line arguments, defaulting to `example.xlsx`:

```bash
python example1.py file.xlsx
python example2.py file.xlsx output.db
python example3.py file.xlsx csv_output
python example4.py file.xlsx parquet_output
python example5.py file.xlsx
python example6.py file.xlsx output.json
```
