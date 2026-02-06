# Deployment Guide

Deploy backend and frontend separately. Both must be reachable; frontend calls backend via `VITE_API_URL`.

**Requirements:**
- Backend listens on `0.0.0.0` and port from `PORT` env
- Backend `CORS_ORIGINS` includes frontend URL
- Frontend built with `VITE_API_URL` = backend URL

---

## Google Cloud (Europe regions)

Project uses **europe-west1** (Belgium). Other options: `europe-west4` (Netherlands), `europe-west9` (Paris).

### Quick start (scripts)

**One command** (after setup):
```bash
./deploy-all-europe.sh
```

**First-time setup:**
```bash
./setup-gcp-europe.sh
firebase login
firebase use video-image-processing-e-30530  # Firebase project for Hosting
```

**Individual deploys:**
```bash
./deploy-backend-europe.sh
BACKEND_URL=https://video-image-api-xxx.run.app ./deploy-frontend-europe.sh
```

### Manual steps

**Backend** (Cloud Run, europe-west1):
- Build: `gcloud builds submit --tag gcr.io/PROJECT_ID/video-image-api`
- Deploy: `gcloud run deploy video-image-api --image gcr.io/PROJECT_ID/video-image-api --region europe-west1 --allow-unauthenticated`

**Frontend** (Firebase Hosting):
- Build: `cd frontend && VITE_API_URL=BACKEND_URL npm run build`
- Deploy: `firebase deploy --only hosting`

### GitHub Actions (CI/CD)

`.github/workflows/deploy-gcp.yml` deploys on push to `main`.

**Important:** Never commit `key.json`, `GCP_SA_KEY` contents, or `.env` files. They are in `.gitignore`.

**Secrets** (Settings → Secrets and variables → Actions):

| Secret | Description |
|--------|-------------|
| `GCP_PROJECT_ID` | GCP project for Cloud Run backend (e.g. `video-image-processing-eu`) |
| `FIREBASE_PROJECT_ID` | Firebase project for Hosting (e.g. `video-image-processing-e-30530`) |
| `GCP_SA_KEY` | Service account JSON key from `github-actions@GCP_PROJECT_ID.iam.gserviceaccount.com` |
| `FIREBASE_TOKEN` | `firebase login:ci` token for Firebase Hosting deploy |

**Alternative:** Cloud Build trigger using `cloudbuild.yaml` (backend only).

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
