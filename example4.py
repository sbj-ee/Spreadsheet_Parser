"""Example 4: Export each sheet of an Excel workbook to a Parquet file.

Parquet is a compressed, columnar format that round-trips dtypes far
better than CSV and loads much faster for large datasets.

Usage:
    python example4.py [path/to/file.xlsx] [output_dir]
"""

import os
import sys

from spreadsheet_utils import load_sheets, sanitize_name, suppress_numpy_warnings

suppress_numpy_warnings()


def main(excel_file: str, out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    for sheet, df in load_sheets(excel_file).items():
        out_path = os.path.join(out_dir, f"{sanitize_name(sheet)}.parquet")
        df.write_parquet(out_path)
        print(f"Wrote {df.height} rows to {out_path}")


if __name__ == "__main__":
    excel_file = sys.argv[1] if len(sys.argv) > 1 else "example.xlsx"
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "parquet_output"
    main(excel_file, out_dir)
