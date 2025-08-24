import re
from typing import List

STOP = set("""the a an and or of for with on in to from is are be this that your you my we it they their our best top viral tiktok buy shop made me""".split())

def extract_candidates(text: str, max_len: int = 40) -> List[str]:
    text = (text or "").lower()
    text = re.sub(r"#", " ", text)
    text = re.sub(r"[^a-z0-9\s\-]", " ", text)
    tokens = [t for t in text.split() if t and t not in STOP]
    # Build simple bigrams/trigrams as product candidates
    cands = set()
    for i in range(len(tokens)):
        for n in (1,2,3):
            if i+n <= len(tokens):
                phrase = " ".join(tokens[i:i+n])
                if 3 <= len(phrase) <= max_len:
                    cands.add(phrase.strip())
    # Return top few by length heuristic (longer phrases often better names)
    out = sorted(cands, key=lambda x: (-len(x), x))[:8]
    return out
