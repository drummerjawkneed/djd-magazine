#!/usr/bin/env python3
"""One-off script that builds september-2026/image-manifest.json using the REAL search results
already gathered (via live web search) while researching and writing this issue — not mocked
empty data. This is NOT part of the reusable image_pipeline module; it's how this specific
issue's manifest was produced, kept for transparency/reproducibility. Future issues call
image_pipeline.source_image() directly from the n8n pipeline with a real, live SearchProvider
instead of this static one.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import image_pipeline as ip

# Real results captured from live web search during this issue's research pass (see this PR's
# description for the actual search queries and full result sets this was drawn from).
REAL_RESULTS = {
    "Rush EPK": [],  # searched — no clean official EPK/media-photo page found on rush.com
    "Rush press kit photos": [
        {"url": "https://www.rush.com/band/", "title": "Band — Rush.com", "snippet": "Official band page"},
    ],
    "Neil Peart Wikimedia Commons public domain photo": [
        {"url": "https://commons.wikimedia.org/wiki/Category:Neil_Peart", "title": "Category:Neil Peart - Wikimedia Commons", "snippet": "2008 photo by Matt Becker, CC-licensed"},
    ],
    "Rohema Nick Petrella official product page": [
        {"url": "https://www.rohema.de/en/products/drumsticks/signature/", "title": "Signature drumsticks — Rohema", "snippet": "Official signature line page"},
    ],
    "Spaun Drums 40-ply maple snare official product page": [
        {"url": "https://spaundrums.com/collections/multi-ply", "title": "Multi Ply — SPAUN", "snippet": "Official multi-ply snare collection"},
    ],
    "Code Drum Heads official product page": [],  # no official product-page image located this pass
}


class StaticSearchProvider:
    def search(self, query: str) -> list[dict]:
        return REAL_RESULTS.get(query, [])


def main() -> None:
    search = StaticSearchProvider()
    results: dict[str, ip.ImageSourceResult] = {}

    # Cover Story + Drummer Spotlight both use the Rush/Peart subject.
    r = ip.source_artist_image("Rush", search, member_names=["Geddy Lee", "Alex Lifeson", "Anika Nilles", "Loren Gold"])
    # source_artist_image's own domain-matching heuristic counts rush.com/band/ as a hit (it IS
    # the artist's own official domain), but a bio page is not the same confidence level as a
    # dedicated EPK/press-photo asset -- and this environment couldn't fetch the page itself to
    # check whether it actually links a usable press photo (rush.com wasn't test-fetched here;
    # commons.wikimedia.org, twitch.tv, and youtube.com were all confirmed blocked by this
    # sandbox's egress proxy, so the same is assumed unverified for rush.com rather than tested
    # optimistically). Overriding the auto-classification to reflect that honestly, rather than
    # letting a same-domain heuristic match read as a confirmed sourced photo:
    r.is_fallback = True
    r.source_kind = "unverified-candidate"
    r.credit = ""
    r.alt_text = "Rush — candidate official page found, not confirmed as a usable press photo"
    r.notes = (
        "Real search found rush.com/band/ (the artist's own official domain, so the "
        "official-domain heuristic matched) but it's a bio page, not confirmed to contain a "
        "dedicated, downloadable EPK/press photo -- this run had no way to fetch the page and "
        "check. Recorded as an unverified candidate, not a sourced photo: a human (or a future "
        "run with real network access) should open rush.com/band/ directly, confirm whether it "
        "links usable press photos, and update this slot before treating it as approved."
    )
    results["cover_rush_band"] = r

    peart = ip.source_artist_image("Neil Peart", search)
    peart.notes = (
        "Real search confirmed a genuine candidate: a 2008 photo of Neil Peart by Matt Becker, "
        "CC-licensed, in Wikimedia Commons' Category:Neil_Peart. This module could not fetch "
        "commons.wikimedia.org directly from this sandbox to pull the exact file URL/license "
        "text (confirmed blocked by the egress proxy, not merely unattempted) -- so the exact "
        "file was NOT verified closely enough to hotlink safely. Recorded here as a found-but-"
        "unverified fallback candidate for a human (or a future run with real network access) "
        "to confirm and drop in; this issue ships with an original editorial illustration "
        "instead, captioned as such, rather than guessing at an unverified Commons file URL."
    )
    results["cover_and_spotlight_peart"] = peart

    results["gear_rohema"] = ip.source_gear_image("Rohema", "Nick Petrella signature drumsticks", search)
    results["gear_spaun"] = ip.source_gear_image("Spaun Drums", "40-ply maple snare", search)
    results["gear_code_drum_heads"] = ip.source_gear_image("Code Drum Heads", "UK distribution announcement", search)
    results["gear_zildjian_greiner"] = ip.source_gear_image("Zildjian", "Matt Greiner Blast Bell", search)

    for name, platform, url in [
        ("Sina Drums", "twitch", "https://twitch.tv/sina-drums"),
        ("Mitch Bruzzese", "twitch", "https://www.twitch.tv/mitchbruzzese"),
        ("OfficeDrummer", "kick", "https://www.kick.com/OfficeDrummer"),
        ("Danger Drums", "twitch", "https://www.twitch.tv/dangerdrums"),
    ]:
        results[f"streamer_{name.lower().replace(' ', '_')}"] = ip.source_streamer_image(
            name, platform, url, platform_client=None
        )

    results["djd_spotlight_self"] = ip.source_self_image("DJD Spotlight September 2026")

    out = ip.build_issue_manifest("september-2026", results)
    print(f"Wrote {out}")
    print(f"Fallback/unavailable slots: {sum(1 for r in results.values() if r.is_fallback)} of {len(results)}")


if __name__ == "__main__":
    main()
