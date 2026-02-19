# Get Anthropic API Key for Claude AI

## Step-by-Step Instructions

1. **Go to Anthropic Console**
   - Visit: https://console.anthropic.com

2. **Sign Up / Login**
   - Click "Sign Up" or "Login"
   - Use Google, GitHub, or email

3. **Navigate to API Keys**
   - Once logged in, click **"API Keys"** in the left sidebar
   - Or go directly to: https://console.anthropic.com/settings/keys

4. **Create New Key**
   - Click **"Create Key"** button
   - Give it a name: "ClearBid Backend"
   - Click **"Create Key"**

5. **Copy the Key**
   - **IMPORTANT:** Copy the key immediately (starts with `sk-ant-`)
   - You won't be able to see it again!
   - Example format: `sk-ant-api03-xxxxxxxxxxxxxxxxxxxxx`

6. **Add to .env File**
   - Open `/Users/mac/Hackathon-QuickStart-template/backend/.env`
   - Find the line: `ANTHROPIC_API_KEY=""`
   - Paste your key: `ANTHROPIC_API_KEY="sk-ant-api03-xxxxxxxxxxxxxxxxxxxxx"`
   - Save the file

7. **Restart Your Server**
   ```bash
   # Stop the current server (Ctrl+C)
   # Then restart:
   uvicorn main:app --reload --port 8000
   ```

8. **Test Claude Integration**
   - Create a tender
   - Submit 2-3 bids
   - Call POST /api/evaluate/:tenderId
   - You should get AI-scored results!

## Pricing Note

- Anthropic offers free credits for new accounts
- Claude 3.5 Sonnet pricing: ~$3 per million input tokens
- For hackathon testing, free credits should be sufficient

## Troubleshooting

- If you get "Claude API not configured" error, check that:
  - API key is correctly pasted in .env
  - No extra spaces or quotes
  - Server was restarted after adding the key
