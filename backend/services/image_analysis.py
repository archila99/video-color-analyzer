"""Image analysis service - detect if image is colorful or black & white."""
from pathlib import Path
import numpy as np
from PIL import Image

from backend.core.config import COLOR_THRESHOLD, COLOR_RATIO_THRESHOLD


def analyze_image(image_path: str | Path) -> dict:
    """
    Analyze image to determine if it's colorful or black & white.
    Returns dict with: is_colorful, colorful_percentage, message.
    """
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    img = Image.open(path)
    img = img.convert("RGB")
    arr = np.array(img)

    colorful_ratio = _compute_colorful_ratio(arr)
    is_colorful = colorful_ratio >= COLOR_RATIO_THRESHOLD

    message = "Colorful" if is_colorful else "Black & White"
    return {
        "is_colorful": is_colorful,
        "colorful_percentage": round(colorful_ratio * 100, 2),
        "message": message,
    }


def _compute_colorful_ratio(arr: np.ndarray) -> float:
    """
    Compute ratio of pixels that have significant color (R, G, B differ).
    Uses channel differences - if max(R,G,B) - min(R,G,B) > threshold, pixel is colorful.
    """
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    diff = max_c.astype(np.int16) - min_c.astype(np.int16)
    colorful_pixels = np.sum(diff > COLOR_THRESHOLD)
    total = arr.shape[0] * arr.shape[1]
    return colorful_pixels / total if total > 0 else 0.0
