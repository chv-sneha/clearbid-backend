// ClearBid API Service
// Update BASE_URL after deploying to Render

const BASE_URL = 'https://clearbid-api.onrender.com';
// For local testing: const BASE_URL = 'http://localhost:8000';

/**
 * Create a new tender
 * @param {Object} tenderData - { title, description, criteria, deadline }
 * @returns {Promise<Object>} { tender_id, tx_id, criteria_hash }
 */
export async function createTender(tenderData) {
  const response = await fetch(`${BASE_URL}/api/tender`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(tenderData),
  });
  
  if (!response.ok) {
    throw new Error(`Failed to create tender: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * Submit a bid for a tender
 * @param {Object} bidData - { tender_id, vendor_name, proposal, price }
 * @returns {Promise<Object>} { bid_id, tx_id, bid_hash }
 */
export async function submitBid(bidData) {
  const response = await fetch(`${BASE_URL}/api/bid`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(bidData),
  });
  
  if (!response.ok) {
    throw new Error(`Failed to submit bid: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * Evaluate all bids for a tender using Claude AI
 * @param {string} tenderId - The tender ID
 * @returns {Promise<Object>} { message, results }
 */
export async function evaluateTender(tenderId) {
  const response = await fetch(`${BASE_URL}/api/evaluate/${tenderId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) {
    throw new Error(`Failed to evaluate tender: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * Get tender details
 * @param {string} tenderId - The tender ID
 * @returns {Promise<Object>} Tender object
 */
export async function getTender(tenderId) {
  const response = await fetch(`${BASE_URL}/api/tender/${tenderId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) {
    throw new Error(`Failed to get tender: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * Get ranked bid results for a tender
 * @param {string} tenderId - The tender ID
 * @returns {Promise<Object>} { tender_id, ranked_bids }
 */
export async function getResults(tenderId) {
  const response = await fetch(`${BASE_URL}/api/results/${tenderId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) {
    throw new Error(`Failed to get results: ${response.statusText}`);
  }
  
  return response.json();
}

// Example usage:
/*
import { createTender, submitBid, evaluateTender, getTender, getResults } from './api';

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
  proposal: "We'll build with React and Node.js",
  price: 50000
});

// Evaluate bids
const evaluation = await evaluateTender(tender.tender_id);

// Get results
const results = await getResults(tender.tender_id);
*/
