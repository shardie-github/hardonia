from typing import Dict
from pytrends.request import TrendReq
import pandas as pd

def trend_momentum(keyword: str, tz=360) -> Dict:
    """Returns momentum classification based on last 30 days slope."""
    try:
        pytrends = TrendReq(hl='en-US', tz=tz)
        pytrends.build_payload([keyword], timeframe='now 30-d', geo='US')
        df = pytrends.interest_over_time()
        if df.empty:
            return {"keyword": keyword, "score": 0, "momentum": "unknown"}
        s = df[keyword].astype(float)
        # Simple slope: last value minus mean of first week
        early = s.head(7).mean()
        late = s.tail(3).mean()
        delta = late - early
        momentum = "emerging" if delta >= 10 else ("declining" if delta <= -10 else "trending")
        return {"keyword": keyword, "score": float(late), "momentum": momentum}
    except Exception:
        return {"keyword": keyword, "score": 0, "momentum": "unknown"}
