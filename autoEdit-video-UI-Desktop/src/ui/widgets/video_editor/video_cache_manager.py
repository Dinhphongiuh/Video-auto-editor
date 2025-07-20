"""
Video Cache Manager
Manages frame caching for smooth playback
"""

from PyQt6.QtCore import QObject, QTimer
from PyQt6.QtGui import QPixmap
from collections import OrderedDict
import threading


class VideoCacheManager(QObject):
    """Manages video frame caching"""

    def __init__(self, max_cache_size=100, parent=None):
        super().__init__(parent)
        self.max_cache_size = max_cache_size
        self.frame_cache = OrderedDict()  # frame_number -> QPixmap
        self.preload_range = 10  # Preload frames around current position
        self.cache_lock = threading.Lock()

        # Cleanup timer
        self.cleanup_timer = QTimer()
        self.cleanup_timer.timeout.connect(self.cleanup_old_frames)
        self.cleanup_timer.start(5000)  # Cleanup every 5 seconds

    def cache_frame(self, frame_number, pixmap):
        """Cache a frame"""
        with self.cache_lock:
            # Remove oldest frames if cache is full
            while len(self.frame_cache) >= self.max_cache_size:
                self.frame_cache.popitem(last=False)

            # Add new frame
            self.frame_cache[frame_number] = pixmap

    def get_cached_frame(self, frame_number):
        """Get cached frame"""
        with self.cache_lock:
            if frame_number in self.frame_cache:
                # Move to end (most recently used)
                pixmap = self.frame_cache.pop(frame_number)
                self.frame_cache[frame_number] = pixmap
                return pixmap
            return None

    def is_frame_cached(self, frame_number):
        """Check if frame is cached"""
        with self.cache_lock:
            return frame_number in self.frame_cache

    def preload_frames(self, current_frame, total_frames):
        """Mark frames for preloading"""
        start_frame = max(0, current_frame - self.preload_range)
        end_frame = min(total_frames, current_frame + self.preload_range)

        preload_list = []
        for frame_num in range(start_frame, end_frame):
            if not self.is_frame_cached(frame_num):
                preload_list.append(frame_num)

        return preload_list

    def cleanup_old_frames(self):
        """Cleanup old cached frames"""
        with self.cache_lock:
            # Keep only the most recent frames
            while len(self.frame_cache) > self.max_cache_size * 0.8:
                self.frame_cache.popitem(last=False)

    def clear_cache(self):
        """Clear all cached frames"""
        with self.cache_lock:
            self.frame_cache.clear()

    def get_cache_info(self):
        """Get cache statistics"""
        with self.cache_lock:
            return {
                "cached_frames": len(self.frame_cache),
                "max_size": self.max_cache_size,
                "usage_percent": (len(self.frame_cache) / self.max_cache_size) * 100,
            }
