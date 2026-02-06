"""File management utilities."""
import shutil
import uuid
from pathlib import Path
from backend.core.config import UPLOADS_DIR, OUTPUTS_DIR


def save_uploaded_file(file_content: bytes, filename: str, subdir: str = "temp") -> Path:
    """Save uploaded file and return its path."""
    dir_path = UPLOADS_DIR / subdir
    dir_path.mkdir(parents=True, exist_ok=True)
    unique_name = f"{uuid.uuid4().hex}_{Path(filename).name}"
    file_path = dir_path / unique_name
    file_path.write_bytes(file_content)
    return file_path


def ensure_output_dir(name: str) -> Path:
    """Create and return output directory path."""
    path = OUTPUTS_DIR / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def cleanup_path(path: Path) -> None:
    """Remove file or directory."""
    if path.exists():
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
