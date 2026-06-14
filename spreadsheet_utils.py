"""Shared helpers for the Spreadsheet Parser examples.

This module consolidates the boilerplate that every example needs:
suppressing noisy numpy warnings and loading every sheet of an Excel
workbook into DataFrames.
"""

import logging
import os
import warnings

import pandas as pd
import polars as pl


def suppress_numpy_warnings() -> None:
    """Silence the spurious numpy/pandas warnings raised while reading Excel."""
    logging.getLogger("numpy").setLevel(logging.ERROR)
    os.environ["NUMPY_WARN_IF_NO_FALLBACK"] = "0"
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings(
        "ignore", message="Signature.*longdouble.*", module="numpy"
    )


def load_sheets_pandas(excel_file: str) -> dict[str, pd.DataFrame]:
    """Load every sheet of *excel_file* into a dict of pandas DataFrames."""
    xls = pd.ExcelFile(excel_file)
    return {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}


def load_sheets(excel_file: str) -> dict[str, pl.DataFrame]:
    """Load every sheet of *excel_file* into a dict of Polars DataFrames."""
    return {
        sheet: pl.from_pandas(df)
        for sheet, df in load_sheets_pandas(excel_file).items()
    }


def sanitize_name(name: str) -> str:
    """Turn a sheet name into a safe table/file identifier."""
    return name.strip().replace(" ", "_")
