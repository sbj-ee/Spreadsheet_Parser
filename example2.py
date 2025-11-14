import pandas as pd
import numpy as np
import warnings, os, logging
from sqlalchemy import create_engine

logging.getLogger("numpy").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")
os.environ["NUMPY_WARN_IF_NO_FALLBACK"] = "0"
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")
warnings.filterwarnings("ignore", message="Signature.*longdouble.*", module="numpy")
warnings.filterwarnings("ignore", category=UserWarning, module=np.__name__)

excel_file = "/home/usrsbj/EQUINIX.xlsx"
xls = pd.ExcelFile(excel_file)
dfs = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}

engine = create_engine('sqlite:///equinix.db')
for sheet, df in dfs.items():
    table_name = sheet.replace(" ", "_")
    df.to_sql(table_name, engine, if_exists='replace', index=False)
