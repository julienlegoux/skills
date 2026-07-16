#!/usr/bin/env bash
# Attach an existing issue as a native GitHub sub-issue of a parent issue.
# Uses POST /repos/{owner}/{repo}/issues/{issue_number}/sub_issues, which
# requires the *numeric id* of the child issue (not its #number) — this
# script resolves that id first so callers only ever deal with issue numbers.
#
# Usage: link_sub_issue.sh <owner>/<repo> <parent_issue_number> <child_issue_number>
set -euo pipefail

if [ "$#" -ne 3 ]; then
  echo "Usage: link_sub_issue.sh <owner>/<repo> <parent_issue_number> <child_issue_number>" >&2
  exit 1
fi

REPO="$1"
PARENT="$2"
CHILD="$3"

CHILD_ID=$(gh api "repos/$REPO/issues/$CHILD" --jq '.id')

# -F (not -f) so sub_issue_id is sent as a JSON number, as the API requires.
gh api -X POST "repos/$REPO/issues/$PARENT/sub_issues" -F sub_issue_id="$CHILD_ID" --silent

echo "Linked issue #$CHILD as a sub-issue of #$PARENT"
