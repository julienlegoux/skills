#!/usr/bin/env bash
# Find a milestone by exact title in owner/repo, creating it if it doesn't exist.
# Prints {"number": N, "title": "..."} on success.
#
# Usage: ensure_milestone.sh <owner>/<repo> "<milestone title>"
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: ensure_milestone.sh <owner>/<repo> <milestone title>" >&2
  exit 1
fi

REPO="$1"
export TITLE="$2"

# gh api's --jq is gojq, which supports env.NAME — avoids interpolating
# untrusted title text into the filter expression itself.
EXISTING=$(gh api "repos/$REPO/milestones?state=all&per_page=100" \
  --jq '[.[] | select(.title == env.TITLE)][0] | select(. != null) | {number, title}')

if [ -n "$EXISTING" ]; then
  echo "$EXISTING"
  exit 0
fi

gh api "repos/$REPO/milestones" -f title="$TITLE" --jq '{number, title}'
