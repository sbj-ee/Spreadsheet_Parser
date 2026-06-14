"""Tests that exercise the shared helpers and every example script."""

import json
import sqlite3

import polars as pl

import example1
import example2
import example3
import example4
import example5
import example6
import spreadsheet_utils as su


# --- spreadsheet_utils ------------------------------------------------------

def test_load_sheets_returns_polars(sample_xlsx):
    dfs = su.load_sheets(sample_xlsx)
    assert set(dfs) == {"Sales North", "Inventory"}
    assert all(isinstance(df, pl.DataFrame) for df in dfs.values())
    assert dfs["Sales North"].height == 3


def test_load_sheets_pandas(sample_xlsx):
    dfs = su.load_sheets_pandas(sample_xlsx)
    assert set(dfs) == {"Sales North", "Inventory"}
    assert list(dfs["Inventory"].columns) == ["product", "in_stock"]


def test_sanitize_name():
    assert su.sanitize_name("Sales North") == "Sales_North"
    assert su.sanitize_name("  Trailing  ") == "Trailing"


# --- example scripts --------------------------------------------------------

def test_example1_runs(sample_xlsx, capsys):
    example1.main(sample_xlsx)
    assert "shape" in capsys.readouterr().out


def test_example2_sqlite(sample_xlsx, tmp_path):
    db = tmp_path / "out.db"
    example2.main(sample_xlsx, str(db))
    con = sqlite3.connect(db)
    tables = {row[0] for row in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )}
    con.close()
    assert {"Sales_North", "Inventory"} <= tables


def test_example3_csv(sample_xlsx, tmp_path):
    out = tmp_path / "csv"
    example3.main(sample_xlsx, str(out))
    assert (out / "Sales_North.csv").exists()
    assert (out / "Inventory.csv").exists()


def test_example4_parquet(sample_xlsx, tmp_path):
    out = tmp_path / "pq"
    example4.main(sample_xlsx, str(out))
    df = pl.read_parquet(out / "Sales_North.parquet")
    assert df.height == 3


def test_example5_combined(sample_xlsx, capsys):
    example5.main(sample_xlsx)
    out = capsys.readouterr().out
    assert "source_sheet" in out
    assert "Combined 2 sheets into 5 rows." in out


def test_example6_json(sample_xlsx, tmp_path):
    out = tmp_path / "out.json"
    example6.main(sample_xlsx, str(out))
    data = json.loads(out.read_text())
    assert set(data) == {"Sales North", "Inventory"}
    assert len(data["Sales North"]) == 3
