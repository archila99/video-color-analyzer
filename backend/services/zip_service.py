"""ZIP creation service for frame extraction and photo sorting."""
import zipfile
import io
from pathlib import Path
from typing import BinaryIO


def create_frames_zip(frames_dir: Path) -> bytes:
    """Create ZIP from directory of frame PNG files."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(frames_dir.glob("*.png")):
            zf.write(f, f.name)
    return buffer.getvalue()


def create_photo_sort_zip(
    files: list[tuple[str, bytes]],
    colorful_files: list[str],
    bw_files: list[str],
) -> bytes:
    """
    Create ZIP with 'colorful' and 'b&w' subfolders containing sorted images.
    """
    buffer = io.BytesIO()
    file_map = {name: content for name, content in files}

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in colorful_files:
            if name in file_map:
                zf.writestr(f"colorful/{name}", file_map[name])
        for name in bw_files:
            if name in file_map:
                zf.writestr(f"b&w/{name}", file_map[name])

    return buffer.getvalue()
