"""
Video Frame Widget
Widget for displaying video frames with scaling and aspect ratio
"""

from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor


class VideoFrameWidget(QLabel):
    """Widget for displaying video frames"""

    # Signals
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_pixmap = None
        self.aspect_ratio = 16.0 / 9.0  # Default aspect ratio
        self.setup_ui()

    def setup_ui(self):
        """Setup frame widget"""
        self.setObjectName("video_frame")
        self.setMinimumSize(400, 225)  # 16:9 minimum
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setScaledContents(False)

        # Default placeholder
        self.show_placeholder()

    def show_placeholder(self):
        """Show placeholder when no video"""
        self.setText("No video loaded")
        self.setStyleSheet(
            """
            QLabel {
                color: #90A4AE;
                font-size: 16px;
                font-weight: 500;
                background-color: #1E1E1E;
                border: 2px dashed #455A64;
            }
        """
        )

    def set_frame(self, pixmap):
        """Set video frame"""
        if pixmap.isNull():
            self.show_placeholder()
            return

        self.original_pixmap = pixmap

        # Calculate aspect ratio
        if pixmap.width() > 0 and pixmap.height() > 0:
            self.aspect_ratio = pixmap.width() / pixmap.height()

        # Scale pixmap to fit widget
        scaled_pixmap = self.scale_pixmap_to_fit(pixmap)
        self.setPixmap(scaled_pixmap)

        # Remove placeholder styling
        self.setStyleSheet(
            """
            QLabel {
                background-color: #1E1E1E;
                border: 1px solid #455A64;
            }
        """
        )

    def scale_pixmap_to_fit(self, pixmap):
        """Scale pixmap to fit widget while maintaining aspect ratio"""
        if pixmap.isNull():
            return pixmap

        widget_size = self.size()
        pixmap_size = pixmap.size()

        # Calculate scaled size maintaining aspect ratio
        scaled_size = pixmap_size.scaled(
            widget_size, Qt.AspectRatioMode.KeepAspectRatio
        )

        # Scale the pixmap
        return pixmap.scaled(
            scaled_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    def resizeEvent(self, event):
        """Handle resize events"""
        super().resizeEvent(event)

        # Re-scale pixmap if we have one
        if self.original_pixmap and not self.original_pixmap.isNull():
            scaled_pixmap = self.scale_pixmap_to_fit(self.original_pixmap)
            self.setPixmap(scaled_pixmap)

    def mousePressEvent(self, event):
        """Handle mouse clicks"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def sizeHint(self):
        """Provide size hint based on aspect ratio"""
        base_width = 640
        base_height = int(base_width / self.aspect_ratio)
        return QSize(base_width, base_height)

    def get_display_size(self):
        """Get current display size"""
        if self.pixmap():
            return self.pixmap().size()
        return self.size()
