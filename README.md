# Drummers & Dreamers Magazine

Monthly eMagazine for the global drum streaming community.

**Live:** https://magazine.drummerjawkneed.com
**Stream:** https://drummerjawkneed.com

## Structure

| Path | Content |
|---|---|
| `/june-2026/` | Issue 01 — June 2026 |
| `/latest/` | Always the current issue |
| `banner.json` | Homepage embed data (auto-updated by n8n) |
| `STANDARDS.md` | Editorial standards and style guide |
| `CHANGELOG.md` | Issue history and corrections |
| `drafts/` | In-progress issues (not deployed) |

## Deploy

Cloudflare Pages auto-deploys on every push to `main`.
Custom domain: `magazine.drummerjawkneed.com`

## New Issue Workflow

1. Run n8n `DJD Magazine Monthly Generation Pipeline` workflow
2. Rename output to `[month-year]/index.html`
3. Copy to `latest/index.html`
4. Update `banner.json` with new month's data
5. `git add . && git commit -m "Issue: [Month Year]" && git push`
6. Cloudflare auto-deploys (~60 seconds)
7. Kit broadcast goes out

## Editorial Standards

See `STANDARDS.md` for full editorial policy, image rules, copyright guidance, and per-issue checklist.
