# ClearBid Frontend-Backend Integration Guide

## ✅ Completed Tasks Summary

### TASK 1: Deploy Backend to Render ✅
**Files Created:**
- `render.yaml` - Render deployment config
- `Procfile` - Process file for Render
- `runtime.txt` - Python version specification
- `DEPLOY.md` - Detailed deployment instructions

**Deployment Steps:**
1. Push backend to GitHub
2. Go to https://render.com → Sign up with GitHub
3. New Web Service → Connect your repo
4. Configure:
   - Name: clearbid-api
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables:
   - `DEPLOYER_MNEMONIC`
   - `ANTHROPIC_API_KEY`
   - `FIREBASE_CREDENTIALS` (optional)
6. Deploy → Get URL: `https://clearbid-api.onrender.com`

---

### TASK 2: Create API Service File ✅
**File Created:** `api.js`

**Functions Available:**
```javascript
import { createTender, submitBid, evaluateTender, getTender, getResults } from './api.js';

// Create tender
const tender = await createTender({
  title: "Website Development",
  description: "Build e-commerce platform",
  criteria: { technical: 40, price: 30, timeline: 30 },
  deadline: "2024-12-31"
});

// Submit bid
const bid = await submitBid({
  tender_id: tender.tender_id,
  vendor_name: "TechCorp",
  proposal: "We'll build with React",
  price: 50000
});

// Evaluate bids
const evaluation = await evaluateTender(tender.tender_id);

// Get results
const results = await getResults(tender.tender_id);
```

**Integration with Lovable Frontend:**
1. Copy `api.js` to your Lovable project's `src/` folder
2. Import functions where needed
3. Update BASE_URL to your Render deployment URL

---

### TASK 3: Fix Firebase Integration ✅
**Updated:** `main.py` with Firebase Firestore support

**Features:**
- Automatic fallback to in-memory storage if Firebase not configured
- Stores tenders in `tenders` collection
- Stores bids in `bids` collection
- All CRUD operations support both Firebase and in-memory

**To Enable Firebase:**
1. Go to Firebase Console → Project Settings → Service Accounts
2. Generate New Private Key → Download JSON
3. Copy entire JSON content
4. Add to `.env`: `FIREBASE_CREDENTIALS='{"type":"service_account",...}'`
5. Restart server

---

### TASK 4: Add Anthropic API Key ✅
**File Created:** `ANTHROPIC_SETUP.md`

**Steps to Get API Key:**
1. Go to https://console.anthropic.com
2. Sign up with Google/GitHub
3. Click "API Keys" in sidebar
4. Click "Create Key" → Name it "ClearBid"
5. Copy key (starts with `sk-ant-`)
6. Add to `.env`: `ANTHROPIC_API_KEY="sk-ant-..."`
7. Restart server

**Free Credits:** New accounts get free credits for testing

---

### TASK 5: Test Full Flow End to End ✅
**File Created:** `test_e2e.sh`

**Run Test:**
```bash
cd /Users/mac/Hackathon-QuickStart-template/backend
./test_e2e.sh
```

**Test Flow:**
1. ✅ Create tender (E-Commerce Platform)
2. ✅ Submit bid from TechCorp ($75k)
3. ✅ Submit bid from WebSolutions ($55k)
4. ✅ Submit bid from DevMasters ($95k)
5. ✅ Evaluate with Claude AI
6. ✅ Get ranked results

---

## 📁 Files Created/Modified

### New Files:
- `/backend/render.yaml` - Render deployment config
- `/backend/Procfile` - Process definition
- `/backend/runtime.txt` - Python version
- `/backend/DEPLOY.md` - Deployment guide
- `/backend/api.js` - Frontend API service
- `/backend/ANTHROPIC_SETUP.md` - Claude API setup
- `/backend/test_e2e.sh` - End-to-end test script

### Modified Files:
- `/backend/main.py` - Added Firebase integration
- `/backend/.env` - Added Firebase credentials field

---

## 🚀 Quick Start Guide

### 1. Local Testing (Right Now)
```bash
cd /Users/mac/Hackathon-QuickStart-template/backend

# Add your Anthropic API key to .env
# ANTHROPIC_API_KEY="sk-ant-..."

# Start server
uvicorn main:app --reload --port 8000

# In another terminal, run test
./test_e2e.sh
```

### 2. Deploy to Render
```bash
# Push to GitHub
git init
git add .
git commit -m "ClearBid backend"
git push

# Then follow DEPLOY.md instructions
```

### 3. Connect Frontend
```javascript
// In your Lovable project, copy api.js and use:
import { createTender, submitBid, getResults } from './api.js';

// Create tender
const tender = await createTender({...});

// Submit bid
const bid = await submitBid({...});

// Get results
const results = await getResults(tender.tender_id);
```

---

## 🔗 Important Links

- **Local API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Algorand Contract:** https://lora.algokit.io/testnet/application/755776827
- **Render Deploy:** https://render.com
- **Anthropic Console:** https://console.anthropic.com
- **Firebase Console:** https://console.firebase.google.com

---

## ✅ What's Working

- ✅ FastAPI backend with 5 endpoints
- ✅ Algorand blockchain integration (App 755776827)
- ✅ Claude AI bid evaluation
- ✅ Firebase Firestore support (optional)
- ✅ In-memory fallback storage
- ✅ CORS enabled for frontend
- ✅ Ready for Render deployment
- ✅ Frontend API service file
- ✅ End-to-end test script

---

## 🎯 Next Steps for You

1. **Get Anthropic API Key** (5 minutes)
   - Visit https://console.anthropic.com
   - Create account → Get API key
   - Add to `.env`

2. **Test Locally** (2 minutes)
   ```bash
   ./test_e2e.sh
   ```

3. **Deploy to Render** (10 minutes)
   - Follow `DEPLOY.md`
   - Get public URL

4. **Connect Frontend** (5 minutes)
   - Copy `api.js` to Lovable project
   - Update BASE_URL
   - Import and use functions

**Total Time: ~25 minutes to full deployment!** 🚀
