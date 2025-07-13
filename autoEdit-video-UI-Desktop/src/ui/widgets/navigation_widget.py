"""
Navigation Widget - Sidebar navigation component
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtCore import Qt, pyqtSignal


class NavigationWidget(QFrame):
    """Sidebar navigation widget"""
    
    page_changed = pyqtSignal(str)  # Signal when page is switched
    
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
        """Create header section with logo and title"""
        header = QWidget()
        header.setFixedHeight(70)
        header.setObjectName("header")
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        # Logo
        logo = QLabel("📹")
        logo.setStyleSheet("font-size: 24px;")
        header_layout.addWidget(logo)
        
        # Title section
        title_layout = QVBoxLayout()
        title_layout.setSpacing(0)
        
        title = QLabel("VideoMaster")
        title.setStyleSheet("""
            color: #FFFFFF;
            font-size: 16px;
            font-weight: bold;
        """)
        title_layout.addWidget(title)
        
        subtitle = QLabel("Pro Editor v2.1")
        subtitle.setStyleSheet("""
            color: #90A4AE;
            font-size: 11px;
        """)
        title_layout.addWidget(subtitle)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Status indicator
        status = QLabel("● Ready")
        status.setStyleSheet("""
            color: #4CAF50;
            font-size: 11px;
            font-weight: bold;
        """)
        header_layout.addWidget(status)
        
        return header
        
    def create_navigation_menu(self, parent_layout):
        """Create main navigation menu"""
        nav_items = [
            ("🏠", "Dashboard", "dashboard"),
            ("🔄", "Format Converter", "format"),
            ("⚡", "Speed Control", "speed"),
            ("🗜️", "Compression", "compression"),
            ("📐", "Resolution", "resolution"),
            ("📁", "Batch Process", "batch")
        ]
        
        for icon, text, page_id in nav_items:
            btn = self.create_nav_button(icon, text, page_id)
            self.nav_buttons[page_id] = btn
            parent_layout.addWidget(btn)
            
    def create_tools_section(self, parent_layout):
        """Create tools section"""
        # Tools label
        tools_label = QLabel("Tools")
        tools_label.setStyleSheet("""
            color: #78909C;
            font-size: 11px;
            font-weight: bold;
            padding: 15px 20px 10px 20px;
        """)
        parent_layout.addWidget(tools_label)
        
        # Tools buttons
        settings_btn = self.create_nav_button("⚙️", "Settings", "settings")
        help_btn = self.create_nav_button("❓", "Help", "help")
        
        self.nav_buttons["settings"] = settings_btn
        self.nav_buttons["help"] = help_btn
        
        parent_layout.addWidget(settings_btn)
        parent_layout.addWidget(help_btn)
        
    def create_nav_button(self, icon, text, page_id):
        """Create individual navigation button"""
        btn = QPushButton()
        btn.setFixedHeight(45)
        btn.setObjectName("nav_button")
        
        btn_layout = QHBoxLayout(btn)
        btn_layout.setContentsMargins(20, 0, 20, 0)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setFixedWidth(20)
        icon_label.setStyleSheet("font-size: 16px;")
        btn_layout.addWidget(icon_label)
        
        # Text
        text_label = QLabel(text)
        text_label.setStyleSheet("""
            color: #ECEFF1;
            font-size: 13px;
            font-weight: 500;
        """)
        btn_layout.addWidget(text_label)
        btn_layout.addStretch()
        
        # Set active state for dashboard
        if page_id == "dashboard":
            btn.setProperty("active", "true")
            
        # Connect click event
        btn.clicked.connect(lambda: self.switch_page(page_id))
        
        return btn
        
    def switch_page(self, page_id):
        """Switch to different page"""
        # Update active state
        self.set_active_page(page_id)
        
        # Emit signal
        self.page_changed.emit(page_id)
        
    def set_active_page(self, page_id):
        """Set active page and update button states"""
        # Remove active state from all buttons
        for btn in self.nav_buttons.values():
            btn.setProperty("active", "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            
        # Set active state for selected button
        if page_id in self.nav_buttons:
            self.nav_buttons[page_id].setProperty("active", "true")
            self.nav_buttons[page_id].style().unpolish(self.nav_buttons[page_id])
            self.nav_buttons[page_id].style().polish(self.nav_buttons[page_id])
            
        self.current_page = page_id
        
    def get_current_page(self):
        """Get current active page"""
        return self.current_page