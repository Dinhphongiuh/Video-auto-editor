"""
Timeline Widget
Multi-track timeline for video editing
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QFrame,
    QLabel,
    QPushButton,
    QSlider,
    QSpinBox,
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QRect, QPoint
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont
import math


class TimelineRuler(QFrame):
    """Timeline ruler showing time markers"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.duration = 60.0  # seconds
        self.zoom_level = 1.0
        self.setObjectName("timeline_ruler")

    def paintEvent(self, event):
        """Paint timeline ruler"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background
        painter.fillRect(self.rect(), QColor("#37474F"))

        # Calculate time scale
        pixels_per_second = 50 * self.zoom_level
        total_width = self.duration * pixels_per_second

        # Draw time markers
        painter.setPen(QPen(QColor("#B0BEC5"), 1))
        painter.setFont(QFont("Arial", 8))

        for i in range(int(self.duration) + 1):
            x = i * pixels_per_second
            if x < self.width():
                # Major tick
                painter.drawLine(int(x), 20, int(x), 30)

                # Time text
                minutes = i // 60
                seconds = i % 60
                time_text = f"{minutes:02d}:{seconds:02d}"
                painter.drawText(int(x) + 2, 15, time_text)

                # Minor ticks (every 10 seconds)
                for j in range(1, 10):
                    minor_x = x + (j * pixels_per_second / 10)
                    if minor_x < self.width():
                        painter.drawLine(int(minor_x), 25, int(minor_x), 30)


class TimelineClip(QFrame):
    """Individual clip on timeline"""

    clip_selected = pyqtSignal(dict)
    clip_moved = pyqtSignal(dict)

    def __init__(self, clip_data, parent=None):
        super().__init__(parent)
        self.clip_data = clip_data
        self.is_selected = False
        self.drag_start_pos = None
        self.setup_ui()

    def setup_ui(self):
        """Setup clip UI"""
        self.setFixedHeight(40)
        self.setObjectName("timeline_clip")

        # Calculate width based on duration
        pixels_per_second = 50  # Default zoom
        duration = self.clip_data.get("duration", 5.0)
        width = int(duration * pixels_per_second)
        self.setFixedWidth(max(width, 50))

    def paintEvent(self, event):
        """Paint clip"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Clip background
        if self.is_selected:
            color = QColor("#2196F3")
        else:
            clip_type = self.clip_data.get("type", "video")
            if clip_type == "video":
                color = QColor("#4CAF50")
            elif clip_type == "audio":
                color = QColor("#FF9800")
            else:
                color = QColor("#9C27B0")

        painter.fillRect(self.rect(), color)

        # Clip border
        painter.setPen(QPen(QColor("#FFFFFF"), 1))
        painter.drawRect(self.rect())

        # Clip name
        painter.setPen(QPen(QColor("#FFFFFF"), 1))
        painter.setFont(QFont("Arial", 9))
        clip_name = self.clip_data.get("name", "Clip")
        painter.drawText(5, 25, clip_name)

    def mousePressEvent(self, event):
        """Handle mouse press"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_selected = True
            self.drag_start_pos = event.position().toPoint()
            self.clip_selected.emit(self.clip_data)
            self.update()

    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if (
            self.drag_start_pos
            and (event.position().toPoint() - self.drag_start_pos).manhattanLength()
            > 10
        ):
            # Handle clip dragging
            new_pos = self.pos() + event.position().toPoint() - self.drag_start_pos
            self.move(new_pos)

    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if self.drag_start_pos:
            self.clip_moved.emit(self.clip_data)
            self.drag_start_pos = None


class TimelineTrack(QFrame):
    """Individual timeline track"""

    def __init__(self, track_type="video", parent=None):
        super().__init__(parent)
        self.track_type = track_type
        self.clips = []
        self.setup_ui()

    def setup_ui(self):
        """Setup track UI"""
        self.setFixedHeight(50)
        self.setObjectName("timeline_track")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)
        layout.setSpacing(0)

        # Track header
        header = self.create_track_header()
        header.setFixedWidth(100)
        layout.addWidget(header)

        # Track content area
        self.content_area = QFrame()
        self.content_area.setObjectName("track_content")
        layout.addWidget(self.content_area)

    def create_track_header(self):
        """Create track header"""
        header = QFrame()
        header.setObjectName("track_header")

        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(10, 5, 10, 5)

        # Track icon and name
        if self.track_type == "video":
            icon = "🎬"
            name = "Video 1"
        elif self.track_type == "audio":
            icon = "🎵"
            name = "Audio 1"
        else:
            icon = "📝"
            name = "Text 1"

        track_label = QLabel(f"{icon} {name}")
        track_label.setStyleSheet("color: #ECEFF1; font-size: 11px; font-weight: bold;")
        header_layout.addWidget(track_label)

        return header

    def add_clip(self, clip_data):
        """Add clip to track"""
        clip = TimelineClip(clip_data)
        clip.clip_selected.connect(self.on_clip_selected)
        clip.clip_moved.connect(self.on_clip_moved)

        # Position clip in content area
        # TODO: Implement proper clip positioning

        self.clips.append(clip)

    def on_clip_selected(self, clip_data):
        """Handle clip selection"""
        # Deselect other clips
        for clip in self.clips:
            if clip.clip_data != clip_data:
                clip.is_selected = False
                clip.update()

    def on_clip_moved(self, clip_data):
        """Handle clip movement"""
        print(f"Clip moved: {clip_data}")


class TimelineWidget(QWidget):
    """Main timeline widget"""

    # Signals
    clip_selected = pyqtSignal(dict)
    timeline_changed = pyqtSignal()
    playback_position_changed = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project_data = None
        self.tracks = []
        self.zoom_level = 1.0
        self.duration = 60.0
        self.current_position = 0.0
        self.is_playing = False
        self.setup_ui()

    def setup_ui(self):
        """Setup timeline UI"""
        self.setObjectName("timeline")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Timeline header
        header = self.create_timeline_header()
        layout.addWidget(header)

        # Timeline ruler
        self.ruler = TimelineRuler()
        layout.addWidget(self.ruler)

        # Scrollable tracks area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Tracks container
        self.tracks_container = QWidget()
        self.tracks_layout = QVBoxLayout(self.tracks_container)
        self.tracks_layout.setContentsMargins(0, 0, 0, 0)
        self.tracks_layout.setSpacing(1)

        # Add default tracks
        self.add_default_tracks()

        scroll_area.setWidget(self.tracks_container)
        layout.addWidget(scroll_area)

    def create_timeline_header(self):
        """Create timeline header with controls"""
        header = QFrame()
        header.setFixedHeight(40)
        header.setObjectName("timeline_header")

        layout = QHBoxLayout(header)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)

        # Title
        title = QLabel("🎬 Timeline")
        title.setStyleSheet("color: #ECEFF1; font-size: 14px; font-weight: bold;")
        layout.addWidget(title)

        layout.addStretch()

        # Zoom controls
        zoom_label = QLabel("Zoom:")
        zoom_label.setStyleSheet("color: #B0BEC5; font-size: 12px;")
        layout.addWidget(zoom_label)

        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setRange(25, 400)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setFixedWidth(100)
        self.zoom_slider.valueChanged.connect(self.on_zoom_changed)
        layout.addWidget(self.zoom_slider)

        zoom_value = QLabel("100%")
        zoom_value.setFixedWidth(40)
        zoom_value.setStyleSheet("color: #ECEFF1; font-size: 12px;")
        layout.addWidget(zoom_value)
        self.zoom_value_label = zoom_value

        # Add track button
        add_track_btn = QPushButton("+ Track")
        add_track_btn.setObjectName("add_track_button")
        add_track_btn.setFixedHeight(25)
        add_track_btn.clicked.connect(self.add_video_track)
        layout.addWidget(add_track_btn)

        return header

    def add_default_tracks(self):
        """Add default tracks"""
        # Video track
        video_track = TimelineTrack("video")
        self.tracks.append(video_track)
        self.tracks_layout.addWidget(video_track)

        # Audio track
        audio_track = TimelineTrack("audio")
        self.tracks.append(audio_track)
        self.tracks_layout.addWidget(audio_track)

        # Text track
        text_track = TimelineTrack("text")
        self.tracks.append(text_track)
        self.tracks_layout.addWidget(text_track)

        # Add stretch to push tracks to top
        self.tracks_layout.addStretch()

    def add_video_track(self):
        """Add new video track"""
        track = TimelineTrack("video")
        self.tracks.append(track)
        # Insert before the stretch
        self.tracks_layout.insertWidget(len(self.tracks) - 1, track)

    def add_media_clip(self, media_path):
        """Add media clip to timeline"""
        import os

        clip_data = {
            "name": os.path.basename(media_path),
            "path": media_path,
            "type": "video",  # TODO: Detect type from file
            "duration": 10.0,  # TODO: Get actual duration
            "start_time": 0.0,
            "in_point": 0.0,
            "out_point": 10.0,
        }

        # Add to first available video track
        for track in self.tracks:
            if track.track_type == "video":
                track.add_clip(clip_data)
                break

        self.timeline_changed.emit()

    def on_zoom_changed(self, value):
        """Handle zoom change"""
        self.zoom_level = value / 100.0
        self.zoom_value_label.setText(f"{value}%")
        self.ruler.zoom_level = self.zoom_level
        self.ruler.update()

        # Update track zoom
        # TODO: Implement track zoom update

    def start_playback(self):
        """Start timeline playback"""
        self.is_playing = True

    def pause_playback(self):
        """Pause timeline playback"""
        self.is_playing = False

    def stop_playback(self):
        """Stop timeline playback"""
        self.is_playing = False
        self.current_position = 0.0

    def seek(self, position):
        """Seek to position"""
        self.current_position = position
        # TODO: Update playhead position

    def update_current_clip_transform(self, transform_data):
        """Update current clip transform"""
        # TODO: Implement transform update
        pass

    def set_project(self, project_data):
        """Set project data"""
        self.project_data = project_data
        # TODO: Load tracks from project data

    def get_data(self):
        """Get timeline data"""
        tracks_data = []
        for track in self.tracks:
            track_data = {
                "type": track.track_type,
                "clips": [clip.clip_data for clip in track.clips],
            }
            tracks_data.append(track_data)

        return {
            "tracks": tracks_data,
            "duration": self.duration,
            "zoom_level": self.zoom_level,
        }
