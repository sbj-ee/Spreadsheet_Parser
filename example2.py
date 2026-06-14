"""Example 2: Export each sheet of an Excel workbook to a SQLite table.

One table is created per sheet (spaces in sheet names become underscores).

Usage:
    python example2.py [path/to/file.xlsx] [output.db]
"""

import sys

from sqlalchemy import create_engine

from spreadsheet_utils import load_sheets_pandas, sanitize_name, suppress_numpy_warnings

suppress_numpy_warnings()


def main(excel_file: str, db_path: str) -> None:
    dfs = load_sheets_pandas(excel_file)
    engine = create_engine(f"sqlite:///{db_path}")
    for sheet, df in dfs.items():
        table_name = sanitize_name(sheet)
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        print(f"Wrote {len(df)} rows to table '{table_name}'")
    print(f"Done. Database written to {db_path}")


if __name__ == "__main__":
    excel_file = sys.argv[1] if len(sys.argv) > 1 else "example.xlsx"
    db_path = sys.argv[2] if len(sys.argv) > 2 else "output.db"
    main(excel_file, db_path)
