"""Example 1: Load every sheet of an Excel workbook into Polars DataFrames.

Usage:
    python example1.py [path/to/file.xlsx]
"""

import sys
from pprint import pprint

import polars as pl

from spreadsheet_utils import load_sheets, suppress_numpy_warnings

suppress_numpy_warnings()
pl.Config.set_tbl_rows(-1)


def main(excel_file: str) -> None:
    dfs = load_sheets(excel_file)
    pprint(dfs)


if __name__ == "__main__":
    excel_file = sys.argv[1] if len(sys.argv) > 1 else "example.xlsx"
    main(excel_file)
