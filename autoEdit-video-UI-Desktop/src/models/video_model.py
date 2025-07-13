"""
Video Model - Data model for video objects
"""

from dataclasses import dataclass
from typing import Optional
from pathlib import Path

@dataclass
class VideoModel:
    """Data model for video files"""
    
    # Basic Info
    id: str
    name: str
    file_path: Path
    
    # File Properties
    size: int  # bytes
    format: str
    duration: float  # seconds
    
    # Video Properties
    width: int
    height: int
    fps: float
    bitrate: int
    
    # Processing Info
    status: str = 'ready'  # ready, processing, completed, error
    thumbnail_path: Optional[Path] = None
    created_at: Optional[str] = None
    modified_at: Optional[str] = None
    
    def __post_init__(self):
        """Post initialization processing"""
        if isinstance(self.file_path, str):
            self.file_path = Path(self.file_path)
    
    @property
    def resolution(self) -> str:
        """Get resolution string"""
        return f"{self.width}x{self.height}"
    
    @property
    def size_mb(self) -> float:
        """Get file size in MB"""
        return self.size / (1024 * 1024)
    
    @property
    def duration_str(self) -> str:
        """Get formatted duration string"""
        hours = int(self.duration // 3600)
        minutes = int((self.duration % 3600) // 60)
        seconds = int(self.duration % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"
