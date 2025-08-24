# Hardonia Intel Scraper — PRO (Free stack)

**Real** daily data for Hardonia from *free* sources:
- TikTok hashtags: `#tiktokmademebuyit`, `#tiktoktrending`, `#tiktokshop` (Playwright headless)
- AliExpress cross-reference: top listings for margin calc (mobile site)
- Google Trends: momentum classification (emerging / trending / declining)

Twice daily via **GitHub Actions** → pushes into your existing **Hardonia Command Center** Google Sheet.

## Secrets to set (GitHub → Settings → Secrets → Actions)
- `GOOGLE_CREDENTIALS` — full JSON of the Google Service Account
- `SHEET_ID` — `162Z8RzdC3t9zYo83c3MZ2zxg8mY2btuixmx66UzMiJY` (your sheet)
- *(optional)* `DRIVE_FOLDER_ID` — if you also want CSV dropped into Drive via Apps Script endpoint

## Quick start
1. Create a private repo and upload this folder.
2. Set the secrets above.
3. The workflow runs at 07:40 & 16:40 UTC by default. Edit cron in `.github/workflows/daily.yml` if needed.
