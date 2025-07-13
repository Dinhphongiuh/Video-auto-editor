"""
Helper Functions - Utility functions for common operations
"""

import os
from pathlib import Path
from typing import List, Optional

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def format_duration(seconds: float) -> str:
    """Format duration in HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"

def get_file_extension(file_path: Path) -> str:
    """Get file extension in lowercase"""
    return file_path.suffix.lower()

def is_video_file(file_path: Path) -> bool:
    """Check if file is a supported video format"""
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
    return get_file_extension(file_path) in video_extensions

def create_directory(directory: Path) -> bool:
    """Create directory if it doesn't exist"""
    try:
        directory.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {directory}: {e}")
        return False

def safe_delete_file(file_path: Path) -> bool:
    """Safely delete file"""
    try:
        if file_path.exists():
            file_path.unlink()
        return True
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
        return False

def generate_unique_filename(base_path: Path, suffix: str = "") -> Path:
    """Generate unique filename by adding number suffix"""
    counter = 1
    original_stem = base_path.stem
    extension = base_path.suffix
    
    new_path = base_path
    while new_path.exists():
        if suffix:
            new_stem = f"{original_stem}_{suffix}_{counter}"
        else:
            new_stem = f"{original_stem}_{counter}"
        new_path = base_path.parent / f"{new_stem}{extension}"
        counter += 1
    
    return new_path

def validate_path(path: str) -> bool:
    """Validate if path is valid"""
    try:
        Path(path)
        return True
    except Exception:
        return False

def get_available_space(path: Path) -> int:
    """Get available disk space in bytes"""
    try:
        stat = os.statvfs(path)
        return stat.f_bavail * stat.f_frsize
    except Exception:
        return 0
