"""Application configuration."""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUTS_DIR = BASE_DIR / "outputs"

# Ensure directories exist
UPLOADS_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

# Photo sorter - color detection threshold (pixels with channel diff > this are "colorful")
COLOR_THRESHOLD = int(os.getenv("COLOR_THRESHOLD", "15"))
COLOR_RATIO_THRESHOLD = float(os.getenv("COLOR_RATIO_THRESHOLD", "0.02"))  # 2% colorful pixels = color image
