"""Application configuration."""
import os
from pathlib import Path

# Base paths - use /tmp on Cloud Run (K_SERVICE) for writable ephemeral storage
BASE_DIR = Path(__file__).resolve().parent.parent.parent
_USE_TMP = bool(os.getenv("K_SERVICE"))  # Cloud Run sets this
if _USE_TMP:
    UPLOADS_DIR = Path("/tmp") / "uploads"
    OUTPUTS_DIR = Path("/tmp") / "outputs"
else:
    UPLOADS_DIR = BASE_DIR / "uploads"
    OUTPUTS_DIR = BASE_DIR / "outputs"

# Ensure directories exist
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# CORS - strip whitespace from each origin
# Always include production frontend URLs so Cloud Run works even if env is misconfigured
_DEFAULT_ORIGINS = "http://localhost:3000"
_ENV_ORIGINS = os.getenv("CORS_ORIGINS", _DEFAULT_ORIGINS)
_PROD_ORIGINS = [
    "https://video-image-processing-e-30530.web.app",
    "https://video-image-processing-e-30530.firebaseapp.com",
]
_env_list = [o.strip() for o in _ENV_ORIGINS.split(",") if o.strip()]
CORS_ORIGINS = list(dict.fromkeys(_env_list + _PROD_ORIGINS))  # dedupe, env first

# Photo sorter - color detection threshold (pixels with channel diff > this are "colorful")
COLOR_THRESHOLD = int(os.getenv("COLOR_THRESHOLD", "15"))
COLOR_RATIO_THRESHOLD = float(os.getenv("COLOR_RATIO_THRESHOLD", "0.02"))  # 2% colorful pixels = color image
