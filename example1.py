import polars as pl
import pandas as pd
import numpy as np
import warnings, os, logging
logging.getLogger("numpy").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")
os.environ["NUMPY_WARN_IF_NO_FALLBACK"] = "0"
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")
warnings.filterwarnings("ignore", message="Signature.*longdouble.*", module="numpy")
warnings.filterwarnings("ignore", category=UserWarning, module=np.__name__)
from pprint import pprint

pl.Config.set_tbl_rows(-1)
excel_file = "/home/usrsbj/EQUINIX.xlsx"
xls = pd.ExcelFile(excel_file)
dfs = {sheet: pl.from_pandas(pd.read_excel(xls, sheet_name=sheet)) for sheet in xls.sheet_names}

pprint(dfs)
