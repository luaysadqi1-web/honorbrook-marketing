#!/usr/bin/env bash
# Ping IndexNow (Bing, Yandex, Naver, Seznam) so new/updated pages get crawled fast.
#
#   ./scripts/indexnow.sh                        # submit every URL in sitemap.xml
#   ./scripts/indexnow.sh /term-life-insurance   # submit specific path(s)
#   ./scripts/indexnow.sh /blog/my-post /blog/   # new post + the index page
#
# When given specific paths it waits (up to ~45s) for each to return 200 before
# submitting, so it is safe to run right after `git push` while Netlify builds.
#
# Google does NOT participate in IndexNow — this reaches Bing, Yandex, Naver and
# Seznam. For Google, rely on sitemap.xml plus Search Console "Request indexing".
#
# The key file must already be live at:
#   https://honorbrook-insurance.com/fe552356957a40beab701665b4d886a9.txt
set -euo pipefail

HOST="honorbrook-insurance.com"
KEY="fe552356957a40beab701665b4d886a9"
KEY_LOCATION="https://${HOST}/${KEY}.txt"
ENDPOINT="https://api.indexnow.org/indexnow"

# Refuse to run if the key file isn't live — IndexNow rejects the batch otherwise.
if [ "$(curl -s -o /dev/null -w '%{http_code}' "$KEY_LOCATION")" != "200" ]; then
  echo "ERROR: key file not reachable at $KEY_LOCATION"
  echo "Deploy the site first, then re-run."
  exit 1
fi

if [ "$#" -gt 0 ]; then
  urls=()
  for p in "$@"; do
    case "$p" in
      https://*) urls+=("$p") ;;
      /*)        urls+=("https://${HOST}${p}") ;;
      *)         urls+=("https://${HOST}/${p}") ;;
    esac
  done
else
  # bash 3.2 (macOS default) has no mapfile, so read the list the portable way.
  urls=()
  while IFS= read -r line; do
    [ -n "$line" ] && urls+=("$line")
  done < <(curl -s "https://${HOST}/sitemap.xml" \
    | grep -oE '<loc>[^<]*</loc>' | sed 's|<loc>||; s|</loc>||')
fi

if [ "${#urls[@]}" -eq 0 ]; then
  echo "No URLs to submit."; exit 1
fi

# When specific URLs are passed (the automated-publish case), make sure each one
# is actually live before telling Bing about it. A deploy takes a few seconds, so
# a routine that pushes and immediately pings would otherwise submit a 404.
# Bulk sitemap runs skip this — those URLs are already published by definition.
if [ "$#" -gt 0 ]; then
  live=()
  for u in "${urls[@]}"; do
    ok=""
    for attempt in 1 2 3 4 5 6 7 8 9 10; do
      if [ "$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 "$u")" = "200" ]; then
        ok="yes"; break
      fi
      [ "$attempt" -lt 10 ] && sleep 5
    done
    if [ -n "$ok" ]; then
      live+=("$u")
    else
      echo "SKIP (never returned 200 after ~45s): $u"
    fi
  done
  if [ "${#live[@]}" -eq 0 ]; then
    echo "ERROR: none of the given URLs are live. Nothing submitted."
    exit 1
  fi
  urls=("${live[@]}")
fi

echo "Submitting ${#urls[@]} URL(s) to IndexNow..."

payload=$(printf '%s\n' "${urls[@]}" | python3 -c '
import json, sys
urls = [l.strip() for l in sys.stdin if l.strip()]
print(json.dumps({
  "host": "'"$HOST"'",
  "key": "'"$KEY"'",
  "keyLocation": "'"$KEY_LOCATION"'",
  "urlList": urls,
}))')

code=$(curl -s -o /tmp/indexnow-resp.txt -w '%{http_code}' \
  -X POST "$ENDPOINT" \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d "$payload")

case "$code" in
  200|202) echo "OK ($code) — accepted. Bing will crawl these shortly." ;;
  400) echo "FAIL (400) Bad request — check the JSON payload."; cat /tmp/indexnow-resp.txt ;;
  403) echo "FAIL (403) Key not valid — is $KEY_LOCATION live and matching?"; cat /tmp/indexnow-resp.txt ;;
  422) echo "FAIL (422) URLs don't match the host, or key mismatch."; cat /tmp/indexnow-resp.txt ;;
  429) echo "FAIL (429) Too many requests — slow down." ;;
  *)   echo "Unexpected response: $code"; cat /tmp/indexnow-resp.txt ;;
esac
