"""
Logging configuration for VideoForge
"""

import os
import logging
import sys
from pathlib import Path
from typing import Optional
from colorama import Fore, Back, Style, init

# Initialize colorama for Windows
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for different log levels"""
    
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Back.WHITE
    }
    
    def format(self, record):
        # Add color to level name
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{Style.RESET_ALL}"
        
        return super().format(record)


def setup_logging(level: str = "INFO", log_file: Optional[str] = None, use_colors: bool = True) -> logging.Logger:
    """
    Setup logging configuration
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        use_colors: Whether to use colored output
        
    Returns:
        Configured logger
    """
    
    # Convert string level to logging level
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Create logger
    logger = logging.getLogger('videoforge')
    logger.setLevel(numeric_level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatters
    if use_colors:
        console_formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
    else:
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
    
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(numeric_level)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)  # Always log everything to file
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    # Get or create the main logger if it doesn't exist
    main_logger = logging.getLogger('videoforge')
    if not main_logger.handlers:
        # Setup default logging if not already configured
        setup_logging()
    
    # Return child logger
    return logging.getLogger(f'videoforge.{name}')


def configure_logging_from_config(config: dict):
    """
    Configure logging from configuration dictionary
    
    Args:
        config: Configuration dictionary with logging settings
    """
    logging_config = config.get('logging', {})
    
    level = logging_config.get('level', 'INFO')
    log_file = logging_config.get('file')
    use_colors = logging_config.get('colors', True)
    
    # Create log directory if specified
    if log_file:
        # Get user data directory
        if sys.platform == 'win32':
            log_dir = Path(os.environ.get('APPDATA', '')) / 'VideoForge' / 'logs'
        elif sys.platform == 'darwin':
            log_dir = Path.home() / 'Library' / 'Application Support' / 'VideoForge' / 'logs'
        else:
            log_dir = Path.home() / '.config' / 'VideoForge' / 'logs'
        
        log_file = log_dir / log_file
    
    setup_logging(level=level, log_file=log_file, use_colors=use_colors)
