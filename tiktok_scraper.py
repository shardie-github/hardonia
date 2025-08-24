import json, re, time, random
from typing import List, Dict
from playwright.sync_api import sync_playwright

TAGS = ["tiktokmademebuyit", "tiktoktrending", "tiktokshop"]

UA_MOBILE = "Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"

def _extract_sigi_state(page_source: str) -> dict:
    # TikTok pages embed a JSON blob under SIGI_STATE
    m = re.search(r'<script id="SIGI_STATE".*?>(.*?)</script>', page_source, re.S)
    if not m:
        return {}
    raw = m.group(1)
    try:
        return json.loads(raw)
    except Exception:
        # Sometimes it has HTML escapes — try unescape
        raw = raw.replace("&quot;", '"').replace("&amp;", "&")
        return json.loads(raw)

def fetch_hashtag(tag: str, max_videos: int = 50) -> List[Dict]:
    url = f"https://www.tiktok.com/tag/{tag}?lang=en"
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent=UA_MOBILE,
            viewport={"width": 390, "height": 844},
            locale="en-US"
        )
        page = ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        # Let the page settle and load content
        time.sleep(3)
        html = page.content()
        state = _extract_sigi_state(html)
        # Fallback: attempt to trigger more content by scrolling
        if not state:
            for _ in range(5):
                page.mouse.wheel(0, 2000)
                time.sleep(1)
            html = page.content()
            state = _extract_sigi_state(html)
        browser.close()

    # Parse videos from state
    if not state:
        return results
    item_module = state.get("ItemModule", {})
    author_module = state.get("UserModule", {}).get("users", {})
    for vid, meta in item_module.items():
        desc = meta.get("desc", "")
        stats = meta.get("stats", {}) or {}
        author_id = meta.get("author", "")
        author_name = author_module.get(author_id, {}).get("uniqueId", author_id)
        # Build a record
        results.append({
            "video_id": vid,
            "desc": desc,
            "author": author_name,
            "plays": int(stats.get("playCount", 0) or 0),
            "likes": int(stats.get("diggCount", 0) or 0),
            "comments": int(stats.get("commentCount", 0) or 0),
            "shares": int(stats.get("shareCount", 0) or 0),
            "tag": tag
        })
        if len(results) >= max_videos:
            break
    # Sort by plays desc
    results.sort(key=lambda r: r["plays"], reverse=True)
    return results
