"""
Input validation utilities for VideoForge
"""

import os
from pathlib import Path
from typing import Union, List, Optional
from ..utils.logger import get_logger

logger = get_logger(__name__)


def validate_input_path(path: Union[str, Path]) -> bool:
    """
    Validate input file or directory path
    
    Args:
        path: Path to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        path = Path(path)
        
        if not path.exists():
            logger.error(f"Input path does not exist: {path}")
            return False
        
        if path.is_file():
            # Validate file extension
            if path.suffix.lower() not in ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv']:
                logger.error(f"Unsupported file format: {path.suffix}")
                return False
            
            # Check file size (not empty)
            if path.stat().st_size == 0:
                logger.error(f"Input file is empty: {path}")
                return False
        
        elif path.is_dir():
            # Check if directory contains video files
            video_files = list(path.rglob('*.mp4')) + list(path.rglob('*.avi')) + \
                         list(path.rglob('*.mov')) + list(path.rglob('*.mkv')) + \
                         list(path.rglob('*.webm')) + list(path.rglob('*.flv')) + \
                         list(path.rglob('*.wmv'))
            
            if not video_files:
                logger.warning(f"No video files found in directory: {path}")
                return False
        
        else:
            logger.error(f"Input path is neither file nor directory: {path}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error validating input path: {e}")
        return False


def validate_output_path(path: Union[str, Path]) -> bool:
    """
    Validate output directory path
    
    Args:
        path: Output path to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        path = Path(path)
        
        # Check if parent directory exists or can be created
        if path.is_file():
            parent_dir = path.parent
        else:
            parent_dir = path
        
        # Try to create directory if it doesn't exist
        try:
            parent_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            logger.error(f"Permission denied creating output directory: {parent_dir}")
            return False
        except OSError as e:
            logger.error(f"Cannot create output directory: {parent_dir} - {e}")
            return False
        
        # Check write permissions
        if not os.access(parent_dir, os.W_OK):
            logger.error(f"No write permission for output directory: {parent_dir}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error validating output path: {e}")
        return False


def validate_resolution(resolution: str) -> bool:
    """
    Validate resolution string format
    
    Args:
        resolution: Resolution string (e.g., "1920x1080")
        
    Returns:
        True if valid, False otherwise
    """
    try:
        if not isinstance(resolution, str):
            return False
        
        parts = resolution.split('x')
        if len(parts) != 2:
            return False
        
        width, height = parts
        width_int = int(width)
        height_int = int(height)
        
        # Check reasonable bounds
        if width_int < 64 or width_int > 7680:  # 64p to 8K width
            logger.error(f"Invalid width: {width_int}")
            return False
        
        if height_int < 64 or height_int > 4320:  # 64p to 8K height
            logger.error(f"Invalid height: {height_int}")
            return False
        
        return True
        
    except ValueError:
        logger.error(f"Invalid resolution format: {resolution}")
        return False
    except Exception as e:
        logger.error(f"Error validating resolution: {e}")
        return False


def validate_aspect_ratio(aspect_ratio: str) -> bool:
    """
    Validate aspect ratio string format
    
    Args:
        aspect_ratio: Aspect ratio string (e.g., "16:9")
        
    Returns:
        True if valid, False otherwise
    """
    try:
        if not isinstance(aspect_ratio, str):
            return False
        
        parts = aspect_ratio.split(':')
        if len(parts) != 2:
            return False
        
        width_ratio, height_ratio = parts
        width_float = float(width_ratio)
        height_float = float(height_ratio)
        
        # Check reasonable bounds
        if width_float <= 0 or height_float <= 0:
            logger.error(f"Invalid aspect ratio values: {width_float}:{height_float}")
            return False
        
        # Check if ratio is reasonable (between 0.1 and 10)
        ratio = width_float / height_float
        if ratio < 0.1 or ratio > 10:
            logger.error(f"Extreme aspect ratio: {ratio}")
            return False
        
        return True
        
    except ValueError:
        logger.error(f"Invalid aspect ratio format: {aspect_ratio}")
        return False
    except Exception as e:
        logger.error(f"Error validating aspect ratio: {e}")
        return False


def validate_speed(speed: float) -> bool:
    """
    Validate speed multiplier
    
    Args:
        speed: Speed multiplier
        
    Returns:
        True if valid, False otherwise
    """
    try:
        if not isinstance(speed, (int, float)):
            return False
        
        # Check reasonable bounds
        if speed < 0.1 or speed > 10.0:
            logger.error(f"Speed out of range: {speed}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error validating speed: {e}")
        return False


def validate_quality(quality: str) -> bool:
    """
    Validate quality setting
    
    Args:
        quality: Quality setting
        
    Returns:
        True if valid, False otherwise
    """
    valid_qualities = ['low', 'medium', 'high', 'ultra']
    
    if quality not in valid_qualities:
        logger.error(f"Invalid quality setting: {quality}. Must be one of: {valid_qualities}")
        return False
    
    return True


def validate_color_adjustment(value: int) -> bool:
    """
    Validate color adjustment value (brightness, contrast, saturation)
    
    Args:
        value: Color adjustment value
        
    Returns:
        True if valid, False otherwise
    """
    try:
        if not isinstance(value, int):
            return False
        
        # Color adjustments should be between -100 and 100
        if value < -100 or value > 100:
            logger.error(f"Color adjustment out of range: {value}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error validating color adjustment: {e}")
        return False


def validate_threads(threads: int) -> bool:
    """
    Validate thread count
    
    Args:
        threads: Number of threads
        
    Returns:
        True if valid, False otherwise
    """
    try:
        if not isinstance(threads, int):
            return False
        
        if threads < 1 or threads > 32:  # Reasonable thread limit
            logger.error(f"Thread count out of range: {threads}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error validating thread count: {e}")
        return False


def validate_file_list(file_list: List[str]) -> List[str]:
    """
    Validate and filter a list of file paths
    
    Args:
        file_list: List of file paths
        
    Returns:
        List of valid file paths
    """
    valid_files = []
    
    for file_path in file_list:
        if validate_input_path(file_path):
            valid_files.append(file_path)
        else:
            logger.warning(f"Skipping invalid file: {file_path}")
    
    return valid_files


def validate_profile_name(profile: str, available_profiles: List[str]) -> bool:
    """
    Validate profile name
    
    Args:
        profile: Profile name
        available_profiles: List of available profile names
        
    Returns:
        True if valid, False otherwise
    """
    if profile not in available_profiles:
        logger.error(f"Invalid profile: {profile}. Available profiles: {available_profiles}")
        return False
    
    return True


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Characters not allowed in filenames
    invalid_chars = '<>:"/\\|?*'
    
    # Replace invalid characters with underscore
    sanitized = filename
    for char in invalid_chars:
        sanitized = sanitized.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(' .')
    
    # Ensure filename is not empty
    if not sanitized:
        sanitized = "untitled"
    
    # Limit filename length
    if len(sanitized) > 255:
        name_part = sanitized[:251]
        extension = Path(filename).suffix[:4]  # Keep extension
        sanitized = name_part + extension
    
    return sanitized


def check_disk_space(path: Union[str, Path], required_space: int) -> bool:
    """
    Check if there's enough disk space
    
    Args:
        path: Path to check
        required_space: Required space in bytes
        
    Returns:
        True if enough space, False otherwise
    """
    try:
        path = Path(path)
        
        # Get parent directory if path is a file
        if path.is_file():
            check_path = path.parent
        else:
            check_path = path
        
        # Get free space
        if hasattr(os, 'statvfs'):  # Unix
            stat = os.statvfs(check_path)
            free_space = stat.f_bavail * stat.f_frsize
        else:  # Windows
            import shutil
            free_space = shutil.disk_usage(check_path).free
        
        if free_space < required_space:
            logger.error(f"Insufficient disk space. Required: {required_space/1024/1024:.1f}MB, Available: {free_space/1024/1024:.1f}MB")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error checking disk space: {e}")
        return False


def validate_processing_options(options: dict) -> dict:
    """
    Validate all processing options
    
    Args:
        options: Dictionary of processing options
        
    Returns:
        Dictionary of validated options (invalid options removed)
    """
    validated = {}
    
    # Resolution
    if 'resolution' in options and options['resolution']:
        if validate_resolution(options['resolution']):
            validated['resolution'] = options['resolution']
    
    # Aspect ratio
    if 'aspect_ratio' in options and options['aspect_ratio']:
        if validate_aspect_ratio(options['aspect_ratio']):
            validated['aspect_ratio'] = options['aspect_ratio']
    
    # Speed
    if 'speed' in options and options['speed'] is not None:
        if validate_speed(options['speed']):
            validated['speed'] = options['speed']
    
    # Quality
    if 'quality' in options and options['quality']:
        if validate_quality(options['quality']):
            validated['quality'] = options['quality']
    
    # Color adjustments
    for color_param in ['brightness', 'contrast', 'saturation']:
        if color_param in options and options[color_param] is not None:
            if validate_color_adjustment(options[color_param]):
                validated[color_param] = options[color_param]
    
    # Threads
    if 'threads' in options and options['threads'] is not None:
        if validate_threads(options['threads']):
            validated['threads'] = options['threads']
    
    # Boolean options (no validation needed, just copy)
    boolean_options = ['auto_subtitle', 'remove_logo', 'gpu', 'dry_run']
    for bool_option in boolean_options:
        if bool_option in options:
            validated[bool_option] = bool(options[bool_option])
    
    # String options (copy as-is)
    string_options = ['profile', 'video_codec', 'audio_codec', 'bitrate']
    for str_option in string_options:
        if str_option in options and options[str_option]:
            validated[str_option] = str(options[str_option])
    
    return validated
