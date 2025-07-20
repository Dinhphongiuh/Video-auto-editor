"""
Video Editor Widget - Main Container (Fixed Version)
Professional video editing interface layout with proper timeline synchronization
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QFrame
from PyQt6.QtCore import Qt, pyqtSignal, QTimer

from .media_library_widget import MediaLibraryWidget
from .timeline_widget import TimelineWidget
from .properties_panel_widget import PropertiesPanelWidget
from .toolbar_widget import ToolbarWidget
from .playback_controls_widget import PlaybackControlsWidget
from .video_preview_widget import VideoPreviewWidget


class VideoEditorWidget(QWidget):
    """Main video editor container widget"""

    # Signals
    project_changed = pyqtSignal()
    timeline_changed = pyqtSignal()
    playback_changed = pyqtSignal(bool)  # True for play, False for pause

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_project = None
        self.is_playing = False
        self.current_position = 0.0
        self.video_duration = 0.0

        # Timer for updating timeline position during playback
        self.playback_timer = QTimer()
        self.playback_timer.setInterval(50)  # Update every 50ms (20 fps)
        self.playback_timer.timeout.connect(self.update_timeline_position)

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        """Setup the video editor UI layout"""
        self.setObjectName("video_editor")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top toolbar
        self.toolbar = ToolbarWidget()
        main_layout.addWidget(self.toolbar)

        # Main content area - horizontal splitter
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.setHandleWidth(2)

        # Left panel - Media Library + Properties
        left_panel = self.create_left_panel()
        left_panel.setFixedWidth(250)
        main_splitter.addWidget(left_panel)

        # Center/Right area - vertical splitter
        center_right_splitter = QSplitter(Qt.Orientation.Vertical)
        center_right_splitter.setHandleWidth(2)

        # Video preview area
        self.video_preview = VideoPreviewWidget()
        center_right_splitter.addWidget(self.video_preview)

        # Timeline area
        timeline_container = self.create_timeline_container()
        center_right_splitter.addWidget(timeline_container)

        # Set initial sizes for vertical splitter (60% preview, 40% timeline)
        center_right_splitter.setSizes([600, 400])

        main_splitter.addWidget(center_right_splitter)

        # Set initial sizes for horizontal splitter (20% left panel, 80% center/right)
        main_splitter.setSizes([250, 1000])

        main_layout.addWidget(main_splitter)

    def create_left_panel(self):
        """Create left panel with media library and properties"""
        left_panel = QFrame()
        left_panel.setObjectName("left_panel")

        layout = QVBoxLayout(left_panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Media library (upper part)
        self.media_library = MediaLibraryWidget()
        layout.addWidget(self.media_library)

        # Properties panel (lower part)
        self.properties_panel = PropertiesPanelWidget()
        layout.addWidget(self.properties_panel)

        return left_panel

    def create_timeline_container(self):
        """Create timeline container with playback controls"""
        container = QFrame()
        container.setObjectName("timeline_container")

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Playback controls
        self.playback_controls = PlaybackControlsWidget()
        self.playback_controls.setFixedHeight(60)
        layout.addWidget(self.playback_controls)

        # Timeline
        self.timeline = TimelineWidget()
        layout.addWidget(self.timeline)

        return container

    def connect_signals(self):
        """Connect widget signals"""
        # Toolbar signals
        self.toolbar.import_clicked.connect(self.import_media)
        self.toolbar.export_clicked.connect(self.export_project)
        self.toolbar.undo_clicked.connect(self.undo_action)
        self.toolbar.redo_clicked.connect(self.redo_action)

        # Playback control signals
        self.playback_controls.play_pause_clicked.connect(self.toggle_playback)
        self.playback_controls.stop_clicked.connect(self.stop_playback)
        self.playback_controls.seek_changed.connect(self.seek_to_position)

        # Media library signals
        self.media_library.media_selected.connect(self.on_media_selected)
        self.media_library.media_added_to_timeline.connect(self.add_media_to_timeline)

        # Timeline signals
        self.timeline.clip_selected.connect(self.on_clip_selected)
        self.timeline.timeline_changed.connect(self.on_timeline_changed)
        self.timeline.playback_position_changed.connect(
            self.on_timeline_position_changed
        )

        # Video preview signals
        self.video_preview.transform_changed.connect(self.on_transform_changed)
        self.video_preview.playback_position_changed.connect(
            self.on_video_position_changed
        )

        # Connect video player signals for proper synchronization
        if hasattr(self.video_preview, "video_player"):
            self.video_preview.video_player.duration_changed.connect(
                self.on_video_duration_changed
            )
            self.video_preview.video_player.position_changed.connect(
                self.on_video_position_changed
            )
            self.video_preview.video_player.playback_finished.connect(
                self.on_playback_finished
            )

    def import_media(self):
        """Handle media import"""
        self.media_library.import_media()

    def export_project(self):
        """Handle project export"""
        print("Exporting project...")
        # TODO: Implement export functionality

    def undo_action(self):
        """Handle undo action"""
        print("Undo action")
        # TODO: Implement undo functionality

    def redo_action(self):
        """Handle redo action"""
        print("Redo action")
        # TODO: Implement redo functionality

    def toggle_playback(self):
        """Toggle play/pause"""
        self.is_playing = not self.is_playing
        self.playback_changed.emit(self.is_playing)

        if self.is_playing:
            self.video_preview.play()
            self.timeline.start_playback()
            self.playback_timer.start()
        else:
            self.video_preview.pause()
            self.timeline.pause_playback()
            self.playback_timer.stop()

    def stop_playback(self):
        """Stop playback"""
        self.is_playing = False
        self.playback_changed.emit(False)
        self.playback_timer.stop()

        self.video_preview.stop()
        self.timeline.stop_playback()

        # Reset position to beginning
        self.current_position = 0.0
        self.playback_controls.set_position(0.0)
        self.timeline.seek(0.0)

    def seek_to_position(self, position):
        """Seek to specific position"""
        self.current_position = position
        self.video_preview.seek(position)
        self.timeline.seek(position)

    def on_media_selected(self, media_path):
        """Handle media selection"""
        self.video_preview.load_media(media_path)
        self.properties_panel.set_media(media_path)

        # Get video duration from player
        if hasattr(self.video_preview, "video_player"):
            self.video_duration = self.video_preview.video_player.get_duration()
            self.playback_controls.set_duration(self.video_duration)
            self.timeline.duration = self.video_duration
            self.timeline.ruler.duration = self.video_duration
            self.timeline.ruler.update()

    def add_media_to_timeline(self, media_path):
        """Add media to timeline"""
        self.timeline.add_media_clip(media_path)

    def on_clip_selected(self, clip_data):
        """Handle clip selection in timeline"""
        self.properties_panel.set_clip(clip_data)
        self.video_preview.set_current_clip(clip_data)

    def on_timeline_changed(self):
        """Handle timeline changes"""
        self.timeline_changed.emit()

    def on_transform_changed(self, transform_data):
        """Handle transform changes from preview"""
        self.properties_panel.update_transform(transform_data)
        self.timeline.update_current_clip_transform(transform_data)

    def on_video_duration_changed(self, duration):
        """Handle video duration change"""
        self.video_duration = duration
        self.playback_controls.set_duration(duration)
        self.timeline.duration = duration
        self.timeline.ruler.duration = duration
        self.timeline.ruler.update()

    def on_video_position_changed(self, position):
        """Handle video position change from player"""
        self.current_position = position
        if not self.playback_controls.seek_slider.isSliderDown():
            self.playback_controls.set_position(position)
        # Update timeline playhead position
        self.timeline.current_position = position
        self.timeline.update()

    def on_timeline_position_changed(self, position):
        """Handle timeline position change"""
        self.seek_to_position(position)

    def on_playback_finished(self):
        """Handle playback finished"""
        self.stop_playback()

    def update_timeline_position(self):
        """Update timeline position during playback"""
        if self.is_playing and hasattr(self.video_preview, "video_player"):
            current_pos = self.video_preview.video_player.get_current_position()
            self.current_position = current_pos

            # Update playback controls position
            if not self.playback_controls.seek_slider.isSliderDown():
                self.playback_controls.set_position(current_pos)

            # Update timeline position
            self.timeline.current_position = current_pos
            # Trigger timeline redraw if needed
            # self.timeline.update()

    def set_project(self, project_data):
        """Set current project"""
        self.current_project = project_data
        self.media_library.set_project(project_data)
        self.timeline.set_project(project_data)
        self.project_changed.emit()

    def get_project_data(self):
        """Get current project data"""
        if not self.current_project:
            return None

        return {
            "media_library": self.media_library.get_data(),
            "timeline": self.timeline.get_data(),
            "properties": self.properties_panel.get_data(),
        }
