# Deploy ClearBid Backend to Render

## Step-by-Step Deployment Instructions

### 1. Push to GitHub (if not already)
```bash
cd /Users/mac/Hackathon-QuickStart-template/backend
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### 2. Deploy on Render.com

1. Go to https://render.com
2. Sign up/Login with GitHub
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository
5. Select the `backend` folder (or root if backend is at root)
6. Configure:
   - **Name:** clearbid-api
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

7. Add Environment Variables (click "Advanced" → "Add Environment Variable"):
   - **DEPLOYER_MNEMONIC:** `lend sure wait devote domain veteran tissue frame kind beauty pistol rapid notice talk either buffalo spare industry plastic around olympic body hour able habit`
   - **ANTHROPIC_API_KEY:** `YOUR_CLAUDE_API_KEY` (get from console.anthropic.com)

8. Click **"Create Web Service"**

9. Wait 5-10 minutes for deployment

10. Your API will be live at: `https://clearbid-api.onrender.com`

### 3. Test Your Deployed API

```bash
curl https://clearbid-api.onrender.com/
```

Expected response:
```json
{"message":"ClearBid API","app_id":755776827}
```

### 4. Update Frontend API URL

Use `https://clearbid-api.onrender.com` as your base URL in the frontend api.js file.

## Troubleshooting

- If deployment fails, check logs in Render dashboard
- Ensure all environment variables are set
- Verify requirements.txt includes all dependencies
- Check that PORT is used from environment: `--port $PORT`
