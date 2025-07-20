"""
Toolbar Widget
Video editor toolbar with main actions
"""

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)
from PyQt6.QtCore import Qt, pyqtSignal


class ToolbarWidget(QWidget):
    """Video editor toolbar"""

    # Signals
    import_clicked = pyqtSignal()
    export_clicked = pyqtSignal()
    undo_clicked = pyqtSignal()
    redo_clicked = pyqtSignal()
    cut_clicked = pyqtSignal()
    copy_clicked = pyqtSignal()
    paste_clicked = pyqtSignal()
    delete_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Setup toolbar UI"""
        self.setObjectName("editor_toolbar")
        self.setFixedHeight(50)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 5, 15, 5)
        layout.setSpacing(10)

        # Title
        title = QLabel("🎬 Video Editor")
        title.setStyleSheet("color: #ECEFF1; font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        layout.addStretch()

        # File operations
        self.import_btn = self.create_toolbar_button(
            "📁", "Import", self.import_clicked
        )
        layout.addWidget(self.import_btn)

        self.export_btn = self.create_toolbar_button(
            "💾", "Export", self.export_clicked
        )
        layout.addWidget(self.export_btn)

        # Separator
        separator1 = self.create_separator()
        layout.addWidget(separator1)

        # Edit operations
        self.undo_btn = self.create_toolbar_button("↶", "Undo", self.undo_clicked)
        layout.addWidget(self.undo_btn)

        self.redo_btn = self.create_toolbar_button("↷", "Redo", self.redo_clicked)
        layout.addWidget(self.redo_btn)

        # Separator
        separator2 = self.create_separator()
        layout.addWidget(separator2)

        # Clipboard operations
        self.cut_btn = self.create_toolbar_button("✂️", "Cut", self.cut_clicked)
        layout.addWidget(self.cut_btn)

        self.copy_btn = self.create_toolbar_button("📋", "Copy", self.copy_clicked)
        layout.addWidget(self.copy_btn)

        self.paste_btn = self.create_toolbar_button("📌", "Paste", self.paste_clicked)
        layout.addWidget(self.paste_btn)

        self.delete_btn = self.create_toolbar_button("🗑️", "Delete", self.delete_clicked)
        layout.addWidget(self.delete_btn)

    def create_toolbar_button(self, icon, text, signal):
        """Create toolbar button"""
        btn = QPushButton(f"{icon}")
        btn.setToolTip(text)
        btn.setObjectName("toolbar_button")
        btn.setFixedSize(35, 35)
        btn.clicked.connect(signal.emit)
        return btn

    def create_separator(self):
        """Create toolbar separator"""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #546E7A;")
        return separator
