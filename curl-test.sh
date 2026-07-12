#!/bin/bash
# Tests the timeline_post API: creates a post, then checks it shows up in GET.

URL="http://localhost:5000/api/timeline_post"
TOKEN="test-$RANDOM"

echo "POST:"
curl -s -X POST "$URL" \
    -d "name=Test User" \
    -d "email=test@example.com" \
    -d "content=$TOKEN"
echo

echo "GET:"
curl -s "$URL"
echo

if curl -s "$URL" | grep -q "$TOKEN"; then
    echo "PASS"
else
    echo "FAIL"
fi
