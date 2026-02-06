# Video & Image Processing

A unified web application combining **Video Frame Extractor** and **Image Identifier**. Built with FastAPI (Python) backend and React/TypeScript frontend.

## Features

### Video Frame Extractor
- Automatic video duration detection
- Time range with validation (start, end, video duration)
- Configurable frame interval (steps of 0.2s)
- Optional overlay timestamp and shadow removal
- Download extracted frames as ZIP

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
├── start_backend.sh
├── start_frontend.sh
└── README.md
```

## Deployment

See [DEPLOY.md](./DEPLOY.md) for Google Cloud, Render, and other clouds.

## Tech Stack

- **Backend:** FastAPI, MoviePy, OpenCV, Pillow, NumPy
- **Frontend:** React, TypeScript, Vite, React Router
