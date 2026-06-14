# Spreadsheet Parser

Python utilities for parsing multi-sheet Excel workbooks and loading them
into a variety of data formats.

## Features

- Load multi-sheet Excel workbooks into Polars DataFrames
- Export Excel data to SQLite databases (one table per sheet)
- Export each sheet to CSV or Parquet files
- Concatenate all sheets into a single DataFrame
- Export an entire workbook to JSON

## Requirements

- Python 3.8+
- polars
- pandas
- numpy
- sqlalchemy
- openpyxl
- pyarrow

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Examples

Every example reads its workbook path from the command line (falling back to
`example.xlsx`), so you can run them against your own file:

| Script | Description | Usage |
| --- | --- | --- |
| `example1.py` | Load each sheet into a dict of Polars DataFrames | `python example1.py file.xlsx` |
| `example2.py` | Export each sheet to a SQLite table | `python example2.py file.xlsx output.db` |
| `example3.py` | Export each sheet to a separate CSV file | `python example3.py file.xlsx csv_output` |
| `example4.py` | Export each sheet to a separate Parquet file | `python example4.py file.xlsx parquet_output` |
| `example5.py` | Concatenate all sheets into one DataFrame (tagged by source sheet) | `python example5.py file.xlsx` |
| `example6.py` | Export the whole workbook to a single JSON file | `python example6.py file.xlsx output.json` |

## Testing

Install the dev dependencies and run the suite, which exercises the shared
helpers and every example against a generated sample workbook:

```bash
pip install -r requirements-dev.txt
pytest
```

## Shared helpers

Common logic lives in `spreadsheet_utils.py` so the examples stay small:

```python
from spreadsheet_utils import load_sheets, load_sheets_pandas, suppress_numpy_warnings

suppress_numpy_warnings()

# dict[str, polars.DataFrame]
dfs = load_sheets("path/to/your/file.xlsx")

# dict[str, pandas.DataFrame]
pdfs = load_sheets_pandas("path/to/your/file.xlsx")
```
