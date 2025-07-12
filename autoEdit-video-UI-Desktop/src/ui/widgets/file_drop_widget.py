"""
File Drop Widget - Drag and drop area for video files
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal, QMimeData
from PyQt6.QtGui import QDragEnterEvent, QDropEvent


class FileDropWidget(QWidget):
    """Drag and drop widget for video files"""
    
    files_dropped = pyqtSignal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setMinimumHeight(200)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        # Drop icon
        icon_label = QLabel("📁")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("QLabel { font-size: 48px; color: #64B5F6; }")
        layout.addWidget(icon_label)
        
        # Main text
        main_text = QLabel("Drop video files here or click to browse")
        main_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_text.setStyleSheet("QLabel { font-size: 18px; font-weight: bold; color: #FFFFFF; }")
        layout.addWidget(main_text)
        
        # Supported formats
        formats_text = QLabel("Supports MP4, AVI, MOV, MKV, WMV formats")
        formats_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        formats_text.setStyleSheet("QLabel { font-size: 14px; color: #B0BEC5; }")
        layout.addWidget(formats_text)
        
        # Browse button
        self.browse_button = QPushButton("📂 Browse Files")
        self.browse_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { 
                background-color: #1976D2; 
            }
        """)
        layout.addWidget(self.browse_button)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        
    def dropEvent(self, event: QDropEvent):
        """Handle drop event"""
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.wmv')):
                files.append(file_path)
        
        if files:
            self.files_dropped.emit(files)
        event.acceptProposedAction()