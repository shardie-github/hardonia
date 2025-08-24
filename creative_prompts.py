import datetime, pandas as pd

def prompt_rows(df: pd.DataFrame):
    rows = []
    for _, r in df.head(20).iterrows():
        product = r.get("ProductGuess","").title()[:80]
        if not product: continue
        # Hooks
        hook1 = f"POV: You just discovered the {product} trend everyone is using"
        hook2 = f"3 seconds to fall in love with {product}"
        # CapCut script
        capcut = (
            "[HOOK 0:00-0:02]\\n"
            f"On-screen: \"{hook1}\"\\n"
            "[DEMO 0:02-0:07]\\n"
            f"Show the {product} solving a pain fast (close-up, hands-in-frame)\\n"
            "[SOCIAL PROOF 0:07-0:10]\\n"
            "Overlay recent comments/ratings\\n"
            "[CTA 0:10-0:12]\\n"
            "Tap to get yours — limited stock"
        )
        veo2 = f"Ultra-cinematic b-roll of {product} in lifestyle context, 4K, shallow depth of field, soft natural light, dynamic camera moves, 0.7x speed, 12s."
        imagen = f"Studio-grade product shot of {product} on seamless backdrop, soft shadows, high contrast, macro details, 8k, photorealistic."
        rows.append({
            "Product": product,
            "CapCut_Script": capcut,
            "Veo2_Prompt": veo2,
            "Imagen_Prompt": imagen
        })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv("hardonia_daily.csv")
    out = prompt_rows(df)
    out.to_csv("creative_prompts.csv", index=False)
    print("Wrote creative_prompts.csv", len(out))
