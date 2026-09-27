# Drummers & Dreamers Magazine — Changelog

## Issue 04 — September 2026
**Published (draft, pending review):** `latest/` mirrors `september-2026/index.html`, `banner.json`
dated 2026-09-01. Cover/feature: Rush's $785,000 gift closes out the $1M Neil Peart memorial
fund at Lakeside Park; the Fifty Something tour adds four more dates through November.

**Full visual and content redesign, per Johnny's direct feedback ("really a 3/10... state of the
art... much better curated info").** Real, verified content this issue (Rush tour dates, the
Peart memorial funding, Ilan Rubin's no-click Foo Fighters sessions, real September gear
releases) replaced anything that would've been invented placeholder text — every factual claim
traces to a live web search run this session, not training-data recall (2026 news is after this
model's knowledge cutoff). Visual system keeps the existing Playfair Display/DM Sans/Space Mono
type stack (already good) but replaces uniform card grids with asymmetric layouts, adds a
colored left-bar per section for stronger department identity, and adds a horizontal feed-strip
component for quick-scan gear news.

**Two new recurring departments, formalized in `STANDARDS.md`:**
- **Drummer Spotlight (Historical)** — Drummerworld-style biographical depth on a legendary
  drummer, timed to real news (this issue: Neil Peart, tied directly to the memorial story).
- **Drummer Pick of the Month** — a Pitchfork-style curated single-work pick with a real
  rationale, not a roundup entry (this issue: Ilan Rubin's Foo Fighters sessions).

**Real-photo sourcing pipeline built as a reusable capability, not a one-off fix**, per Johnny's
explicit follow-up requirement (every image must be a precisely-matching real photo, sourced
automatically every month, never generic stock by default): `scripts/image_pipeline.py`
implements the full per-subject-type sourcing policy (artist EPK, streamer public profile, gear
manufacturer product photo, DJD's own local real assets only) plus WebP conversion, real alt
text, and focal-point-aware cropping, callable once per image slot by the monthly n8n pipeline.
`STANDARDS.md`'s Image Policy section now documents this as the actual, binding policy. See this
issue's `image-manifest.json` and the PR description for exactly how each of this issue's 11
image slots was sourced — 1 came back a confirmed real manufacturer source (Spaun Drums), the
other 10 are honestly flagged `is_fallback`/`unverified` because this session's own sandbox
blocks direct fetches to twitch.tv, youtube.com, and commons.wikimedia.org (confirmed live, not
assumed) — every one of those slots uses this site's existing branded-SVG-illustration fallback
per `STANDARDS.md`'s own pre-existing "honesty over stock" rule, never a swapped-in stock photo.

## Issue 03 — August 2026
**Published:** confirmed live — `latest/` mirrors `august-2026/index.html` exactly, `banner.json`
dated 2026-08-01. Cover/feature per `banner.json`: "Ringo Turns 86, Rush Rolls On, Drummers Keep
Building" (Ringo's 86th at the Peace & Love Statue, the Fifty Something tour, drum streamers
building real catalogs).
**Doc-drift note (found+corrected 2026-09-24):** this changelog and README.md's structure table
had never been updated past Issue 02's "in progress" entry below — Issues 02 and 03 were both
already published and live with no changelog/README entry recording it. Corrected here from repo
evidence (file diffs, git log dates, `banner.json`), not from the original editorial brief/QA
process — a full "Corrections Applied"/"What Worked" retrospective like Issue 01's below wasn't
reconstructed, since that needs the same real fact-checking Issue 01 got, not a guess from outside
context. Whoever ran Issue 02/03 to publish should backfill those sections properly if useful.

## Issue 02 — July 2026
**Published:** confirmed live at `july-2026/index.html` (superseded by Issue 03 as `latest/`).
**Corrected 2026-09-24**: this entry previously said "In Progress"/"not yet published" and pointed
at `drafts/issue-02-july-2026/BRIEF.md`, which doesn't exist anywhere in this repo (checked) — the
issue was actually finished and published, just never reflected here. Real content per the planned
brief (Roland TD-50 setup guide, Rush Fort Worth recap, Linear Drumming lesson) — not independently
re-verified against the final published HTML this pass.
**Also found+fixed same pass**: a stray, wrongly-dated `july-2025/index.html` (title literally read
"July 2025," a year before this magazine's June 2026 launch) was sitting in the repo root,
unlinked from README/CHANGELOG/`latest/` — since Cloudflare Pages auto-deploys every folder on
push to `main`, this was live and publicly reachable at `magazine.drummerjawkneed.com/july-2025/`.
Confirmed via diff it's an earlier, superseded draft of this same issue (different CSS/font choices
than the real `july-2026/index.html`), not distinct content — deleted.
**Also found+fixed**: `banner.json`'s homepage-embed `link` pointed at
`https://mag.drummersanddreamers.com/august-2026` — confirmed via DNS lookup this domain does not
resolve at all (`ENOTFOUND`), while `magazine.drummerjawkneed.com` (this repo's actual documented
domain throughout README/CHANGELOG) is real. Fixed the link here; **the underlying n8n workflow
that auto-generates `banner.json` monthly still needs the same fix** (not accessible from this
session — no live infra access) or this will regenerate wrong again next month.

## Issue 01 — June 2026
**Published:** June 13, 2026
**URL:** https://magazine.drummerjawkneed.com/june-2026

### Corrections Applied
- Added Loren Gold (keyboardist) to Rush Fifty Something lineup — initially omitted
- Fixed Art Cruz photo credit: Travis Shinn for Modern Drummer
- Added Anika Nilles album count correction (4 albums, not 2)
- Confirmed tour scope: 88 shows across 24 cities (not initial 12-date announcement)

### What Worked
- Real Twitch og:image URLs for streamer profiles
- Full-bleed cover photo with SVG logo overlay
- JBL BandBox Trio official product CDN image
- Ghost Notes lesson section — keep and evolve
- YouTube drum cam embed for Anika Nilles opening night
