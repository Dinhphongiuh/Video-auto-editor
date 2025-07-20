"""
Video Preview Widget - Updated with Real Video Player
Video preview area with playback and transform controls
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QSlider,
    QSpinBox,
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QPixmap
import os

from .video_player_core import VideoPlayerCore
from .video_frame_widget import VideoFrameWidget
from .video_cache_manager import VideoCacheManager


class VideoPreviewWidget(QWidget):
    """Video preview widget with real video playback"""

    # Signals
    transform_changed = pyqtSignal(dict)  # transform_data
    playback_position_changed = pyqtSignal(float)  # position in seconds

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_media = None
        self.duration = 0.0
        self.transform_data = {
            "position_x": 0,
            "position_y": 0,
            "scale": 100,
            "rotation": 0,
        }

        # Video player components
        self.video_player = VideoPlayerCore()
        self.cache_manager = VideoCacheManager()

        self.setup_ui()
        self.connect_video_signals()

    def setup_ui(self):
        """Setup video preview UI"""
        self.setObjectName("video_preview")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Preview area
        self.preview_area = self.create_preview_area()
        layout.addWidget(self.preview_area)

        # Transform controls
        transform_controls = self.create_transform_controls()
        transform_controls.setFixedHeight(100)
        layout.addWidget(transform_controls)

    def create_preview_area(self):
        """Create main video preview area"""
        preview_frame = QFrame()
        preview_frame.setObjectName("preview_area")
        preview_frame.setMinimumHeight(300)

        layout = QVBoxLayout(preview_frame)
        layout.setContentsMargins(20, 20, 20, 20)

        # Video display area
        self.video_display = VideoFrameWidget()
        self.video_display.setMinimumHeight(250)
        self.video_display.clicked.connect(self.toggle_playback)
        layout.addWidget(self.video_display)

        # Status label
        self.status_label = QLabel("No video loaded")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(
            """
            color: #90A4AE; 
            font-size: 14px; 
            font-weight: 500;
            padding: 10px;
        """
        )
        layout.addWidget(self.status_label)

        return preview_frame

    def create_transform_controls(self):
        """Create transform control panel"""
        controls = QFrame()
        controls.setObjectName("transform_controls")

        layout = QVBoxLayout(controls)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(8)

        # Title
        title = QLabel("🔧 Transform")
        title.setStyleSheet(
            """
            color: #ECEFF1; 
            font-size: 13px; 
            font-weight: bold;
        """
        )
        layout.addWidget(title)

        # Transform controls grid
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(15)

        # Position controls
        pos_group = self.create_position_controls()
        controls_layout.addWidget(pos_group)

        # Scale control
        scale_group = self.create_scale_control()
        controls_layout.addWidget(scale_group)

        # Rotation control
        rotation_group = self.create_rotation_control()
        controls_layout.addWidget(rotation_group)

        controls_layout.addStretch()

        # Reset button
        reset_btn = QPushButton("Reset")
        reset_btn.setObjectName("reset_button")
        reset_btn.setFixedSize(60, 25)
        reset_btn.clicked.connect(self.reset_transform)
        controls_layout.addWidget(reset_btn)

        layout.addLayout(controls_layout)

        return controls

    def create_position_controls(self):
        """Create position X/Y controls"""
        group = QFrame()
        layout = QVBoxLayout(group)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)

        # Label
        label = QLabel("Position")
        label.setStyleSheet("color: #B0BEC5; font-size: 11px; font-weight: 500;")
        layout.addWidget(label)

        # X position
        x_layout = QHBoxLayout()
        x_layout.setSpacing(5)
        x_label = QLabel("X:")
        x_label.setFixedWidth(15)
        x_label.setStyleSheet("color: #ECEFF1; font-size: 10px;")
        x_layout.addWidget(x_label)

        self.pos_x_spin = QSpinBox()
        self.pos_x_spin.setRange(-1000, 1000)
        self.pos_x_spin.setValue(0)
        self.pos_x_spin.setFixedSize(60, 20)
        self.pos_x_spin.valueChanged.connect(self.on_position_x_changed)
        x_layout.addWidget(self.pos_x_spin)

        layout.addLayout(x_layout)

        # Y position
        y_layout = QHBoxLayout()
        y_layout.setSpacing(5)
        y_label = QLabel("Y:")
        y_label.setFixedWidth(15)
        y_label.setStyleSheet("color: #ECEFF1; font-size: 10px;")
        y_layout.addWidget(y_label)

        self.pos_y_spin = QSpinBox()
        self.pos_y_spin.setRange(-1000, 1000)
        self.pos_y_spin.setValue(0)
        self.pos_y_spin.setFixedSize(60, 20)
        self.pos_y_spin.valueChanged.connect(self.on_position_y_changed)
        y_layout.addWidget(self.pos_y_spin)

        layout.addLayout(y_layout)

        return group

    def create_scale_control(self):
        """Create scale control"""
        group = QFrame()
        layout = QVBoxLayout(group)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)

        # Label
        label = QLabel("Scale")
        label.setStyleSheet("color: #B0BEC5; font-size: 11px; font-weight: 500;")
        layout.addWidget(label)

        # Scale slider and spinbox
        scale_layout = QHBoxLayout()
        scale_layout.setSpacing(5)

        self.scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.scale_slider.setRange(10, 500)
        self.scale_slider.setValue(100)
        self.scale_slider.setFixedWidth(80)
        self.scale_slider.valueChanged.connect(self.on_scale_changed)
        scale_layout.addWidget(self.scale_slider)

        self.scale_spin = QSpinBox()
        self.scale_spin.setRange(10, 500)
        self.scale_spin.setValue(100)
        self.scale_spin.setSuffix("%")
        self.scale_spin.setFixedSize(60, 20)
        self.scale_spin.valueChanged.connect(self.on_scale_spin_changed)
        scale_layout.addWidget(self.scale_spin)

        layout.addLayout(scale_layout)

        return group

    def create_rotation_control(self):
        """Create rotation control"""
        group = QFrame()
        layout = QVBoxLayout(group)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)

        # Label
        label = QLabel("Rotation")
        label.setStyleSheet("color: #B0BEC5; font-size: 11px; font-weight: 500;")
        layout.addWidget(label)

        # Rotation slider and spinbox
        rotation_layout = QHBoxLayout()
        rotation_layout.setSpacing(5)

        self.rotation_slider = QSlider(Qt.Orientation.Horizontal)
        self.rotation_slider.setRange(-180, 180)
        self.rotation_slider.setValue(0)
        self.rotation_slider.setFixedWidth(80)
        self.rotation_slider.valueChanged.connect(self.on_rotation_changed)
        rotation_layout.addWidget(self.rotation_slider)

        self.rotation_spin = QSpinBox()
        self.rotation_spin.setRange(-180, 180)
        self.rotation_spin.setValue(0)
        self.rotation_spin.setSuffix("°")
        self.rotation_spin.setFixedSize(60, 20)
        self.rotation_spin.valueChanged.connect(self.on_rotation_spin_changed)
        rotation_layout.addWidget(self.rotation_spin)

        layout.addLayout(rotation_layout)

        return group

    def connect_video_signals(self):
        """Connect video player signals"""
        self.video_player.frame_ready.connect(self.on_frame_ready)
        self.video_player.position_changed.connect(self.on_position_changed)
        self.video_player.duration_changed.connect(self.on_duration_changed)
        self.video_player.playback_finished.connect(self.on_playback_finished)
        self.video_player.error_occurred.connect(self.on_video_error)

    def on_frame_ready(self, pixmap):
        """Handle new video frame"""
        self.video_display.set_frame(pixmap)

    def on_position_changed(self, position):
        """Handle position change"""
        self.playback_position_changed.emit(position)

    def on_duration_changed(self, duration):
        """Handle duration change"""
        self.duration = duration

    def on_playback_finished(self):
        """Handle playback finished"""
        print("Video playback finished")

    def on_video_error(self, error_message):
        """Handle video error"""
        self.status_label.setText(f"Error: {error_message}")
        print(f"Video error: {error_message}")

    def on_position_x_changed(self, value):
        """Handle position X change"""
        self.transform_data["position_x"] = value
        self.update_transform()

    def on_position_y_changed(self, value):
        """Handle position Y change"""
        self.transform_data["position_y"] = value
        self.update_transform()

    def on_scale_changed(self, value):
        """Handle scale slider change"""
        self.scale_spin.blockSignals(True)
        self.scale_spin.setValue(value)
        self.scale_spin.blockSignals(False)
        self.transform_data["scale"] = value
        self.update_transform()

    def on_scale_spin_changed(self, value):
        """Handle scale spinbox change"""
        self.scale_slider.blockSignals(True)
        self.scale_slider.setValue(value)
        self.scale_slider.blockSignals(False)
        self.transform_data["scale"] = value
        self.update_transform()

    def on_rotation_changed(self, value):
        """Handle rotation slider change"""
        self.rotation_spin.blockSignals(True)
        self.rotation_spin.setValue(value)
        self.rotation_spin.blockSignals(False)
        self.transform_data["rotation"] = value
        self.update_transform()

    def on_rotation_spin_changed(self, value):
        """Handle rotation spinbox change"""
        self.rotation_slider.blockSignals(True)
        self.rotation_slider.setValue(value)
        self.rotation_slider.blockSignals(False)
        self.transform_data["rotation"] = value
        self.update_transform()

    def update_transform(self):
        """Update transform and emit signal"""
        self.transform_changed.emit(self.transform_data.copy())

    def reset_transform(self):
        """Reset all transform values"""
        self.transform_data = {
            "position_x": 0,
            "position_y": 0,
            "scale": 100,
            "rotation": 0,
        }

        # Update UI controls
        self.pos_x_spin.setValue(0)
        self.pos_y_spin.setValue(0)
        self.scale_slider.setValue(100)
        self.scale_spin.setValue(100)
        self.rotation_slider.setValue(0)
        self.rotation_spin.setValue(0)

        self.update_transform()

    def load_media(self, media_path):
        """Load media file for preview"""
        self.current_media = media_path

        # Load video in player
        if self.video_player.load_video(media_path):
            self.status_label.setText(f"Loaded: {os.path.basename(media_path)}")
        else:
            self.status_label.setText(f"Failed to load: {os.path.basename(media_path)}")

    def play(self):
        """Start playback"""
        if self.video_player.is_video_loaded():
            self.video_player.play()

    def pause(self):
        """Pause playback"""
        self.video_player.pause()

    def stop(self):
        """Stop playback"""
        self.video_player.stop()

    def toggle_playback(self):
        """Toggle play/pause"""
        if self.video_player.is_video_loaded():
            if self.video_player.is_playing and not self.video_player.is_paused:
                self.pause()
            else:
                self.play()

    def seek(self, position):
        """Seek to position (in seconds)"""
        if self.video_player.is_video_loaded():
            self.video_player.seek_to_position(position)

    def set_current_clip(self, clip_data):
        """Set current clip data"""
        if "path" in clip_data:
            self.load_media(clip_data["path"])

    def cleanup(self):
        """Cleanup video player resources"""
        self.video_player.cleanup()
        self.cache_manager.clear_cache()
