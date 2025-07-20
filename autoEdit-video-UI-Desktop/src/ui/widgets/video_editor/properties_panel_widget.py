"""
Properties Panel Widget
Effects and properties control panel
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QSlider,
    QSpinBox,
    QComboBox,
    QPushButton,
    QScrollArea,
    QTabWidget,
    QCheckBox,
    QGroupBox,
)
from PyQt6.QtCore import Qt, pyqtSignal


class TransformTab(QWidget):
    """Transform controls tab"""

    transform_changed = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.transform_data = {
            "position_x": 0,
            "position_y": 0,
            "scale": 100,
            "rotation": 0,
        }
        self.setup_ui()

    def setup_ui(self):
        """Setup transform UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Position
        position_group = self.create_position_group()
        layout.addWidget(position_group)

        # Scale
        scale_group = self.create_scale_group()
        layout.addWidget(scale_group)

        # Rotation
        rotation_group = self.create_rotation_group()
        layout.addWidget(rotation_group)

        layout.addStretch()

    def create_position_group(self):
        """Create position controls"""
        group = QGroupBox("Position")
        group.setObjectName("properties_group")

        layout = QVBoxLayout(group)
        layout.setSpacing(8)

        # X position
        x_layout = QHBoxLayout()
        x_label = QLabel("X:")
        x_label.setFixedWidth(20)
        x_layout.addWidget(x_label)

        x_spin = QSpinBox()
        x_spin.setRange(-2000, 2000)
        x_spin.setValue(0)
        x_spin.valueChanged.connect(lambda v: self.update_transform("position_x", v))
        x_layout.addWidget(x_spin)

        layout.addLayout(x_layout)

        # Y position
        y_layout = QHBoxLayout()
        y_label = QLabel("Y:")
        y_label.setFixedWidth(20)
        y_layout.addWidget(y_label)

        y_spin = QSpinBox()
        y_spin.setRange(-2000, 2000)
        y_spin.setValue(0)
        y_spin.valueChanged.connect(lambda v: self.update_transform("position_y", v))
        y_layout.addWidget(y_spin)

        layout.addLayout(y_layout)

        return group

    def create_scale_group(self):
        """Create scale controls"""
        group = QGroupBox("Scale")
        group.setObjectName("properties_group")

        layout = QVBoxLayout(group)
        layout.setSpacing(8)

        scale_layout = QHBoxLayout()

        scale_slider = QSlider(Qt.Orientation.Horizontal)
        scale_slider.setRange(10, 500)
        scale_slider.setValue(100)
        scale_slider.valueChanged.connect(lambda v: self.update_transform("scale", v))
        scale_layout.addWidget(scale_slider)

        scale_spin = QSpinBox()
        scale_spin.setRange(10, 500)
        scale_spin.setValue(100)
        scale_spin.setSuffix("%")
        scale_spin.valueChanged.connect(lambda v: self.update_transform("scale", v))
        scale_layout.addWidget(scale_spin)

        # Connect slider and spinbox
        scale_slider.valueChanged.connect(scale_spin.setValue)
        scale_spin.valueChanged.connect(scale_slider.setValue)

        layout.addLayout(scale_layout)

        return group

    def create_rotation_group(self):
        """Create rotation controls"""
        group = QGroupBox("Rotation")
        group.setObjectName("properties_group")

        layout = QVBoxLayout(group)
        layout.setSpacing(8)

        rotation_layout = QHBoxLayout()

        rotation_slider = QSlider(Qt.Orientation.Horizontal)
        rotation_slider.setRange(-180, 180)
        rotation_slider.setValue(0)
        rotation_slider.valueChanged.connect(
            lambda v: self.update_transform("rotation", v)
        )
        rotation_layout.addWidget(rotation_slider)

        rotation_spin = QSpinBox()
        rotation_spin.setRange(-180, 180)
        rotation_spin.setValue(0)
        rotation_spin.setSuffix("°")
        rotation_spin.valueChanged.connect(
            lambda v: self.update_transform("rotation", v)
        )
        rotation_layout.addWidget(rotation_spin)

        # Connect slider and spinbox
        rotation_slider.valueChanged.connect(rotation_spin.setValue)
        rotation_spin.valueChanged.connect(rotation_slider.setValue)

        layout.addLayout(rotation_layout)

        return group

    def update_transform(self, key, value):
        """Update transform value and emit signal"""
        self.transform_data[key] = value
        self.transform_changed.emit(self.transform_data.copy())


class EffectsTab(QWidget):
    """Effects control tab"""

    effect_applied = pyqtSignal(str, dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Setup effects UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Effects library
        effects_group = QGroupBox("Effects Library")
        effects_group.setObjectName("properties_group")

        effects_layout = QVBoxLayout(effects_group)
        effects_layout.setSpacing(10)

        effects = [
            ("🌟", "Blur", lambda: self.apply_effect("blur", {"strength": 5})),
            ("✨", "Sharpen", lambda: self.apply_effect("sharpen", {"strength": 3})),
            ("🎨", "Sepia", lambda: self.apply_effect("sepia", {"intensity": 80})),
            ("⚫", "Black & White", lambda: self.apply_effect("black_white", {})),
        ]

        for icon, name, callback in effects:
            btn = QPushButton(f"{icon} {name}")
            btn.setObjectName("effect_button")
            btn.setFixedHeight(30)
            btn.clicked.connect(callback)
            effects_layout.addWidget(btn)

        layout.addWidget(effects_group)
        layout.addStretch()

    def apply_effect(self, effect_name, params):
        """Apply effect"""
        self.effect_applied.emit(effect_name, params)


class PropertiesPanelWidget(QWidget):
    """Main properties panel widget with tabs"""

    # Signals
    transform_changed = pyqtSignal(dict)
    effect_applied = pyqtSignal(str, dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_media = None
        self.current_clip = None
        self.setup_ui()

    def setup_ui(self):
        """Setup properties panel UI"""
        self.setObjectName("properties_panel")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = self.create_header()
        layout.addWidget(header)

        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("properties_tabs")

        # Transform tab
        self.transform_tab = TransformTab()
        self.transform_tab.transform_changed.connect(self.transform_changed.emit)
        self.tab_widget.addTab(self.transform_tab, "Transform")

        # Effects tab
        self.effects_tab = EffectsTab()
        self.effects_tab.effect_applied.connect(self.effect_applied.emit)
        self.tab_widget.addTab(self.effects_tab, "Effects")

        layout.addWidget(self.tab_widget)

    def create_header(self):
        """Create header"""
        header = QFrame()
        header.setFixedHeight(40)
        header.setObjectName("properties_header")

        layout = QHBoxLayout(header)
        layout.setContentsMargins(10, 5, 10, 5)

        title = QLabel("⚙️ Properties")
        title.setStyleSheet("color: #ECEFF1; font-size: 14px; font-weight: bold;")
        layout.addWidget(title)

        layout.addStretch()

        return header

    def set_media(self, media_path):
        """Set current media"""
        self.current_media = media_path

    def set_clip(self, clip_data):
        """Set current clip"""
        self.current_clip = clip_data

    def update_transform(self, transform_data):
        """Update transform from external source"""
        # Update UI controls with transform data
        pass

    def get_data(self):
        """Get properties data"""
        return {
            "transform": self.transform_tab.transform_data,
            "effects": [],  # TODO: Implement effects data
        }
