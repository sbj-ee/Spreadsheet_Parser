"""Shared pytest fixtures.

Placing this file at the repository root puts the root on ``sys.path`` so the
example modules and ``spreadsheet_utils`` import cleanly from the tests.
"""

import pandas as pd
import pytest


@pytest.fixture
def sample_xlsx(tmp_path):
    """Write a small two-sheet workbook and return its path."""
    path = tmp_path / "sample.xlsx"
    sales = pd.DataFrame(
        {
            "order_id": [1, 2, 3],
            "product": ["Widget", "Gadget", "Gizmo"],
            "revenue": [10.5, 20.0, 30.25],
        }
    )
    inventory = pd.DataFrame(
        {
            "product": ["Widget", "Gadget"],
            "in_stock": [100, 50],
        }
    )
    with pd.ExcelWriter(path) as writer:
        sales.to_excel(writer, sheet_name="Sales North", index=False)
        inventory.to_excel(writer, sheet_name="Inventory", index=False)
    return str(path)
