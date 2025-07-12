"""
Main Window - Hello World Version
Primary application window with basic layout
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QTextEdit, QFrame,
    QMenuBar, QStatusBar, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap


class MainWindow(QMainWindow):
    """Main application window class"""
    
    # Signals
    file_selected = pyqtSignal(str)
    processing_started = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize main window"""
        super().__init__(parent)
        self.setWindowTitle("AutoEdit Video UI Desktop - Hello World")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(800, 600)
        
        # Setup UI
        self.setup_ui()
        self.setup_menu()
        self.setup_statusbar()
        self.apply_styles()
        
    def setup_ui(self):
        """Setup user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel (Sidebar)
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel (Main content)
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([300, 900])
        splitter.setStretchFactor(0, 0)  # Left panel fixed
        splitter.setStretchFactor(1, 1)  # Right panel stretches
        
    def create_left_panel(self):
        """Create left sidebar panel"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        panel.setMinimumWidth(250)
        panel.setMaximumWidth(400)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🎬 AutoEdit Video UI")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2196F3;
                padding: 10px;
                background-color: #F0F8FF;
                border-radius: 8px;
                border: 2px solid #E3F2FD;
            }
        """)
        layout.addWidget(title)
        
        # Features list
        features_label = QLabel("✨ Features:")
        features_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #333;")
        layout.addWidget(features_label)
        
        features = [
            "📁 File Management",
            "🎥 Video Preview", 
            "🎨 Filter System",
            "⚡ Fast Processing",
            "📤 Multiple Export Formats",
            "🔄 Batch Operations"
        ]
        
        for feature in features:
            feature_label = QLabel(feature)
            feature_label.setStyleSheet("""
                QLabel {
                    padding: 8px;
                    background-color: #FAFAFA;
                    border-radius: 4px;
                    border-left: 3px solid #2196F3;
                }
            """)
            layout.addWidget(feature_label)
        
        layout.addStretch()
        
        # Action buttons
        self.load_button = QPushButton("📂 Load Videos")
        self.load_button.setStyleSheet(self.get_button_style("primary"))
        self.load_button.clicked.connect(self.on_load_clicked)
        layout.addWidget(self.load_button)
        
        self.process_button = QPushButton("⚡ Start Processing")
        self.process_button.setStyleSheet(self.get_button_style("secondary"))
        self.process_button.clicked.connect(self.on_process_clicked)
        layout.addWidget(self.process_button)
        
        return panel
        
    def create_right_panel(self):
        """Create right main content panel"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Welcome header
        welcome_header = QLabel("🎉 Welcome to AutoEdit Video UI Desktop!")
        welcome_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_header.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1976D2;
                padding: 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #E3F2FD, stop:1 #BBDEFB);
                border-radius: 12px;
                border: 1px solid #90CAF9;
            }
        """)
        layout.addWidget(welcome_header)
        
        # Description
        description = QLabel("""
        <div style='text-align: center; line-height: 1.6;'>
            <h3 style='color: #333; margin-bottom: 15px;'>Professional Video Processing Made Simple</h3>
            <p style='color: #666; font-size: 14px;'>
                This is the <strong>Hello World</strong> version of AutoEdit Video UI Desktop.<br>
                A modern, user-friendly interface for the VideoForge video processing engine.
            </p>
            <br>
            <p style='color: #2196F3; font-weight: bold;'>
                🚀 Ready to transform your video editing workflow!
            </p>
        </div>
        """)
        description.setWordWrap(True)
        description.setStyleSheet("""
            QLabel {
                background-color: #FAFAFA;
                padding: 20px;
                border-radius: 8px;
                border: 1px solid #E0E0E0;
            }
        """)
        layout.addWidget(description)
        
        # Status text area
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(200)
        self.status_text.setStyleSheet("""
            QTextEdit {
                background-color: #F8F9FA;
                border: 1px solid #DEE2E6;
                border-radius: 6px;
                padding: 10px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }
        """)
        
        # Add initial status message
        self.status_text.append("✅ AutoEdit Video UI Desktop initialized successfully!")
        self.status_text.append("🔗 Ready to connect to VideoForge backend...")
        self.status_text.append("📁 Click 'Load Videos' to get started!")
        
        layout.addWidget(QLabel("📊 Status Log:"))
        layout.addWidget(self.status_text)
        
        layout.addStretch()
        
        return panel
    
    def setup_menu(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('&File')
        
        open_action = file_menu.addAction('&Open Videos...')
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.on_load_clicked)
        
        file_menu.addSeparator()
        
        settings_action = file_menu.addAction('&Settings...')
        settings_action.setShortcut('Ctrl+,')
        settings_action.triggered.connect(self.on_settings_clicked)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction('E&xit')
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        
        # Edit menu
        edit_menu = menubar.addMenu('&Edit')
        
        prefs_action = edit_menu.addAction('&Preferences...')
        prefs_action.triggered.connect(self.on_settings_clicked)
        
        # View menu
        view_menu = menubar.addMenu('&View')
        
        refresh_action = view_menu.addAction('&Refresh')
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.on_refresh_clicked)
        
        fullscreen_action = view_menu.addAction('&Full Screen')
        fullscreen_action.setShortcut('F11')
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        
        # Help menu
        help_menu = menubar.addMenu('&Help')
        
        about_action = help_menu.addAction('&About...')
        about_action.triggered.connect(self.on_about_clicked)
        
        docs_action = help_menu.addAction('&Documentation')
        docs_action.triggered.connect(self.on_docs_clicked)
        
    def setup_statusbar(self):
        """Setup status bar"""
        self.statusBar().showMessage("Ready - AutoEdit Video UI Desktop v1.0.0")
        
    def apply_styles(self):
        """Apply custom styles to the window"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
            }
            QFrame {
                background-color: #FFFFFF;
                border-radius: 8px;
            }
            QMenuBar {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E0E0E0;
                padding: 4px;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 8px 12px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
            QStatusBar {
                background-color: #FFFFFF;
                border-top: 1px solid #E0E0E0;
                padding: 4px;
            }
        """)
    
    def get_button_style(self, button_type="primary"):
        """Get button style based on type"""
        if button_type == "primary":
            return """
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 12px 20px;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #1565C0;
                }
            """
        else:  # secondary
            return """
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 12px 20px;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #45A049;
                }
                QPushButton:pressed {
                    background-color: #3D8B40;
                }
            """
    
    # Event handlers
    def on_load_clicked(self):
        """Handle load videos button click"""
        self.status_text.append("🔍 Load Videos clicked - Feature coming soon!")
        self.statusBar().showMessage("Load Videos feature will be implemented next...")
        self.file_selected.emit("demo_file.mp4")
        
    def on_process_clicked(self):
        """Handle process button click"""
        self.status_text.append("⚡ Start Processing clicked - Feature coming soon!")
        self.statusBar().showMessage("Processing feature will be implemented next...")
        self.processing_started.emit()
        
    def on_settings_clicked(self):
        """Handle settings menu click"""
        self.status_text.append("⚙️ Settings clicked - Feature coming soon!")
        
    def on_refresh_clicked(self):
        """Handle refresh menu click"""
        self.status_text.append("🔄 Refresh clicked!")
        self.statusBar().showMessage("Interface refreshed")
        
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.isFullScreen():
            self.showNormal()
            self.status_text.append("🪟 Exited fullscreen mode")
        else:
            self.showFullScreen()
            self.status_text.append("🖥️ Entered fullscreen mode")
            
    def on_about_clicked(self):
        """Handle about menu click"""
        self.status_text.append("ℹ️ About clicked - Feature coming soon!")
        
    def on_docs_clicked(self):
        """Handle documentation menu click"""
        self.status_text.append("📖 Documentation clicked - Feature coming soon!")
        
    def closeEvent(self, event):
        """Handle window close event"""
        self.status_text.append("👋 Closing AutoEdit Video UI Desktop...")
        event.accept()
