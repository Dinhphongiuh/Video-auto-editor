"""
Playback Controls Widget (Fixed Version)
Video playback controls for timeline with proper progress synchronization
"""

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QFrame,
    QSpinBox,
)
from PyQt6.QtCore import Qt, pyqtSignal


class PlaybackControlsWidget(QWidget):
    """Playback controls widget"""

    # Signals
    play_pause_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    seek_changed = pyqtSignal(float)  # position in seconds

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_playing = False
        self.duration = 60.0
        self.current_position = 0.0
        self._is_seeking = False
        self.setup_ui()

    def setup_ui(self):
        """Setup playback controls UI"""
        self.setObjectName("playback_controls")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)

        # Playback buttons
        self.play_pause_btn = QPushButton("▶️")
        self.play_pause_btn.setObjectName("play_button")
        self.play_pause_btn.setFixedSize(40, 40)
        self.play_pause_btn.clicked.connect(self.on_play_pause_clicked)
        layout.addWidget(self.play_pause_btn)

        self.stop_btn = QPushButton("⏹️")
        self.stop_btn.setObjectName("stop_button")
        self.stop_btn.setFixedSize(40, 40)
        self.stop_btn.clicked.connect(self.on_stop_clicked)
        layout.addWidget(self.stop_btn)

        # Time display
        self.time_label = QLabel("00:00")
        self.time_label.setFixedWidth(50)
        self.time_label.setStyleSheet(
            "color: #ECEFF1; font-size: 12px; font-weight: bold;"
        )
        layout.addWidget(self.time_label)

        # Seek slider
        self.seek_slider = QSlider(Qt.Orientation.Horizontal)
        self.seek_slider.setRange(0, int(self.duration * 1000))  # milliseconds
        self.seek_slider.setValue(0)
        self.seek_slider.sliderPressed.connect(self.on_slider_pressed)
        self.seek_slider.sliderReleased.connect(self.on_slider_released)
        self.seek_slider.sliderMoved.connect(self.on_slider_moved)
        layout.addWidget(self.seek_slider)

        # Duration display
        self.duration_label = QLabel("01:00")
        self.duration_label.setFixedWidth(50)
        self.duration_label.setStyleSheet("color: #B0BEC5; font-size: 12px;")
        layout.addWidget(self.duration_label)

        # Zoom controls
        zoom_label = QLabel("Zoom:")
        zoom_label.setStyleSheet("color: #B0BEC5; font-size: 12px;")
        layout.addWidget(zoom_label)

        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setRange(25, 400)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setFixedWidth(100)
        layout.addWidget(self.zoom_slider)

        zoom_value = QLabel("100%")
        zoom_value.setFixedWidth(40)
        zoom_value.setStyleSheet("color: #ECEFF1; font-size: 12px;")
        layout.addWidget(zoom_value)
        self.zoom_value_label = zoom_value

        # Connect zoom slider
        self.zoom_slider.valueChanged.connect(self.on_zoom_changed)

    def on_play_pause_clicked(self):
        """Handle play/pause button click"""
        self.is_playing = not self.is_playing
        self.update_play_button()
        self.play_pause_clicked.emit()

    def on_stop_clicked(self):
        """Handle stop button click"""
        self.is_playing = False
        self.current_position = 0.0
        self.update_play_button()
        self.update_time_display()
        self.seek_slider.setValue(0)
        self.stop_clicked.emit()

    def on_slider_pressed(self):
        """Handle slider press"""
        self._is_seeking = True

    def on_slider_released(self):
        """Handle slider release"""
        self._is_seeking = False
        value = self.seek_slider.value()
        position = value / 1000.0  # Convert to seconds
        self.seek_changed.emit(position)

    def on_slider_moved(self, value):
        """Handle slider movement"""
        position = value / 1000.0  # Convert to seconds
        self.current_position = position
        self.update_time_display()

        # Only emit seek signal if user is actively dragging
        if self._is_seeking:
            self.seek_changed.emit(position)

    def on_zoom_changed(self, value):
        """Handle zoom change"""
        self.zoom_value_label.setText(f"{value}%")

    def update_play_button(self):
        """Update play button text"""
        if self.is_playing:
            self.play_pause_btn.setText("⏸️")
        else:
            self.play_pause_btn.setText("▶️")

    def update_time_display(self):
        """Update time display"""
        minutes = int(self.current_position // 60)
        seconds = int(self.current_position % 60)
        self.time_label.setText(f"{minutes:02d}:{seconds:02d}")

    def set_duration(self, duration):
        """Set timeline duration"""
        self.duration = duration
        self.seek_slider.setRange(0, int(duration * 1000))

        minutes = int(duration // 60)
        seconds = int(duration % 60)
        self.duration_label.setText(f"{minutes:02d}:{seconds:02d}")

    def set_position(self, position):
        """Set current position (called during playback)"""
        if self._is_seeking:
            # Don't update if user is dragging slider
            return

        self.current_position = position

        # Block signals to prevent triggering seek
        self.seek_slider.blockSignals(True)
        self.seek_slider.setValue(int(position * 1000))
        self.seek_slider.blockSignals(False)

        self.update_time_display()

    def is_seeking(self):
        """Check if user is currently seeking"""
        return self._is_seeking or self.seek_slider.isSliderDown()
