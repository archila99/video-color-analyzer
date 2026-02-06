"""Folder processing service - batch analyze and sort images."""
from pathlib import Path
from backend.services.image_analysis import analyze_image

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def process_folder(files: list[tuple[str, bytes]]) -> dict:
    """
    Process a list of (filename, content) tuples.
    Returns dict with total, colorful_count, bw_count, colorful_files, bw_files.
    """
    colorful_files: list[str] = []
    bw_files: list[str] = []

    for filename, content in files:
        ext = Path(filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            continue

        # Save temp file and analyze
        from backend.services.file_manager import save_uploaded_file
        temp_path = save_uploaded_file(content, filename, subdir="photo_sort")
        try:
            result = analyze_image(temp_path)
            if result["is_colorful"]:
                colorful_files.append(filename)
            else:
                bw_files.append(filename)
        finally:
            temp_path.unlink(missing_ok=True)

    return {
        "total": len(colorful_files) + len(bw_files),
        "colorful_count": len(colorful_files),
        "bw_count": len(bw_files),
        "colorful_files": colorful_files,
        "bw_files": bw_files,
    }
