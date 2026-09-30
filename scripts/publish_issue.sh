#!/bin/bash
# publish_issue.sh <slug>  -- merge the reviewed issue branch, mirror to /latest, update banner.json, push, verify live.
# Used after the n8n monthly run fires (that workflow only drafts to draft/next-issue now).
set -euo pipefail
SLUG=${1:?slug e.g. october-2026}; REPO=$HOME/repos/djd-magazine; cd "$REPO"
NTFY_CFG=$HOME/.config/ntfy-djd-alerts.env
notify(){ [[ -f "$NTFY_CFG" ]] && . "$NTFY_CFG"; curl -s -u "djd:${NTFY_DJD_PASSWORD:-}" -H "Title: $1" -d "$2" https://ntfy.drummerjawkneed.com/djd-alerts >/dev/null 2>&1 || true; }
git fetch -q origin; git checkout -q main; git pull -q --ff-only
if ! git merge --no-ff -q "origin/issue/$SLUG" -m "Publish $SLUG" 2>/dev/null; then git merge --abort 2>/dev/null || true; notify "Magazine publish FAILED" "merge of issue/$SLUG conflicted; needs a human/Claude"; exit 1; fi
cp "$SLUG/index.html" latest/index.html
python3 - "$SLUG" <<'PY'
import json,sys
slug=sys.argv[1]; c=json.load(open(f"{slug}/content.json",encoding="utf-8"))
json.dump({"month":c["month"],"headline":c["headline_short"],"summary":c["summary"],"link":f"https://magazine.drummerjawkneed.com/{slug}","updated":c["date_published"].replace("Z",".000Z")},open("banner.json","w",encoding="utf-8"),indent=2,ensure_ascii=False)
PY
git add -A
git commit -q -m "Publish $SLUG: mirror to /latest, update banner.json" || true
git push -q origin main
sleep 120
code=$(curl -s -o /tmp/pub.html -w "%{http_code}" "https://magazine.drummerjawkneed.com/$SLUG/" || echo 000)
if [[ "$code" == "200" ]] && grep -q "Drummers" /tmp/pub.html; then notify "Magazine $SLUG is LIVE" "https://magazine.drummerjawkneed.com/$SLUG/ (HTTP 200)"; else notify "Magazine $SLUG not live yet" "HTTP $code after push; check Cloudflare Pages deploy"; fi
