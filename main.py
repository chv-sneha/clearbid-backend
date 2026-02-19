from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
from dotenv import load_dotenv
from algosdk.v2client import algod
from algosdk import account, mnemonic, transaction
import google.generativeai as genai
import hashlib
import json
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

load_dotenv()

app = FastAPI(title="ClearBid API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase
firebase_creds = os.getenv("FIREBASE_CREDENTIALS")
if firebase_creds and not firebase_admin._apps:
    cred = credentials.Certificate(json.loads(firebase_creds))
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    USE_FIREBASE = True
else:
    db = None
    USE_FIREBASE = False
    # Fallback to in-memory storage
    tenders_db: Dict[str, dict] = {}
    bids_db: Dict[str, dict] = {}

# Initialize Algorand
algod_client = algod.AlgodClient("", "https://testnet-api.algonode.cloud")
deployer_mnemonic = os.getenv("DEPLOYER_MNEMONIC")
deployer_private_key = mnemonic.to_private_key(deployer_mnemonic)
deployer_address = account.address_from_private_key(deployer_private_key)
APP_ID = int(os.getenv("ALGORAND_APP_ID", "755776827"))

# Initialize Gemini AI
gemini_key = os.getenv("GEMINI_API_KEY")
if gemini_key:
    genai.configure(api_key=gemini_key)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
else:
    gemini_model = None

class TenderCreate(BaseModel):
    title: str
    description: str
    criteria: dict
    deadline: str

class BidSubmit(BaseModel):
    tender_id: str
    vendor_name: str
    proposal: str
    price: float

@app.post("/api/tender")
async def create_tender(tender: TenderCreate):
    tender_id = hashlib.sha256(f"{tender.title}{datetime.now()}".encode()).hexdigest()[:16]
    criteria_hash = hashlib.sha256(json.dumps(tender.criteria).encode()).hexdigest()
    
    tender_data = {
        "tender_id": tender_id,
        "title": tender.title,
        "description": tender.description,
        "criteria": tender.criteria,
        "deadline": tender.deadline,
        "criteria_hash": criteria_hash,
        "created_at": datetime.now().isoformat(),
        "status": "OPEN"
    }
    
    # Store in Firebase or memory
    if USE_FIREBASE:
        db.collection("tenders").document(tender_id).set(tender_data)
    else:
        tenders_db[tender_id] = tender_data
    
    # Write to Algorand
    params = algod_client.suggested_params()
    txn = transaction.ApplicationNoOpTxn(
        sender=deployer_address,
        sp=params,
        index=APP_ID,
        app_args=[criteria_hash.encode()]
    )
    signed_txn = txn.sign(deployer_private_key)
    tx_id = algod_client.send_transaction(signed_txn)
    
    return {"tender_id": tender_id, "tx_id": tx_id, "criteria_hash": criteria_hash}

@app.post("/api/bid")
async def submit_bid(bid: BidSubmit):
    bid_id = hashlib.sha256(f"{bid.tender_id}{bid.vendor_name}{datetime.now()}".encode()).hexdigest()[:16]
    bid_hash = hashlib.sha256(json.dumps({"proposal": bid.proposal, "price": bid.price}).encode()).hexdigest()
    
    bid_data = {
        "bid_id": bid_id,
        "tender_id": bid.tender_id,
        "vendor_name": bid.vendor_name,
        "proposal": bid.proposal,
        "price": bid.price,
        "bid_hash": bid_hash,
        "submitted_at": datetime.now().isoformat()
    }
    
    # Store in Firebase or memory
    if USE_FIREBASE:
        db.collection("bids").document(bid_id).set(bid_data)
    else:
        bids_db[bid_id] = bid_data
    
    # Write to Algorand
    params = algod_client.suggested_params()
    txn = transaction.ApplicationNoOpTxn(
        sender=deployer_address,
        sp=params,
        index=APP_ID,
        app_args=[bid_hash.encode()]
    )
    signed_txn = txn.sign(deployer_private_key)
    tx_id = algod_client.send_transaction(signed_txn)
    
    return {"bid_id": bid_id, "tx_id": tx_id, "bid_hash": bid_hash}

@app.post("/api/evaluate/{tender_id}")
async def evaluate_tender(tender_id: str):
    # Get tender from Firebase or memory
    if USE_FIREBASE:
        tender_doc = db.collection("tenders").document(tender_id).get()
        if not tender_doc.exists:
            raise HTTPException(status_code=404, detail="Tender not found")
        tender = tender_doc.to_dict()
        
        bids_ref = db.collection("bids").where("tender_id", "==", tender_id).stream()
        bids = [bid.to_dict() for bid in bids_ref]
    else:
        if tender_id not in tenders_db:
            raise HTTPException(status_code=404, detail="Tender not found")
        tender = tenders_db[tender_id]
        bids = [b for b in bids_db.values() if b["tender_id"] == tender_id]
    
    if not bids:
        raise HTTPException(status_code=400, detail="No bids to evaluate")
    
    if not gemini_model:
        raise HTTPException(status_code=503, detail="Gemini API not configured")
    
    # Prepare prompt for Gemini
    prompt = f"""Evaluate these bids for tender: {tender['title']}
Criteria weights: {json.dumps(tender['criteria'])}

Bids:
{json.dumps([{'vendor': b['vendor_name'], 'proposal': b['proposal'], 'price': b['price']} for b in bids], indent=2)}

Score each bid 0-100 based on the criteria weights. Return ONLY valid JSON: {{"scores": [{{"vendor": "name", "score": 85, "reasoning": "..."}}]}}"""
    
    # Call Gemini
    response = gemini_model.generate_content(prompt)
    result_text = response.text.strip()
    
    # Extract JSON from response
    if "```json" in result_text:
        result_text = result_text.split("```json")[1].split("```")[0].strip()
    elif "```" in result_text:
        result_text = result_text.split("```")[1].split("```")[0].strip()
    
    result = json.loads(result_text)
    
    # Store results
    for bid in bids:
        score_data = next((s for s in result["scores"] if s["vendor"] == bid["vendor_name"]), None)
        if score_data:
            if USE_FIREBASE:
                db.collection("bids").document(bid["bid_id"]).update({
                    "score": score_data["score"],
                    "reasoning": score_data["reasoning"]
                })
            else:
                bids_db[bid["bid_id"]].update({
                    "score": score_data["score"],
                    "reasoning": score_data["reasoning"]
                })
    
    if USE_FIREBASE:
        db.collection("tenders").document(tender_id).update({"status": "EVALUATED"})
    else:
        tenders_db[tender_id]["status"] = "EVALUATED"
    
    return {"message": "Evaluation complete", "results": result}

@app.get("/api/tender/{tender_id}")
async def get_tender(tender_id: str):
    if USE_FIREBASE:
        tender_doc = db.collection("tenders").document(tender_id).get()
        if not tender_doc.exists:
            raise HTTPException(status_code=404, detail="Tender not found")
        return tender_doc.to_dict()
    else:
        if tender_id not in tenders_db:
            raise HTTPException(status_code=404, detail="Tender not found")
        return tenders_db[tender_id]

@app.get("/api/results/{tender_id}")
async def get_results(tender_id: str):
    if USE_FIREBASE:
        bids_ref = db.collection("bids").where("tender_id", "==", tender_id).stream()
        bids = [bid.to_dict() for bid in bids_ref]
    else:
        bids = [b for b in bids_db.values() if b["tender_id"] == tender_id]
    
    ranked = sorted([b for b in bids if "score" in b], key=lambda x: x["score"], reverse=True)
    return {"tender_id": tender_id, "ranked_bids": ranked}

@app.get("/api/tenders")
async def get_tenders():
    if USE_FIREBASE:
        tenders_ref = db.collection("tenders").stream()
        tenders = [t.to_dict() for t in tenders_ref]
    else:
        tenders = list(tenders_db.values())
    
    return {"tenders": tenders}

@app.get("/")
async def root():
    return {"message": "ClearBid API", "app_id": APP_ID}
