# ClearBid Backend API

FastAPI backend for ClearBid - Transparent blockchain-based tender management system.

## Features

- **POST /api/tender** - Create tender, store in Firebase, write hash to Algorand (App ID: 755776827)
- **POST /api/bid** - Submit bid, store in Firebase, write bid hash to Algorand
- **POST /api/evaluate/:tenderId** - Use Claude AI to score all bids
- **GET /api/tender/:tenderId** - Get tender details from Firebase
- **GET /api/results/:tenderId** - Get ranked bid results

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your Firebase credentials and Anthropic API key
```

3. Run the server:
```bash
uvicorn main:app --reload --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

- `DEPLOYER_MNEMONIC` - Algorand wallet mnemonic (already configured)
- `FIREBASE_CREDENTIALS` - Firebase service account JSON (as string)
- `ANTHROPIC_API_KEY` - Claude AI API key

## Example Usage

### Create Tender
```bash
curl -X POST http://localhost:8000/api/tender \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Website Development",
    "description": "Build e-commerce site",
    "criteria": {"technical": 40, "price": 30, "timeline": 30},
    "deadline": "2024-12-31"
  }'
```

### Submit Bid
```bash
curl -X POST http://localhost:8000/api/bid \
  -H "Content-Type: application/json" \
  -d '{
    "tender_id": "abc123",
    "vendor_name": "TechCorp",
    "proposal": "We will build using React and Node.js",
    "price": 50000
  }'
```

### Evaluate Bids
```bash
curl -X POST http://localhost:8000/api/evaluate/abc123
```

### Get Results
```bash
curl http://localhost:8000/api/results/abc123
```

## Algorand Integration

All tender criteria hashes and bid hashes are written to Algorand TestNet App ID: **755776827**

View on Lora: https://lora.algokit.io/testnet/application/755776827
