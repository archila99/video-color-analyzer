"""Frame extraction service using MoviePy and OpenCV."""
from pathlib import Path
import cv2
import numpy as np
from moviepy import VideoFileClip

from backend.core.config import OUTPUTS_DIR
from backend.services.file_manager import ensure_output_dir


def extract_frames(
    video_path: str | Path,
    start_time: float,
    end_time: float,
    interval: float = 0.1,
    crop: tuple[int, int, int, int] | None = None,
    overlay_time: bool = True,
    remove_shadows: bool = True,
) -> Path:
    """
    Extract frames from video in the given time range.
    Returns path to directory containing extracted frames.
    """
    video_path = Path(video_path)
    output_dir = ensure_output_dir(f"frames_{video_path.stem}")
    # Clear existing frames
    for f in output_dir.glob("frame_*.png"):
        f.unlink()

    clip = VideoFileClip(str(video_path))
    try:
        t = start_time
        frame_idx = 0
        while t <= end_time:
            frame = clip.get_frame(t)
            frame = _process_frame(
                frame, t, crop=crop, overlay_time=overlay_time, remove_shadows=remove_shadows
            )
            out_path = output_dir / f"frame_{frame_idx:05d}.png"
            cv2.imwrite(str(out_path), cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            frame_idx += 1
            t += interval
        return output_dir
    finally:
        clip.close()


def _process_frame(
    frame: np.ndarray,
    timestamp: float,
    crop: tuple[int, int, int, int] | None = None,
    overlay_time: bool = True,
    remove_shadows: bool = True,
) -> np.ndarray:
    """Apply crop, shadow removal, and timestamp overlay."""
    if crop:
        x1, y1, x2, y2 = crop
        frame = frame[y1:y2, x1:x2]
    if remove_shadows:
        frame = _remove_shadows(frame)
    if overlay_time:
        frame = _overlay_timestamp(frame, timestamp)
    return frame


def _remove_shadows(frame: np.ndarray) -> np.ndarray:
    """Brighten dark areas / reduce shadows."""
    lab = cv2.cvtColor(frame, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    lab = cv2.merge([l, a, b])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)


def _overlay_timestamp(frame: np.ndarray, t: float) -> np.ndarray:
    """Draw timestamp on frame."""
    frame = np.ascontiguousarray(frame.copy())  # OpenCV needs writable array
    minutes = int(t // 60)
    seconds = t % 60
    text = f"{minutes:02d}:{seconds:05.2f}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = min(frame.shape[0], frame.shape[1]) / 1000
    thickness = max(1, int(2 * scale))
    (tw, th), _ = cv2.getTextSize(text, font, scale, thickness)
    x = 10
    y = 20 + th
    cv2.rectangle(frame, (x - 2, y - th - 4), (x + tw + 4, y + 4), (0, 0, 0), -1)
    cv2.putText(frame, text, (x, y), font, scale, (255, 255, 255), thickness)
    return frame
