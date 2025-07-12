"""
Constants and configuration values for the application
"""

# Application Info
APP_NAME = "AutoEdit Video UI Desktop"
APP_VERSION = "1.0.0"
APP_AUTHOR = "VideoForge Team"

# Video Formats
SUPPORTED_VIDEO_FORMATS = [
    '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'
]

VIDEO_QUALITIES = {
    'LOW': 'low',
    'MEDIUM': 'medium', 
    'HIGH': 'high',
    'ULTRA': 'ultra'
}

# UI Constants
DEFAULT_WINDOW_SIZE = (1200, 800)
MIN_WINDOW_SIZE = (800, 600)
DEFAULT_SIDEBAR_WIDTH = 250

# Processing
MAX_CONCURRENT_PROCESSES = 2
PROGRESS_UPDATE_INTERVAL = 1000  # milliseconds
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

# VideoForge Integration
VIDEOFORGE_DEFAULT_HOST = "localhost"
VIDEOFORGE_DEFAULT_PORT = 8000
API_TIMEOUT = 30

# Themes
AVAILABLE_THEMES = ['light', 'dark']
DEFAULT_THEME = 'light'

# File Paths
TEMP_DIR = 'temp'
CONFIG_DIR = 'config'
RESOURCES_DIR = 'resources'
