import polars as pl
import pandas as pd

excel_file = "your_workbook.xlsx"
xls = pd.ExcelFile(excel_file)
dfs = {sheet: pl.from_pandas(pd.read_excel(xls, sheet_name=sheet)) for sheet in xls.sheet_names}
