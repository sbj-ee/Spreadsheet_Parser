"""Example 5: Concatenate all sheets into one Polars DataFrame.

Each sheet's rows are tagged with a "source_sheet" column so the origin
is preserved after the merge. Sheets are aligned by column name, so
missing columns are filled with nulls (diagonal concat).

Usage:
    python example5.py [path/to/file.xlsx]
"""

import sys

import polars as pl

from spreadsheet_utils import load_sheets, suppress_numpy_warnings

suppress_numpy_warnings()
pl.Config.set_tbl_rows(-1)


def main(excel_file: str) -> None:
    frames = [
        df.with_columns(pl.lit(sheet).alias("source_sheet"))
        for sheet, df in load_sheets(excel_file).items()
    ]
    combined = pl.concat(frames, how="diagonal_relaxed")
    print(combined)
    print(f"\nCombined {len(frames)} sheets into {combined.height} rows.")


if __name__ == "__main__":
    excel_file = sys.argv[1] if len(sys.argv) > 1 else "example.xlsx"
    main(excel_file)
