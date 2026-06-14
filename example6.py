"""Example 6: Export an Excel workbook to a single JSON file.

Produces one JSON object keyed by sheet name, each value being a list of
row records. Handy for feeding spreadsheet data into web APIs or NoSQL
stores.

Usage:
    python example6.py [path/to/file.xlsx] [output.json]
"""

import json
import sys

from spreadsheet_utils import load_sheets, suppress_numpy_warnings

suppress_numpy_warnings()


def main(excel_file: str, json_path: str) -> None:
    data = {sheet: df.to_dicts() for sheet, df in load_sheets(excel_file).items()}
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"Wrote {len(data)} sheets to {json_path}")


if __name__ == "__main__":
    excel_file = sys.argv[1] if len(sys.argv) > 1 else "example.xlsx"
    json_path = sys.argv[2] if len(sys.argv) > 2 else "output.json"
    main(excel_file, json_path)
