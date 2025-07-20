"""
Media Library Widget
File browser and media management for video editor
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QFileDialog,
    QFrame,
    QScrollArea,
    QGridLayout,
    QMenu,
)
from PyQt6.QtCore import Qt, pyqtSignal, QMimeData, QUrl
from PyQt6.QtGui import QPixmap, QIcon, QDrag, QAction
import os
from pathlib import Path


class MediaThumbnailItem(QWidget):
    """Custom media thumbnail item"""

    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.drag_start_position = None
        self.setup_ui()

    def setup_ui(self):
        """Setup thumbnail UI"""
        self.setFixedSize(100, 120)
        self.setObjectName("media_item")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Thumbnail area
        thumbnail_frame = QFrame()
        thumbnail_frame.setFixedSize(90, 70)
        thumbnail_frame.setObjectName("thumbnail_frame")

        thumbnail_layout = QVBoxLayout(thumbnail_frame)
        thumbnail_layout.setContentsMargins(0, 0, 0, 0)

        # File type icon based on extension
        file_ext = Path(self.file_path).suffix.lower()
        if file_ext in [".mp4", ".avi", ".mov", ".mkv", ".wmv"]:
            icon_text = "🎬"
        elif file_ext in [".mp3", ".wav", ".aac", ".m4a"]:
            icon_text = "🎵"
        elif file_ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
            icon_text = "🖼️"
        else:
            icon_text = "📄"

        icon_label = QLabel(icon_text)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 24px;")
        thumbnail_layout.addWidget(icon_label)

        layout.addWidget(thumbnail_frame)

        # File name
        name_label = QLabel(self.file_name)
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet(
            """
            color: #ECEFF1; 
            font-size: 10px; 
            font-weight: 500;
            background: transparent;
        """
        )
        layout.addWidget(name_label)

    def mousePressEvent(self, event):
        """Handle mouse press for drag start"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.position().toPoint()

    def mouseMoveEvent(self, event):
        """Handle mouse move for drag operation"""
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return

        if (
            event.position().toPoint() - self.drag_start_position
        ).manhattanLength() < self.style().pixelMetric(
            self.style().PixelMetric.PM_DragDistance
        ):
            return

        # Start drag operation
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.file_path)
        mime_data.setUrls([QUrl.fromLocalFile(self.file_path)])
        drag.setMimeData(mime_data)

        # Execute drag
        drag.exec(Qt.DropAction.CopyAction)


class MediaLibraryWidget(QWidget):
    """Media library widget for managing project media"""

    # Signals
    media_selected = pyqtSignal(str)  # file_path
    media_added_to_timeline = pyqtSignal(str)  # file_path
    media_imported = pyqtSignal(list)  # list of file_paths

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project_data = None
        self.media_items = []
        self.setup_ui()

    def setup_ui(self):
        """Setup media library UI"""
        self.setObjectName("media_library")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Header
        header = self.create_header()
        layout.addWidget(header)

        # Media grid
        self.create_media_grid(layout)

    def create_header(self):
        """Create header with title and import button"""
        header = QFrame()
        header.setObjectName("media_header")

        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)

        # Title
        title = QLabel("📁 Media Library")
        title.setStyleSheet(
            """
            color: #ECEFF1; 
            font-size: 14px; 
            font-weight: bold;
            padding: 5px 0px;
        """
        )
        header_layout.addWidget(title)

        # Import button
        self.import_btn = QPushButton("+ Import Media")
        self.import_btn.setObjectName("import_button")
        self.import_btn.setFixedHeight(32)
        self.import_btn.clicked.connect(self.import_media)
        header_layout.addWidget(self.import_btn)

        return header

    def create_media_grid(self, parent_layout):
        """Create scrollable media grid"""
        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Media container
        self.media_container = QWidget()
        self.media_layout = QVBoxLayout(self.media_container)
        self.media_layout.setContentsMargins(0, 0, 0, 0)
        self.media_layout.setSpacing(10)

        # Grid for media items
        self.media_grid = QGridLayout()
        self.media_grid.setSpacing(10)
        self.media_layout.addLayout(self.media_grid)

        # Add stretch to push items to top
        self.media_layout.addStretch()

        scroll_area.setWidget(self.media_container)
        parent_layout.addWidget(scroll_area)

    def import_media(self):
        """Import media files"""
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter(
            "Media Files (*.mp4 *.avi *.mov *.mkv *.wmv *.mp3 *.wav *.aac *.m4a *.jpg *.jpeg *.png *.bmp *.gif)"
        )
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        file_dialog.setWindowTitle("Import Media Files")

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            self.add_media_files(selected_files)
            self.media_imported.emit(selected_files)

    def add_media_files(self, file_paths):
        """Add media files to library"""
        for file_path in file_paths:
            if file_path not in [item.file_path for item in self.media_items]:
                self.add_media_item(file_path)

    def add_media_item(self, file_path):
        """Add single media item to grid"""
        media_item = MediaThumbnailItem(file_path)

        # Add to grid (2 columns)
        row = len(self.media_items) // 2
        col = len(self.media_items) % 2
        self.media_grid.addWidget(media_item, row, col)

        self.media_items.append(media_item)

        # Connect signals
        media_item.mousePressEvent = (
            lambda event, path=file_path: self.on_media_clicked(path, event)
        )

    def on_media_clicked(self, file_path, event):
        """Handle media item click"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.media_selected.emit(file_path)
        elif event.button() == Qt.MouseButton.RightButton:
            self.show_context_menu(file_path, event.globalPosition().toPoint())

    def show_context_menu(self, file_path, position):
        """Show context menu for media item"""
        menu = QMenu(self)

        # Add to timeline action
        add_action = QAction("Add to Timeline", self)
        add_action.triggered.connect(
            lambda: self.media_added_to_timeline.emit(file_path)
        )
        menu.addAction(add_action)

        # Properties action
        props_action = QAction("Properties", self)
        props_action.triggered.connect(lambda: self.show_media_properties(file_path))
        menu.addAction(props_action)

        # Remove from library action
        remove_action = QAction("Remove from Library", self)
        remove_action.triggered.connect(lambda: self.remove_media_item(file_path))
        menu.addAction(remove_action)

        menu.exec(position)

    def show_media_properties(self, file_path):
        """Show media properties dialog"""
        print(f"Showing properties for: {file_path}")
        # TODO: Implement properties dialog

    def remove_media_item(self, file_path):
        """Remove media item from library"""
        # Find and remove the item
        for i, item in enumerate(self.media_items):
            if item.file_path == file_path:
                # Remove from grid
                item.setParent(None)
                item.deleteLater()

                # Remove from list
                self.media_items.pop(i)

                # Rebuild grid layout
                self.rebuild_grid()
                break

    def rebuild_grid(self):
        """Rebuild the grid layout after removal"""
        # Clear the layout
        for i in reversed(range(self.media_grid.count())):
            self.media_grid.itemAt(i).widget().setParent(None)

        # Re-add all items
        for i, item in enumerate(self.media_items):
            row = i // 2
            col = i % 2
            self.media_grid.addWidget(item, row, col)

    def set_project(self, project_data):
        """Set project data"""
        self.project_data = project_data
        if project_data and "media_files" in project_data:
            self.add_media_files(project_data["media_files"])

    def get_data(self):
        """Get media library data"""
        return {"media_files": [item.file_path for item in self.media_items]}

    def clear_media(self):
        """Clear all media items"""
        for item in self.media_items:
            item.setParent(None)
            item.deleteLater()
        self.media_items.clear()
