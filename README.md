# Hardonia Super Super Pack

**Lean, automated, self-improving** repo scaffold. Combines:
- AutoVendor (push + PR modes)
- Release asset verification
- Pack Guardian (policy + secrets + malware)
- Semantic Version Advisor
- Release Hygiene

## Quick start
1) Commit this repo to GitHub.
2) Add secrets (as needed): `SLACK_WEBHOOK` for Slack notifications.
3) Publish a release (e.g., `v1.0.0`) — AutoVendor vendors `/packs/*` automatically.

## Local vendoring
```bash
export GITHUB_OWNER=your-org
export GITHUB_REPO=your-repo
bash scripts/vendor-packs.sh v1.0.0
```

## Verify assets
```bash
export GITHUB_OWNER=your-org
export GITHUB_REPO=your-repo
bash scripts/verify-assets.sh v1.0.0
```

## Smart add-ons
- Pack Guardian: `.github/workflows/pack-guardian.yml`
- Semantic Version Advisor: `.github/workflows/semantic-version-advisor.yml`
- Release Hygiene: `.github/workflows/release-hygiene.yml`

## Upload and unpack — 3 ways
1) **Release asset**: attach `Hardonia_Super_Super_Pack.zip` to a Release → it unpacks into the repo automatically.
2) **Repo upload**: upload any `*.zip` to the `.uploads/` folder in the web UI → it unpacks on push.
3) **Manual URL**: run the “Unpack Super Pack (Manual URL)” workflow and paste a direct ZIP URL.

## Badges without hardcoding owner/repo
The `Stamp Badges` workflow replaces `OWNER/REPO` in README with the actual `owner/repo` (`$GITHUB_REPOSITORY`) and commits it.
