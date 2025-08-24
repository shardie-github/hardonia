import re, json, time
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

def search_aliexpress_mobile(query: str, max_items: int = 3) -> List[Dict]:
    # Use mobile search (lighter HTML)
    url = "https://m.aliexpress.com/search.htm"
    params = {"keywords": query}
    r = requests.get(url, params=params, headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    scripts = soup.find_all("script")
    run_params = None
    for s in scripts:
        if s.string and "window.runParams" in s.string:
            run_params = s.string
            break
    items = []
    if run_params:
        # Extract JSON after "window.runParams = "
        m = re.search(r"window\.runParams\s*=\s*({.*});", run_params, re.S)
        if m:
            data = json.loads(m.group(1))
            prods = data.get("result", {}).get("products", []) or data.get("items", [])
            for p in prods[:max_items]:
                title = p.get("title") or p.get("productTitle") or ""
                price = p.get("actPrice", {}).get("value") or p.get("salePrice", {}).get("value") or p.get("price", "")
                orders = p.get("orders", 0) or p.get("ordersCount", 0)
                rating = p.get("avgRating", 0) or p.get("rating", 0)
                product_id = p.get("productId") or p.get("productIdStr") or ""
                link = f"https://www.aliexpress.com/item/{product_id}.html" if product_id else p.get("productDetailUrl","")
                items.append({
                    "title": title,
                    "price": float(str(price).replace('$','').replace(',','') or 0),
                    "orders": int(orders or 0),
                    "rating": float(rating or 0),
                    "link": link
                })
    return items
