"""
Format Converter Widget
UI component for video format conversion
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QComboBox, QLineEdit, QProgressBar,
    QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from ...services.video_converter_service import VideoConverterService, VideoConverterThread


class FormatConverterWidget(QFrame):
    """Widget for format conversion functionality"""
    
    # Signals
    conversion_started = pyqtSignal()
    conversion_completed = pyqtSignal(bool, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("section")
        self.converter_thread = None
        self.is_converting = False
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("🔄 Format Conversion")
        header.setStyleSheet("color: #64B5F6; font-size: 16px; font-weight: bold;")
        layout.addWidget(header)
        
        # Output format selection
        format_label = QLabel("Output Format")
        format_label.setStyleSheet("color: #ECEFF1; font-size: 13px; font-weight: 500;")
        layout.addWidget(format_label)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(VideoConverterService.get_supported_formats())
        self.format_combo.setFixedHeight(35)
        self.format_combo.currentTextChanged.connect(self.on_format_changed)
        layout.addWidget(self.format_combo)
        
        # Custom parameters
        params_label = QLabel("Custom Parameters (Optional)")
        params_label.setStyleSheet("color: #ECEFF1; font-size: 13px; font-weight: 500;")
        layout.addWidget(params_label)
        
        self.params_input = QLineEdit()
        self.params_input.setPlaceholderText("e.g., -b:v 2M -r 30")
        self.params_input.setFixedHeight(35)
        layout.addWidget(self.params_input)
        
        # Progress section
        self.progress_widget = self.create_progress_widget()
        self.progress_widget.setVisible(False)
        layout.addWidget(self.progress_widget)
        
        # Convert button
        self.convert_button = QPushButton("🔄 Start Conversion")
        self.convert_button.setObjectName("primary_button")
        self.convert_button.setFixedHeight(40)
        self.convert_button.clicked.connect(self.start_conversion)
        layout.addWidget(self.convert_button)
        
        layout.addStretch()
        
    def create_progress_widget(self):
        """Create progress display widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 10, 0, 0)
        layout.setSpacing(8)
        
        # Current file label
        self.current_file_label = QLabel("Preparing...")
        self.current_file_label.setStyleSheet("color: #B0BEC5; font-size: 12px;")
        layout.addWidget(self.current_file_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(20)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #90A4AE; font-size: 11px;")
        layout.addWidget(self.status_label)
        
        return widget
        
    def on_format_changed(self, format_text):
        """Handle format selection change"""
        # Update placeholder based on format
        format_tips = {
            "MP4": "-preset fast -crf 22",
            "AVI": "-b:v 2M -b:a 192k",
            "MOV": "-preset medium -movflags +faststart",
            "MKV": "-c:v libx265 -crf 28",
            "WMV": "-b:v 1M -b:a 128k",
            "WEBM": "-b:v 1M -deadline good"
        }
        
        tip = format_tips.get(format_text, "")
        if tip:
            self.params_input.setPlaceholderText(f"e.g., {tip}")
            
    def set_folders(self, input_folder: str, output_folder: str):
        """Set input and output folders"""
        self.input_folder = input_folder
        self.output_folder = output_folder
        
    def start_conversion(self):
        """Start the conversion process"""
        if self.is_converting:
            # Stop conversion
            if self.converter_thread:
                self.converter_thread.stop()
            return
            
        # Get folders from parent (main window should provide these)
        input_folder = getattr(self, 'input_folder', '')
        output_folder = getattr(self, 'output_folder', '')
        
        # Validate folders
        valid, message = VideoConverterService.validate_folders(input_folder, output_folder)
        if not valid:
            QMessageBox.warning(self, "Invalid Folders", message)
            return
            
        # Start conversion
        self.is_converting = True
        self.convert_button.setText("⏹ Stop Conversion")
        self.convert_button.setObjectName("stop_button")
        self.convert_button.style().unpolish(self.convert_button)
        self.convert_button.style().polish(self.convert_button)
        
        self.progress_widget.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Create and start converter thread
        self.converter_thread = VideoConverterThread()
        self.converter_thread.setup(
            input_folder,
            output_folder,
            self.format_combo.currentText().lower(),
            self.params_input.text()
        )
        
        # Connect signals
        self.converter_thread.progress.connect(self.update_progress)
        self.converter_thread.status.connect(self.update_status)
        self.converter_thread.current_file.connect(self.update_current_file)
        self.converter_thread.file_progress.connect(self.update_file_progress)
        self.converter_thread.conversion_finished.connect(self.on_conversion_finished)
        
        # Start thread
        self.converter_thread.start()
        self.conversion_started.emit()
        
    @pyqtSlot(int)
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(value)
        
    @pyqtSlot(str)
    def update_status(self, status):
        """Update status label"""
        self.status_label.setText(status)
        
    @pyqtSlot(str)
    def update_current_file(self, filename):
        """Update current file label"""
        self.current_file_label.setText(f"Converting: {filename}")
        
    @pyqtSlot(int, int)
    def update_file_progress(self, current, total):
        """Update file progress"""
        self.status_label.setText(f"File {current} of {total}")
        
    @pyqtSlot(bool, str)
    def on_conversion_finished(self, success, message):
        """Handle conversion completion"""
        self.is_converting = False
        self.convert_button.setText("🔄 Start Conversion")
        self.convert_button.setObjectName("primary_button")
        self.convert_button.style().unpolish(self.convert_button)
        self.convert_button.style().polish(self.convert_button)
        
        # Show completion message
        if success:
            QMessageBox.information(self, "Conversion Complete", message)
        else:
            QMessageBox.warning(self, "Conversion Failed", message)
            
        self.conversion_completed.emit(success, message)
        
        # Reset progress after a delay
        self.progress_bar.setValue(100 if success else 0)