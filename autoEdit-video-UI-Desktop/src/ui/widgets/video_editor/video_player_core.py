"""
Video Player Core Engine
OpenCV-based video player with frame management
"""

import cv2
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, QMutex, QMutexLocker
from PyQt6.QtGui import QImage, QPixmap
import os
import time


class VideoPlayerCore(QThread):
    """Core video player engine using OpenCV"""

    # Signals
    frame_ready = pyqtSignal(QPixmap)
    position_changed = pyqtSignal(float)  # Current position in seconds
    duration_changed = pyqtSignal(float)  # Total duration in seconds
    playback_finished = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_capture = None
        self.video_path = None
        self.is_playing = False
        self.is_paused = False
        self.should_stop = False
        self.current_frame = 0
        self.total_frames = 0
        self.fps = 30.0
        self.duration = 0.0
        self.seek_frame = -1
        self.mutex = QMutex()

    def load_video(self, video_path):
        """Load video file"""
        try:
            if not os.path.exists(video_path):
                self.error_occurred.emit(f"Video file not found: {video_path}")
                return False

            # Release previous video
            if self.video_capture:
                self.video_capture.release()

            # Load new video
            self.video_path = video_path
            self.video_capture = cv2.VideoCapture(video_path)

            if not self.video_capture.isOpened():
                self.error_occurred.emit(f"Cannot open video: {video_path}")
                return False

            # Get video properties
            self.total_frames = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = self.video_capture.get(cv2.CAP_PROP_FPS)
            if self.fps <= 0:
                self.fps = 30.0  # Default FPS

            self.duration = self.total_frames / self.fps if self.fps > 0 else 0
            self.current_frame = 0

            # Emit duration
            self.duration_changed.emit(self.duration)

            # Load first frame
            self.seek_to_frame(0)

            return True

        except Exception as e:
            self.error_occurred.emit(f"Error loading video: {str(e)}")
            return False

    def play(self):
        """Start playback"""
        with QMutexLocker(self.mutex):
            if self.video_capture and self.video_capture.isOpened():
                self.is_playing = True
                self.is_paused = False
                if not self.isRunning():
                    self.start()

    def pause(self):
        """Pause playback"""
        with QMutexLocker(self.mutex):
            self.is_paused = True

    def stop(self):
        """Stop playback"""
        with QMutexLocker(self.mutex):
            self.is_playing = False
            self.is_paused = False
            self.should_stop = True
            self.current_frame = 0

    def seek_to_position(self, position_seconds):
        """Seek to specific position in seconds"""
        if self.video_capture and self.video_capture.isOpened():
            target_frame = int(position_seconds * self.fps)
            target_frame = max(0, min(target_frame, self.total_frames - 1))

            with QMutexLocker(self.mutex):
                self.seek_frame = target_frame

    def seek_to_frame(self, frame_number):
        """Seek to specific frame"""
        if self.video_capture and self.video_capture.isOpened():
            frame_number = max(0, min(frame_number, self.total_frames - 1))

            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = self.video_capture.read()

            if ret:
                self.current_frame = frame_number
                pixmap = self.convert_frame_to_pixmap(frame)
                self.frame_ready.emit(pixmap)

                # Emit position
                position = self.current_frame / self.fps if self.fps > 0 else 0
                self.position_changed.emit(position)

    def convert_frame_to_pixmap(self, frame):
        """Convert OpenCV frame to QPixmap"""
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Get frame dimensions
            height, width, channel = rgb_frame.shape
            bytes_per_line = 3 * width

            # Create QImage
            q_image = QImage(
                rgb_frame.data,
                width,
                height,
                bytes_per_line,
                QImage.Format.Format_RGB888,
            )

            # Convert to QPixmap
            pixmap = QPixmap.fromImage(q_image)

            return pixmap

        except Exception as e:
            print(f"Error converting frame: {e}")
            return QPixmap()

    def run(self):
        """Main playback thread"""
        if not self.video_capture or not self.video_capture.isOpened():
            return

        frame_delay = 1.0 / self.fps if self.fps > 0 else 1.0 / 30.0

        while True:
            with QMutexLocker(self.mutex):
                if self.should_stop:
                    break

                # Handle seeking
                if self.seek_frame >= 0:
                    self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, self.seek_frame)
                    self.current_frame = self.seek_frame
                    self.seek_frame = -1

                if not self.is_playing or self.is_paused:
                    self.msleep(16)  # Sleep for ~60fps
                    continue

            # Read frame
            ret, frame = self.video_capture.read()

            if not ret:
                # End of video
                self.playback_finished.emit()
                break

            # Convert and emit frame
            pixmap = self.convert_frame_to_pixmap(frame)
            self.frame_ready.emit(pixmap)

            # Update position
            self.current_frame = int(self.video_capture.get(cv2.CAP_PROP_POS_FRAMES))
            position = self.current_frame / self.fps if self.fps > 0 else 0
            self.position_changed.emit(position)

            # Frame timing
            time.sleep(frame_delay)

        # Reset state
        with QMutexLocker(self.mutex):
            self.is_playing = False
            self.should_stop = False

    def get_current_position(self):
        """Get current position in seconds"""
        return self.current_frame / self.fps if self.fps > 0 else 0

    def get_duration(self):
        """Get total duration in seconds"""
        return self.duration

    def is_video_loaded(self):
        """Check if video is loaded"""
        return self.video_capture is not None and self.video_capture.isOpened()

    def cleanup(self):
        """Cleanup resources"""
        self.stop()
        if self.isRunning():
            self.wait(3000)  # Wait up to 3 seconds

        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None
