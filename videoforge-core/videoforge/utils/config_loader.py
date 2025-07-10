"""
Configuration loader and manager for VideoForge
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Optional, Any
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ConfigLoader:
    """Manages configuration loading and saving"""
    
    DEFAULT_CONFIG = {
        "processing": {
            "max_concurrent_jobs": 4,
            "temp_directory": "./temp",
            "output_quality": "high",
            "preserve_metadata": True,
            "auto_cleanup": True
        },
        "ai": {
            "speech_recognition": True,
            "whisper_model": "base",
            "subtitle_language": "vi",
            "translation_service": "google",
            "logo_detection": True,
            "scene_detection": True
        },
        "video": {
            "default_codec": "libx264",
            "default_audio_codec": "aac",
            "gpu_acceleration": "auto",
            "quality_presets": {
                "low": {"crf": 28, "preset": "fast"},
                "medium": {"crf": 23, "preset": "medium"},
                "high": {"crf": 18, "preset": "slow"},
                "ultra": {"crf": 15, "preset": "veryslow"}
            }
        },
        "profiles": {
            "youtube_shorts": {
                "resolution": "1080x1920",
                "aspect_ratio": "9:16",
                "max_duration": 60,
                "auto_subtitle": True,
                "subtitle_language": "vi",
                "quality": "high"
            },
            "instagram_reels": {
                "resolution": "1080x1920", 
                "aspect_ratio": "9:16",
                "max_duration": 90,
                "auto_subtitle": True,
                "brightness": 5,
                "contrast": 10,
                "saturation": 15,
                "quality": "high"
            },
            "tiktok": {
                "resolution": "1080x1920",
                "aspect_ratio": "9:16", 
                "max_duration": 180,
                "auto_subtitle": True,
                "speed": 1.1,
                "quality": "medium"
            },
            "facebook_video": {
                "resolution": "1920x1080",
                "aspect_ratio": "16:9",
                "auto_subtitle": True,
                "quality": "high"
            },
            "twitter_video": {
                "resolution": "1280x720",
                "aspect_ratio": "16:9",
                "max_duration": 140,
                "quality": "medium"
            },
            "linkedin_video": {
                "resolution": "1920x1080",
                "aspect_ratio": "16:9",
                "max_duration": 600,
                "auto_subtitle": True,
                "quality": "high"
            }
        },
        "logging": {
            "level": "INFO",
            "file": "videoforge.log",
            "colors": True,
            "max_file_size": "10MB",
            "backup_count": 3
        },
        "api": {
            "host": "localhost",
            "port": 8080,
            "cors_origins": ["*"],
            "max_upload_size": "2GB"
        },
        "paths": {
            "ffmpeg_path": None,
            "temp_directory": None,
            "models_directory": None
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize config loader
        
        Args:
            config_path: Optional path to config file
        """
        self.config_path = self._get_config_path(config_path)
        self.config = self.DEFAULT_CONFIG.copy()
        
    def _get_config_path(self, custom_path: Optional[str] = None) -> Path:
        """Get configuration file path"""
        
        if custom_path:
            return Path(custom_path)
        
        # Default config locations by platform
        if sys.platform == 'win32':
            config_dir = Path(os.environ.get('APPDATA', '')) / 'VideoForge'
        elif sys.platform == 'darwin':
            config_dir = Path.home() / 'Library' / 'Application Support' / 'VideoForge'
        else:
            config_dir = Path.home() / '.config' / 'VideoForge'
        
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / 'config.json'
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file
        
        Returns:
            Configuration dictionary
        """
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                
                # Merge with default config
                self.config = self._merge_configs(self.DEFAULT_CONFIG, user_config)
                logger.info(f"Configuration loaded from {self.config_path}")
            else:
                # Create default config file
                self.save_config()
                logger.info(f"Created default configuration at {self.config_path}")
                
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            logger.info("Using default configuration")
        
        # Validate and post-process config
        self._validate_config()
        self._post_process_config()
        
        return self.config
    
    def save_config(self, config: Optional[Dict] = None) -> bool:
        """
        Save configuration to file
        
        Args:
            config: Optional configuration to save (uses current if None)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if config:
                self.config = config
            
            # Ensure config directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Configuration saved to {self.config_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        
        Args:
            key: Configuration key (e.g., 'ai.whisper_model')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """
        Set configuration value using dot notation
        
        Args:
            key: Configuration key (e.g., 'ai.whisper_model')
            value: Value to set
            
        Returns:
            True if successful, False otherwise
        """
        keys = key.split('.')
        config = self.config
        
        try:
            # Navigate to parent of target key
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            # Set the value
            config[keys[-1]] = value
            return True
            
        except Exception as e:
            logger.error(f"Error setting config value {key}: {e}")
            return False
    
    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """Recursively merge user config with default config"""
        result = default.copy()
        
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _validate_config(self):
        """Validate configuration values"""
        
        # Validate processing settings
        max_jobs = self.get('processing.max_concurrent_jobs', 4)
        if not isinstance(max_jobs, int) or max_jobs < 1:
            logger.warning("Invalid max_concurrent_jobs, using default: 4")
            self.set('processing.max_concurrent_jobs', 4)
        
        # Validate AI settings
        whisper_models = ['tiny', 'base', 'small', 'medium', 'large']
        whisper_model = self.get('ai.whisper_model', 'base')
        if whisper_model not in whisper_models:
            logger.warning(f"Invalid whisper_model '{whisper_model}', using 'base'")
            self.set('ai.whisper_model', 'base')
        
        # Validate quality presets
        required_preset_keys = ['crf', 'preset']
        for preset_name, preset_config in self.get('video.quality_presets', {}).items():
            if not all(key in preset_config for key in required_preset_keys):
                logger.warning(f"Invalid quality preset '{preset_name}', missing required keys")
    
    def _post_process_config(self):
        """Post-process configuration after loading"""
        
        # Set up temp directory
        temp_dir = self.get('processing.temp_directory')
        if temp_dir == './temp':
            # Use system temp directory
            import tempfile
            temp_dir = tempfile.gettempdir()
            self.set('processing.temp_directory', temp_dir)
        
        # Auto-detect GPU acceleration
        gpu_acceleration = self.get('video.gpu_acceleration')
        if gpu_acceleration == 'auto':
            gpu_available = self._detect_gpu()
            self.set('video.gpu_acceleration', gpu_available)
        
        # Validate paths
        self._validate_paths()
    
    def _detect_gpu(self) -> bool:
        """Detect if GPU acceleration is available"""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            try:
                import subprocess
                result = subprocess.run(['nvidia-smi'], capture_output=True)
                return result.returncode == 0
            except FileNotFoundError:
                return False
    
    def _validate_paths(self):
        """Validate and auto-detect system paths"""
        
        # FFmpeg path
        ffmpeg_path = self.get('paths.ffmpeg_path')
        if not ffmpeg_path:
            ffmpeg_path = self._find_ffmpeg()
            self.set('paths.ffmpeg_path', ffmpeg_path)
        
        # Models directory
        models_dir = self.get('paths.models_directory')
        if not models_dir:
            if sys.platform == 'win32':
                models_dir = Path(os.environ.get('APPDATA', '')) / 'VideoForge' / 'models'
            elif sys.platform == 'darwin':
                models_dir = Path.home() / 'Library' / 'Application Support' / 'VideoForge' / 'models'
            else:
                models_dir = Path.home() / '.config' / 'VideoForge' / 'models'
            
            models_dir.mkdir(parents=True, exist_ok=True)
            self.set('paths.models_directory', str(models_dir))
    
    def _find_ffmpeg(self) -> Optional[str]:
        """Find FFmpeg executable in system PATH"""
        import subprocess
        
        try:
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True)
            if result.returncode == 0:
                return 'ffmpeg'  # Available in PATH
        except FileNotFoundError:
            pass
        
        # Common installation paths
        common_paths = [
            '/usr/bin/ffmpeg',
            '/usr/local/bin/ffmpeg',
            'C:\\ffmpeg\\bin\\ffmpeg.exe',
            'C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe'
        ]
        
        for path in common_paths:
            if Path(path).exists():
                return path
        
        logger.warning("FFmpeg not found in system PATH or common locations")
        return None
    
    def reset_to_defaults(self) -> bool:
        """Reset configuration to default values"""
        try:
            self.config = self.DEFAULT_CONFIG.copy()
            self.save_config()
            logger.info("Configuration reset to defaults")
            return True
        except Exception as e:
            logger.error(f"Error resetting configuration: {e}")
            return False
    
    def export_config(self, export_path: str) -> bool:
        """Export current configuration to file"""
        try:
            export_path = Path(export_path)
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"Configuration exported to {export_path}")
            return True
        except Exception as e:
            logger.error(f"Error exporting configuration: {e}")
            return False
    
    def import_config(self, import_path: str) -> bool:
        """Import configuration from file"""
        try:
            import_path = Path(import_path)
            if not import_path.exists():
                logger.error(f"Import file not found: {import_path}")
                return False
            
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            self.config = self._merge_configs(self.DEFAULT_CONFIG, imported_config)
            self._validate_config()
            self._post_process_config()
            self.save_config()
            
            logger.info(f"Configuration imported from {import_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error importing configuration: {e}")
            return False
