#!/bin/bash

# ClearBid End-to-End Test Script
# Tests the complete flow: Create Tender → Submit Bids → Evaluate → Get Results

BASE_URL="http://localhost:8000"
# For deployed version: BASE_URL="https://clearbid-api.onrender.com"

echo "🧪 ClearBid End-to-End Test"
echo "================================"
echo ""

# Step 1: Create Tender
echo "📝 Step 1: Creating tender..."
TENDER_RESPONSE=$(curl -s -X POST "$BASE_URL/api/tender" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "E-Commerce Platform Development",
    "description": "Build a modern e-commerce platform with payment integration",
    "criteria": {
      "technical_expertise": 40,
      "price_competitiveness": 30,
      "delivery_timeline": 30
    },
    "deadline": "2024-12-31"
  }')

TENDER_ID=$(echo $TENDER_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['tender_id'])")
echo "✅ Tender created: $TENDER_ID"
echo "Response: $TENDER_RESPONSE"
echo ""

# Step 2: Submit Bid 1
echo "💼 Step 2: Submitting bid from TechCorp..."
BID1_RESPONSE=$(curl -s -X POST "$BASE_URL/api/bid" \
  -H "Content-Type: application/json" \
  -d "{
    \"tender_id\": \"$TENDER_ID\",
    \"vendor_name\": \"TechCorp\",
    \"proposal\": \"We will build a scalable e-commerce platform using React, Node.js, and PostgreSQL. Our team has 10+ years of experience. We offer 24/7 support and 6-month warranty.\",
    \"price\": 75000
  }")
echo "✅ Bid 1 submitted"
echo "Response: $BID1_RESPONSE"
echo ""

# Step 3: Submit Bid 2
echo "💼 Step 3: Submitting bid from WebSolutions..."
BID2_RESPONSE=$(curl -s -X POST "$BASE_URL/api/bid" \
  -H "Content-Type: application/json" \
  -d "{
    \"tender_id\": \"$TENDER_ID\",
    \"vendor_name\": \"WebSolutions\",
    \"proposal\": \"Modern e-commerce solution with Next.js and Stripe integration. Fast delivery in 3 months. Includes mobile app. Competitive pricing with flexible payment terms.\",
    \"price\": 55000
  }")
echo "✅ Bid 2 submitted"
echo "Response: $BID2_RESPONSE"
echo ""

# Step 4: Submit Bid 3
echo "💼 Step 4: Submitting bid from DevMasters..."
BID3_RESPONSE=$(curl -s -X POST "$BASE_URL/api/bid" \
  -H "Content-Type: application/json" \
  -d "{
    \"tender_id\": \"$TENDER_ID\",
    \"vendor_name\": \"DevMasters\",
    \"proposal\": \"Enterprise-grade e-commerce platform with advanced analytics, AI-powered recommendations, and multi-currency support. Premium quality with extended support.\",
    \"price\": 95000
  }")
echo "✅ Bid 3 submitted"
echo "Response: $BID3_RESPONSE"
echo ""

# Step 5: Evaluate Bids
echo "🤖 Step 5: Evaluating bids with Claude AI..."
EVAL_RESPONSE=$(curl -s -X POST "$BASE_URL/api/evaluate/$TENDER_ID" \
  -H "Content-Type: application/json")
echo "✅ Evaluation complete"
echo "Response: $EVAL_RESPONSE"
echo ""

# Step 6: Get Results
echo "🏆 Step 6: Getting ranked results..."
RESULTS=$(curl -s -X GET "$BASE_URL/api/results/$TENDER_ID" \
  -H "Content-Type: application/json")
echo "✅ Results retrieved"
echo ""
echo "📊 FINAL RANKED RESULTS:"
echo "================================"
echo "$RESULTS" | python3 -m json.tool
echo ""

echo "✅ End-to-End Test Complete!"
echo ""
echo "🔗 View tender on Algorand:"
echo "   https://lora.algokit.io/testnet/application/755776827"
