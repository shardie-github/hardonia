# Hardonia Minimal — Click-by-click Setup

## 1) Google Service Account
1. console.cloud.google.com → IAM & Admin → **Service Accounts** → **Create**.
2. Service Account → **Keys** → **Add key** → **Create new key** → **JSON** (download).
3. Open your Google Sheet → **Share** → add the service account email as **Editor**.
4. Copy your **Sheet ID** (between `/d/` and `/edit` in the URL).

## 2) GitHub → Netlify
1. Push this repo to GitHub (use `scripts/push.ps1` if helpful).
2. Netlify → **New site from Git** → pick repo.
3. Site → **Settings → Environment variables**:
   - `SHEET_ID` = the ID from Step 1
   - `GOOGLE_CREDENTIALS` = full JSON from Step 1 (paste entire content)
   - (optional) `ALLOWED_ORIGIN` = https://hardonia.netlify.app

## 3) Sanity Check
- Visit `/.netlify/functions/health` on your site → expect `{ ok: true }`

## 4) Bookmarklet
1. Visit `/bookmarklet.html`
2. Enter your site origin → drag the button to your bookmarks bar.
3. On any TikTok video page → click the bookmark → a row appears in `AdSpy_UGC` tab of your Sheet.

## Troubleshooting
- **403**: Share the Sheet with the service-account email as **Editor**.
- **500**: Check env vars exist and JSON is complete.
- **No rows**: Ensure you are on a `tiktok.com` URL when clicking the bookmarklet.
