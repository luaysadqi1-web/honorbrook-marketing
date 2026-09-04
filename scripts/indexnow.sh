#!/usr/bin/env bash
# Ping IndexNow (Bing, Yandex, Naver, Seznam) so new/updated pages get crawled fast.
#
#   ./scripts/indexnow.sh                        # submit every URL in sitemap.xml
#   ./scripts/indexnow.sh /term-life-insurance   # submit specific path(s)
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
