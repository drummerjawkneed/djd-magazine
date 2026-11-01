# November 2026 (Issue 06): draft notes

Drafted unattended on IMAC, 2026-10-28. Research done live on 2026-10-28 with `mag-tool grok` (3 calls), and every claim was then checked by fetching the cited page with `mag-tool web`. `mag-tool build` passes.

## Stories and sources

| Section | Story | Sources fetched |
|---|---|---|
| Cover | Nicko McBrain's autobiography *Hello Boys And Girls!* (Oct 22), spoken-word tour from Oct 26 | Blabbermouth (Oct 21), Wikipedia: Nicko McBrain, Piece of Mind, Clive Burr |
| This Month | Joey Kramer back with Aerosmith for the Hollywood Bowl (Oct 29 / Nov 1) | Loudwire (Oct 21), Drumming News Network |
| This Month | Dream Theater start album 17 with Portnoy (Oct 13) | Rock To Roll Radio (Oct 15) |
| This Month | Anika Nilles has the flu; Rush move San Jose Oct 17 to Dec 6 | Blabbermouth (Oct 17) |
| This Month | Peart memorial follow-up (October's What's Next promise): no October news found; opening tentatively late 2027 | City of St. Catharines news post |
| This Month | Fill-ins: Neil Sanderson / Shaun Foist; Jussi 69 / Vilho Rajala | Blabbermouth (Oct 25, Oct 22) |
| This Month | Jahdiel Aviles wins Zildjian US Young Drummer of the Year (final Oct 11) | Blair School of Music page; Zildjian winner video title on YouTube |
| This Month | In memoriam: Nigel Durham (ex-Saxon), 61 | Blabbermouth (Oct 25) |
| Drummer Spotlight | Gene Krupa (died Oct 16, 1973) | Wikipedia: Gene Krupa |
| Gear & Tech | Alesis Kitstream ($399), Gretsch Catalina EVO, Roland TD-07DMK2/KV2, Sabian effects models | digitalDrummer, Alesis release (MusicPlayers), Yamaha EAD50 award release, DNN, Music Instrument News, sabian.com |
| Pick of the Month | McBrain, "Where Eagles Dare" | Wikipedia: Nicko McBrain, Piece of Mind |
| Drum Lesson | Single paradiddle, 4 steps (rendered as a `news`-type section, since the builder has no lesson type) | PAS International Drum Rudiments |
| Streamer Scene | SmoothMcGroove 81,876 · davidfrankdrums 37,260 · GRUNDYontheDRUMS 2,359 · DrummerMiles 2,143 (none of them in September's list) | SullyGnome channel pages, read 2026-10-28 |
| Drum Culture | 4 opinion takes (postponing for sick drummers, fill-ins, kick-hoop mics, Krupa) | as linked per take |
| Work With DJD | Now three services: Build a Concert $95/1h30, lessons $35, consult $55 | drummerjawkneed.com, read 2026-10-28 |

Photos (all Wikimedia Commons; credits copied from each `.credit.json`): McBrain (Mike Lawrence, CC BY-SA 2.0), Kramer (Ed Vill, CC BY 2.0), Portnoy (Birgit Fostervold, CC BY-SA 4.0), Krupa (William P. Gottlieb, public domain).

## Critic loop (rule 18): Gemini was available for all three passes
1. **Pass 1, ISSUES (4).** Krupa's 1978 Hall of Fame line came before his 1973 death; Yamaha's EAD has a separate module, so Take 3 was wrong to lump it in with Alesis; the Kramer line was set before the show but publishes after it; the headline "One Kick Pedal" was ambiguous. All four fixed. For Kramer I did **not** write that he played. The draft says we went to press before the show.
2. **Pass 2, ISSUES (1).** The Editor's Note said Drum Culture "argues with" the injury news, which it doesn't. Fixed.
3. **Pass 3, CLEAN.**

## Dropped or changed because it couldn't be verified
- **Chris Welsh (Died Pretty) death, reported Oct 8.** The only source was a Facebook post whose body would not load (title only), so I couldn't confirm his age or the cause. Dropped.
- **Grok's detail that SmoothMcGroove "plays VGM drum covers with paid requests" and davidfrankdrums "drums for T-Pain".** Not confirmed on a page I fetched. I only used the stream titles and stats SullyGnome shows.
- **Prices for PDP Hickory sticks ($8.99) and Gretsch Catalina EVO.** Not on the pages I fetched. PDP was left out, and the Gretsch item says no price was given.
- **The date of Sabian's effects launch.** No date on sabian.com, so none is printed.
- **Clive Burr as the Historical Spotlight.** No freely licensed photo exists on Commons, so he appears in the cover story instead and Krupa got the Spotlight.

## Things for Johnny to review
- **No DJD Spotlight this month.** No new real DJD photos are in `assets/djd-real-photos/`, and an unattended run had nothing verified about this month's DJD activity. I left it out rather than invent it. Add one if you have material.
- **Follower counts come from SullyGnome, not TwitchTracker or Streams Charts.** STANDARDS names those two. Streams Charts returned 403 (Cloudflare), and TwitchTracker's page text doesn't show follower totals. SullyGnome is the tracker September used. All counts were read 2026-10-28, inside the 7-day window.
- **The streamer cards have no images.** Only Commons photos can be fetched here, and channel avatars are not on Commons.
- **The Kramer item is worded from before the show** (Oct 29). If you publish after confirming the show happened, you can change it to the past tense.
- **The Work With DJD section now lists "Build a Concert" ($95).** It appeared on drummerjawkneed.com; October listed only two services.
- **No `image-manifest.json` was produced** (same as October). Every image is a non-fallback Commons photo with a `.credit.json`.
