"""
Default configuration settings for VideoForge
"""

# Default processing configuration
DEFAULT_PROCESSING_CONFIG = {
    "max_concurrent_jobs": 4,
    "temp_directory": "./temp",
    "output_quality": "high",
    "preserve_metadata": True,
    "auto_cleanup": True,
    "chunk_size": 1024,
    "memory_limit": "2GB"
}

# Default AI configuration
DEFAULT_AI_CONFIG = {
    "speech_recognition": True,
    "whisper_model": "base",
    "whisper_device": "auto",
    "subtitle_language": "vi",
    "translation_service": "google",
    "logo_detection": True,
    "logo_detection_threshold": 0.7,
    "scene_detection": True,
    "scene_detection_threshold": 0.3
}

# Default video configuration
DEFAULT_VIDEO_CONFIG = {
    "default_codec": "libx264",
    "default_audio_codec": "aac",
    "gpu_acceleration": "auto",
    "hardware_encoder": "auto",
    "pixel_format": "yuv420p",
    "audio_sample_rate": 48000,
    "audio_bitrate": "128k"
}

# Processing profiles for different platforms
PROCESSING_PROFILES = {
    "youtube_shorts": {
        "name": "YouTube Shorts",
        "description": "Optimized for YouTube Shorts vertical videos",
        "resolution": "1080x1920",
        "aspect_ratio": "9:16",
        "max_duration": 60,
        "fps": 30,
        "video_codec": "libx264",
        "audio_codec": "aac",
        "quality": "high",
        "auto_subtitle": True,
        "subtitle_language": "vi",
        "target_bitrate": "2M"
    },
    "instagram_reels": {
        "name": "Instagram Reels",
        "description": "Optimized for Instagram Reels",
        "resolution": "1080x1920",
        "aspect_ratio": "9:16",
        "max_duration": 90,
        "fps": 30,
        "video_codec": "libx264",
        "audio_codec": "aac",
        "quality": "high",
        "auto_subtitle": True,
        "brightness": 5,
        "contrast": 10,
        "saturation": 15,
        "target_bitrate": "3M"
    },
    "tiktok": {
        "name": "TikTok",
        "description": "Optimized for TikTok videos",
        "resolution": "1080x1920",
        "aspect_ratio": "9:16",
        "max_duration": 180,
        "fps": 30,
        "video_codec": "libx264",
        "audio_codec": "aac",
        "quality": "medium",
        "auto_subtitle": True,
        "speed": 1.1,
        "target_bitrate": "2M"
    },
    "facebook_video": {
        "name": "Facebook Video",
        "description": "Optimized for Facebook video posts",
        "resolution": "1920x1080",
        "aspect_ratio": "16:9",
        "fps": 30,
        "video_codec": "libx264",
        "audio_codec": "aac",
        "quality": "high",
        "auto_subtitle": True,
        "target_bitrate": "4M"
    },
    "twitter_video": {
        "name": "Twitter Video",
        "description": "Optimized for Twitter video posts",
        "resolution": "1280x720",
        "aspect_ratio": "16:9",
        "max_duration": 140,
        "fps": 30,
        "video_codec": "libx264",
        "audio_codec": "aac",
        "quality": "medium",
        "target_bitrate": "2M"
    },
    "linkedin_video": {
        "name": "LinkedIn Video",
        "description": "Optimized for LinkedIn video posts",
        "resolution": "1920x1080",
        "aspect_ratio": "16:9",
        "max_duration": 600,
        "fps": 30,
        "video_codec": "libx264",
        "audio_codec": "aac",
        "quality": "high",
        "auto_subtitle": True,
        "target_bitrate": "5M"
    },
    "compress_web": {
        "name": "Web Optimized",
        "description": "Compressed for web streaming",
        "resolution": "1280x720",
        "aspect_ratio": "16:9",
        "fps": 30,
        "video_codec": "libx264",
        "audio_codec": "aac",
        "quality": "medium",
        "target_bitrate": "1.5M"
    }
}

# Quality presets
QUALITY_PRESETS = {
    "low": {
        "crf": 28,
        "preset": "fast",
        "profile": "baseline",
        "level": "3.0",
        "max_bitrate": "1M",
        "buffer_size": "2M"
    },
    "medium": {
        "crf": 23,
        "preset": "medium",
        "profile": "main",
        "level": "3.1",
        "max_bitrate": "3M",
        "buffer_size": "6M"
    },
    "high": {
        "crf": 18,
        "preset": "slow",
        "profile": "high",
        "level": "4.0",
        "max_bitrate": "8M",
        "buffer_size": "16M"
    },
    "ultra": {
        "crf": 15,
        "preset": "veryslow",
        "profile": "high",
        "level": "4.1",
        "max_bitrate": "15M",
        "buffer_size": "30M"
    }
}

# Supported formats
SUPPORTED_VIDEO_FORMATS = [
    '.mp4', '.avi', '.mov', '.mkv', '.webm', 
    '.flv', '.wmv', '.m4v', '.3gp', '.ogv'
]

SUPPORTED_AUDIO_FORMATS = [
    '.mp3', '.wav', '.aac', '.ogg', '.flac', 
    '.m4a', '.wma', '.opus'
]

SUPPORTED_SUBTITLE_FORMATS = [
    '.srt', '.vtt', '.ass', '.ssa', '.sub'
]
