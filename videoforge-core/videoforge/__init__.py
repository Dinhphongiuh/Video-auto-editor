"""
VideoForge Core - Professional Video Processing Engine

This package provides a comprehensive video processing solution with AI capabilities.
"""

__version__ = "0.1.0"
__author__ = "VideoForge Team"
__email__ = "contact@videoforge.com"
__description__ = "Professional Video Processing Engine with AI capabilities"

from .core.video_processor import VideoProcessor
from .core.batch_manager import BatchManager
from .utils.config_loader import ConfigLoader
from .utils.logger import get_logger

# Main exports
__all__ = [
    "VideoProcessor",
    "BatchManager", 
    "ConfigLoader",
    "get_logger",
    "__version__",
]

# Initialize default logger
logger = get_logger(__name__)
logger.info(f"VideoForge Core v{__version__} initialized")
