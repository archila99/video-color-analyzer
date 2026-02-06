"""Frame extraction API route."""
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import Response
from backend.services.frame_extractor import extract_frames
from backend.services.file_manager import save_uploaded_file
from backend.services.zip_service import create_frames_zip
from pathlib import Path

router = APIRouter(prefix="/extract-frames", tags=["frames"])


@router.post("")
async def extract_frames_api(
    video: UploadFile = File(...),
    start_time: float = Form(0, ge=0),
    end_time: float = Form(..., ge=0),
    interval: float = Form(0.1, gt=0),
    crop_x1: int | None = Form(None),
    crop_y1: int | None = Form(None),
    crop_x2: int | None = Form(None),
    crop_y2: int | None = Form(None),
    overlay_time: bool = Form(True),
    remove_shadows: bool = Form(True),
):
    """Extract frames from video and return as ZIP."""
    content = await video.read()
    path = save_uploaded_file(content, video.filename or "video", subdir="videos")
    crop = None
    if all(v is not None for v in (crop_x1, crop_y1, crop_x2, crop_y2)):
        crop = (crop_x1, crop_y1, crop_x2, crop_y2)

    try:
        frames_dir = extract_frames(
            path,
            start_time=start_time,
            end_time=end_time,
            interval=interval,
            crop=crop,
            overlay_time=overlay_time,
            remove_shadows=remove_shadows,
        )
        zip_bytes = create_frames_zip(frames_dir)
        return Response(
            content=zip_bytes,
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=frames.zip"},
        )
    finally:
        path.unlink(missing_ok=True)
