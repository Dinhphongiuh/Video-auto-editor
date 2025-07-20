"""
Main Window - VideoMaster Dashboard Design
Professional video processing interface with embedded widgets
"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QSplitter,
    QScrollArea,
    QProgressBar,
    QComboBox,
    QSlider,
    QLineEdit,
    QTextEdit,
    QFileDialog,
    QGridLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal, QMimeData
from PyQt6.QtGui import QFont, QDragEnterEvent, QDropEvent, QPainter, QPen

# Import widgets - using relative import
from ..widgets.file_drop_widget import FileDropWidget
from ..widgets.folder_selector_widget import FolderSelectorWidget
from ..widgets.format_converter_widget import FormatConverterWidget
from ..widgets.video_editor.video_editor_widget import VideoEditorWidget


class NavigationWidget(QFrame):
    """Sidebar navigation widget"""

    page_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_page = "dashboard"
        self.nav_buttons = {}
        self.setup_ui()

    def setup_ui(self):
        """Setup navigation UI"""
        self.setFixedWidth(200)
        self.setObjectName("sidebar")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header section
        header = self.create_header()
        layout.addWidget(header)

        # Navigation menu
        self.create_navigation_menu(layout)

        layout.addStretch()

        # Tools section
        self.create_tools_section(layout)

    def create_header(self):
        """Create header section"""
        header = QWidget()
        header.setFixedHeight(70)
        header.setObjectName("header")

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 15, 20, 15)

        logo = QLabel("📹")
        logo.setStyleSheet("font-size: 24px;")
        header_layout.addWidget(logo)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(0)

        title = QLabel("VideoMaster")
        title.setStyleSheet("color: #FFFFFF; font-size: 16px; font-weight: bold;")
        title_layout.addWidget(title)

        subtitle = QLabel("Pro Editor v2.1")
        subtitle.setStyleSheet("color: #90A4AE; font-size: 11px;")
        title_layout.addWidget(subtitle)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        status = QLabel("● Ready")
        status.setStyleSheet("color: #4CAF50; font-size: 11px; font-weight: bold;")
        header_layout.addWidget(status)

        return header

    def create_navigation_menu(self, parent_layout):
        """Create main navigation menu"""
        nav_items = [
            ("🏠", "Dashboard", "dashboard"),
            ("🎬", "Video Editor", "video_editor"),
            ("⚡", "Speed Control", "speed"),
            ("🗜️", "Compression", "compression"),
            ("📐", "Resolution", "resolution"),
            ("📁", "Batch Process", "batch"),
        ]

        for icon, text, page_id in nav_items:
            btn = self.create_nav_button(icon, text, page_id)
            self.nav_buttons[page_id] = btn
            parent_layout.addWidget(btn)

    def create_tools_section(self, parent_layout):
        """Create tools section"""
        tools_label = QLabel("Tools")
        tools_label.setStyleSheet(
            "color: #78909C; font-size: 11px; font-weight: bold; padding: 15px 20px 10px 20px;"
        )
        parent_layout.addWidget(tools_label)

        settings_btn = self.create_nav_button("⚙️", "Settings", "settings")
        help_btn = self.create_nav_button("❓", "Help", "help")

        self.nav_buttons["settings"] = settings_btn
        self.nav_buttons["help"] = help_btn

        parent_layout.addWidget(settings_btn)
        parent_layout.addWidget(help_btn)

    def create_nav_button(self, icon, text, page_id):
        """Create navigation button"""
        btn = QPushButton()
        btn.setFixedHeight(45)
        btn.setObjectName("nav_button")

        btn_layout = QHBoxLayout(btn)
        btn_layout.setContentsMargins(20, 0, 20, 0)

        icon_label = QLabel(icon)
        icon_label.setFixedWidth(20)
        icon_label.setStyleSheet("font-size: 16px;")
        btn_layout.addWidget(icon_label)

        text_label = QLabel(text)
        text_label.setStyleSheet("color: #ECEFF1; font-size: 13px; font-weight: 500;")
        btn_layout.addWidget(text_label)
        btn_layout.addStretch()

        if page_id == "dashboard":
            btn.setProperty("active", "true")

        btn.clicked.connect(lambda: self.switch_page(page_id))
        return btn

    def switch_page(self, page_id):
        """Switch page"""
        self.set_active_page(page_id)
        self.page_changed.emit(page_id)

    def set_active_page(self, page_id):
        """Set active page"""
        for btn in self.nav_buttons.values():
            btn.setProperty("active", "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        if page_id in self.nav_buttons:
            self.nav_buttons[page_id].setProperty("active", "true")
            self.nav_buttons[page_id].style().unpolish(self.nav_buttons[page_id])
            self.nav_buttons[page_id].style().polish(self.nav_buttons[page_id])

        self.current_page = page_id


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("VideoMaster - Pro Editor v2.1")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 800)
        self.current_page = "dashboard"
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        """Setup the main UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left sidebar
        self.navigation = NavigationWidget()
        self.navigation.page_changed.connect(self.switch_page)
        main_layout.addWidget(self.navigation)

        # Main content area
        self.content_area = self.create_content_area()
        main_layout.addWidget(self.content_area)

        # Connect folder signals after UI is created
        self.connect_folder_signals()

    def create_content_area(self):
        """Create main content area"""
        content = QFrame()
        content.setObjectName("content")

        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Top bar
        top_bar = self.create_top_bar()
        layout.addWidget(top_bar)

        # Scrollable content area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet(
            "QScrollArea { background-color: #263238; border: none; }"
        )

        # Main content
        self.main_content = self.create_dashboard_content()
        scroll_area.setWidget(self.main_content)
        layout.addWidget(scroll_area)

        return content

    def create_top_bar(self):
        """Create top navigation bar"""
        top_bar = QFrame()
        top_bar.setFixedHeight(60)
        top_bar.setObjectName("top_bar")

        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(30, 0, 30, 0)

        title = QLabel("Video Processing Controller")
        title.setStyleSheet("color: #ECEFF1; font-size: 18px; font-weight: 600;")
        layout.addWidget(title)

        layout.addStretch()

        status = QLabel("● Ready")
        status.setStyleSheet("color: #4CAF50; font-size: 13px; font-weight: bold;")
        layout.addWidget(status)

        return top_bar

    def create_dashboard_content(self):
        """Create dashboard main content"""
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # File drop area
        self.file_drop = FileDropWidget()
        self.file_drop.setFixedHeight(200)
        layout.addWidget(self.file_drop)

        # Folder selectors
        self.folder_selector = FolderSelectorWidget()
        self.folder_selector.setMaximumHeight(120)
        layout.addWidget(self.folder_selector)

        # Processing sections - Using Grid Layout for better organization
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)

        # First row
        format_section = self.create_format_section()
        format_section.setMinimumHeight(200)
        grid_layout.addWidget(format_section, 0, 0)

        speed_section = self.create_speed_section()
        speed_section.setMinimumHeight(200)
        grid_layout.addWidget(speed_section, 0, 1)

        # Second row
        compression_section = self.create_compression_section()
        compression_section.setMinimumHeight(200)
        grid_layout.addWidget(compression_section, 1, 0)

        resolution_section = self.create_resolution_section()
        resolution_section.setMinimumHeight(200)
        grid_layout.addWidget(resolution_section, 1, 1)

        layout.addLayout(grid_layout)

        # Processing progress section
        progress_section = self.create_progress_section()
        layout.addWidget(progress_section)

        # Add stretch at the end to push content up
        layout.addStretch()

        return content

    def create_format_section(self):
        """Create format conversion section"""
        self.format_converter = FormatConverterWidget()
        return self.format_converter

    def connect_folder_signals(self):
        """Connect folder selection signals to widgets"""
        if hasattr(self, "folder_selector") and hasattr(self, "format_converter"):
            # Connect both input and output folder signals
            self.folder_selector.input_folder_changed.connect(
                self.on_input_folder_changed
            )
            self.folder_selector.output_folder_changed.connect(
                self.on_output_folder_changed
            )

    def on_input_folder_changed(self, input_folder):
        """Handle input folder change"""
        if hasattr(self, "format_converter"):
            output_folder = self.folder_selector.get_output_folder()
            self.format_converter.set_folders(input_folder, output_folder)

    def on_output_folder_changed(self, output_folder):
        """Handle output folder change"""
        if hasattr(self, "format_converter"):
            input_folder = self.folder_selector.get_input_folder()
            self.format_converter.set_folders(input_folder, output_folder)

    def update_widget_folders(self, input_folder, output_folder):
        """Update folders in all widgets"""
        if hasattr(self, "format_converter"):
            self.format_converter.set_folders(input_folder, output_folder)

    def create_speed_section(self):
        """Create speed adjustment section"""
        section = QFrame()
        section.setObjectName("section")

        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        header = QLabel("✅ Speed Adjustment")
        header.setStyleSheet("color: #4CAF50; font-size: 16px; font-weight: bold;")
        layout.addWidget(header)

        speed_label = QLabel("Speed Multiplier")
        speed_label.setStyleSheet("color: #ECEFF1; font-size: 13px; font-weight: 500;")
        layout.addWidget(speed_label)

        slider_layout = QHBoxLayout()
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(25)
        self.speed_slider.setMaximum(400)
        self.speed_slider.setValue(100)
        self.speed_slider.setFixedHeight(25)
        slider_layout.addWidget(self.speed_slider)

        self.speed_value = QLabel("1x")
        self.speed_value.setFixedWidth(40)
        self.speed_value.setStyleSheet("color: #ECEFF1; font-weight: bold;")
        slider_layout.addWidget(self.speed_value)

        layout.addLayout(slider_layout)

        quick_layout = QHBoxLayout()
        quick_layout.setSpacing(10)
        for speed, label in [(50, "0.5x"), (100, "1x"), (200, "2x"), (400, "4x")]:
            btn = QPushButton(label)
            btn.setFixedSize(50, 30)
            btn.setObjectName("quick_button")
            quick_layout.addWidget(btn)
        quick_layout.addStretch()
        layout.addLayout(quick_layout)

        layout.addStretch()

        return section

    def create_compression_section(self):
        """Create compression section"""
        section = QFrame()
        section.setObjectName("section")

        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        header = QLabel("✨ Video Compression")
        header.setStyleSheet("color: #9C27B0; font-size: 16px; font-weight: bold;")
        layout.addWidget(header)

        quality_label = QLabel("Quality Level")
        quality_label.setStyleSheet(
            "color: #ECEFF1; font-size: 13px; font-weight: 500;"
        )
        layout.addWidget(quality_label)

        self.quality_combo = QComboBox()
        self.quality_combo.addItems(
            [
                "High Quality (Low Compression)",
                "Medium Quality",
                "Low Quality (High Compression)",
                "Custom",
            ]
        )
        self.quality_combo.setFixedHeight(35)
        layout.addWidget(self.quality_combo)

        size_label = QLabel("Target Size (MB)")
        size_label.setStyleSheet("color: #ECEFF1; font-size: 13px; font-weight: 500;")
        layout.addWidget(size_label)

        self.size_input = QLineEdit()
        self.size_input.setPlaceholderText("Enter target size")
        self.size_input.setFixedHeight(35)
        layout.addWidget(self.size_input)

        layout.addStretch()

        return section

    def create_resolution_section(self):
        """Create resolution section"""
        section = QFrame()
        section.setObjectName("section")

        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        header = QLabel("🔧 Resolution Control")
        header.setStyleSheet("color: #FF9800; font-size: 16px; font-weight: bold;")
        layout.addWidget(header)

        res_label = QLabel("Output Resolution")
        res_label.setStyleSheet("color: #ECEFF1; font-size: 13px; font-weight: 500;")
        layout.addWidget(res_label)

        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(
            [
                "4K (3840x2160)",
                "1440p (2560x1440)",
                "1080p (1920x1080)",
                "720p (1280x720)",
                "480p (854x480)",
                "Custom",
            ]
        )
        self.resolution_combo.setFixedHeight(35)
        layout.addWidget(self.resolution_combo)

        custom_layout = QHBoxLayout()
        custom_layout.setSpacing(10)

        self.width_input = QLineEdit()
        self.width_input.setPlaceholderText("Width")
        self.width_input.setFixedHeight(35)
        custom_layout.addWidget(self.width_input)

        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Height")
        self.height_input.setFixedHeight(35)
        custom_layout.addWidget(self.height_input)

        layout.addLayout(custom_layout)

        layout.addStretch()

        return section

    def create_progress_section(self):
        """Create processing progress section"""
        section = QFrame()
        section.setObjectName("section")
        section.setFixedHeight(160)

        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        header_layout = QHBoxLayout()
        header = QLabel("Processing Progress")
        header.setStyleSheet("color: #ECEFF1; font-size: 16px; font-weight: bold;")
        header_layout.addWidget(header)

        header_layout.addStretch()

        time_label = QLabel("🕒 Estimated: 2m 34s")
        time_label.setStyleSheet("color: #64B5F6; font-size: 13px; font-weight: bold;")
        header_layout.addWidget(time_label)

        layout.addLayout(header_layout)

        file_label = QLabel("Converting video_sample.mp4")
        file_label.setStyleSheet("color: #B0BEC5; font-size: 13px;")
        layout.addWidget(file_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(65)
        self.progress_bar.setFixedHeight(25)
        layout.addWidget(self.progress_bar)

        details_layout = QHBoxLayout()
        speed_label = QLabel("Speed: 1.2x realtime")
        speed_label.setStyleSheet("color: #90A4AE; font-size: 12px;")
        details_layout.addWidget(speed_label)

        details_layout.addStretch()

        size_label = QLabel("Size: 45.2MB / 68.7MB")
        size_label.setStyleSheet("color: #90A4AE; font-size: 12px;")
        details_layout.addWidget(size_label)

        layout.addLayout(details_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        start_btn = QPushButton("▶ Start Processing")
        start_btn.setObjectName("start_button")
        start_btn.setFixedHeight(35)
        buttons_layout.addWidget(start_btn)

        pause_btn = QPushButton("⏸ Pause")
        pause_btn.setObjectName("pause_button")
        pause_btn.setFixedHeight(35)
        buttons_layout.addWidget(pause_btn)

        stop_btn = QPushButton("⏹ Stop")
        stop_btn.setObjectName("stop_button")
        stop_btn.setFixedHeight(35)
        buttons_layout.addWidget(stop_btn)

        export_btn = QPushButton("💾 Export")
        export_btn.setObjectName("export_button")
        export_btn.setFixedHeight(35)
        buttons_layout.addWidget(export_btn)

        layout.addLayout(buttons_layout)
        return section

    def switch_page(self, page_id):
        """Switch to different page"""
        if page_id == "video_editor":
            # Remove existing content
            if hasattr(self, "main_content"):
                self.main_content.setParent(None)

            # Create video editor content
            self.main_content = self.create_video_editor_content()

            # Add to scroll area
            scroll_area = self.content_area.layout().itemAt(1).widget()
            scroll_area.setWidget(self.main_content)
        else:
            # Handle other pages...
            if page_id == "dashboard":
                if hasattr(self, "main_content"):
                    self.main_content.setParent(None)
                self.main_content = self.create_dashboard_content()
                scroll_area = self.content_area.layout().itemAt(1).widget()
                scroll_area.setWidget(self.main_content)

        self.current_page = page_id
        self.navigation.set_active_page(page_id)

    def apply_styles(self):
        """Apply custom styles"""
        self.setStyleSheet(
            """
            QMainWindow { background-color: #263238; }
            QFrame#sidebar { background-color: #37474F; border-right: 1px solid #455A64; }
            QWidget#header { background-color: #455A64; border-bottom: 1px solid #546E7A; }
            QFrame#content { background-color: #263238; }
            QFrame#top_bar { background-color: #37474F; border-bottom: 1px solid #455A64; }
            QPushButton#nav_button { background-color: transparent; border: none; text-align: left; color: #ECEFF1; }
            QPushButton#nav_button:hover { background-color: #455A64; }
            QPushButton#nav_button[active="true"] { background-color: #1976D2; color: #FFFFFF; }
            QFrame#section { background-color: #37474F; border: 1px solid #455A64; border-radius: 8px; }
            QComboBox { background-color: #455A64; border: 1px solid #546E7A; border-radius: 4px; padding: 8px 12px; color: #ECEFF1; font-size: 13px; }
            QComboBox:hover { border-color: #607D8B; }
            QComboBox::drop-down { border: none; width: 20px; }
            QComboBox::down-arrow { width: 0px; height: 0px; border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 6px solid #B0BEC5; }
            QLineEdit { background-color: #455A64; border: 1px solid #546E7A; border-radius: 4px; padding: 8px 12px; color: #ECEFF1; font-size: 13px; }
            QLineEdit:focus { border-color: #2196F3; }
            QSlider::groove:horizontal { border: 1px solid #546E7A; height: 6px; background: #455A64; border-radius: 3px; }
            QSlider::handle:horizontal { background: #2196F3; border: 2px solid #1976D2; width: 16px; margin: -6px 0; border-radius: 8px; }
            QPushButton#quick_button { background-color: #546E7A; color: #ECEFF1; border: none; border-radius: 3px; font-size: 11px; }
            QPushButton#quick_button:hover { background-color: #607D8B; }
            QProgressBar { border: 1px solid #546E7A; border-radius: 4px; background-color: #455A64; text-align: center; color: #ECEFF1; font-weight: bold; }
            QProgressBar::chunk { background-color: #2196F3; border-radius: 3px; }
            QPushButton#start_button { background-color: #2196F3; color: white; border: none; border-radius: 6px; padding: 10px 20px; font-size: 13px; font-weight: bold; }
            QPushButton#start_button:hover { background-color: #1976D2; }
            QPushButton#pause_button { background-color: #FF9800; color: white; border: none; border-radius: 6px; padding: 10px 20px; font-size: 13px; font-weight: bold; }
            QPushButton#pause_button:hover { background-color: #F57C00; }
            QPushButton#stop_button { background-color: #F44336; color: white; border: none; border-radius: 6px; padding: 10px 20px; font-size: 13px; font-weight: bold; }
            QPushButton#stop_button:hover { background-color: #D32F2F; }
            QPushButton#export_button { background-color: #4CAF50; color: white; border: none; border-radius: 6px; padding: 10px 20px; font-size: 13px; font-weight: bold; }
            QPushButton#export_button:hover { background-color: #388E3C; }
            QPushButton#primary_button { 
                background-color: #2196F3; 
                color: white; 
                border: none; 
                border-radius: 6px; 
                padding: 10px 20px; 
                font-size: 13px; 
                font-weight: bold; 
            }
            QPushButton#primary_button:hover { 
                background-color: #1976D2; 
            }
        """
            """
            /* Video Editor Styles */
            QFrame#video_frame {
                background-color: #1E1E1E;
                border: 1px solid #455A64;
                border-radius: 4px;
            }

            QFrame#preview_area {
                background-color: #37474F;
                border: 1px solid #455A64;
                border-radius: 8px;
            }

            QFrame#transform_controls {
                background-color: #37474F;
                border: 1px solid #455A64;
                border-radius: 8px;
            }

            QGroupBox#properties_group {
                color: #ECEFF1;
                font-weight: bold;
                border: 1px solid #546E7A;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 5px;
            }

            QGroupBox#properties_group::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }

            QPushButton#toolbar_button {
                background-color: #546E7A;
                color: #ECEFF1;
                border: none;
                border-radius: 6px;
                font-size: 16px;
            }

            QPushButton#toolbar_button:hover {
                background-color: #607D8B;
            }

            QPushButton#effect_button {
                background-color: #546E7A;
                color: #ECEFF1;
                border: none;
                border-radius: 4px;
                text-align: left;
                padding: 8px 12px;
            }

            QPushButton#effect_button:hover {
                background-color: #607D8B;
            }

            QPushButton#reset_button {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
            }

            QPushButton#reset_button:hover {
                background-color: #F57C00;
            }

            QFrame#editor_toolbar {
                background-color: #37474F;
                border-bottom: 1px solid #455A64;
            }

            QTabWidget#properties_tabs {
                border: none;
            }

            QTabWidget#properties_tabs::pane {
                border: 1px solid #455A64;
                border-radius: 4px;
                background-color: #37474F;
            }

            QTabWidget#properties_tabs::tab-bar {
                alignment: center;
            }

            QTabBar::tab {
                background-color: #546E7A;
                color: #ECEFF1;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }

            QTabBar::tab:selected {
                background-color: #2196F3;
                color: white;
            }

            QTabBar::tab:hover {
                background-color: #607D8B;
            }
            """
        )

    def create_video_editor_content(self):
        """Create video editor content"""
        return VideoEditorWidget()
        return VideoEditorWidget()

    def setup_menu(self):
        """Setup menu bar"""
        pass

    def setup_statusbar(self):
        """Setup status bar"""
        pass
