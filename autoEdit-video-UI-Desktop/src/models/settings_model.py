"""
Settings Model - Application settings data model
"""

from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class SettingsModel:
    """Data model for application settings"""
    
    # App Settings
    theme: str = 'light'
    language: str = 'vi'
    auto_save: bool = True
    
    # Window Settings
    window_width: int = 1200
    window_height: int = 800
    window_maximized: bool = False
    sidebar_width: int = 250
    
    # VideoForge Backend
    backend_host: str = 'localhost'
    backend_port: int = 8000
    auto_connect: bool = True
    
    # Processing Settings
    max_concurrent_processes: int = 2
    enable_gpu_acceleration: bool = True
    memory_limit: int = 4096
    temp_directory: str = 'temp'
    
    # File Settings
    max_file_size: int = 500 * 1024 * 1024  # 500MB
    auto_cleanup: bool = True
    thumbnail_cache_size: int = 100
    
    # UI Settings
    show_tooltips: bool = True
    show_statusbar: bool = True
    progress_update_interval: int = 1000
    
    # Export Settings
    default_output_format: str = 'mp4'
    default_quality: str = 'high'
    output_directory: str = ''
    
    # Advanced Settings
    debug_mode: bool = False
    log_level: str = 'INFO'
    custom_settings: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary"""
        return {
            'app': {
                'theme': self.theme,
                'language': self.language,
                'auto_save': self.auto_save,
            },
            'window': {
                'width': self.window_width,
                'height': self.window_height,
                'maximized': self.window_maximized,
                'sidebar_width': self.sidebar_width,
            },
            'backend': {
                'host': self.backend_host,
                'port': self.backend_port,
                'auto_connect': self.auto_connect,
            },
            'processing': {
                'max_concurrent': self.max_concurrent_processes,
                'gpu_acceleration': self.enable_gpu_acceleration,
                'memory_limit': self.memory_limit,
                'temp_directory': self.temp_directory,
            },
            'files': {
                'max_file_size': self.max_file_size,
                'auto_cleanup': self.auto_cleanup,
                'thumbnail_cache_size': self.thumbnail_cache_size,
            },
            'ui': {
                'show_tooltips': self.show_tooltips,
                'show_statusbar': self.show_statusbar,
                'progress_interval': self.progress_update_interval,
            },
            'export': {
                'default_format': self.default_output_format,
                'default_quality': self.default_quality,
                'output_directory': self.output_directory,
            },
            'advanced': {
                'debug_mode': self.debug_mode,
                'log_level': self.log_level,
                'custom': self.custom_settings,
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SettingsModel':
        """Create settings from dictionary"""
        return cls(
            # App settings
            theme=data.get('app', {}).get('theme', 'light'),
            language=data.get('app', {}).get('language', 'vi'),
            auto_save=data.get('app', {}).get('auto_save', True),
            
            # Window settings
            window_width=data.get('window', {}).get('width', 1200),
            window_height=data.get('window', {}).get('height', 800),
            window_maximized=data.get('window', {}).get('maximized', False),
            sidebar_width=data.get('window', {}).get('sidebar_width', 250),
            
            # Backend settings
            backend_host=data.get('backend', {}).get('host', 'localhost'),
            backend_port=data.get('backend', {}).get('port', 8000),
            auto_connect=data.get('backend', {}).get('auto_connect', True),
            
            # Processing settings
            max_concurrent_processes=data.get('processing', {}).get('max_concurrent', 2),
            enable_gpu_acceleration=data.get('processing', {}).get('gpu_acceleration', True),
            memory_limit=data.get('processing', {}).get('memory_limit', 4096),
            temp_directory=data.get('processing', {}).get('temp_directory', 'temp'),
            
            # File settings
            max_file_size=data.get('files', {}).get('max_file_size', 500 * 1024 * 1024),
            auto_cleanup=data.get('files', {}).get('auto_cleanup', True),
            thumbnail_cache_size=data.get('files', {}).get('thumbnail_cache_size', 100),
            
            # UI settings
            show_tooltips=data.get('ui', {}).get('show_tooltips', True),
            show_statusbar=data.get('ui', {}).get('show_statusbar', True),
            progress_update_interval=data.get('ui', {}).get('progress_interval', 1000),
            
            # Export settings
            default_output_format=data.get('export', {}).get('default_format', 'mp4'),
            default_quality=data.get('export', {}).get('default_quality', 'high'),
            output_directory=data.get('export', {}).get('output_directory', ''),
            
            # Advanced settings
            debug_mode=data.get('advanced', {}).get('debug_mode', False),
            log_level=data.get('advanced', {}).get('log_level', 'INFO'),
            custom_settings=data.get('advanced', {}).get('custom', {}),
        )
