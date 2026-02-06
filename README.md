# Video & Image Processing

A unified web application combining **Video Frame Extractor** and **Image Identifier**. Built with FastAPI (Python) backend and React/TypeScript frontend.

**Live:** [video-image-processing-e-30530.web.app](https://video-image-processing-e-30530.web.app)

## Features

### Video Frame Extractor
- Automatic video duration detection (MoviePy/ffmpeg – HEVC, MOV, MP4)
- Time range with validation (start, end, video duration)
- Configurable frame interval (steps of 0.2s)
- Optional overlay timestamp and shadow removal
- Download extracted frames as ZIP (max 500 frames per request)

### Image Identifier
- Single or multiple image analysis
- Identifies color vs monochrome
- Batch download sorted into `colorful/` and `b&w/` folders

## Setup

### Backend (Python 3.10+)

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

API: `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App: `http://localhost:3000`

## Environment Variables

### Backend
| Variable | Default | Description |
|----------|---------|-------------|
| `CORS_ORIGINS` | `http://localhost:3000` | Allowed origins (comma-separated) |
| `COLOR_THRESHOLD` | `15` | Photo sorter color detection threshold |
| `COLOR_RATIO_THRESHOLD` | `0.02` | Minimum colorful pixel ratio for "color" classification |

### Frontend
| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_URL` | (empty) | Backend API URL for production (e.g. `https://api.example.com`) |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/video-metadata` | Get video duration, fps, size |
| POST | `/extract-frames` | Extract frames from video (returns ZIP) |
| GET | `/health` | Health check |
| POST | `/photos/analyze` | Analyze single image |
| POST | `/photos/process-folder` | Process multiple images |
| POST | `/photos/download-sorted` | Download sorted images as ZIP |

## Project Structure

```
video-image-processing/
├── backend/
│   ├── main.py
│   ├── api/routes/
│   ├── services/
│   ├── models/
│   └── core/
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   └── components/
│   └── package.json
├── requirements.txt
├── Dockerfile
├── firebase.json
├── deploy-all-europe.sh
├── deploy-backend-europe.sh
├── deploy-frontend-europe.sh
├── setup-gcp-europe.sh
├── start_backend.sh
├── start_frontend.sh
└── README.md
```

## Deployment

**One-command deploy** (Google Cloud, Europe):
```bash
./setup-gcp-europe.sh   # first time only
./deploy-all-europe.sh  # backend + frontend + CORS
```

See [DEPLOY.md](./DEPLOY.md) for details and GitHub Actions CI/CD.

## Pushing to GitHub

**Before pushing, ensure you never commit:**
- `key.json` or any service account keys
- `.env` or `.env.local` files
- Firebase tokens or credentials

These are already in `.gitignore`. To push:
```bash
git add .
git status   # verify no secrets listed
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/video-image-processing.git
git push -u origin main
```

For GitHub Actions, add secrets: `GCP_PROJECT_ID`, `GCP_SA_KEY`, `FIREBASE_PROJECT_ID`, `FIREBASE_TOKEN`.

**After pushing:** Either run `./deploy-all-europe.sh` locally to deploy, or push to `main` to trigger GitHub Actions (if configured).

## Tech Stack

- **Backend:** FastAPI, MoviePy, OpenCV (headless), Pillow, NumPy
- **Frontend:** React, TypeScript, Vite, React Router
