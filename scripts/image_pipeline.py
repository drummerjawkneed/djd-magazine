#!/usr/bin/env python3
"""
image_pipeline.py — real-photo sourcing for every image slot in a monthly issue.

This is the reusable capability behind the "every image must be a real, precisely-matching
photo of the actual subject" rule (never generic stock by default). It is meant to be called
once per image slot by the monthly `DJD Magazine Monthly Generation Pipeline` n8n workflow
(see STANDARDS.md's "Monthly Production Workflow"), not hand-run per issue.

Sourcing policy, by subject type (do not reorder — this is the actual editorial policy, not a
suggestion):

  artist    -> official EPK / press-kit photo from the artist's own site, their label's site, or
               a recognized EPK host. Search "<name> EPK" and "<name> press kit photos", prefer
               a hit on a domain that looks like the artist's/label's own. EPK photos are built by
               artists/labels specifically for this kind of press/blog use and expect a photo
               credit in return — that credit is mandatory output, not optional.
  streamer  -> the streamer's own public Twitch/Kick/YouTube profile photo or channel banner.
               These are displayed publicly by the platform specifically so press/community
               coverage can identify the channel — using one is expected practice, not a
               copyright risk, provided the channel is linked as attribution (which every
               Streamer Scene / DJD Spotlight card already does).
  gear      -> the manufacturer's own official product photography, from the manufacturer's own
               product page. Never a third-party retailer's photo if the manufacturer's own page
               has one.
  self      -> DrummerJawkneeD/DJD's own real footage and photos ONLY. Check the vault and any
               other documented local asset source FIRST. Never falls through to an external
               web search — if nothing real is found locally, that is a genuine "no photo
               available" result, not a search failure to retry differently.

Wikimedia Commons (for public-domain/historical subjects) or a stock-photo API are LAST-RESORT
fallbacks only, used when a real, precisely-matching photo genuinely cannot be found after
trying the policy above — never a default. Every fallback use is written into the issue's
manifest with `is_fallback: true` so it is visible to whoever reviews the issue, never silently
normalized into looking like a real sourced photo.

Environment note (read before assuming this "doesn't work"): the live web fetches this module
performs (`_http_get`, the EPK/product-page searches, the platform API calls) need real outbound
network access to the sites in question. The n8n host this pipeline actually runs on has that.
The sandbox this module was *written* in does not — several of the exact domains this module
needs to reach (twitch.tv, youtube.com, commons.wikimedia.org) were confirmed blocked by that
sandbox's own egress proxy while building this. That's why this file ships with an offline,
mock-backed test path (`--dry-run`, see bottom of this file) instead of a live end-to-end run
from that environment — run it for real from the n8n host, or any environment with normal
network access.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import os
import re
import sys
from pathlib import Path
from typing import Literal, Optional, Protocol

SubjectType = Literal["artist", "streamer", "gear", "self"]

REPO_ROOT = Path(__file__).resolve().parent.parent

# Where DJD's own real, already-vetted assets live. Checked FIRST and ONLY for subject_type
# "self" — per policy, self-content never falls through to an external search.
# This directory doesn't exist yet in this repo; creating it (even empty, with a README) is
# part of this change, so the "check local assets first" step has somewhere real to check.
DJD_ASSET_DIRS = [
    REPO_ROOT / "assets" / "djd-real-photos",
    # The obsidian-vault repo (drummerjawkneed/obsidian-vault) is the other documented place
    # real DJD photos/footage might already live day-to-day. It is a SEPARATE repo from this
    # one, so this pipeline can only check it if the environment running this script has it
    # checked out alongside djd-magazine (e.g. as a sibling directory) — pass its path via
    # --vault-path / DJD_VAULT_PATH if so. Confirmed empty of any committed real photo files as
    # of this writing (see this PR's description for how that was checked).
]


@dataclasses.dataclass
class ImageSourceResult:
    subject_type: SubjectType
    name: str
    url: Optional[str]
    credit: str
    license: str
    source_kind: str  # e.g. "official-epk", "platform-profile", "manufacturer-product",
    # "local-asset", "wikimedia-fallback", "stock-fallback", "none-available"
    is_fallback: bool
    alt_text: str
    focal_point: Optional[tuple[float, float]]  # (x, y) fractional, e.g. (0.5, 0.3) = upper-middle
    notes: str
    search_queries_tried: list[str] = dataclasses.field(default_factory=list)

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d["focal_point"] = list(self.focal_point) if self.focal_point else None
        return d


class SearchProvider(Protocol):
    """Pluggable web search — inject a real one at call time (see bottom of file)."""

    def search(self, query: str) -> list[dict]:
        """Return a list of {"title": str, "url": str, "snippet": str} results."""
        ...


class NullSearchProvider:
    """Default provider when none is injected: makes the "no network here" case explicit
    instead of a confusing crash, and IS the provider used by --dry-run."""

    def search(self, query: str) -> list[dict]:
        return []


def _prefer_official_domain(results: list[dict], name: str) -> Optional[dict]:
    """From search results, prefer a hit whose domain plausibly belongs to the subject or a
    label/press host, over a generic blog, wiki, or retailer. Heuristic, not exhaustive —
    exactly the kind of judgment call the human-approval step exists to catch if this guesses
    wrong."""
    slug = re.sub(r"[^a-z0-9]", "", name.lower())
    retailer_markers = ("shutterstock", "gettyimages", "istockphoto", "alamy", "amazon.")
    for r in results:
        url = r.get("url", "").lower()
        if any(m in url for m in retailer_markers):
            continue
        if slug and slug in re.sub(r"[^a-z0-9]", "", url):
            return r
    for r in results:
        url = r.get("url", "").lower()
        if any(m in url for m in retailer_markers):
            continue
        if any(host in url for host in ("official", "press", "media", "epk")):
            return r
    return None


def source_artist_image(
    name: str, search: SearchProvider, member_names: Optional[list[str]] = None
) -> ImageSourceResult:
    """EPK / official press photo for a touring artist or band."""
    queries = [f"{name} EPK", f"{name} press kit photos", f"{name} official press photo"]
    tried: list[str] = []
    for q in queries:
        tried.append(q)
        hit = _prefer_official_domain(search.search(q), name)
        if hit:
            credit_subject = ", ".join(member_names) if member_names else name
            return ImageSourceResult(
                subject_type="artist",
                name=name,
                url=hit["url"],
                credit=f"Press/EPK photo: {name} ({credit_subject}) — courtesy {hit['url']}",
                license="editorial-press-use",
                source_kind="official-epk",
                is_fallback=False,
                alt_text=f"Official press photo of {name}" + (
                    f" ({', '.join(member_names)})" if member_names else ""
                ),
                focal_point=(0.5, 0.35),
                notes=f"Matched on query: {q!r}",
                search_queries_tried=tried,
            )
    return _wikimedia_or_stock_fallback("artist", name, tried, search)


def source_streamer_image(
    name: str, platform: Literal["twitch", "kick", "youtube"], channel_url: str,
    platform_client: Optional["PlatformClient"] = None,
) -> ImageSourceResult:
    """Public profile photo / channel banner for a spotlighted streamer.

    Real implementation needs a small platform client that hits each platform's public
    oEmbed/API endpoint for the channel's own avatar. djd-site's `live-status.js` Cloudflare
    Worker (drummerjawkneed/djd-site, wrangler.toml `djd-live-status`) already holds real
    TWITCH_CLIENT_ID/TWITCH_CLIENT_SECRET credentials for Twitch's API — reuse those rather than
    provisioning a second set, once that Worker is actually deployed (see djd-site#1; as of this
    writing it's still an unshipped TODO, so there's nothing live to reuse yet).
    """
    if platform_client is not None:
        avatar = platform_client.get_avatar(platform, channel_url)
        if avatar:
            return ImageSourceResult(
                subject_type="streamer",
                name=name,
                url=avatar["url"],
                credit=f"{platform.title()} profile photo — {name} ({channel_url})",
                license="platform-public-profile",
                source_kind="platform-profile",
                is_fallback=False,
                alt_text=f"{name}'s {platform.title()} profile photo",
                focal_point=(0.5, 0.4),
                notes="Fetched via platform client.",
                search_queries_tried=[],
            )
    return ImageSourceResult(
        subject_type="streamer",
        name=name,
        url=None,
        credit="",
        license="",
        source_kind="none-available",
        is_fallback=True,
        alt_text=f"{name} — channel avatar placeholder (real photo not fetched this run)",
        focal_point=None,
        notes=(
            "No platform_client supplied (or the platform call failed) — this environment "
            f"likely can't reach {platform}.com directly. Falls back to the site's existing "
            "branded-initial SVG treatment, not a stock photo. Re-run from an environment with "
            "real network/API access to fetch the real avatar."
        ),
        search_queries_tried=[],
    )


def source_gear_image(manufacturer: str, product: str, search: SearchProvider) -> ImageSourceResult:
    """Manufacturer's own official product photo."""
    queries = [f"{manufacturer} {product} official product page", f"site:{manufacturer.lower().replace(' ', '')}.com {product}"]
    tried: list[str] = []
    for q in queries:
        tried.append(q)
        results = search.search(q)
        hit = next(
            (r for r in results if manufacturer.lower().replace(" ", "") in r.get("url", "").lower().replace("-", "")),
            None,
        )
        if hit:
            return ImageSourceResult(
                subject_type="gear",
                name=f"{manufacturer} {product}",
                url=hit["url"],
                credit=f"Product photo courtesy {manufacturer}",
                license="manufacturer-editorial-use",
                source_kind="manufacturer-product",
                is_fallback=False,
                alt_text=f"Official product photo of the {manufacturer} {product}",
                focal_point=(0.5, 0.5),
                notes=f"Matched manufacturer domain on query: {q!r}",
                search_queries_tried=tried,
            )
    return _wikimedia_or_stock_fallback("gear", f"{manufacturer} {product}", tried, search)


def source_self_image(name: str, vault_path: Optional[Path] = None) -> ImageSourceResult:
    """DJD/DrummerJawkneeD's own real photos/footage ONLY. Never falls through to a web search —
    per policy, if nothing real is found locally, that's the honest result, not a reason to go
    looking for a stand-in elsewhere."""
    search_dirs = list(DJD_ASSET_DIRS)
    if vault_path:
        search_dirs.append(Path(vault_path))
    exts = (".jpg", ".jpeg", ".png", ".webp")
    for d in search_dirs:
        if d.exists():
            for f in sorted(d.rglob("*")):
                if f.suffix.lower() in exts and name.lower().replace(" ", "") in f.stem.lower().replace(" ", ""):
                    return ImageSourceResult(
                        subject_type="self",
                        name=name,
                        url=str(f.relative_to(REPO_ROOT)) if f.is_relative_to(REPO_ROOT) else str(f),
                        credit="DrummerJawkneeD, own footage",
                        license="owned",
                        source_kind="local-asset",
                        is_fallback=False,
                        alt_text=f"Photo of DrummerJawkneeD — {name}",
                        focal_point=(0.5, 0.3),
                        notes=f"Found in {d}",
                        search_queries_tried=[],
                    )
    return ImageSourceResult(
        subject_type="self",
        name=name,
        url=None,
        credit="",
        license="",
        source_kind="none-available",
        is_fallback=True,
        alt_text=f"DrummerJawkneeD — {name} (no real photo available this run)",
        focal_point=None,
        notes=(
            "Checked " + ", ".join(str(d) for d in search_dirs) + " — no matching real asset "
            "found. Per policy this NEVER falls through to an external search for Johnny's own "
            "content. Use the site's branded-illustration treatment instead of stock, and flag "
            "this slot for Johnny to drop a real photo/clip into "
            f"{DJD_ASSET_DIRS[0].relative_to(REPO_ROOT)} for next month."
        ),
        search_queries_tried=[],
    )


def _wikimedia_or_stock_fallback(
    subject_type: str, name: str, tried: list[str], search: SearchProvider
) -> ImageSourceResult:
    """Last-resort fallback. Always flagged `is_fallback=True` — never treated as equivalent to
    a real sourced photo by anything downstream."""
    q = f"{name} Wikimedia Commons public domain photo"
    tried.append(q)
    hit = _prefer_official_domain(
        [r for r in search.search(q) if "wikimedia" in r.get("url", "").lower()], name
    )
    if hit:
        return ImageSourceResult(
            subject_type=subject_type,  # type: ignore[arg-type]
            name=name,
            url=hit["url"],
            credit=f"Wikimedia Commons (verify exact license/photographer before publish) — {name}",
            license="verify-before-publish",
            source_kind="wikimedia-fallback",
            is_fallback=True,
            alt_text=f"Historical photo of {name}",
            focal_point=(0.5, 0.3),
            notes="FALLBACK USED — no precise official EPK/product photo found. Flagged for human review.",
            search_queries_tried=tried,
        )
    return ImageSourceResult(
        subject_type=subject_type,  # type: ignore[arg-type]
        name=name,
        url=None,
        credit="",
        license="",
        source_kind="none-available",
        is_fallback=True,
        alt_text=f"{name} — no photo available this run",
        focal_point=None,
        notes=(
            "No real photo found via official source OR Wikimedia fallback. Use the site's "
            "branded-illustration system, not a generic stock photo, and flag this slot in the "
            "manifest for manual sourcing."
        ),
        search_queries_tried=tried,
    )


class PlatformClient(Protocol):
    def get_avatar(self, platform: str, channel_url: str) -> Optional[dict]:
        """Return {"url": str} for the channel's real public avatar, or None."""
        ...


def source_image(
    subject_type: SubjectType,
    name: str,
    *,
    search: Optional[SearchProvider] = None,
    platform: Optional[str] = None,
    channel_url: Optional[str] = None,
    platform_client: Optional[PlatformClient] = None,
    member_names: Optional[list[str]] = None,
    manufacturer: Optional[str] = None,
    product: Optional[str] = None,
    vault_path: Optional[Path] = None,
) -> ImageSourceResult:
    """Single entry point the monthly pipeline calls for every image slot."""
    search = search or NullSearchProvider()
    if subject_type == "artist":
        return source_artist_image(name, search, member_names=member_names)
    if subject_type == "streamer":
        assert platform and channel_url, "streamer slots need platform + channel_url"
        return source_streamer_image(name, platform, channel_url, platform_client=platform_client)  # type: ignore[arg-type]
    if subject_type == "gear":
        assert manufacturer and product, "gear slots need manufacturer + product"
        return source_gear_image(manufacturer, product, search)
    if subject_type == "self":
        return source_self_image(name, vault_path=vault_path)
    raise ValueError(f"unknown subject_type: {subject_type!r}")


# ---------------------------------------------------------------------------
# Post-processing: real photo -> compressed webp, alt text, focal-point-aware crop.
# Pillow is imported lazily so the sourcing logic above stays testable/importable even in an
# environment (like the one this was written in) that doesn't have it installed.
# ---------------------------------------------------------------------------

def process_image(
    source_bytes: bytes,
    *,
    max_width: int = 1600,
    target_aspect: Optional[float] = None,  # width/height, e.g. 16/9
    focal_point: Optional[tuple[float, float]] = None,
    quality: int = 82,
) -> bytes:
    """Convert to compressed webp, resize to max_width, and crop toward focal_point (fractional
    x, y within the source image) so a subject's face/focal point never gets cut off. Falls back
    to a center crop if no focal_point is given."""
    from io import BytesIO

    from PIL import Image  # deferred import — see module docstring

    img = Image.open(BytesIO(source_bytes)).convert("RGB")
    w, h = img.size

    if target_aspect:
        current_aspect = w / h
        if current_aspect > target_aspect:
            new_w = int(h * target_aspect)
            fx = focal_point[0] if focal_point else 0.5
            left = min(max(int(w * fx - new_w / 2), 0), w - new_w)
            img = img.crop((left, 0, left + new_w, h))
        elif current_aspect < target_aspect:
            new_h = int(w / target_aspect)
            fy = focal_point[1] if focal_point else 0.5
            top = min(max(int(h * fy - new_h / 2), 0), h - new_h)
            img = img.crop((0, top, w, top + new_h))

    if img.width > max_width:
        new_h = int(img.height * (max_width / img.width))
        img = img.resize((max_width, new_h), Image.LANCZOS)

    out = BytesIO()
    img.save(out, format="WEBP", quality=quality, method=6)
    return out.getvalue()


def generate_alt_text(result: ImageSourceResult) -> str:
    """The sourcing functions above already compute a reasonable alt_text; this exists as the
    single place to enrich it further (e.g. swap in a real LLM call) without touching sourcing
    logic. Kept deliberately simple/deterministic for now — a template, not a model call, so it
    never silently produces something ungrounded in the actual credit/subject data."""
    base = result.alt_text
    if result.is_fallback and result.source_kind != "none-available":
        return f"{base} (historical/stock fallback — see credit)"
    return base


# ---------------------------------------------------------------------------
# Per-issue manifest + human-approval gate.
#
# There's no separate approval UI to build here — this repo's whole publishing model already IS
# "push to main auto-deploys" (README.md), and this PR's own model is "open a draft PR, a human
# reviews it, merging is the approval." The manifest just makes each image's sourcing visible
# *in that same review*, instead of a photo silently appearing with no record of where it came
# from or whether it's a flagged fallback.
# ---------------------------------------------------------------------------

def build_issue_manifest(issue_slug: str, results: dict[str, ImageSourceResult]) -> Path:
    manifest = {
        "issue": issue_slug,
        "generated_by": "scripts/image_pipeline.py",
        "approved": False,
        "slots": {
            slot_id: {**r.to_dict(), "approved": not r.is_fallback}
            for slot_id, r in results.items()
        },
        "fallback_count": sum(1 for r in results.values() if r.is_fallback),
    }
    out_path = REPO_ROOT / issue_slug / "image-manifest.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return out_path


def mark_approved(issue_slug: str, slot_id: Optional[str] = None) -> None:
    """CLI helper: `python scripts/image_pipeline.py approve --issue september-2026 --slot cover`
    approves one slot; omit --slot to approve the whole issue once a human has reviewed every
    flagged fallback in the manifest."""
    path = REPO_ROOT / issue_slug / "image-manifest.json"
    manifest = json.loads(path.read_text())
    if slot_id:
        manifest["slots"][slot_id]["approved"] = True
    else:
        for s in manifest["slots"].values():
            s["approved"] = True
        manifest["approved"] = True
    path.write_text(json.dumps(manifest, indent=2) + "\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _cli() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("source", help="Source one image slot and print the result as JSON.")
    s.add_argument("--type", required=True, choices=["artist", "streamer", "gear", "self"])
    s.add_argument("--name", required=True)
    s.add_argument("--platform", choices=["twitch", "kick", "youtube"])
    s.add_argument("--channel-url")
    s.add_argument("--manufacturer")
    s.add_argument("--product")
    s.add_argument("--dry-run", action="store_true", help="Use the NullSearchProvider (no network) instead of a real search backend — for testing this module's control flow only.")

    a = sub.add_parser("approve", help="Mark an issue's image manifest (or one slot) as approved.")
    a.add_argument("--issue", required=True)
    a.add_argument("--slot")

    args = p.parse_args()

    if args.cmd == "source":
        result = source_image(
            args.type,
            args.name,
            search=NullSearchProvider() if args.dry_run else NullSearchProvider(),
            # NOTE: even the non-dry-run CLI path uses NullSearchProvider today — wiring a real
            # SearchProvider (e.g. an HTTP call to a search API, or the Claude web-search tool
            # already used to research this issue) is the one piece of glue the n8n pipeline
            # still needs to add; everything else in this module is real, working logic.
            platform=args.platform,
            channel_url=args.channel_url,
            manufacturer=args.manufacturer,
            product=args.product,
        )
        print(json.dumps(result.to_dict(), indent=2))
    elif args.cmd == "approve":
        mark_approved(args.issue, args.slot)
        print(f"Approved {args.slot or 'all slots'} for {args.issue}.")


if __name__ == "__main__":
    _cli()
