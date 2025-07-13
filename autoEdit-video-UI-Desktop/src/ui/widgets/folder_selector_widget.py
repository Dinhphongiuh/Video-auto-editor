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
        self.create_input_section(layout)
        
        # Output folder section
        self.create_output_section(layout)
        
    def create_input_section(self, parent_layout):
        """Create input folder selection section"""
        input_label = QLabel("📁 Input Folder")
        input_label.setStyleSheet("""
            QLabel { 
                font-size: 14px; 
                font-weight: bold; 
                color: #FFFFFF; 
            }
        """)
        parent_layout.addWidget(input_label)
        
        input_row = QHBoxLayout()
        
        self.input_path = QLineEdit()
        self.input_path.setPlaceholderText("Select input folder...")
        self.input_path.setReadOnly(True)
        self.input_path.setStyleSheet(self.get_lineedit_style())
        input_row.addWidget(self.input_path)
        
        input_btn = QPushButton("Browse")
        input_btn.setStyleSheet(self.get_button_style())
        input_btn.clicked.connect(self.browse_input_folder)
        input_row.addWidget(input_btn)
        
        parent_layout.addLayout(input_row)
        
    def create_output_section(self, parent_layout):
        """Create output folder selection section"""
        output_label = QLabel("📤 Output Folder")
        output_label.setStyleSheet("""
            QLabel { 
                font-size: 14px; 
                font-weight: bold; 
                color: #FFFFFF; 
            }
        """)
        parent_layout.addWidget(output_label)
        
        output_row = QHBoxLayout()
        
        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("Select output folder...")
        self.output_path.setReadOnly(True)
        self.output_path.setStyleSheet(self.get_lineedit_style())
        output_row.addWidget(self.output_path)
        
        output_btn = QPushButton("Browse")
        output_btn.setStyleSheet(self.get_button_style())
        output_btn.clicked.connect(self.browse_output_folder)
        output_row.addWidget(output_btn)
        
        parent_layout.addLayout(output_row)
        
    def get_lineedit_style(self):
        """Get line edit style"""
        return """
            QLineEdit {
                background-color: #455A64;
                border: 1px solid #546E7A;
                border-radius: 6px;
                padding: 10px 12px;
                color: #FFFFFF;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #2196F3;
            }
        """
        
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
        
    def set_input_folder(self, folder_path):
        """Set input folder path"""
        self.input_path.setText(folder_path)
        
    def set_output_folder(self, folder_path):
        """Set output folder path"""
        self.output_path.setText(folder_path)