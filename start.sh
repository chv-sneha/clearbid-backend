#!/bin/bash

echo "🚀 Starting ClearBid Backend Server..."
cd /Users/mac/Hackathon-QuickStart-template/backend
uvicorn main:app --port 8000 --reload

# Server will run at http://localhost:8000
# API Docs at http://localhost:8000/docs
