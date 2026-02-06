"""Video metadata extraction service."""
from pathlib import Path


def get_video_metadata(video_path: str | Path) -> dict:
    """
    Extract metadata from a video file.
    Returns duration (seconds), fps, and size [width, height].
    Uses MoviePy (ffmpeg) first - better codec support on Linux/Cloud Run.
    Falls back to OpenCV if MoviePy fails.
    """
    path = Path(video_path)
    if not path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    # MoviePy uses ffmpeg - supports HEVC, MOV, etc. on Linux (Cloud Run)
    try:
        from moviepy import VideoFileClip

        clip = VideoFileClip(str(path))
        try:
            w, h = clip.size
            return {
                "duration": round(float(clip.duration), 2),
                "fps": round(float(clip.fps) or 30.0, 2),
                "size": [int(w), int(h)],
            }
        finally:
            clip.close()
    except Exception:
        pass

    # Fallback: OpenCV (may fail on HEVC/MOV on Linux)
    import cv2

    cap = cv2.VideoCapture(str(path))
    try:
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = frame_count / fps if fps > 0 else 0.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
        if width == 0 and height == 0:
            raise ValueError("Could not read video metadata (unsupported codec?). Try MP4/H.264.")
        return {
            "duration": round(duration, 2),
            "fps": round(fps, 2),
            "size": [width, height],
        }
    finally:
        cap.release()
