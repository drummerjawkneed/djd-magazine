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

## 📷 Image Policy

### Permitted Sources (in order of preference)

1. **Original photos** — shot by DJD or submitted by subjects with permission
2. **Unsplash / Pexels** — free commercial license, download properly
3. **Official product CDN images** — JBL, Roland, Yamaha etc. linking to product pages (editorial use)
4. **Twitch og:image** — fetched directly from `twitch.tv/{channel}` page meta, public
5. **YouTube channel avatars** — `yt3.googleusercontent.com` format
6. **Press photos with explicit attribution** — credit photographer + publication, link to source

### Prohibited

- ❌ Hotlinking copyrighted press photos without explicit permission (e.g., Getty, Travis Shinn for MD)
- ❌ Stock photos representing real named people or specific real events
- ❌ Images that misrepresent what is being described (e.g., generic "singer" photo for "drummer" article)
- ❌ AI-generated photos of real named people

### Attribution Format
```
Photo: [Photographer Name] for [Publication] · [Year]
```
Always link to original source article.

### If No Real Photo Available
Use **branded SVG illustration** (our drum icon system) rather than a misleading stock photo. Honesty > aesthetics.

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
| Gear & Tech | Factual, useful, with opinion |
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
| Cover Story | 400-600 words | One major feature, full-bleed photo |
| Gear & Tech | 3-5 items | Mix of big releases + smaller news |
| Drum Lesson | 1 lesson + 4 steps | Intermediate or beginner, rotating difficulty |
| Streamer Scene | 4 streamers | Rotate monthly, always verified data |
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
- [ ] **New Products** roundup — brief notes on gear announcements
- [ ] **Educational Department rotation** — different lesson topics each issue by guest contributors
- [ ] **Letters/Community** section — curated community responses/tips

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
