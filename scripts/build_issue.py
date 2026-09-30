#!/usr/bin/env python3
"""build_issue.py -- render a magazine issue from <issue>/content.json into <issue>/index.html.

Design goals (Johnny, 2026-09-30): industry-standard editorial page -- photo-led, every image credited,
every story sourced, accessible, fast, no hidden-until-scroll content, correct OG/JSON-LD, mobile-first.
Content lives in JSON so the n8n/Claude pipeline can fill it; this file is the only place markup lives.

  python3 scripts/build_issue.py october-2026
Validation (fails the build): every <img> has alt+credit, every section with claims has >=1 source,
no banned phrases (STANDARDS.md), no [REDACTED / mojibake, image files exist.
"""
import json, sys, os, re, html, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANNED = ["delve into", "it's worth noting", "it’s worth noting", "in conclusion", "as we all know", "needless to say", "exciting new"]
SITE = "https://magazine.drummerjawkneed.com"
e = lambda s: html.escape(str(s), quote=True)

def para(ps, cls=""):
    return "".join(f'<p{(" class=%s" % cls) if cls else ""}>{p}</p>' for p in ps)   # paragraphs may contain trusted inline HTML (links/em)

def figure(issue, img, cls="", sizes="100vw", eager=False):
    path = f"/{issue}/assets/{img['file']}"
    w, h = img.get("w", 1600), img.get("h", 900)
    cap = f'<figcaption><span class="cap">{img["caption"]}</span><span class="credit">{img["credit"]}</span></figcaption>'
    return (f'<figure class="ph {cls}"><img src="{path}" alt="{e(img["alt"])}" width="{w}" height="{h}" '
            f'sizes="{sizes}" {"fetchpriority=high" if eager else "loading=lazy"} decoding="async">{cap}</figure>')

def sources(items):
    if not items: return ""
    li = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in items)
    return f'<details class="src"><summary>Sources ({len(items)})</summary><ul>{li}</ul></details>'

def section_head(n, label, idx, tone="r"):
    return f'<div class="sh"><span class="bar {tone}"></span><h2 class="lab">{e(label)}</h2><span class="rule"></span><span class="num">{n}</span></div>'

def build(issue):
    c = json.load(open(os.path.join(ROOT, issue, "content.json"), encoding="utf-8"))
    im = c["images"]
    logo = open(os.path.join(ROOT, "scripts", "logo.svg.inc"), encoding="utf-8").read()
    url = f"{SITE}/{issue}/"
    hero = im[c["hero_image"]]
    toc = [(s["id"], s["label"]) for s in c["sections"]]
    parts = []
    for i, s in enumerate(c["sections"]):
        t = s["type"]; sid = s["id"]; n = f"{i:02d}"
        head = section_head(n, s["label"], i, s.get("tone", "r"))
        body = ""
        if t == "editor":
            body = f'<div class="edwrap"><div class="bignum" aria-hidden="true">{c["issue_number"]}</div><div class="prose">{para(s["body"])}<p class="sign">{s["sign"]}</p></div></div>'
        elif t == "cover":
            gal = "".join(f'<figure class="tile"><img src="/{issue}/assets/{im[k]["file"]}" alt="{e(im[k]["alt"])}" width="{im[k]["w"]}" height="{im[k]["h"]}" loading="lazy" decoding="async"><figcaption><span class="cap">{im[k]["caption"]}</span><span class="credit">{im[k]["credit"]}</span></figcaption></figure>' for k in s["gallery"])
            body = (f'<article class="story"><h3 class="hl">{s["headline"]}</h3><p class="dek">{s["dek"]}</p>{figure(issue, im[s["image"]], "wide")}'
                    f'<div class="prose cols">{para(s["body"])}</div>'
                    f'<aside class="pull"><blockquote>{s["pull"]["text"]}</blockquote><cite>{s["pull"]["cite"]}</cite></aside>'
                    f'<div class="prose cols">{para(s["body2"])}</div><div class="gallery">{gal}</div>{sources(s["sources"])}</article>')
        elif t == "news":
            items = "".join(f'<article class="card"><span class="tag">{it["tag"]}</span><h3>{it["headline"]}</h3>{para(it["body"])}'
                            f'{figure(issue, im[it["image"]], "inline") if it.get("image") else ""}{sources(it["sources"])}</article>' for it in s["items"])
            body = f'<div class="cards">{items}</div>'
        elif t == "spotlight":
            facts = "".join(f'<li><b>{e(a)}</b><span>{e(b)}</span></li>' for a, b in s["facts"])
            body = (f'<article class="story spot"><div class="spgrid">{figure(issue, im[s["image"]], "tall")}<div><span class="tag">{s["kicker"]}</span>'
                    f'<h3 class="hl">{s["headline"]}</h3><p class="dek">{s["dek"]}</p><div class="prose">{para(s["body"])}</div></div></div>'
                    f'<ul class="facts">{facts}</ul>{sources(s["sources"])}</article>')
        elif t == "gear":
            items = ""
            for it in s["items"]:
                spec = "".join(f'<li>{e(x)}</li>' for x in it.get("specs", []))
                items += (f'<article class="card gear"><span class="tag">{it["tag"]}</span><h3>{it["headline"]}</h3>'
                          f'{figure(issue, im[it["image"]], "inline") if it.get("image") else ""}{para(it["body"])}'
                          f'{("<ul class=specs>%s</ul>" % spec) if spec else ""}{sources(it["sources"])}</article>')
            body = f'<div class="cards two">{items}</div>'
        elif t == "pick":
            body = (f'<article class="story pick"><span class="tag">{s["kicker"]}</span><h3 class="hl">{s["headline"]}</h3>'
                    f'<p class="dek">{s["dek"]}</p><div class="prose narrow">{para(s["body"])}</div>{sources(s["sources"])}</article>')
        elif t == "streamer":
            body = (f'<article class="story"><span class="tag">{s["kicker"]}</span><h3 class="hl">{s["headline"]}</h3><div class="prose narrow">{para(s["body"])}</div>'
                    f'<p><a class="btn" href="{e(s["link"])}" target="_blank" rel="noopener">{e(s["cta"])}</a></p>{sources(s["sources"])}</article>')
        elif t == "djd":
            gal = "".join(f'<figure class="tile"><img src="/{issue}/assets/{im[k]["file"]}" alt="{e(im[k]["alt"])}" width="{im[k]["w"]}" height="{im[k]["h"]}" loading="lazy" decoding="async"><figcaption><span class="cap">{im[k]["caption"]}</span><span class="credit">{im[k]["credit"]}</span></figcaption></figure>' for k in s["gallery"])
            body = (f'<article class="story"><span class="tag">{s["kicker"]}</span><h3 class="hl">{s["headline"]}</h3><p class="dek">{s["dek"]}</p>'
                    f'<div class="gallery three">{gal}</div><div class="prose narrow">{para(s["body"])}</div>'
                    f'<p><a class="btn" href="https://drummerjawkneed.com" target="_blank" rel="noopener">Watch live at drummerjawkneed.com</a></p>{sources(s.get("sources", []))}</article>')
        elif t == "culture":
            items = "".join(f'<article class="card take"><span class="tag">Take {k+1}</span><h3>{it["headline"]}</h3>{para(it["body"])}{sources(it.get("sources", []))}</article>' for k, it in enumerate(s["items"]))
            body = f'<div class="cards three">{items}</div>'
        elif t == "work":
            items = "".join(f'<article class="card"><span class="tag">{it["tag"]}</span><h3>{it["headline"]}</h3>{para(it["body"])}</article>' for it in s["items"])
            body = f'<div class="cards two">{items}</div><p class="note">{s["note"]}</p>'
        elif t == "newsletter":
            body = (f'<div class="nl"><span class="tag">{s["kicker"]}</span><h3>{s["headline"]}</h3><p>{s["body"]}</p>'
                    f'<a class="btn" href="https://app.kit.com/forms/designers/9489280" target="_blank" rel="noopener">Subscribe free &rarr;</a></div>')
        elif t == "corrections":
            li = "".join(f"<li>{x}</li>" for x in s["items"])
            body = f'<div class="corr"><ul>{li}</ul></div>'
        elif t == "next":
            items = "".join(f'<article class="card"><span class="tag">{it["tag"]}</span><h3>{it["headline"]}</h3>{para(it["body"])}</article>' for it in s["items"])
            body = f'<div class="cards three">{items}</div>'
        else:
            raise SystemExit("unknown section type " + t)
        parts.append(f'<section id="{sid}" class="sec">{head}{body}</section>')
    toc_html = "".join(f'<li><a href="#{i}">{e(l)}</a></li>' for i, l in toc)
    jsonld = {"@context": "https://schema.org", "@type": "NewsArticle", "headline": c["headline"], "description": c["summary"],
              "datePublished": c["date_published"], "image": [f"{SITE}/{issue}/assets/{hero['file']}"], "mainEntityOfPage": url,
              "author": {"@type": "Organization", "name": "Drummers & Dreamers Magazine"}, "publisher": {"@type": "Organization", "name": "Drummers & Dreamers, Inc."}}
    page = PAGE.format(
        title=e(f'{c["month"]} — Drummers & Dreamers Magazine'), desc=e(c["summary"]), url=url, og_img=f"{SITE}/{issue}/assets/{hero['file']}",
        month=e(c["month"]), logo=logo, headline=c["headline"], dek=c["dek"], kicker=e(c["kicker"]),
        hero=figure(issue, dict(hero, caption="", credit=""), "hero", eager=True).replace('<figcaption><span class="cap"></span><span class="credit"></span></figcaption>',''), herocap=f'<div class="herocap"><span>{hero["caption"]}</span> <span class="credit">{hero["credit"]}</span></div>', toc=toc_html, body="\n".join(parts), jsonld=json.dumps(jsonld, ensure_ascii=False),
        ticker="".join(f"<li>{t}</li>" for t in c["ticker"]), year=datetime.date.today().year, updated=c["date_published"][:10])
    out = os.path.join(ROOT, issue, "index.html")
    open(out, "w", encoding="utf-8").write(page)
    validate(issue, page, c)
    print("built", out, len(page), "bytes")

def validate(issue, page, c):
    errs = []
    for b in BANNED:
        if b in page.lower(): errs.append("banned phrase: " + b)
    if re.search(r"\[REDACTED|Ã¢|â€", page): errs.append("redaction/mojibake artifact")
    for m in re.finditer(r'<img [^>]*src="([^"]+)"[^>]*>', page):
        tag = m.group(0); p = os.path.join(ROOT, m.group(1).lstrip("/"))
        if 'alt="' not in tag or 'alt=""' in tag: errs.append("img missing alt: " + m.group(1))
        if not os.path.exists(p): errs.append("missing image file: " + m.group(1))
    figs = len(re.findall(r"<figure", page)); creds = len(re.findall(r'class="credit"', page))  # hero credit lives in .herocap
    if figs != creds: errs.append(f"figure/credit mismatch {figs}/{creds}")
    for s in c["sections"]:
        if s["type"] in ("cover", "spotlight", "pick", "streamer") and not s.get("sources"): errs.append("no sources: " + s["id"])
        if s["type"] in ("news", "gear"):
            for it in s["items"]:
                if not it.get("sources"): errs.append("item without sources in " + s["id"])
    if errs:
        print("VALIDATION FAILED:\n - " + "\n - ".join(errs)); sys.exit(1)

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:site_name" content="Drummers &amp; Dreamers Magazine">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{og_img}">
<meta name="theme-color" content="#080810">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Rajdhani:wght@600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<script type="application/ld+json">{jsonld}</script>
<style>
:root{{--bg:#080810;--sur:#12121d;--lft:#1b1b2b;--tx:#e8e8f2;--dm:#a4a4bd;--r:#ff4d5a;--c:#2bc4e6;--g:#f5a623;--bz:#d79a63;--bd:rgba(255,255,255,.1);--mw:1120px;--fd:'Playfair Display',Georgia,serif;--fb:'DM Sans',system-ui,sans-serif;--fm:'Space Mono',ui-monospace,monospace}}
*{{box-sizing:border-box;margin:0;padding:0}}html{{scroll-behavior:smooth;scroll-padding-top:70px}}
body{{background:var(--bg);color:var(--tx);font-family:var(--fb);font-size:1.0625rem;line-height:1.7;-webkit-font-smoothing:antialiased}}
a{{color:var(--c);text-underline-offset:3px}}a:hover{{color:#fff}}img{{display:block;max-width:100%;height:auto}}
.skip{{position:absolute;left:-999px;top:0;background:#fff;color:#000;padding:.6rem 1rem;z-index:99}}.skip:focus{{left:0}}
.mast{{position:sticky;top:0;z-index:50;display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:.6rem clamp(1rem,4vw,2.5rem);background:rgba(8,8,16,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--bd)}}
.mast svg{{height:28px;width:auto}}.mast nav{{display:flex;gap:1.1rem;align-items:center;font:700 .72rem var(--fm);letter-spacing:.12em;text-transform:uppercase}}
.mast nav a{{color:var(--dm);text-decoration:none}}.mast nav a:hover{{color:#fff}}.issue{{color:#fff;background:var(--r);padding:.2rem .55rem;border-radius:2px}}
.toc-btn{{font:700 .72rem var(--fm);letter-spacing:.12em;text-transform:uppercase;color:#fff;background:none;border:1px solid var(--bd);padding:.35rem .7rem;cursor:pointer}}
.toc{{display:none;position:fixed;inset:54px 0 auto 0;z-index:49;background:var(--sur);border-bottom:1px solid var(--bd);padding:1.2rem clamp(1rem,4vw,2.5rem)}}.toc.open{{display:block}}
.toc ol{{list-style:none;columns:2;max-width:var(--mw);margin:auto}}.toc li{{padding:.25rem 0}}.toc a{{color:var(--tx);text-decoration:none}}
.hero-wrap{{position:relative;min-height:min(86vh,760px);display:grid;align-items:end;isolation:isolate}}
.hero{{position:absolute;inset:0;margin:0;z-index:-1}}.hero img{{width:100%;height:100%;object-fit:cover;object-position:50% 30%}}
.hero::after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,8,16,.25) 0%,rgba(8,8,16,.55) 45%,rgba(8,8,16,.96) 100%)}}
.hero-in{{max-width:var(--mw);margin:0 auto;padding:clamp(6rem,18vh,11rem) clamp(1rem,4vw,2.5rem) 3.2rem;width:100%}}
.kick{{font:700 .78rem var(--fm);letter-spacing:.2em;text-transform:uppercase;color:var(--r)}}
.hero-in h1{{font-family:var(--fd);font-weight:900;font-size:clamp(2.3rem,6.4vw,4.6rem);line-height:1.04;margin:.7rem 0 1rem;max-width:18ch;text-wrap:balance}}
.hero-in .dek{{font-size:clamp(1.05rem,2vw,1.35rem);color:#d8d8e8;max-width:58ch}}
.herocap{{max-width:var(--mw);margin:0 auto;padding:.7rem clamp(1rem,4vw,2.5rem);font-size:.78rem;color:var(--dm)}}.herocap .credit{{margin-left:.6rem}}
.ticker{{overflow:hidden;background:var(--r);color:#fff;font:700 .74rem var(--fm);letter-spacing:.1em;text-transform:uppercase}}
.ticker ul{{display:flex;gap:2.5rem;list-style:none;padding:.65rem 1rem;white-space:nowrap;animation:tk 60s linear infinite;width:max-content}}@keyframes tk{{to{{transform:translateX(-50%)}}}}
@media (prefers-reduced-motion:reduce){{.ticker ul{{animation:none;flex-wrap:wrap;white-space:normal;width:auto}}html{{scroll-behavior:auto}}}}
main{{max-width:var(--mw);margin:0 auto;padding:0 clamp(1rem,4vw,2.5rem)}}
.sec{{padding:clamp(3rem,7vw,5.5rem) 0 0}}.sh{{display:flex;align-items:center;gap:.9rem;margin-bottom:2rem}}
.bar{{width:5px;height:1.3rem;background:var(--r)}}.bar.c{{background:var(--c)}}.bar.g{{background:var(--g)}}.bar.bz{{background:var(--bz)}}
.lab{{font:700 .8rem var(--fm);letter-spacing:.2em;text-transform:uppercase;color:var(--c)}}.rule{{flex:1;height:1px;background:var(--bd)}}.num{{font:400 .75rem var(--fm);color:var(--dm)}}
.prose{{max-width:68ch}}.prose p{{margin:0 0 1.15em}}.prose.narrow{{max-width:64ch}}.prose.cols{{max-width:none}}
@media (min-width:900px){{.prose.cols{{columns:2;column-gap:3rem}}.prose.cols p{{break-inside:avoid-column}}}}
.edwrap{{display:grid;grid-template-columns:minmax(120px,220px) 1fr;gap:2rem;align-items:start}}.bignum{{font:900 clamp(4rem,12vw,8rem)/1 var(--fd);color:var(--r)}}
.sign{{font:700 .75rem var(--fm);letter-spacing:.18em;text-transform:uppercase;color:var(--r)}}
.hl{{font-family:var(--fd);font-weight:900;font-size:clamp(1.8rem,4.2vw,3rem);line-height:1.1;margin:.4rem 0 .8rem;text-wrap:balance}}.dek{{font-size:1.2rem;color:#d3d3e6;max-width:62ch;margin-bottom:1.6rem}}
.tag{{display:inline-block;font:700 .7rem var(--fm);letter-spacing:.16em;text-transform:uppercase;color:var(--g)}}
.ph{{margin:0 0 1.6rem}}.ph img{{width:100%;border-radius:4px;background:var(--lft)}}.ph.wide img{{aspect-ratio:16/9;object-fit:cover;object-position:50% 25%}}.ph.tall img{{aspect-ratio:4/5;object-fit:cover}}
figcaption{{display:flex;flex-direction:column;gap:.15rem;margin-top:.5rem;font-size:.82rem;color:var(--dm);line-height:1.45}}.credit{{font-family:var(--fm);font-size:.68rem;letter-spacing:.04em;color:#8b8ba8}}
.pull{{margin:2rem 0;padding:1.4rem 0 1.4rem 1.6rem;border-left:4px solid var(--r)}}.pull blockquote{{font:italic 700 clamp(1.4rem,3vw,2rem)/1.3 var(--fd)}}.pull cite{{display:block;margin-top:.6rem;font:400 .75rem var(--fm);letter-spacing:.08em;color:var(--dm);font-style:normal}}
.gallery{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.9rem;margin:2rem 0}}.gallery.three{{grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}}.tile img{{width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:4px}}.gallery.three .tile img{{aspect-ratio:16/9}}
.cards{{display:grid;gap:1.4rem}}.cards.two{{grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}}.cards.three{{grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}}
.card{{background:var(--sur);border:1px solid var(--bd);border-radius:6px;padding:1.5rem}}.card h3{{font:700 1.35rem/1.25 var(--fd);margin:.4rem 0 .8rem}}.card p{{margin:0 0 1em;color:#d6d6e6}}.card .ph{{margin:.5rem 0 1rem}}
.specs{{list-style:none;display:flex;flex-wrap:wrap;gap:.4rem;margin:.5rem 0 1rem}}.specs li{{font:400 .72rem var(--fm);border:1px solid var(--bd);padding:.2rem .5rem;border-radius:3px;color:var(--dm)}}
.spgrid{{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:2.4rem;align-items:start}}@media (max-width:600px){{.mast nav span:first-child{{display:none}}}}
@media (max-width:820px){{.spgrid{{grid-template-columns:1fr}}.edwrap{{grid-template-columns:1fr}}}}
.facts{{list-style:none;display:flex;flex-wrap:wrap;gap:2rem;margin:1.6rem 0}}.facts li{{display:flex;flex-direction:column}}.facts b{{font:900 1.8rem var(--fd);color:var(--bz)}}.facts span{{font:400 .7rem var(--fm);letter-spacing:.1em;text-transform:uppercase;color:var(--dm)}}
.btn{{display:inline-block;background:var(--c);color:#04141a;font:700 .8rem var(--fm);letter-spacing:.12em;text-transform:uppercase;padding:.85rem 1.3rem;border-radius:3px;text-decoration:none}}.btn:hover{{background:#fff;color:#000}}
.src{{margin-top:1.4rem;font-size:.85rem;color:var(--dm)}}.src summary{{cursor:pointer;font:700 .7rem var(--fm);letter-spacing:.14em;text-transform:uppercase}}.src ul{{margin:.6rem 0 0 1.1rem}}
.nl,.corr{{background:var(--sur);border:1px solid var(--bd);border-radius:8px;padding:clamp(1.4rem,4vw,2.6rem)}}.nl h3{{font:900 clamp(1.6rem,4vw,2.4rem) var(--fd);margin:.4rem 0 .6rem}}.nl p{{max-width:56ch;margin-bottom:1.2rem;color:#d6d6e6}}.corr li{{margin:0 0 .8em 1.1rem}}
.note{{margin-top:1.2rem;color:var(--dm);font-size:.9rem;max-width:70ch}}
footer{{margin-top:5rem;border-top:1px solid var(--bd);padding:2.5rem clamp(1rem,4vw,2.5rem);text-align:center;color:var(--dm);font-size:.85rem}}footer svg{{height:36px;width:auto;margin-bottom:.8rem}}footer nav{{display:flex;justify-content:center;gap:1.4rem;margin:.8rem 0}}
.prog{{position:fixed;top:0;left:0;height:3px;width:0;background:linear-gradient(90deg,var(--r),var(--c),var(--g));z-index:60}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="prog" id="prog"></div>
{logo}
<header class="mast"><a href="/" aria-label="Drummers and Dreamers Magazine home"><svg viewBox="0 0 480 160" role="img" aria-label="Drummers and Dreamers"><use href="#djd-logo-src"/></svg></a>
<nav><span>Vol. 1 · {month}</span><span class="issue">Issue</span><button class="toc-btn" id="tocbtn" aria-expanded="false" aria-controls="toc">Contents</button></nav></header>
<div class="toc" id="toc"><ol>{toc}</ol></div>
<div class="hero-wrap">{hero}<div class="hero-in"><div class="kick">{kicker}</div><h1>{headline}</h1><p class="dek">{dek}</p></div></div>
{herocap}
<div class="ticker" aria-label="Headlines"><ul>{ticker}{ticker}</ul></div>
<main id="main">
{body}
</main>
<footer><svg viewBox="0 0 480 160" role="img" aria-label="Drummers and Dreamers"><use href="#djd-logo-src"/></svg><div>Dream Loud · Est. 2026</div>
<nav><a href="https://drummerjawkneed.com" target="_blank" rel="noopener">Website</a><a href="https://twitch.tv/drummerjawkneed" target="_blank" rel="noopener">Twitch</a><a href="https://kick.com/drummerjawkneed" target="_blank" rel="noopener">Kick</a><a href="https://youtube.com/@drummerjawkneed" target="_blank" rel="noopener">YouTube</a></nav>
<div>Published by Drummers &amp; Dreamers, Inc. Editor: DrummerJawkneeD. Every story lists its sources; every photo is credited to its photographer with a licence link. Spot a mistake? Tell us and we will print a correction.</div><div>© {year} Drummers &amp; Dreamers, Inc. Updated {updated}.</div></footer>
<script>
(function(){{var b=document.getElementById('tocbtn'),t=document.getElementById('toc');b.addEventListener('click',function(){{var o=t.classList.toggle('open');b.setAttribute('aria-expanded',o)}});
t.addEventListener('click',function(e){{if(e.target.tagName==='A')t.classList.remove('open')}});
addEventListener('scroll',function(){{var s=document.documentElement;document.getElementById('prog').style.width=(s.scrollTop/(s.scrollHeight-s.clientHeight)*100)+'%'}},{{passive:true}})}})();
</script>
</body></html>
"""

if __name__ == "__main__":
    build(sys.argv[1])
