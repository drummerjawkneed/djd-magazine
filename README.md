# Drummers & Dreamers Magazine

Monthly eMagazine for the global drum streaming community.

**Live:** https://magazine.drummerjawkneed.com
**Stream:** https://drummerjawkneed.com

## Structure

| Path | Content |
|---|---|
| `/june-2026/` | Issue 01 — June 2026 |
| `/july-2026/` | Issue 02 — July 2026 |
| `/august-2026/` | Issue 03 — August 2026 |
| `/september-2026/` | Issue 04 — September 2026 (current) |
| `/latest/` | Always the current issue (mirrors the newest issue folder) |
| `<month>-<year>/image-manifest.json` | That issue's real-photo sourcing record (see `STANDARDS.md`'s Image Policy) |
| `scripts/image_pipeline.py` | Reusable real-photo sourcing module, called once per image slot |
| `assets/djd-real-photos/` | Real DJD photos/footage, checked first for any "self" image slot |
| `banner.json` | Homepage embed data (auto-updated by n8n) |
| `STANDARDS.md` | Editorial standards and style guide |
| `CHANGELOG.md` | Issue history and corrections |
| `drafts/` | In-progress issues (not deployed) |

## Deploy

Cloudflare Pages auto-deploys on every push to `main`.
Custom domain: `magazine.drummerjawkneed.com`

## New Issue Workflow (as of Oct 2026)
Issues are now built from `<month-year>/content.json` by `scripts/build_issue.py` (photo-led template, sources + credits enforced by the build's validator). Images are sourced with real licensed photos (Wikimedia Commons CC, manufacturer press images, DJD's own footage) — never stock, never hotlinked. The n8n monthly workflow only drafts to branch `draft/next-issue`; nothing publishes without review.

### Older manual workflow

1. Run n8n `DJD Magazine Monthly Generation Pipeline` workflow
2. Rename output to `[month-year]/index.html`
3. Call `scripts/image_pipeline.py source` for every image slot; review the resulting
   `[month-year]/image-manifest.json` and resolve every `is_fallback: true` slot
4. Copy to `latest/index.html`
5. Update `banner.json` with new month's data
6. `git add . && git commit -m "Issue: [Month Year]" && git push`
7. Cloudflare auto-deploys (~60 seconds)
8. Kit broadcast goes out

## Editorial Standards

See `STANDARDS.md` for full editorial policy, image rules, copyright guidance, and per-issue checklist.
