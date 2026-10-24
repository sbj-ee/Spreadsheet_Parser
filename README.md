# Spreadsheet Parser

Small, self-contained Python examples for reading every sheet of an Excel
workbook and exporting the data to Polars, SQLite, CSV, Parquet, or JSON.

## Features

- Load every sheet of a workbook into a dict of Polars (or pandas) DataFrames
- Export each sheet to its own SQLite table
- Export each sheet to its own CSV or Parquet file
- Concatenate all sheets into one DataFrame, tagged by source sheet
- Export the whole workbook to a single JSON file

## Requirements

- Python 3.9+ (developed and tested on 3.14)
- polars, pandas, numpy, sqlalchemy, openpyxl, pyarrow (see `requirements.txt`)

`openpyxl` is the engine pandas uses to read `.xlsx` files, and `pyarrow` is
needed both by `pl.from_pandas` and for Parquet export.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Sample workbook

`example.xlsx` is included so every script runs out of the box. It has three
sheets:

| Sheet | Rows | Columns |
| --- | --- | --- |
| `Sales` | 4 | `order_id`, `product`, `region`, `units`, `revenue` |
| `Inventory` | 3 | `product`, `in_stock`, `reorder_level`, `supplier` |
| `Employees` | 3 | `emp_id`, `name`, `department`, `start_date` |

## Examples

Every script takes the workbook path as its first argument (default
`example.xlsx`). Scripts that write output take the destination as a second
argument; relative output paths are resolved against the current directory.

| Script | What it does | Usage | Default output |
| --- | --- | --- | --- |
| `example1.py` | Load each sheet into a dict of Polars DataFrames and print it | `python example1.py [file.xlsx]` | stdout |
| `example2.py` | Write each sheet to a SQLite table | `python example2.py [file.xlsx] [output.db]` | `output.db` |
| `example3.py` | Write each sheet to a CSV file | `python example3.py [file.xlsx] [out_dir]` | `csv_output/` |
| `example4.py` | Write each sheet to a Parquet file | `python example4.py [file.xlsx] [out_dir]` | `parquet_output/` |
| `example5.py` | Concatenate all sheets into one DataFrame and print it | `python example5.py [file.xlsx]` | stdout |
| `example6.py` | Write the whole workbook to one JSON file | `python example6.py [file.xlsx] [output.json]` | `output.json` |

### Behaviour notes

- **Table and file names** come from sheet names via `sanitize_name()`, which
  strips surrounding whitespace and replaces spaces with underscores
  (`"Sales North"` → `Sales_North`). Other characters are left as-is.
- **example1** and **example5** print every row (`pl.Config.set_tbl_rows(-1)`),
  so large workbooks produce long output.
- **example2** writes with pandas `to_sql(..., if_exists="replace")`, so
  re-running it overwrites existing tables of the same name.
- **example3** and **example4** create the output directory if needed and
  overwrite existing files.
- **example5** adds a `source_sheet` column to each sheet and combines them
  with a `diagonal_relaxed` concat: columns are matched by name, columns
  missing from a sheet are filled with nulls, and compatible dtypes are
  widened. With the sample workbook this yields 10 rows × 13 columns.
- **example6** writes one JSON object keyed by sheet name, each value a list
  of row records. Values JSON can't represent natively (such as dates) are
  serialized with `str()`.

Example run against the sample workbook:

```console
$ python example2.py
Wrote 4 rows to table 'Sales'
Wrote 3 rows to table 'Inventory'
Wrote 3 rows to table 'Employees'
Done. Database written to output.db
```

Generated outputs (`*.db`, `*.json`, `csv_output/`, `parquet_output/`) are
listed in `.gitignore`.

## Shared helpers

Common logic lives in `spreadsheet_utils.py` so each example stays short:

| Function | Purpose |
| --- | --- |
| `suppress_numpy_warnings()` | Silence noisy numpy/pandas warnings raised while reading Excel |
| `load_sheets_pandas(path)` | Return `dict[str, pandas.DataFrame]`, one entry per sheet |
| `load_sheets(path)` | Return `dict[str, polars.DataFrame]`, one entry per sheet |
| `sanitize_name(name)` | Turn a sheet name into a table/file identifier |

```python
from spreadsheet_utils import load_sheets, load_sheets_pandas, suppress_numpy_warnings

suppress_numpy_warnings()

dfs = load_sheets("path/to/file.xlsx")          # dict[str, polars.DataFrame]
pdfs = load_sheets_pandas("path/to/file.xlsx")  # dict[str, pandas.DataFrame]
```

Each example also exposes a `main(...)` function, so it can be imported and
called directly, e.g. `example2.main("file.xlsx", "output.db")`.

## Testing

```bash
pip install -r requirements-dev.txt
pytest
```

The suite (`tests/test_examples.py`) covers the shared helpers and calls each
example's `main()`. It does not use `example.xlsx`: a fixture in `conftest.py`
generates a two-sheet workbook (`Sales North`, `Inventory`) in a temporary
directory, so the sheet name with a space exercises `sanitize_name()`.

## License

MIT — see [LICENSE](LICENSE).
