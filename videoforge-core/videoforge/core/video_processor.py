"""
Main Video Processing Engine for VideoForge
"""

import os
import time
import tempfile
from pathlib import Path
from typing import Dict, Optional, Union, List
from dataclasses import dataclass, asdict
import ffmpeg
import cv2
import numpy as np
from PIL import Image, ImageEnhance

from ..utils.logger import get_logger
from ..utils.progress_tracker import ProgressTracker

# Optional AI imports - will be loaded only if available
try:
    from ..ai.speech_recognition import SpeechRecognizer
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SpeechRecognizer = None
    SPEECH_RECOGNITION_AVAILABLE = False

try:
    from ..ai.logo_detection import LogoDetector
    LOGO_DETECTION_AVAILABLE = True
except ImportError:
    LogoDetector = None
    LOGO_DETECTION_AVAILABLE = False

logger = get_logger(__name__)


@dataclass
class ProcessingResult:
    """Result of video processing operation"""
    success: bool
    input_path: str
    output_path: Optional[str] = None
    error: Optional[str] = None
    processing_time: float = 0.0
    file_size_before: int = 0
    file_size_after: int = 0
    metadata: Dict = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class ProcessingOptions:
    """Video processing options"""
    resolution: Optional[str] = None  # "1920x1080"
    aspect_ratio: Optional[str] = None  # "16:9"
    speed: float = 1.0
    profile: Optional[str] = None
    auto_subtitle: bool = False
    remove_logo: bool = False
    brightness: int = 0
    contrast: int = 0
    saturation: int = 0
    quality: str = "high"
    threads: int = 4
    gpu: bool = False
    dry_run: bool = False
    
    # Advanced options
    video_codec: str = "libx264"
    audio_codec: str = "aac"
    bitrate: Optional[str] = None
    fps: Optional[int] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    
    def __post_init__(self):
        """Validate options after initialization"""
        if self.speed < 0.1 or self.speed > 10.0:
            raise ValueError("Speed must be between 0.1 and 10.0")
        
        if self.brightness < -100 or self.brightness > 100:
            raise ValueError("Brightness must be between -100 and 100")
        
        if self.contrast < -100 or self.contrast > 100:
            raise ValueError("Contrast must be between -100 and 100")
        
        if self.saturation < -100 or self.saturation > 100:
            raise ValueError("Saturation must be between -100 and 100")


class VideoProcessor:
    """Main video processing engine"""
    
    SUPPORTED_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv']
    
    QUALITY_PRESETS = {
        'low': {'crf': 28, 'preset': 'fast'},
        'medium': {'crf': 23, 'preset': 'medium'},
        'high': {'crf': 18, 'preset': 'slow'},
        'ultra': {'crf': 15, 'preset': 'veryslow'}
    }
    
    def __init__(self, config: Dict):
        """Initialize video processor"""
        self.config = config
        
        # Initialize AI modules only if available
        self.speech_recognizer = None
        self.logo_detector = None
        
        if SPEECH_RECOGNITION_AVAILABLE and config.get('ai', {}).get('speech_recognition', True):
            self.speech_recognizer = SpeechRecognizer(config)
            
        if LOGO_DETECTION_AVAILABLE and config.get('ai', {}).get('logo_detection', True):
            self.logo_detector = LogoDetector(config)
        
        # Create temp directory
        self.temp_dir = Path(tempfile.mkdtemp(prefix='videoforge_'))
        logger.info(f"VideoProcessor initialized with temp dir: {self.temp_dir}")
    
    def process_video(self, input_path: str, output_path: str, **kwargs) -> ProcessingResult:
        """
        Process a single video file
        
        Args:
            input_path: Path to input video file
            output_path: Path to output video file
            **kwargs: Processing options
            
        Returns:
            ProcessingResult object with operation details
        """
        start_time = time.time()
        input_path = Path(input_path)
        output_path = Path(output_path)
        
        # Validate input
        if not input_path.exists():
            return ProcessingResult(
                success=False,
                input_path=str(input_path),
                error=f"Input file not found: {input_path}"
            )
        
        if input_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            return ProcessingResult(
                success=False,
                input_path=str(input_path),
                error=f"Unsupported format: {input_path.suffix}"
            )
        
        # Parse options
        options = ProcessingOptions(**kwargs)
        
        if options.dry_run:
            return self._dry_run_analysis(input_path, output_path, options)
        
        try:
            # Create output directory
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Get file size before processing
            file_size_before = input_path.stat().st_size
            
            # Load profile if specified
            if options.profile:
                self._apply_profile(options)
            
            # Process video
            result = self._process_video_internal(input_path, output_path, options)
            
            # Get file size after processing
            file_size_after = 0
            if result.success and Path(result.output_path).exists():
                file_size_after = Path(result.output_path).stat().st_size
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Update result
            result.processing_time = processing_time
            result.file_size_before = file_size_before
            result.file_size_after = file_size_after
            
            logger.info(f"Video processing completed in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            logger.exception(f"Error processing video: {e}")
            return ProcessingResult(
                success=False,
                input_path=str(input_path),
                error=str(e),
                processing_time=time.time() - start_time
            )
    
    def _process_video_internal(self, input_path: Path, output_path: Path, options: ProcessingOptions) -> ProcessingResult:
        """Internal video processing logic"""
        
        try:
            # Step 1: Analyze input video
            metadata = self._get_video_metadata(input_path)
            
            # Step 2: Prepare FFmpeg pipeline
            ffmpeg_input = ffmpeg.input(str(input_path))
            
            # Apply video filters
            video_stream = self._apply_video_filters(ffmpeg_input.video, options, metadata)
            audio_stream = self._apply_audio_filters(ffmpeg_input.audio, options)
            
            # Step 3: Apply quality settings
            quality_settings = self.QUALITY_PRESETS.get(options.quality, self.QUALITY_PRESETS['high'])
            
            # Step 4: Output configuration
            output_args = self._get_output_args(options, quality_settings)
            
            # Step 5: Execute FFmpeg
            output = ffmpeg.output(
                video_stream,
                audio_stream,
                str(output_path),
                **output_args
            )
            
            # Run FFmpeg
            ffmpeg.run(output, overwrite_output=True, quiet=True)
            
            return ProcessingResult(
                success=True,
                input_path=str(input_path),
                output_path=str(output_path),
                metadata=metadata
            )
            
        except ffmpeg.Error as e:
            error_msg = f"FFmpeg error: {e.stderr.decode() if e.stderr else str(e)}"
            logger.error(error_msg)
            return ProcessingResult(
                success=False,
                input_path=str(input_path),
                error=error_msg
            )
            
        except Exception as e:
            logger.exception(f"Unexpected error in video processing: {e}")
            return ProcessingResult(
                success=False,
                input_path=str(input_path),
                error=str(e)
            )
    
    def _apply_video_filters(self, video_stream, options: ProcessingOptions, metadata: Dict):
        """Apply video filters based on options"""
        
        # Resolution change
        if options.resolution:
            width, height = map(int, options.resolution.split('x'))
            video_stream = ffmpeg.filter(video_stream, 'scale', width, height)
        
        # Aspect ratio change
        elif options.aspect_ratio:
            video_stream = self._apply_aspect_ratio(video_stream, options.aspect_ratio, metadata)
        
        # Speed change
        if options.speed != 1.0:
            video_stream = ffmpeg.filter(video_stream, 'setpts', f'{1/options.speed}*PTS')
        
        # Color adjustments
        if any([options.brightness, options.contrast, options.saturation]):
            video_stream = self._apply_color_filters(video_stream, options)
        
        # Frame rate
        if options.fps:
            video_stream = ffmpeg.filter(video_stream, 'fps', fps=options.fps)
        
        return video_stream
    
    def _apply_audio_filters(self, audio_stream, options: ProcessingOptions):
        """Apply audio filters based on options"""
        
        # Speed change affects audio tempo
        if options.speed != 1.0:
            audio_stream = ffmpeg.filter(audio_stream, 'atempo', options.speed)
        
        return audio_stream
    
    def _apply_aspect_ratio(self, video_stream, aspect_ratio: str, metadata: Dict):
        """Apply aspect ratio conversion"""
        
        # Parse aspect ratio
        ratio_parts = aspect_ratio.split(':')
        if len(ratio_parts) != 2:
            raise ValueError(f"Invalid aspect ratio format: {aspect_ratio}")
        
        target_ratio = float(ratio_parts[0]) / float(ratio_parts[1])
        
        # Get current dimensions
        current_width = metadata.get('width', 1920)
        current_height = metadata.get('height', 1080)
        current_ratio = current_width / current_height
        
        if abs(current_ratio - target_ratio) < 0.01:
            return video_stream  # Already correct ratio
        
        # Calculate new dimensions
        if target_ratio > current_ratio:
            # Need to make wider - crop height
            new_height = int(current_width / target_ratio)
            video_stream = ffmpeg.filter(video_stream, 'crop', current_width, new_height)
        else:
            # Need to make taller - crop width  
            new_width = int(current_height * target_ratio)
            video_stream = ffmpeg.filter(video_stream, 'crop', new_width, current_height)
        
        return video_stream
    
    def _apply_color_filters(self, video_stream, options: ProcessingOptions):
        """Apply color correction filters"""
        
        # Build eq filter parameters
        eq_params = []
        
        if options.brightness != 0:
            eq_params.append(f"brightness={options.brightness/100}")
        
        if options.contrast != 0:
            eq_params.append(f"contrast={1 + options.contrast/100}")
        
        if options.saturation != 0:
            eq_params.append(f"saturation={1 + options.saturation/100}")
        
        if eq_params:
            video_stream = ffmpeg.filter(video_stream, 'eq', ':'.join(eq_params))
        
        return video_stream
    
    def _get_video_metadata(self, input_path: Path) -> Dict:
        """Get video metadata using FFprobe"""
        
        try:
            probe = ffmpeg.probe(str(input_path))
            video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
            
            return {
                'duration': float(probe['format']['duration']),
                'width': int(video_info['width']),
                'height': int(video_info['height']),
                'fps': eval(video_info['r_frame_rate']),
                'codec': video_info['codec_name'],
                'bitrate': int(probe['format'].get('bit_rate', 0)),
                'format': probe['format']['format_name']
            }
            
        except Exception as e:
            logger.error(f"Error getting video metadata: {e}")
            return {}
    
    def _get_output_args(self, options: ProcessingOptions, quality_settings: Dict) -> Dict:
        """Get FFmpeg output arguments"""
        
        args = {
            'vcodec': options.video_codec,
            'acodec': options.audio_codec,
            'crf': quality_settings['crf'],
            'preset': quality_settings['preset'],
            'threads': options.threads
        }
        
        # Add bitrate if specified
        if options.bitrate:
            args['video_bitrate'] = options.bitrate
        
        # GPU acceleration
        if options.gpu:
            args['hwaccel'] = 'cuda'
            args['vcodec'] = 'h264_nvenc'
        
        return args
    
    def _apply_profile(self, options: ProcessingOptions):
        """Apply processing profile settings"""
        
        profiles = self.config.get('profiles', {})
        if options.profile not in profiles:
            logger.warning(f"Profile not found: {options.profile}")
            return
        
        profile = profiles[options.profile]
        
        # Apply profile settings (don't override existing options)
        for key, value in profile.items():
            if hasattr(options, key) and getattr(options, key) is None:
                setattr(options, key, value)
    
    def _dry_run_analysis(self, input_path: Path, output_path: Path, options: ProcessingOptions) -> ProcessingResult:
        """Perform dry run analysis without actual processing"""
        
        try:
            metadata = self._get_video_metadata(input_path)
            
            # Estimate output file size and processing time
            estimated_size = self._estimate_output_size(input_path, options, metadata)
            estimated_time = self._estimate_processing_time(metadata, options)
            
            analysis = {
                'input_metadata': metadata,
                'estimated_output_size': estimated_size,
                'estimated_processing_time': estimated_time,
                'operations': self._list_operations(options)
            }
            
            return ProcessingResult(
                success=True,
                input_path=str(input_path),
                output_path=str(output_path),
                metadata=analysis
            )
            
        except Exception as e:
            return ProcessingResult(
                success=False,
                input_path=str(input_path),
                error=f"Dry run analysis failed: {e}"
            )
    
    def _estimate_output_size(self, input_path: Path, options: ProcessingOptions, metadata: Dict) -> int:
        """Estimate output file size"""
        
        input_size = input_path.stat().st_size
        
        # Size factor based on quality
        quality_factors = {
            'low': 0.5,
            'medium': 0.7,
            'high': 1.0,
            'ultra': 1.5
        }
        
        factor = quality_factors.get(options.quality, 1.0)
        
        # Adjust for resolution changes
        if options.resolution:
            new_width, new_height = map(int, options.resolution.split('x'))
            current_pixels = metadata.get('width', 1920) * metadata.get('height', 1080)
            new_pixels = new_width * new_height
            factor *= (new_pixels / current_pixels)
        
        # Adjust for speed changes
        factor *= options.speed
        
        return int(input_size * factor)
    
    def _estimate_processing_time(self, metadata: Dict, options: ProcessingOptions) -> float:
        """Estimate processing time in seconds"""
        
        duration = metadata.get('duration', 60)
        base_factor = 0.5  # Base processing factor (real-time ratio)
        
        # Adjust for quality
        quality_factors = {
            'low': 0.3,
            'medium': 0.5,
            'high': 1.0,
            'ultra': 2.0
        }
        
        factor = quality_factors.get(options.quality, 1.0)
        
        # Add time for AI features
        if options.auto_subtitle:
            factor += 1.0
        
        if options.remove_logo:
            factor += 0.5
        
        return duration * base_factor * factor
    
    def _list_operations(self, options: ProcessingOptions) -> List[str]:
        """List operations that will be performed"""
        
        operations = []
        
        if options.resolution:
            operations.append(f"Change resolution to {options.resolution}")
        
        if options.aspect_ratio:
            operations.append(f"Change aspect ratio to {options.aspect_ratio}")
        
        if options.speed != 1.0:
            operations.append(f"Change speed to {options.speed}x")
        
        if options.auto_subtitle:
            operations.append("Generate automatic subtitles")
        
        if options.remove_logo:
            operations.append("Remove logos automatically")
        
        if any([options.brightness, options.contrast, options.saturation]):
            operations.append("Apply color corrections")
        
        operations.append(f"Encode with {options.quality} quality")
        
        return operations
    
    def __del__(self):
        """Cleanup temporary files"""
        try:
            if hasattr(self, 'temp_dir') and self.temp_dir.exists():
                import shutil
                shutil.rmtree(self.temp_dir)
                logger.debug(f"Cleaned up temp directory: {self.temp_dir}")
        except Exception as e:
            logger.error(f"Error cleaning up temp directory: {e}")
