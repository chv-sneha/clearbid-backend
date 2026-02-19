# Deploy ClearBid Backend to Render - Quick Guide

## Step 1: Push to GitHub

```bash
cd /Users/mac/Hackathon-QuickStart-template/backend

# Initialize git if not already
git init

# Add all files
git add .

# Commit
git commit -m "ClearBid backend with Gemini AI"

# Create repo on GitHub, then:
git remote add origin YOUR_GITHUB_REPO_URL
git branch -M main
git push -u origin main
```

## Step 2: Deploy on Render

1. Go to https://render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name:** `clearbid-api`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

5. **Add Environment Variables:**
   Click "Advanced" → "Add Environment Variable":
   
   ```
   DEPLOYER_MNEMONIC = lend sure wait devote domain veteran tissue frame kind beauty pistol rapid notice talk either buffalo spare industry plastic around olympic body hour able habit
   
   GEMINI_API_KEY = YOUR_GEMINI_KEY_HERE
   
   ALGORAND_APP_ID = 755776827
   ```

6. Click **"Create Web Service"**

7. Wait 5-10 minutes for deployment

8. Your API will be live at: `https://clearbid-api.onrender.com`

## Step 3: Test Deployment

```bash
curl https://clearbid-api.onrender.com/
```

Expected: `{"message":"ClearBid API","app_id":755776827}`

## Your Render URL

After deployment, your URL will be:
**https://clearbid-api.onrender.com**

Use this URL in your frontend api.js file.
