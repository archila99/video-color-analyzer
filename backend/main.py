"""FastAPI application - combined Video Frame Extractor & Smart Photo Sorter."""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.core.config import CORS_ORIGINS
from backend.api.routes import video, frames, health, photos

app = FastAPI(
    title="Video & Image Processing API",
    description="Extract frames from videos and sort photos by color/B&W",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(video.router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Ensure CORS headers are present on error responses (fixes CORS + 500)."""
    origin = request.headers.get("origin", "")
    headers = {}
    if origin and origin in CORS_ORIGINS:
        headers["Access-Control-Allow-Origin"] = origin
        headers["Access-Control-Allow-Credentials"] = "true"
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
        headers=headers,
    )
app.include_router(frames.router)
app.include_router(health.router)
app.include_router(photos.router)


@app.get("/")
async def root():
    return {
        "message": "Video & Image Processing API",
        "docs": "/docs",
        "endpoints": {
            "video": "POST /video-metadata",
            "frames": "POST /extract-frames",
            "health": "GET /health",
            "photos_analyze": "POST /photos/analyze",
            "photos_folder": "POST /photos/process-folder",
            "photos_download": "POST /photos/download-sorted",
        },
    }
