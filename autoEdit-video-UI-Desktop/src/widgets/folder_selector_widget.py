"""
Folder Selector Widget - Input and Output folder selection
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QLineEdit, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal


class FolderSelectorWidget(QWidget):
    """Widget for selecting input and output folders"""
    
    input_folder_changed = pyqtSignal(str)
    output_folder_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Input folder section
        input_layout = QVBoxLayout()
        
        input_label = QLabel("📁 Input Folder")
        input_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #FFFFFF;
                margin-bottom: 8px;
            }
        """)
        input_layout.addWidget(input_label)
        
        input_row = QHBoxLayout()
        
        self.input_path = QLineEdit()
        self.input_path.setPlaceholderText("Select input folder...")
        self.input_path.setReadOnly(True)
        self.input_path.setStyleSheet("""
            QLineEdit {
                background-color: #455A64;
                border: 1px solid #546E7A;
                border-radius: 6px;
                padding: 10px 12px;
                color: #FFFFFF;
                font-size: 13px;
            }
        """)
        input_row.addWidget(self.input_path)
        
        self.input_browse_btn = QPushButton("Browse")
        self.input_browse_btn.setStyleSheet(self.get_button_style())
        self.input_browse_btn.clicked.connect(self.browse_input_folder)
        input_row.addWidget(self.input_browse_btn)
        
        input_layout.addLayout(input_row)
        layout.addLayout(input_layout)
        
        # Output folder section
        output_layout = QVBoxLayout()
        
        output_label = QLabel("📤 Output Folder")
        output_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #FFFFFF;
                margin-bottom: 8px;
            }
        """)
        output_layout.addWidget(output_label)
        
        output_row = QHBoxLayout()
        
        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("Select output folder...")
        self.output_path.setReadOnly(True)
        self.output_path.setStyleSheet("""
            QLineEdit {
                background-color: #455A64;
                border: 1px solid #546E7A;
                border-radius: 6px;
                padding: 10px 12px;
                color: #FFFFFF;
                font-size: 13px;
            }
        """)
        output_row.addWidget(self.output_path)
        
        self.output_browse_btn = QPushButton("Browse")
        self.output_browse_btn.setStyleSheet(self.get_button_style())
        self.output_browse_btn.clicked.connect(self.browse_output_folder)
        output_row.addWidget(self.output_browse_btn)
        
        output_layout.addLayout(output_row)
        layout.addLayout(output_layout)
        
    def get_button_style(self):
        """Get button style"""
        return """
            QPushButton {
                background-color: #546E7A;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 16px;
                font-size: 13px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #607D8B;
            }
            QPushButton:pressed {
                background-color: #455A64;
            }
        """
        
    def browse_input_folder(self):
        """Browse for input folder"""
        folder = QFileDialog.getExistingDirectory(
            self, 
            "Select Input Folder",
            "",
            QFileDialog.Option.ShowDirsOnly
        )
        if folder:
            self.input_path.setText(folder)
            self.input_folder_changed.emit(folder)
            
    def browse_output_folder(self):
        """Browse for output folder"""
        folder = QFileDialog.getExistingDirectory(
            self, 
            "Select Output Folder",
            "",
            QFileDialog.Option.ShowDirsOnly
        )
        if folder:
            self.output_path.setText(folder)
            self.output_folder_changed.emit(folder)
            
    def get_input_folder(self):
        """Get input folder path"""
        return self.input_path.text()
        
    def get_output_folder(self):
        """Get output folder path"""
        return self.output_path.text()