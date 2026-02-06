# Deployment Guide

Deploy backend and frontend separately. Both must be reachable; frontend calls backend via `VITE_API_URL`.

**Requirements:**
- Backend listens on `0.0.0.0` and port from `PORT` env
- Backend `CORS_ORIGINS` includes frontend URL
- Frontend built with `VITE_API_URL` = backend URL

---

## Google Cloud (Cloud Run)

### Backend

Uses the project `Dockerfile`. Ensure `Dockerfile` and `.dockerignore` are in the repo root.

1. Build and push image:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/video-image-api
   ```

2. Deploy:
   ```bash
   gcloud run deploy video-image-api \
     --image gcr.io/YOUR_PROJECT_ID/video-image-api \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars CORS_ORIGINS=https://YOUR_FRONTEND_URL
   ```

3. Copy the service URL (e.g. `https://video-image-api-xxx.run.app`).

### Frontend

1. Build with backend URL:
   ```bash
   cd frontend
   VITE_API_URL=https://YOUR_BACKEND_URL npm run build
   ```

2. Deploy to **Firebase Hosting** (recommended for static):
   ```bash
   npm install -g firebase-tools
   firebase login
   firebase init hosting  # pick frontend/dist as public dir, single-page app: yes
   firebase deploy
   ```
   Or use **Cloud Storage + Load Balancer** for static hosting.

---

## Render

### Backend (Web Service)

- **Build:** `pip install -r requirements.txt`
- **Start:** `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- **Env:** `CORS_ORIGINS` = frontend URL

### Frontend (Static Site)

- **Root:** `frontend`
- **Build:** `npm install && npm run build`
- **Publish:** `frontend/dist`
- **Env:** `VITE_API_URL` = backend URL

---

## Other Clouds (Railway, Heroku, Fly.io, AWS)

Use the same commands. Backend: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`. Frontend: build with `VITE_API_URL` set, then serve static files or run `npm run preview`.
