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

## Architecture

Two example patterns are provided:

1. **example1.py** - Loads all sheets from an Excel file into a dictionary of Polars DataFrames
2. **example2.py** - Loads all sheets from an Excel file into SQLite tables (one table per sheet, spaces replaced with underscores in table names)

Both scripts share a common pattern for suppressing numpy warnings that can be reused.

## Running Scripts

```bash
python example1.py  # Load Excel to Polars DataFrames
python example2.py  # Load Excel to SQLite database
```

Note: Scripts expect an Excel file path to be configured in the `excel_file` variable.
