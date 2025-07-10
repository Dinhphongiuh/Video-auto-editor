"""
Progress tracking utilities for VideoForge
"""

import time
from typing import Optional, Callable
from dataclasses import dataclass
from tqdm import tqdm

from .logger import get_logger

logger = get_logger(__name__)


@dataclass
class ProgressInfo:
    """Progress information"""
    current: int
    total: int
    percentage: float
    message: str
    elapsed_time: float
    estimated_total_time: Optional[float] = None
    estimated_remaining_time: Optional[float] = None


class ProgressTracker:
    """Tracks progress of video processing operations"""
    
    def __init__(self, task_name: str, total: int = 100, callback: Optional[Callable] = None):
        """
        Initialize progress tracker
        
        Args:
            task_name: Name of the task being tracked
            total: Total progress units (default 100 for percentage)
            callback: Optional callback function for progress updates
        """
        self.task_name = task_name
        self.total = total
        self.current = 0
        self.start_time = time.time()
        self.callback = callback
        self.message = "Starting..."
        
        # Initialize progress bar
        self.pbar = tqdm(
            total=total,
            desc=task_name,
            unit='%',
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'
        )
        
        logger.debug(f"Progress tracker initialized for: {task_name}")
    
    def update(self, progress: int, message: str = None):
        """
        Update progress
        
        Args:
            progress: Current progress value
            message: Optional status message
        """
        if progress > self.total:
            progress = self.total
        
        if progress < self.current:
            logger.warning(f"Progress went backwards: {progress} < {self.current}")
        
        # Update values
        old_progress = self.current
        self.current = progress
        self.message = message or self.message
        
        # Update progress bar
        self.pbar.update(progress - old_progress)
        if message:
            self.pbar.set_description(f"{self.task_name}: {message}")
        
        # Calculate timing
        elapsed_time = time.time() - self.start_time
        percentage = (progress / self.total) * 100 if self.total > 0 else 0
        
        # Estimate remaining time
        estimated_total_time = None
        estimated_remaining_time = None
        
        if progress > 0 and percentage > 0:
            estimated_total_time = elapsed_time / (percentage / 100)
            estimated_remaining_time = estimated_total_time - elapsed_time
        
        # Create progress info
        progress_info = ProgressInfo(
            current=progress,
            total=self.total,
            percentage=percentage,
            message=self.message,
            elapsed_time=elapsed_time,
            estimated_total_time=estimated_total_time,
            estimated_remaining_time=estimated_remaining_time
        )
        
        # Call callback if provided
        if self.callback:
            try:
                self.callback(progress_info)
            except Exception as e:
                logger.error(f"Error in progress callback: {e}")
        
        # Log significant progress milestones
        if progress % 10 == 0 or progress == self.total:
            logger.debug(f"Progress: {percentage:.1f}% - {self.message}")
    
    def increment(self, amount: int = 1, message: str = None):
        """
        Increment progress by specified amount
        
        Args:
            amount: Amount to increment
            message: Optional status message
        """
        self.update(self.current + amount, message)
    
    def set_message(self, message: str):
        """
        Update status message without changing progress
        
        Args:
            message: Status message
        """
        self.message = message
        self.pbar.set_description(f"{self.task_name}: {message}")
    
    def finish(self, message: str = "Complete"):
        """
        Mark progress as finished
        
        Args:
            message: Final status message
        """
        self.update(self.total, message)
        self.pbar.close()
        
        elapsed_time = time.time() - self.start_time
        logger.info(f"Task '{self.task_name}' completed in {elapsed_time:.2f}s")
    
    def get_progress_info(self) -> ProgressInfo:
        """
        Get current progress information
        
        Returns:
            ProgressInfo object
        """
        elapsed_time = time.time() - self.start_time
        percentage = (self.current / self.total) * 100 if self.total > 0 else 0
        
        estimated_total_time = None
        estimated_remaining_time = None
        
        if self.current > 0 and percentage > 0:
            estimated_total_time = elapsed_time / (percentage / 100)
            estimated_remaining_time = estimated_total_time - elapsed_time
        
        return ProgressInfo(
            current=self.current,
            total=self.total,
            percentage=percentage,
            message=self.message,
            elapsed_time=elapsed_time,
            estimated_total_time=estimated_total_time,
            estimated_remaining_time=estimated_remaining_time
        )
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if exc_type is None:
            self.finish()
        else:
            self.finish("Failed")
            logger.error(f"Task '{self.task_name}' failed: {exc_val}")


class BatchProgressTracker:
    """Tracks progress for batch operations"""
    
    def __init__(self, total_items: int, task_name: str = "Batch Processing"):
        """
        Initialize batch progress tracker
        
        Args:
            total_items: Total number of items to process
            task_name: Name of the batch task
        """
        self.total_items = total_items
        self.completed_items = 0
        self.failed_items = 0
        self.task_name = task_name
        self.start_time = time.time()
        
        # Individual item trackers
        self.current_item_tracker: Optional[ProgressTracker] = None
        
        # Overall progress bar
        self.overall_pbar = tqdm(
            total=total_items,
            desc=task_name,
            unit='files',
            position=0,
            leave=True
        )
        
        logger.info(f"Batch processing started: {total_items} items")
    
    def start_item(self, item_name: str) -> ProgressTracker:
        """
        Start tracking a new item
        
        Args:
            item_name: Name of the item being processed
            
        Returns:
            ProgressTracker for the item
        """
        # Close previous item tracker if exists
        if self.current_item_tracker:
            self.current_item_tracker.pbar.close()
        
        # Create new item tracker
        self.current_item_tracker = ProgressTracker(
            task_name=f"Processing {item_name}",
            total=100
        )
        
        # Update overall description
        self.overall_pbar.set_description(f"{self.task_name}: {item_name}")
        
        return self.current_item_tracker
    
    def complete_item(self, success: bool = True):
        """
        Mark current item as completed
        
        Args:
            success: Whether the item was processed successfully
        """
        if self.current_item_tracker:
            self.current_item_tracker.finish("Complete" if success else "Failed")
            self.current_item_tracker = None
        
        if success:
            self.completed_items += 1
        else:
            self.failed_items += 1
        
        # Update overall progress
        self.overall_pbar.update(1)
        
        # Update description with stats
        self.overall_pbar.set_description(
            f"{self.task_name}: {self.completed_items} completed, {self.failed_items} failed"
        )
        
        logger.debug(f"Item completed. Success: {success}")
    
    def get_summary(self) -> dict:
        """
        Get batch processing summary
        
        Returns:
            Dictionary with batch statistics
        """
        elapsed_time = time.time() - self.start_time
        processed_items = self.completed_items + self.failed_items
        success_rate = (self.completed_items / processed_items * 100) if processed_items > 0 else 0
        
        return {
            'total_items': self.total_items,
            'completed_items': self.completed_items,
            'failed_items': self.failed_items,
            'processed_items': processed_items,
            'remaining_items': self.total_items - processed_items,
            'success_rate': success_rate,
            'elapsed_time': elapsed_time,
            'average_time_per_item': elapsed_time / processed_items if processed_items > 0 else 0
        }
    
    def finish(self):
        """Finish batch processing"""
        if self.current_item_tracker:
            self.current_item_tracker.pbar.close()
        
        self.overall_pbar.close()
        
        summary = self.get_summary()
        logger.info(f"Batch processing completed: {summary['completed_items']}/{summary['total_items']} successful")
