"""
Batch Manager for processing multiple videos
"""

import os
import concurrent.futures
from pathlib import Path
from typing import List, Dict, Iterator
from dataclasses import dataclass

from .video_processor import VideoProcessor, ProcessingResult, ProcessingOptions
from ..utils.logger import get_logger
from ..utils.progress_tracker import ProgressTracker

logger = get_logger(__name__)


@dataclass
class BatchJob:
    """Represents a batch processing job"""
    input_path: str
    output_path: str
    options: ProcessingOptions
    status: str = "pending"  # pending, processing, completed, failed
    result: ProcessingResult = None


class BatchManager:
    """Manages batch processing of multiple videos"""
    
    def __init__(self, config: Dict):
        """Initialize batch manager"""
        self.config = config
        self.video_processor = VideoProcessor(config)
        self.max_workers = config.get('processing', {}).get('max_concurrent_jobs', 4)
        
    def process_directory(self, input_dir: str, output_dir: str, **kwargs) -> List[ProcessingResult]:
        """
        Process all videos in a directory
        
        Args:
            input_dir: Input directory path
            output_dir: Output directory path
            **kwargs: Processing options
            
        Returns:
            List of ProcessingResult objects
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        # Find all video files
        video_files = self._find_video_files(input_path)
        
        if not video_files:
            logger.warning(f"No video files found in {input_dir}")
            return []
        
        # Create batch jobs
        jobs = self._create_batch_jobs(video_files, input_path, output_path, kwargs)
        
        # Process jobs
        results = self._process_jobs(jobs)
        
        return results
    
    def process_file_list(self, file_list: List[str], output_dir: str, **kwargs) -> List[ProcessingResult]:
        """
        Process a list of video files
        
        Args:
            file_list: List of input file paths
            output_dir: Output directory path
            **kwargs: Processing options
            
        Returns:
            List of ProcessingResult objects
        """
        output_path = Path(output_dir)
        
        # Create batch jobs
        jobs = []
        for input_file in file_list:
            input_path = Path(input_file)
            if input_path.exists() and input_path.suffix.lower() in VideoProcessor.SUPPORTED_FORMATS:
                output_file = output_path / input_path.name
                options = ProcessingOptions(**kwargs)
                jobs.append(BatchJob(
                    input_path=str(input_path),
                    output_path=str(output_file),
                    options=options
                ))
        
        # Process jobs
        results = self._process_jobs(jobs)
        
        return results
    
    def _find_video_files(self, directory: Path) -> List[Path]:
        """Find all video files in directory and subdirectories"""
        video_files = []
        
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in VideoProcessor.SUPPORTED_FORMATS:
                video_files.append(file_path)
        
        logger.info(f"Found {len(video_files)} video files")
        return video_files
    
    def _create_batch_jobs(self, video_files: List[Path], input_base: Path, output_base: Path, options_dict: Dict) -> List[BatchJob]:
        """Create batch jobs from video files"""
        jobs = []
        options = ProcessingOptions(**options_dict)
        
        # Create output directory
        output_base.mkdir(parents=True, exist_ok=True)
        
        for video_file in video_files:
            # Maintain directory structure in output
            relative_path = video_file.relative_to(input_base)
            output_file = output_base / relative_path
            
            # Create output subdirectory if needed
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            jobs.append(BatchJob(
                input_path=str(video_file),
                output_path=str(output_file),
                options=options
            ))
        
        logger.info(f"Created {len(jobs)} batch jobs")
        return jobs
    
    def _process_jobs(self, jobs: List[BatchJob]) -> List[ProcessingResult]:
        """Process batch jobs with concurrent execution"""
        results = []
        
        logger.info(f"Starting batch processing with {self.max_workers} workers")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all jobs
            future_to_job = {
                executor.submit(self._process_single_job, job): job 
                for job in jobs
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_job):
                job = future_to_job[future]
                try:
                    result = future.result()
                    job.result = result
                    job.status = "completed" if result.success else "failed"
                    results.append(result)
                    
                    # Log progress
                    completed = len(results)
                    total = len(jobs)
                    logger.info(f"Progress: {completed}/{total} ({completed/total*100:.1f}%)")
                    
                except Exception as e:
                    logger.error(f"Job failed with exception: {e}")
                    job.status = "failed"
                    result = ProcessingResult(
                        success=False,
                        input_path=job.input_path,
                        error=str(e)
                    )
                    job.result = result
                    results.append(result)
        
        logger.info(f"Batch processing completed. {len(results)} files processed")
        return results
    
    def _process_single_job(self, job: BatchJob) -> ProcessingResult:
        """Process a single batch job"""
        job.status = "processing"
        
        logger.debug(f"Processing: {job.input_path}")
        
        # Convert ProcessingOptions back to dict for video_processor
        options_dict = {
            'resolution': job.options.resolution,
            'aspect_ratio': job.options.aspect_ratio,
            'speed': job.options.speed,
            'profile': job.options.profile,
            'auto_subtitle': job.options.auto_subtitle,
            'remove_logo': job.options.remove_logo,
            'brightness': job.options.brightness,
            'contrast': job.options.contrast,
            'saturation': job.options.saturation,
            'quality': job.options.quality,
            'threads': job.options.threads,
            'gpu': job.options.gpu,
            'dry_run': job.options.dry_run,
            'video_codec': job.options.video_codec,
            'audio_codec': job.options.audio_codec,
            'bitrate': job.options.bitrate,
            'fps': job.options.fps,
            'start_time': job.options.start_time,
            'end_time': job.options.end_time
        }
        
        # Filter out None values
        options_dict = {k: v for k, v in options_dict.items() if v is not None}
        
        result = self.video_processor.process_video(
            input_path=job.input_path,
            output_path=job.output_path,
            **options_dict
        )
        
        return result
    
    def get_progress_iterator(self, jobs: List[BatchJob]) -> Iterator[BatchJob]:
        """Get an iterator that yields job progress updates"""
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all jobs
            future_to_job = {
                executor.submit(self._process_single_job, job): job 
                for job in jobs
            }
            
            # Yield results as they complete
            for future in concurrent.futures.as_completed(future_to_job):
                job = future_to_job[future]
                try:
                    result = future.result()
                    job.result = result
                    job.status = "completed" if result.success else "failed"
                    yield job
                    
                except Exception as e:
                    logger.error(f"Job failed with exception: {e}")
                    job.status = "failed"
                    job.result = ProcessingResult(
                        success=False,
                        input_path=job.input_path,
                        error=str(e)
                    )
                    yield job
