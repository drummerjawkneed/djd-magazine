# Drummers & Dreamers Magazine — Editorial Standards
**Living Document · Version 1.0 · Updated June 2026**
Maintained in: `github.com/drummerjawkneed/djd-magazine/STANDARDS.md`

---

## 🎯 Mission

A monthly eMagazine for the global drum streaming community. Covers: live drum streamers, drum news, gear, culture, technique, and the intersection of drumming with music, streaming, and life. Primary differentiator from Modern Drummer: **streaming community coverage + DJD editorial voice + digital-native format**.

---

## ✅ Factual Accuracy Rules

### Before Every Issue Ships

Run this checklist on every fact:

| Check | Method |
|---|---|
| Drummer ages | Cross-reference birth year with current month/year |
| Album counts | Check artist's official site or Wikipedia |
| Tour dates and scope | Verify against official artist site |
| Twitch/YouTube follower counts | Check twitchtracker.com or streamscharts.com within 7 days of publish |
| Gear prices | Verify on manufacturer's official site |
| Product availability dates | Check press releases or manufacturer news |
| Quote attribution | Must link to original source; never paraphrase as direct quote |

### Known Fact Errors to Avoid (Learned from Issue 01)

- ❌ "Fifty Something is Rush's 50th anniversary tour" → ✅ It's called Fifty Something, celebrating roughly 50 years, not a specific anniversary
- ❌ Anika Nilles age as of announcement date → ✅ Always use current age at time of publication (born May 29, 1983)
- ❌ Saying Rush toured "in 2011" or "for the last time in 2013" → ✅ R40 tour ended August 1, 2015
- ❌ "two full-length albums" for Anika Nilles → ✅ Four: Pikalar (2017), For a Colorful Soul (2020), Opuntia (2022), False Truth (2025)
- ❌ Omitting keyboardist Loren Gold from Rush lineup → ✅ Always include: Geddy Lee, Alex Lifeson, Anika Nilles, Loren Gold

---

## ✅ Pre-Publish Fact-Check Checklist

Run this on every issue **before** it ships, not after. Every item below traces back to an actual correction made in Issue 01 — treat it as the minimum bar, not a suggestion.

- [ ] **Full lineup check** — for any band/act covered, list every current member by name and cross-reference against the official site. Don't drop members (Loren Gold was initially omitted from the Rush lineup).
- [ ] **Tour/album naming** — verify the *exact* official name of a tour or album. Don't infer or paraphrase a name (Rush's "Fifty Something" was wrongly called a "50th anniversary tour").
- [ ] **Historical dates** — for any "last time X happened" or "ended in" claim, verify the precise end date against a primary source (R40 tour ended August 1, 2015 — not 2011, not 2013).
- [ ] **Ages** — calculate from birth year against the *current* publication date, not the date a fact was researched or an event was announced.
- [ ] **Discography counts** — list every album by title and year from the artist's official site or label page before stating a count (Anika Nilles: 4 albums — *Pikalar* (2017), *For a Colorful Soul* (2020), *Opuntia* (2022), *False Truth* (2025) — not 2).
- [ ] **Photo credit** — every photo has a named photographer + publication + year, or it doesn't run (Art Cruz photo required explicit credit: Travis Shinn for Modern Drummer).
- [ ] **Final read-through** — one pass reading only for factual claims (names, numbers, dates, titles), separate from the voice/style pass.

---

## 📷 Image Policy

**Updated September 2026 — every image in every issue must be a precisely-matching real photo
of the actual subject. Generic stock is never a default choice, only a documented last resort.**
This is implemented as a reusable pipeline, `scripts/image_pipeline.py`, that the monthly
generation workflow calls once per image slot — see that file's own docstring for the full
design. The rules below are that pipeline's actual policy, not just guidance for a human editor.

### Sourcing rules, by subject type

| Subject type | Real source | Notes |
|---|---|---|
| **Touring artist/band** | Official EPK / press-kit photo — search `"<name> EPK"` and `"<name> press kit photos"`, prefer a hit on the artist's or label's own domain | EPKs are built by artists/labels specifically for this kind of use and expect a photo credit in return — that credit is mandatory, not optional |
| **Streamer (Twitch/Kick/YouTube)** | The streamer's own public profile photo or channel banner | Publicly displayed by the platform for exactly this identification/promotional purpose — always link the channel as attribution |
| **Gear/product** | The manufacturer's own official product photography, from the manufacturer's own product page | Never a third-party retailer's photo if the manufacturer's own page has one |
| **DJD/DrummerJawkneeD himself** | His own real footage/photos ONLY — check `assets/djd-real-photos/` (and the `obsidian-vault` repo, if checked out alongside this one) first | **Never** falls through to an external search for his own content — if nothing real is found locally, that's a genuine "no photo available" result, not a reason to substitute a stand-in |

### Last-resort fallback — documented, never a default

Wikimedia Commons (public-domain/historical subjects) or a stock-photo API with clear visible
attribution, used **only** when a real, precisely-matching photo genuinely cannot be found after
trying the table above. Every fallback use is written into the issue's `image-manifest.json`
with `is_fallback: true` — visible to whoever reviews the issue before it publishes, never
silently normalized into looking like a real sourced photo. Same principle covers a source that's
blocked or unreachable in a given run (e.g. a sandboxed environment that can't reach a given
platform) — that's recorded as `none-available`/`unverified-candidate` in the manifest, not
guessed at.

### Prohibited

- ❌ Hotlinking copyrighted press photos without explicit permission (e.g., Getty, Travis Shinn for MD)
- ❌ Stock photos representing real named people or specific real events
- ❌ Images that misrepresent what is being described (e.g., generic "singer" photo for "drummer" article)
- ❌ AI-generated photos of real named people
- ❌ Treating a fallback/unverified image as if it were a confirmed real sourced photo — the
  manifest's `is_fallback`/`approved` fields must stay honest, not optimistic

### Attribution Format
```
Photo: [Photographer Name] for [Publication] · [Year]
```
Always link to original source article. For a manifest-sourced image, `credit` and
`source_kind` in `image-manifest.json` are the attribution record; the rendered page's visible
caption should match it.

### Human approval before publish

Every issue's `image-manifest.json` starts with `"approved": false` at the issue level, and each
individual slot defaults to approved only if it's a real, non-fallback source (`is_fallback:
false`). Any fallback slot needs a human to review it and flip it to `approved: true` — in
practice, that review happens as part of reviewing this issue's draft PR; merging the PR is the
approval gate, not a separate tool. Run `python scripts/image_pipeline.py approve --issue
<slug>` (optionally `--slot <id>` for one slot at a time) once reviewed.

### Post-processing (also handled by the pipeline)

Every sourced image is converted to compressed WebP at a sane max width, gets real (non-generic)
alt text generated from its actual credit/subject data, and is cropped toward a focal point so a
subject's face never gets cut off by an aspect-ratio change — see `process_image()` and
`generate_alt_text()` in `scripts/image_pipeline.py`.

### If No Real Photo Available
Use **branded SVG illustration** (our drum icon system) rather than a misleading stock photo. Honesty > aesthetics. This is also the fallback the pipeline uses for a subject-type-appropriate source it couldn't reach or verify this run.

---

## ©️ Copyright Rules

### Original Content
All editorial text must be written originally. No reproduction of other publications' text.

### Quotes
- Direct quotes: under 15 words, attributed to person + source + date
- Must link to original interview/source
- Never attribute a quote we can't verify

### Song Lyrics / Sheet Music
Never reproduce. Reference by title only.

### Images
See Image Policy above.

### Fair Use Principle
Editorial news commentary, criticism, and education = generally protected. Product images used to illustrate coverage of a product = generally acceptable with attribution. Always link back to source.

---

## 🖊️ Voice & Tone

### The DJD Magazine Voice
- **Direct.** No passive voice. No "it is worth noting."
- **Human.** We play drums. We stream. We have opinions.
- **Informed.** We cite sources. We name dates. We don't vague-post.
- **Not neutral.** We editorialize in culture sections. We take positions.
- **Not promotional.** Even DJD content gets honest treatment.

### Banned Phrases
- "delve into"
- "it's worth noting"
- "in conclusion"
- "as we all know"
- "needless to say"
- "exciting new"
- Any phrase that sounds like it was written by a press release

### Tone by Section
| Section | Tone |
|---|---|
| Editor's Note | Personal, direct, punchy |
| Cover Story | Long-form journalism, earned authority |
| Drummer Spotlight (Historical) | Reverent but not hagiographic — real biography, real context |
| Gear & Tech | Factual, useful, with opinion |
| Drummer Pick of the Month | Opinionated, specific, argues its case in a paragraph or two |
| Drum Lesson | Teaching voice, clear steps, encouraging |
| Streamer Scene | Enthusiastic but accurate, community-first |
| DJD Spotlight | Honest, never self-promotional |
| Drum Culture | Opinionated, sharp takes |
| Gear Picks | Transparent — say when it's affiliate |

---

## 📐 Structure Per Issue (Minimum)

| Section | Content | Notes |
|---|---|---|
| Editor's Note | 200-250 words | Must reference biggest story of month |
| Cover Story | 400-600 words | One major feature |
| Drummer Spotlight (Historical) | 250-350 words | **Added September 2026.** Goes backward, not forward — a real historical figure, not this month's news. Drummerworld-style biographical depth |
| Gear & Tech | 3-5 items | Mix of big releases + smaller news |
| Drummer Pick of the Month | 100-200 words | **Added September 2026.** One specific, curated piece of drumming, argued for directly (Pitchfork-style single-work focus) — not a roundup entry |
| Drum Lesson | 1 lesson + 4 steps | Intermediate or beginner, rotating difficulty |
| Streamer Scene | 4 streamers | Rotate monthly, always verified data, never the same 4 as last issue |
| DJD Spotlight | 250-300 words | Honest, not hype |
| Drum Culture | 4 takes, 150-200 words each | Opinionated, linked |
| Gear Picks | 4 affiliate cards | Mark clearly as affiliate |
| What's Next | 3 items | ALL must be committed/confirmed content |
| Dream Loud Moment | 1 real sourced quote | Never fabricated |

### What's Next Commitment Rule
**If it's in What's Next, it must appear in the next issue.** No exceptions. Treat it as a contract with readers. If coverage changes, add a correction note in the following issue's Editor's Note.

---

## 🔄 Monthly Production Workflow

### Week 1 (Days 1-7): Research
- [ ] Run n8n RSS scrape workflow
- [ ] Review scraped articles, select top 5-7 stories
- [ ] Verify all facts on selected stories
- [ ] Identify 4 drum streamers to feature (check live/active status)
- [ ] Pull real images for each story (follow Image Policy)
- [ ] Check TwitchTracker/StreamsCharts for current follower counts

### Week 2 (Days 8-14): Write & Build
- [ ] Run Claude composition pass via n8n Anthropic node
- [ ] Review and edit Claude output — apply voice corrections
- [ ] Build HTML using current template
- [ ] Call `scripts/image_pipeline.py source` for every image slot (cover, spotlight, gear, streamers) — never hand-pick a stock photo instead
- [ ] Review the issue's `image-manifest.json`; resolve every `is_fallback: true` slot (real photo, illustration, or an explicit call to leave it) before approving
- [ ] Embed all real images with attribution
- [ ] Test all links (no dead links)
- [ ] Spell check all names against official sources

### Week 3-4 (Days 15-28): Polish & Publish
- [ ] Final factual review against checklist above
- [ ] Copyright audit on all images
- [ ] Push to GitHub repo → auto-deploy to magazine.drummerjawkneed.com
- [ ] Update banner.json for homepage embed
- [ ] Send Kit broadcast (draft → review → send)
- [ ] Discord announcement
- [ ] Social posts

---

## 📊 Competitor Analysis (Updated June 2026)

| Publication | Strengths | Our Gap | Our Edge |
|---|---|---|---|
| Modern Drummer | 49-year authority, 35+ educational depts, industry access, professional interviews | Depth of education, gear lab reviews | Streaming community, digital-native, free, monthly momentum |
| Drumeo Blog | Tutorial depth, YouTube integration, accessibility | Education content | Our cultural coverage, community focus |
| Digital Drummer | Streaming-adjacent coverage, gear reviews | Consistency, design quality | DJD brand, voice, affiliated community |
| Drummerworld | Reference depth, drummer database | We don't compete here | Current news, streaming focus |
| Pitchfork (model) | Voice, authority, takes positions | We need sharper music reviews | Drum-specific, community-first |

### What MD Does We Should Adopt
- [ ] **Readers Poll** — annual poll for best drum streamer, best gear release, best lesson
- [ ] **Recording Reviews** — short reviews of albums with notable drumming
- [x] **New Products** roundup — brief notes on gear announcements — **live as the Gear & Tech recurring department, September 2026**
- [ ] **Educational Department rotation** — different lesson topics each issue by guest contributors
- [ ] **Letters/Community** section — curated community responses/tips
- [x] **Drummerworld-style historical depth** — **live as the Drummer Spotlight (Historical) recurring department, September 2026** — see Structure Per Issue above

### What We Do They Can't
- ✅ Drum streaming community coverage at depth
- ✅ Real-time n8n-automated research pipeline
- ✅ Interactive web format (TOC, scroll reveal, progress bar)
- ✅ Free, monthly, no paywall
- ✅ DJD editorial voice — first person, authentic, from a working streamer

---

## 🛠️ Technical Standards

### File Structure (GitHub repo: `djd-magazine`)
```
/
├── index.html              → Redirects to /latest
├── latest/index.html       → Always current issue
├── june-2026/index.html    → Archived Issue 01
├── july-2026/index.html    → Issue 02 (when published)
├── drafts/issue-XX-month-year/ → In-progress issue (brief, research, draft HTML, candidate assets) — not deployed, promoted to a dated folder above at publish time
├── <month>-<year>/image-manifest.json → Per-issue real-photo sourcing record (see Image Policy) — reviewed as part of that issue's PR, not deployed as a page itself but committed alongside one
├── scripts/image_pipeline.py → Reusable real-photo sourcing module, called once per image slot by the monthly generation pipeline
├── assets/djd-real-photos/ → Real DJD/DrummerJawkneeD photos & footage, checked first for any "self" image slot
├── requirements.txt        → Python deps for scripts/image_pipeline.py (Pillow, requests)
├── style.css               → Shared styles (extract from HTML each issue)
├── banner.json             → Homepage embed data (auto-updated by n8n)
├── STANDARDS.md            → This file
├── CHANGELOG.md            → Issue-by-issue corrections and changes
└── _redirects              → /magazine → /latest, etc.
```

### Cloudflare Pages
- Custom domain: `magazine.drummerjawkneed.com`
- CNAME: `magazine` → `djd-magazine.pages.dev`
- Deploy: auto on every `git push` to main

### n8n Workflow
- Trigger: 1st of month, 8AM
- Sources: Modern Drummer RSS, Digital Drummer RSS, MusicRadar Drums, Reddit r/drums, Twitch streamer search
- Compose: Claude Sonnet via Anthropic node
- Deliver: GitHub API → Cloudflare Pages, Kit broadcast draft, Discord announcement

---

## 📝 CHANGELOG

### Issue 01 — June 2026
**Corrections Made:**
- Added Loren Gold (keyboardist) to Rush lineup — initially omitted
- Clarified tour is "Fifty Something" — not "50th anniversary"
- Fixed Art Cruz photo credit — Travis Shinn for Modern Drummer
- Added YouTube drum cam embed for Anika Nilles opening night footage
- Added Kit subscribe CTA mid-page
- Added Anika Nilles album count (4 albums, not 2)

**What Worked:**
- Real Twitch og:image URLs for streamer profiles — keep this approach
- Full-bleed cover photo with logo overlay — strong visual hierarchy
- JBL BandBox Trio product CDN image — accurate, direct from manufacturer
- Drum Lesson section — high engagement potential, keep and evolve
- "What's Next" commitment section — creates accountability

**What to Improve in Issue 02:**
- Add recording/album reviews section
- Add a "New Products" brief roundup (1-2 sentences each, 5+ items)
- Integrate YouTube embeds more naturally into articles
- Add social share buttons to each article section
- Consider a community Q&A or reader tips section
- Pull actual Anika Nilles or Art Cruz real photo (not stock) for cover story
