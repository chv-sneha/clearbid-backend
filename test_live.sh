#!/bin/bash

# Test ClearBid Live Backend on Render
# Update BASE_URL after deployment

BASE_URL="https://clearbid-api.onrender.com"

echo "🧪 Testing ClearBid Live Backend"
echo "================================"
echo "URL: $BASE_URL"
echo ""

# Test root endpoint
echo "📡 Testing root endpoint..."
curl -s "$BASE_URL/" | python3 -m json.tool
echo ""

# Create test tender
echo "📝 Creating test tender..."
TENDER_RESPONSE=$(curl -s -X POST "$BASE_URL/api/tender" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mobile App Development",
    "description": "Build iOS and Android app",
    "criteria": {"technical": 50, "price": 30, "timeline": 20},
    "deadline": "2024-12-31"
  }')

echo "$TENDER_RESPONSE" | python3 -m json.tool
TENDER_ID=$(echo $TENDER_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['tender_id'])" 2>/dev/null)

if [ -z "$TENDER_ID" ]; then
  echo "❌ Failed to create tender"
  exit 1
fi

echo ""
echo "✅ Tender created: $TENDER_ID"
echo ""
echo "🔗 View on Algorand: https://lora.algokit.io/testnet/application/755776827"
echo ""
echo "✅ Live backend is working!"
