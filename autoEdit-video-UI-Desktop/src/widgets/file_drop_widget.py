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
        self.apply_styles()
        
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Drop icon
        icon_label = QLabel("📁")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setObjectName("drop_icon")
        layout.addWidget(icon_label)
        
        # Main text
        main_text = QLabel("Drop video files here or click to browse")
        main_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_text.setObjectName("drop_text")
        main_text.setWordWrap(True)
        layout.addWidget(main_text)
        
        # Supported formats
        formats_text = QLabel("Supports MP4, AVI, MOV, MKV, WMV formats")
        formats_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        formats_text.setObjectName("formats_text")
        formats_text.setWordWrap(True)
        layout.addWidget(formats_text)
        
        # Browse button
        self.browse_button = QPushButton("📂 Browse Files")
        self.browse_button.setObjectName("browse_button")
        self.browse_button.setFixedSize(200, 50)
        layout.addWidget(self.browse_button, 0, Qt.AlignmentFlag.AlignCenter)
        
    def apply_styles(self):
        """Apply widget styles"""
        self.setStyleSheet("""
            FileDropWidget {
                background-color: #37474F;
                border: 2px dashed #546E7A;
                border-radius: 12px;
            }
            
            FileDropWidget:hover {
                border-color: #607D8B;
                background-color: #455A64;
            }
            
            QLabel#drop_icon {
                font-size: 48px;
                color: #64B5F6;
                background: transparent;
                border: none;
            }
            
            QLabel#drop_text {
                font-size: 18px;
                font-weight: bold;
                color: #FFFFFF;
                background: transparent;
                border: none;
            }
            
            QLabel#formats_text {
                font-size: 14px;
                color: #B0BEC5;
                background: transparent;
                border: none;
            }
            
            QPushButton#browse_button {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            
            QPushButton#browse_button:hover {
                background-color: #1976D2;
            }
            
            QPushButton#browse_button:pressed {
                background-color: #1565C0;
            }
        """)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setProperty("dragActive", True)
            self.style().unpolish(self)
            self.style().polish(self)
        
    def dragLeaveEvent(self, event):
        """Handle drag leave event"""
        self.setProperty("dragActive", False)
        self.style().unpolish(self)
        self.style().polish(self)
        
    def dropEvent(self, event: QDropEvent):
        """Handle drop event"""
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.wmv')):
                files.append(file_path)
        
        if files:
            self.files_dropped.emit(files)
            
        self.setProperty("dragActive", False)
        self.style().unpolish(self)
        self.style().polish(self)
        event.acceptProposedAction()