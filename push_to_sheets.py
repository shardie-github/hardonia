import os, json, datetime, pandas as pd
from google.oauth2.service_account import Credentials
import gspread

SHEET_ID = os.getenv("SHEET_ID")
CREDS_JSON = os.getenv("GOOGLE_CREDENTIALS")

def ensure_worksheet(client, title: str, header: list):
    sh = client.open_by_key(SHEET_ID)
    try:
        ws = sh.worksheet(title)
    except Exception:
        ws = sh.add_worksheet(title=title, rows=1000, cols=max(10, len(header)))
        ws.append_row(header)
        return ws
    # Ensure header exists
    vals = ws.get_all_values()
    if not vals:
        ws.append_row(header)
    return ws

def push_dataframe(df: pd.DataFrame, title: str):
    creds = Credentials.from_service_account_info(json.loads(CREDS_JSON), scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ])
    client = gspread.authorize(creds)
    header = list(df.columns)
    ws = ensure_worksheet(client, title, header)
    # Append rows
    rows = df.astype(object).where(pd.notna(df), "").values.tolist()
    if rows:
        ws.append_rows(rows, value_input_option="USER_ENTERED")
    return True
