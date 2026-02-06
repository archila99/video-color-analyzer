"""Video metadata API route."""
from fastapi import APIRouter, File, UploadFile
from backend.services.video_metadata import get_video_metadata
from backend.services.file_manager import save_uploaded_file
from backend.models.schemas import VideoMetadata

router = APIRouter(prefix="/video-metadata", tags=["video"])


@router.post("", response_model=VideoMetadata)
async def video_metadata(video: UploadFile = File(...)):
    """Get metadata about a video file (duration, fps, size)."""
    content = await video.read()
    path = save_uploaded_file(content, video.filename or "video", subdir="videos")
    try:
        meta = get_video_metadata(path)
        return VideoMetadata(**meta)
    finally:
        path.unlink(missing_ok=True)
