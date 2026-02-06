"""Photo analysis and sorting API routes."""
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import Response
from backend.services.image_analysis import analyze_image
from backend.services.folder_processor import process_folder, ALLOWED_EXTENSIONS
from backend.services.file_manager import save_uploaded_file
from backend.services.zip_service import create_photo_sort_zip
from backend.models.schemas import PhotoAnalysisResult, FolderProcessResult
from pathlib import Path

router = APIRouter(prefix="/photos", tags=["photos"])


@router.post("/analyze", response_model=PhotoAnalysisResult)
async def analyze_photo(photo: UploadFile = File(...)):
    """Analyze a single photo - determine if colorful or B&W."""
    content = await photo.read()
    filename = photo.filename or "image.jpg"
    path = save_uploaded_file(content, filename, subdir="photo_sort")
    try:
        result = analyze_image(path)
        return PhotoAnalysisResult(
            filename=filename,
            is_colorful=result["is_colorful"],
            colorful_percentage=result["colorful_percentage"],
            message=result["message"],
        )
    finally:
        path.unlink(missing_ok=True)


@router.post("/process-folder", response_model=FolderProcessResult)
async def process_folder_api(files: list[UploadFile] = File(...)):
    """Process a folder of images and return sort results."""
    file_list: list[tuple[str, bytes]] = []
    for f in files:
        if not f.filename:
            continue
        ext = Path(f.filename).suffix.lower()
        if ext in ALLOWED_EXTENSIONS:
            content = await f.read()
            file_list.append((f.filename, content))

    result = process_folder(file_list)
    return FolderProcessResult(**result)


@router.post("/download-sorted")
async def download_sorted_folder(files: list[UploadFile] = File(...)):
    """Process folder and return ZIP with sorted images (colorful/ and b&w/)."""
    file_list: list[tuple[str, bytes]] = []
    for f in files:
        if not f.filename:
            continue
        ext = Path(f.filename).suffix.lower()
        if ext in ALLOWED_EXTENSIONS:
            content = await f.read()
            file_list.append((f.filename, content))

    result = process_folder(file_list)
    zip_bytes = create_photo_sort_zip(
        file_list,
        result["colorful_files"],
        result["bw_files"],
    )
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=sorted_photos.zip"},
    )
