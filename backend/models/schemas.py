"""Pydantic schemas for API validation."""
from pydantic import BaseModel, Field


class VideoMetadata(BaseModel):
    """Video metadata response."""
    duration: float
    fps: float
    size: list[int]


class PhotoAnalysisResult(BaseModel):
    """Single photo analysis result."""
    filename: str
    is_colorful: bool
    colorful_percentage: float
    message: str


class FolderProcessResult(BaseModel):
    """Folder processing result."""
    total: int
    colorful_count: int
    bw_count: int
    colorful_files: list[str]
    bw_files: list[str]
