"""Video metadata extraction service."""
from pathlib import Path
import cv2


def get_video_metadata(video_path: str | Path) -> dict:
    """
    Extract metadata from a video file.
    Returns duration (seconds), fps, and size [width, height].
    """
    path = Path(video_path)
    if not path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    cap = cv2.VideoCapture(str(path))
    try:
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = frame_count / fps if fps > 0 else 0.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)

        return {
            "duration": round(duration, 2),
            "fps": round(fps, 2),
            "size": [width, height],
        }
    finally:
        cap.release()
