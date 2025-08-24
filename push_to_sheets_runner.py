import os, pandas as pd
from push_to_sheets import push_dataframe
from scraper import build_report
from creative_prompts import prompt_rows

TARGET_SHEET_PRODUCTS = "Scraped_Products"
TARGET_SHEET_PROMPTS = "Creative_Prompts"

if __name__ == "__main__":
    df, csv_path = build_report()
    push_dataframe(df, TARGET_SHEET_PRODUCTS)
    pr = prompt_rows(df)
    push_dataframe(pr, TARGET_SHEET_PROMPTS)
    print("✅ Pushed", len(df), "products and", len(pr), "prompts.")
