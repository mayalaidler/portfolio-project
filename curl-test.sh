#!/bin/bash
#
# Tests the timeline_post API end-to-end:
#   1. POSTs a randomly generated timeline post
#   2. GETs all posts and confirms the new one is present
#
# Usage: ./curl-test.sh [base_url]
#   base_url defaults to http://localhost:5000

set -e

BASE_URL="${1:-http://localhost:5000}"
ENDPOINT="$BASE_URL/api/timeline_post"

# Build a unique post so we can reliably find it again in the GET response
TOKEN="test-$RANDOM-$(date +%s)"
NAME="Test User $RANDOM"
EMAIL="test$RANDOM@example.com"
CONTENT="Automated test post [$TOKEN]"

echo "→ POST $ENDPOINT"
POST_RESPONSE=$(curl -s -X POST "$ENDPOINT" \
    --data-urlencode "name=$NAME" \
    --data-urlencode "email=$EMAIL" \
    --data-urlencode "content=$CONTENT")
echo "$POST_RESPONSE"
echo

echo "→ GET $ENDPOINT"
GET_RESPONSE=$(curl -s "$ENDPOINT")
echo "$GET_RESPONSE"
echo

if echo "$GET_RESPONSE" | grep -q "$TOKEN"; then
    echo "✅ PASS — the new post ($TOKEN) was found in the GET response."
    exit 0
else
    echo "❌ FAIL — the new post ($TOKEN) was NOT found in the GET response."
    exit 1
fi
