# Spreadsheet Parser

Python utilities for parsing Excel spreadsheets and loading them into different data formats.

## Features

- Load multi-sheet Excel workbooks into Polars DataFrames
- Export Excel data to SQLite databases (one table per sheet)

## Requirements

- Python 3.8+
- polars
- pandas
- numpy
- sqlalchemy
- openpyxl

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Load Excel to Polars DataFrames

```python
import polars as pl
import pandas as pd

excel_file = "path/to/your/file.xlsx"
xls = pd.ExcelFile(excel_file)
dfs = {sheet: pl.from_pandas(pd.read_excel(xls, sheet_name=sheet)) for sheet in xls.sheet_names}
```

### Load Excel to SQLite Database

```python
import pandas as pd
from sqlalchemy import create_engine

excel_file = "path/to/your/file.xlsx"
xls = pd.ExcelFile(excel_file)
dfs = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}

engine = create_engine('sqlite:///output.db')
for sheet, df in dfs.items():
    table_name = sheet.replace(" ", "_")
    df.to_sql(table_name, engine, if_exists='replace', index=False)
```

## Examples

- `example1.py` - Demonstrates loading Excel sheets into Polars DataFrames
- `example2.py` - Demonstrates exporting Excel sheets to SQLite tables
