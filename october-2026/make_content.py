#!/usr/bin/env python3
"""Authoring script for the October 2026 issue: fills content.json (text + verified sources) and pulls image
credit/dimensions from the assets' *.credit.json so credits can never drift from what was downloaded."""
import json, os, glob
HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")

def cj(name):
    d = json.load(open(os.path.join(A, name + ".credit.json"), encoding="utf-8"))
    cred = f'Photo: {d["author"]} / <a href="{d["page"]}" target="_blank" rel="noopener">Wikimedia Commons</a> ({d["license"]})'
    return cred, d

def img(key, file, alt, caption, w, h, credit=None):
    if credit is None:
        credit, _ = cj(file.rsplit(".", 1)[0])
    return {"file": file, "alt": alt, "caption": caption, "credit": credit, "w": w, "h": h}

DJD = "Photo: DrummerJawkneeD (frame from Insta360 footage, Australian Botanic Garden Mount Annan)"
IM = {
    "peart": img("peart", "peart-2008.webp", "Neil Peart in a black t-shirt and red headband, looking down at his drum kit during a Rush concert.", "Neil Peart on stage with Rush at the Xcel Energy Center, St. Paul, May 22, 2008.", 1800, 1350),
    "pavilion": img("pavilion", "peart-pavilion-2026.webp", "The Neil Peart Pavilion, a large timber-and-glass picnic shelter with a red roof, at Lakeside Park in Port Dalhousie.", "The Neil Peart Pavilion at Lakeside Park, Port Dalhousie (St. Catharines), Ontario, 2026.", 1400, 1050),
    "hawkins": img("hawkins", "hawkins-2018.webp", "Taylor Hawkins playing drums on stage with Hollywood Vampires at the SSE Arena, London.", "Taylor Hawkins with Hollywood Vampires, SSE Arena, London, June 20, 2018.", 1800, 1012),
    "nilles": img("nilles", "nilles-clinic.webp", "Anika Nilles seated at a drum kit during a clinic.", "Anika Nilles at a drum clinic, February 2020.", 1600, 1200),
    "harrison": img("harrison", "harrison-clinic.webp", "Gavin Harrison playing drums at a clinic.", "Gavin Harrison at a drum clinic, 2011.", 900, 598),
    "dunn": img("dunn", "tiff-dunn.webp", "Sam Dunn, co-director, smiling in front of the TIFF step-and-repeat wall.", "Sam Dunn, co-director, at the premiere.", 760, 1140),
    "mcfadyen": img("mcfadyen", "tiff-mcfadyen.webp", "Scot McFadyen, co-director, in a green jacket in front of the TIFF wall.", "Scot McFadyen, co-director.", 760, 1140),
    "lee": img("lee", "tiff-lee.webp", "Geddy Lee in tinted glasses and a tan jacket at the TIFF premiere.", "Geddy Lee.", 760, 1140),
    "smith": img("smith", "tiff-smith.webp", "Chad Smith in a blue cap making the devil-horns gesture with both hands.", "Chad Smith.", 760, 1140),
    "nilles_tiff": img("nilles_tiff", "tiff-nilles.webp", "Anika Nilles in a black blazer at the TIFF premiere.", "Anika Nilles, Rush's current drummer.", 760, 1140),
    "yamaha": img("yamaha", "yamaha-ead20-press.png", "Yamaha EAD20 electronic acoustic drum module announcement artwork.", "Yamaha's announcement artwork for the EAD20.", 1080, 540,
                  'Image: Yamaha Corporation, from its <a href="https://www.yamaha.com/en/news_release/2026/26090301/" target="_blank" rel="noopener">September 3, 2026 press release</a>'),
    "flowers": img("flowers", "djd-mtannan-flowers.webp", "A path beside a bed of pink and white wildflowers in bloom, with visitors walking along it.", "Wildflower beds in bloom.", 1600, 900, DJD),
    "pond": img("pond", "djd-mtannan-pond.webp", "A clear garden pond edged with tree ferns and pandanus palms.", "The pond and tree-fern garden.", 1600, 900, DJD),
    "sign": img("sign", "djd-mtannan-sign.webp", "A colourful metal tree sculpture above a sign reading The Australian Botanic Garden Mount Annan.", "The sign that answered the question of where we were.", 1600, 900, DJD),
}
for k in ("dunn", "mcfadyen", "lee", "smith", "nilles_tiff"):
    IM[k]["credit"] = IM[k]["credit"]  # Gabriel Hutchinson / WikiPortraits, CC BY-SA 4.0 (from the credit json)

S = lambda t, u: (t, u)
CBC_DOC = S("CBC: Neil Peart's legendary drumming honoured by all-star drummers", "https://www.cbc.ca/documentaries/the-passionate-eye/no-one-s-disciple-neil-peart-rush-9.7343374")
CBC_11 = S("CBC News: 11 things we learned from the Neil Peart documentary", "https://www.cbc.ca/news/entertainment/neil-peart-rush-documentary-9.7343638")
BLAB = S("Blabbermouth: Official trailer for Neil Peart documentary", "https://blabbermouth.net/news/see-official-trailer-for-neil-peart-documentary-no-ones-disciple")
ORIG = S("Original Cin: Q&A with directors Scot McFadyen and Sam Dunn (Sept. 21, 2026)", "https://www.original-cin.ca/posts/2026/9/21/original-cin-qampa-the-directors-of-neil-peart-no-ones-disciple-on-the-late-rush-drummers-legacy")
TIFF = S("TIFF: Neil Peart: No One's Disciple", "https://www.tiff.net/films/neil-peart-no-ones-disciple")

c = {
  "issue_number": "05", "month": "October 2026", "kicker": "October 2026 · Cover Story",
  "headline": "Four Drummers Try to Play Neil Peart. The Cameras Stay On.",
  "dek": "Neil Peart: No One's Disciple premiered in Toronto on September 16. Its best idea is also its simplest: give Peart's parts to drummers who knew him, then film what happens.",
  "summary": "Four drummers try to play Neil Peart's parts in a new documentary, Rush finish the Peart memorial fund, the Fifty Something tour adds four arenas, and Taylor Hawkins gets this month's Drummer Spotlight.",
  "headline_short": "Four Drummers Try to Play Neil Peart", "date_published": "2026-10-01T12:00:00Z",
  "hero_image": "peart", "images": IM,
  "ticker": ["Neil Peart: No One's Disciple premiered at TIFF on September 16", "Rush's $785,000 gift closes the $1M Neil Peart memorial fund",
             "Fifty Something adds Houston, St. Louis, Cincinnati and Pittsburgh", "Yamaha launches the EAD20 electronic acoustic drum module (Sept. 3)",
             "Rohema releases Nick Petrella NP5 and NP10 concert sticks (Sept. 25)"],
  "sections": [
   {"id": "ed", "type": "editor", "label": "Editor's Note", "tone": "r", "body": [
     "Stewart Copeland, Danny Carey, Chad Smith and Gavin Harrison did something most drummers only daydream about. They stood in a room with Geddy Lee and Alex Lifeson and tried to play Neil Peart's parts. The cameras were rolling. Nobody got to hide.",
     "That is the story of this issue. <em>Neil Peart: No One's Disciple</em> premiered at the Toronto International Film Festival on September 16 and reached CBC a week later. It gives the drumming world something rare: four experts being honest about how hard the job is. Gavin Harrison charted &ldquo;Dreamline&rdquo; before he touched a kit. Danny Carey stumbled through the <em>2112</em> overture and said so.",
     "We also changed how we work. Every photo in this issue has a named photographer and a licence you can click. Every story lists its sources. And where we got September wrong, there is a corrections box near the bottom, because a magazine that won't say when it missed is not worth reading.",
     "Go play something you think is beyond you. Chart it first if you have to."],
     "sign": "DRUMMERJAWKNEED &middot; DREAM LOUD"},
   {"id": "cover", "type": "cover", "label": "Cover Story", "tone": "g", "image": "peart",
     "headline": "What happens when Peart's friends try to play Peart",
     "dek": "The film runs 96 minutes. The part that matters is a studio, six musicians and a set of drum parts that do not forgive.",
     "body": [
      "<em>Neil Peart: No One's Disciple</em> comes from Scot McFadyen and Sam Dunn, who made the 2010 Rush documentary <em>Beyond the Lighted Stage</em>. It had its world premiere at the Toronto International Film Festival on September 16, a public screening on September 19, and aired on CBC's <em>The Passionate Eye</em> on September 23. It is streaming on CBC Gem in Canada.",
      "The hook is a set of studio sessions. Geddy Lee and Alex Lifeson play alongside four drummers: Stewart Copeland of The Police, Danny Carey of Tool, Chad Smith of the Red Hot Chili Peppers, and Gavin Harrison of Porcupine Tree and King Crimson. McFadyen told Original Cin the four were chosen because they were Peart's friends, close enough to have been at his funeral, not just famous names.",
      "The details are where it gets good. According to CBC's coverage, Harrison wrote out detailed charts before attempting &ldquo;Dreamline&rdquo; and came away convinced of how much thought sits inside every drum part. Carey, after a rough run at the overture to <em>2112</em>, admitted the opening was tricky. Lifeson said he was wowed by Peart's triplets, and Smith was struck by how straight-faced Peart played: no theatrics, just the part."],
     "pull": {"text": "&ldquo;That beginning was tricky, man.&rdquo;", "cite": "Danny Carey, after a run at the 2112 overture &middot; as reported by CBC"},
     "body2": [
      "Dunn says the film is meant to show Peart as &ldquo;a very loyal and loving friend, an inspiration to a lot of people&rdquo; and to put the drumming first, because its complexity is what general audiences miss. The directors built it from unused footage from <em>Beyond the Lighted Stage</em> and the <em>Rock Icons</em> series, MuchMusic archive, and Peart's own instructional videos, so his voice stays in the room.",
      "Two absences shape the film. Taylor Hawkins would have taken part if he had lived, the directors say. And Anika Nilles, Rush's current drummer, gets an epilogue even though she never met Peart: she learned his material from the records. She was at the premiere.",
      "Why it matters if you play, teach or stream: this is a rare film that treats the hardest job in rock drumming, playing someone else's parts correctly, as the drama. It is an argument for doing the homework. Watch for a screening or streaming option in your region."],
     "gallery": ["dunn", "mcfadyen", "lee", "smith", "nilles_tiff"],
     "sources": [CBC_DOC, CBC_11, BLAB, ORIG, TIFF, S("Wikimedia Commons: TIFF 2026 WikiPortraits (Gabriel Hutchinson)", "https://commons.wikimedia.org/wiki/Category:WikiPortraits_at_2026_Toronto_International_Film_Festival")]},
   {"id": "news", "type": "news", "label": "This Month", "tone": "c", "items": [
     {"tag": "Memorial", "headline": "Rush finish the Neil Peart memorial fund", "image": "pavilion", "body": [
       "Geddy Lee and Alex Lifeson donated $785,000, taking the City of St. Catharines' campaign for a Neil Peart memorial to its $1 million goal, according to CBC. The money came from a portion of the proceeds of Rush's Fifty Something tour; Lee also set aside proceeds from his 2023 book tour.",
       "The memorial is two bronze statues by Morgan MacDonald of the Newfoundland Bronze Foundry. Loudwire reported in 2022 that the younger Peart, roughly 12 feet tall, holds a book and drumsticks, and that the older figure sits with a snare drum and sticks; CBC's current description has the older figure offering his sticks to visitors. The city expects to finish next year, at the Neil Peart Pavilion in Lakeside Park, the place his 1975 song &ldquo;Lakeside Park&rdquo; is named for."],
      "sources": [S("CBC: After a donation from his Rush bandmates, Neil Peart art memorial will be a reality", "https://www.cbc.ca/news/canada/hamilton/neil-peart-rush-drummer-memorial-lakeside-park-9.7358386"), S("Loudwire (Nov. 10, 2022): Neil Peart to be honored with two statues", "https://loudwire.com/rush-neil-peart-statues-lakeside-park/"), S("Wikipedia: Lakeside Park (song)", "https://en.wikipedia.org/wiki/Lakeside_Park_(song)")]},
     {"tag": "Touring", "headline": "Fifty Something adds four arenas", "body": [
       "Rush added Houston (Toyota Center, October 1), St. Louis (Enterprise Center, October 21), Cincinnati (Heritage Bank Center, October 23) and Pittsburgh (PPG Paints Arena, November 15). Lee and Lifeson left wide gaps in the original routing because they did not know how they would hold up on the road. They are doing fine and having a blast, so they filled some of the gaps.",
       "&ldquo;Dreamline&rdquo; is on the tour's setlist, and Anika Nilles is behind the kit."],
      "sources": [S("Pollstar: Rush adds Houston, St. Louis, Cincinnati, Pittsburgh", "https://news.pollstar.com/2026/08/31/rush-adds-houston-st-louis-cincinnati-pittsburgh-to-fifty-something-tour/"), S("Loudwire: Rush add 4 new dates to 2026 Fifty Something tour", "https://loudwire.com/rush-4-new-dates-2026-fifty-something-tour/"), S("Wikipedia: Fifty Something tour", "https://en.wikipedia.org/wiki/Fifty_Something_tour")]}]},
   {"id": "hspot", "type": "spotlight", "label": "Drummer Spotlight", "tone": "bz", "image": "hawkins", "kicker": "Historical", "headline": "Taylor Hawkins: the drummer who sang from behind the kit",
     "dek": "Born February 17, 1972. Died March 25, 2022. The Peart film's directors say he would have been in it.",
     "body": [
      "Oliver Taylor Hawkins was born in Fort Worth, Texas, and grew up in Laguna Beach, California. Before Foo Fighters he toured as a drummer for Sass Jordan and Alanis Morissette. He joined Foo Fighters in 1997 and stayed until March 2022, recording eight studio albums with the band between 1999 and 2021.",
      "His signature move broke a rule: the drummer sings. Hawkins shared lead vocals with Dave Grohl live and took covers like Queen's &ldquo;Somebody to Love&rdquo;, the last song of his final show. He co-wrote on at least one song on every Foo Fighters album from <em>There Is Nothing Left to Lose</em> onward, and in 2004 he formed his own band, Taylor Hawkins and the Coattail Riders, which released three albums.",
      "His influences read like a map of big-hearted rock drumming: Phil Collins, Stewart Copeland (whom he idolized and eventually befriended), Roger Taylor, Stephen Perkins and Neil Peart. It was Taylor who mattered in 2000, when Guns N' Roses asked Hawkins to replace Josh Freese and Roger Taylor talked him into staying with the Foos.",
      "Rhythm magazine voted him Best Rock Drummer in 2005, and he went into the Rock and Roll Hall of Fame with Foo Fighters in 2021. He died in Bogot&aacute;, Colombia, on March 25, 2022, on the day of a festival set. Two tribute concerts followed in September 2022; Stewart Copeland was among the drummers at the Wembley show on September 3."],
     "facts": [["8", "studio albums with Foo Fighters"], ["1997", "joined the band"], ["2021", "Rock Hall induction"]],
     "sources": [S("Wikipedia: Taylor Hawkins", "https://en.wikipedia.org/wiki/Taylor_Hawkins"), ORIG]},
   {"id": "gear", "type": "gear", "label": "Gear & Tech", "tone": "c", "items": [
     {"tag": "Recording &amp; streaming", "headline": "Yamaha EAD20 electronic acoustic drum module", "image": "yamaha", "body": [
       "Announced September 3. A sensor unit attaches to the bass drum hoop and captures the whole acoustic kit, so you can monitor through a PA or headphones and add effects such as reverb. The pitch for streamers is the USB audio interface: multitrack recording, DAW integration and streaming, plus a Rec'n'Share app for shooting and sharing performance videos on a phone.",
       "You can add pads or triggers for hybrid acoustic and electronic playing, and trigger sensitivity is set by hitting the drums. The press release we read does not list pricing or a ship date, so check Yamaha before you plan around it. We have not tested it."],
      "specs": ["Sensor unit on bass drum hoop", "USB audio interface", "Rec'n'Share app", "Works with pads / triggers"],
      "sources": [S("Yamaha Corporation press release, Sept. 3, 2026", "https://www.yamaha.com/en/news_release/2026/26090301/")]},
     {"tag": "Sticks", "headline": "Rohema Nick Petrella NP5 and NP10 General", "body": [
       "Released September 25. Nick Petrella, an American drummer, percussionist, educator and author, worked with German maker Rohema on two concert sticks. The NP5 is 422 mm by 17 mm with a long taper and an acorn tip. The NP10 General is 416 mm by 16.5 mm, slightly lighter, with a larger rounded tip.",
       "Both are made from Rohema's laminated Hornwood with a wax-oil finish, so they avoid tropical hardwoods. They are built for concert and orchestral playing, so treat them as a practice and rudiment stick, not a rock stick."],
      "specs": ["NP5: 422 x 17 mm, acorn tip", "NP10: 416 x 16.5 mm, rounded tip", "Laminated Hornwood", "Wax-oil finish"],
      "sources": [S("Drumming News Network: Rohema introduce Nick Petrella signature drumsticks", "https://www.drummingnewsnetwork.com/rohema-introduce-new-nick-petrella-signature-drumsticks-precision-response-and-feel/"), S("Rohema: signature drumsticks", "https://www.rohema.de/en/products/drumsticks/signature/")]}]},
   {"id": "pick", "type": "pick", "label": "Pick of the Month", "tone": "r", "kicker": "Drummer Pick of the Month", "headline": "Neil Peart, &ldquo;Dreamline&rdquo; (<em>Roll the Bones</em>, 1991)",
     "dek": "Because Gavin Harrison charted it.",
     "body": [
       "Our pick is one drum part, and the reason is in the film. Gavin Harrison has spent decades taking odd time apart, and he still wrote out charts before he tried &ldquo;Dreamline&rdquo; with Lee and Lifeson.",
       "The song came out on Rush's 1991 album <em>Roll the Bones</em>, reached number one on the US Mainstream Rock chart, and Geddy Lee has said it captures the wanderlust and invulnerability of a hard stretch in your life. It appears on the Fifty Something setlist, with Anika Nilles behind the kit.",
       "Listen three times. Once for the song. Once only for the hi-hat and snare. Once only for where the kick goes. Then open a chart. The part sounds like momentum and is actually a stack of decisions. That is what a Pick is for: one piece of playing you can go and do something with."],
     "sources": [CBC_11, S("Wikipedia: Dreamline", "https://en.wikipedia.org/wiki/Dreamline"), S("Wikipedia: Fifty Something tour", "https://en.wikipedia.org/wiki/Fifty_Something_tour")]},
   {"id": "djd", "type": "djd", "label": "DJD Spotlight", "tone": "g", "kicker": "On location", "headline": "Mount Annan in 360: a walk through Australia's largest botanic garden",
     "dek": "Footage from the DrummerJawkneeD channel's September trip, cut into short reels.",
     "gallery": ["flowers", "pond", "sign"],
     "body": [
       "The Australian Botanic Garden Mount Annan covers about 416 hectares in South Western Sydney, between Campbelltown and Camden. It is the largest botanical garden in Australia, it specialises in native plants, and its collection runs past 4,000 species. It opened in 1988 on Dharawal land, and more than 20 kilometres of walking tracks cross it, plus a native-flora research facility and the PlantBank seed-storage building.",
       "The DrummerJawkneeD channel walked it in September with an Insta360 camera. A 360 camera records every direction at once and lets you choose the shot afterwards, which is exactly why drum channels should care: put one at the kit and you can cut a wide room shot, a hi-hat close-up and a pedal angle from a single take. The garden footage is the same workflow pointed at flower beds instead of a snare.",
       "The result is a set of 24-second reels, reframed from the 360 capture, colour-corrected and loudness-matched, with more cuts still coming. The opening frames sit low among pink and white wildflowers in bloom; the pond shot below is tree ferns and pandanus. The sign in the third frame is how we know exactly where we were. There is no music on the reels yet, and that part stays the drummer's call."],
     "sources": [S("Wikipedia: Australian Botanic Garden Mount Annan", "https://en.wikipedia.org/wiki/Australian_Botanic_Garden_Mount_Annan")]},
   {"id": "culture", "type": "culture", "label": "Drum Culture", "tone": "c", "items": [
     {"headline": "Charts are not cheating", "body": ["We love the myth that great drummers play everything by feel. The Peart film quietly kills it: Gavin Harrison charted &ldquo;Dreamline&rdquo; first. Writing a part down forces you to hear where every note lives.",
       "If you cover songs on stream, your audience cannot see your homework, but they can hear whether you did it. Transcribe one part a week. It is the cheapest upgrade in drumming."],
       "sources": [CBC_11]},
     {"headline": "Drummers deserve statues", "body": ["Drummers sit at the back of the stage, in the dark, behind a wall of cymbals. A bronze statue in a public park reverses that. It is unusual for fans to raise hundreds of thousands of dollars for one, and more unusual for his bandmates to close the gap with $785,000.",
       "The detail that matters is the order: the community built the campaign first. Public art for drummers should be normal."],
       "sources": [S("CBC: Neil Peart memorial will be a reality", "https://www.cbc.ca/news/canada/hamilton/neil-peart-rush-drummer-memorial-lakeside-park-9.7358386")]},
     {"headline": "Most drum streams sound worse than they look", "body": ["A kit on camera looks like a show. Through a stream encoder, without enough microphones or the time to place them, it often sounds like a cardboard box being hit in another room.",
       "One-sensor systems like Yamaha's EAD20 will not replace good mic technique, and we have not tested it. But anything that makes a decent stream mix easier is aimed at the real problem. Fix the sound before you fix the lights."],
       "sources": [S("Yamaha press release", "https://www.yamaha.com/en/news_release/2026/26090301/")]}]},
   {"id": "work", "type": "work", "label": "Work With DJD", "tone": "c", "items": [
     {"tag": "1-on-1 &middot; Booked via TidyCal", "headline": "Drum lessons: $35 per hour", "body": ["Live lessons with DrummerJawkneeD, scheduled through the Work With Me section of drummerjawkneed.com. Level and format are worked out when you book."]},
     {"tag": "1-on-1 &middot; Booked via TidyCal", "headline": "Streamer consultation: $55 per hour", "body": ["For creators building a drum-streaming setup: OBS, multi-platform routing and gear choices. Same booking flow as lessons."]}],
     "note": "These are the two bookable services listed on drummerjawkneed.com as of this issue. Prices and availability are set on the booking page."},
   {"id": "newsletter", "type": "newsletter", "label": "Newsletter", "tone": "r", "kicker": "Free &middot; Monthly &middot; No spam", "headline": "Get November in your inbox",
     "body": "A Drummer Spotlight, a Pick of the Month and the month's verified drum news, on the first of every month."},
   {"id": "corr", "type": "corrections", "label": "Corrections", "tone": "g", "items": [
     "<b>September, Cover Story.</b> We described the older Peart statue as &ldquo;cradling a snare drum.&rdquo; Loudwire's 2022 report has the older figure seated with drumsticks and a snare in his lap; CBC's current coverage describes him offering his sticks to visitors. Reports differ and the statues have not been unveiled, so treat every description as provisional. The story also left out the sculptor, Morgan MacDonald of the Newfoundland Bronze Foundry, and the roughly 12-foot height of the younger figure.",
     "<b>September, Pick of the Month.</b> We wrote that Ilan Rubin's Foo Fighters album was cut live with no click track. We could not confirm the recording method in a primary source. What we can confirm: Rubin is the drummer on <em>Your Favorite Toy</em>, released April 24, 2026, and after 17 years of playing to a click live, Dave Grohl has said he encouraged Rubin to play more freely.",
     "<b>September, photos.</b> The September issue ran without real photographs of its subjects. Every photo in this issue is credited to its photographer with a licence link."]},
   {"id": "next", "type": "next", "label": "What's Next", "tone": "r", "items": [
     {"tag": "November issue", "headline": "Drummer Spotlight and Pick of the Month", "body": ["Both departments return, with sources on every story and a named photographer on every picture."]},
     {"tag": "November issue", "headline": "A Drum Lesson, and Streamer Scene", "body": ["One rudiment in four steps, and Streamer Scene back at full size with audience numbers checked against a tracker inside the seven-day window."]},
     {"tag": "Watch", "headline": "The Peart memorial", "body": ["If the City of St. Catharines publishes a construction or unveiling update, we will report it."]}]}
  ]
}
json.dump(c, open(os.path.join(HERE, "content.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("content.json written:", len(c["sections"]), "sections,", len(IM), "images")
