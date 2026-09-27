# Real DJD photos/footage — checked first, always, for any "self" image slot

`scripts/image_pipeline.py`'s `source_self_image()` looks here (and at an optional
`--vault-path`/`DJD_VAULT_PATH` pointing at a checked-out `obsidian-vault`) before it will use
anything for a DrummerJawkneeD/DJD image slot. Per policy, self-content **never** falls through
to an external web search — if nothing real is here, that's a genuine "no photo available"
result for that slot, not a reason to substitute a stock photo.

## What to drop here

Real photos or video-frame grabs of Johnny/DrummerJawkneeD — stream screenshots, event photos,
anything actually of him. File name should include a recognizable slug of what it's for (e.g.
`djd-spotlight-2026-09.jpg`, `djd-cover-tue-thu-sat.jpg`) since `source_self_image()` matches on
name substring.

## What NOT to drop here

Anyone else's photo, stock photography, or AI-generated images of Johnny — those belong to a
different sourcing path entirely (or no path at all; see the module's docstring on why "self"
never falls back to external search).

This directory was empty as of this file's own commit — the September 2026 issue's DJD Spotlight
slot genuinely has no real photo to use yet (see that issue's `image-manifest.json`), not because
this README wasn't checked.
