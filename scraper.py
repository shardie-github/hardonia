import os, datetime, pandas as pd
from tiktok_scraper import fetch_hashtag, TAGS
from product_extract import extract_candidates
from aliexpress import search_aliexpress_mobile
from trends import trend_momentum

def build_report():
    # 1) Scrape TikTok hashtags
    tiktok_rows = []
    for tag in TAGS:
        vids = fetch_hashtag(tag, max_videos=40)
        for v in vids:
            candidates = extract_candidates(v.get("desc",""))
            # Take first candidate as product guess
            prod_guess = candidates[0] if candidates else ""
            tiktok_rows.append({
                "Date": datetime.date.today().isoformat(),
                "Tag": tag,
                "VideoID": v["video_id"],
                "Author": v["author"],
                "Desc": v["desc"],
                "Plays": v["plays"],
                "Likes": v["likes"],
                "Comments": v["comments"],
                "Shares": v["shares"],
                "ProductGuess": prod_guess
            })
    df_tt = pd.DataFrame(tiktok_rows).drop_duplicates(subset=["VideoID"])

    # 2) Cross-reference on AliExpress (top-1)
    ali_rows = []
    for prod in df_tt["ProductGuess"].dropna().unique().tolist()[:40]:
        if not prod: continue
        hits = search_aliexpress_mobile(prod, max_items=1)
        if hits:
            h = hits[0]
            ali_rows.append({
                "ProductGuess": prod,
                "AE_Title": h["title"],
                "AE_Price": h["price"],
                "AE_Orders": h["orders"],
                "AE_Rating": h["rating"],
                "AE_Link": h["link"]
            })
    df_ali = pd.DataFrame(ali_rows)

    # 3) Google Trends momentum
    mom_rows = []
    for prod in df_tt["ProductGuess"].dropna().unique().tolist()[:40]:
        if not prod: continue
        m = trend_momentum(prod)
        mom_rows.append({
            "ProductGuess": prod,
            "TrendScore": m["score"],
            "Momentum": m["momentum"]
        })
    df_mom = pd.DataFrame(mom_rows)

    # 4) Join & compute simple margin estimate (assume retail 2.5x cost baseline)
    df = df_tt.merge(df_ali, on="ProductGuess", how="left").merge(df_mom, on="ProductGuess", how="left")
    df["Est_Retail"] = (df["AE_Price"].fillna(0) * 2.5).round(2)
    df["Est_Margin_$"] = (df["Est_Retail"] - df["AE_Price"].fillna(0)).round(2)
    df["Est_Margin_%"] = ((df["Est_Margin_$"] / df["Est_Retail"].replace(0, pd.NA)) * 100).round(1)

    # 5) Classify stage
    def stage(row):
        if (row.get("Momentum") == "emerging") and (row.get("Plays",0) > 500000):
            return "Emerging"
        if (row.get("Momentum") == "trending") and (row.get("Plays",0) > 1000000):
            return "Trending"
        if row.get("Momentum") == "declining":
            return "Declining"
        return "Watchlist"
    df["Stage"] = df.apply(stage, axis=1)

    # Sort by Plays desc then Margin
    df = df.sort_values(["Stage","Plays","Est_Margin_$"], ascending=[True, False, False])

    # Save CSV
    out_csv = "hardonia_daily.csv"
    df.to_csv(out_csv, index=False)
    return df, out_csv

if __name__ == "__main__":
    df, path = build_report()
    print("Wrote", path, "rows:", len(df))
