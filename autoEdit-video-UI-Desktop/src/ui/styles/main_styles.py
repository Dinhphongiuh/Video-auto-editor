"""
Main Styles - Centralized styling for the application
"""

# Color palette
COLORS = {
    'primary': '#2196F3',
    'primary_dark': '#1976D2',
    'primary_darker': '#1565C0',
    'secondary': '#4CAF50',
    'warning': '#FF9800',
    'danger': '#F44336',
    'success': '#4CAF50',
    'background': '#263238',
    'surface': '#37474F',
    'surface_dark': '#455A64',
    'border': '#546E7A',
    'border_light': '#607D8B',
    'text': '#ECEFF1',
    'text_secondary': '#B0BEC5',
    'text_muted': '#90A4AE',
}

# Common button styles
def get_button_style(bg_color, hover_color, text_color='white'):
    return f"""
        QPushButton {{
            background-color: {bg_color};
            color: {text_color};
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-size: 13px;
            font-weight: bold;
            min-height: 20px;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
        QPushButton:pressed {{
            background-color: {hover_color};
        }}
    """

# Main stylesheet
MAIN_STYLESHEET = f"""
    QMainWindow {{
        background-color: {COLORS['background']};
    }}
    
    QFrame#sidebar {{
        background-color: {COLORS['surface']};
        border-right: 1px solid {COLORS['surface_dark']};
    }}
    
    QWidget#header {{
        background-color: {COLORS['surface_dark']};
        border-bottom: 1px solid {COLORS['border']};
    }}
    
    QFrame#content {{
        background-color: {COLORS['background']};
    }}
    
    QFrame#top_bar {{
        background-color: {COLORS['surface']};
        border-bottom: 1px solid {COLORS['surface_dark']};
    }}
    
    QPushButton#nav_button {{
        background-color: transparent;
        border: none;
        text-align: left;
        color: {COLORS['text']};
        padding: 8px 20px;
        border-radius: 0px;
    }}
    
    QPushButton#nav_button:hover {{
        background-color: {COLORS['surface_dark']};
    }}
    
    QPushButton#nav_button[active="true"] {{
        background-color: {COLORS['primary_dark']};
        color: #FFFFFF;
    }}
    
    QFrame#section {{
        background-color: {COLORS['surface']};
        border: 1px solid {COLORS['surface_dark']};
        border-radius: 8px;
    }}
    
    FileDropWidget {{
        background-color: {COLORS['surface']};
        border: 2px dashed {COLORS['border']};
        border-radius: 12px;
    }}
    
    QComboBox {{
        background-color: {COLORS['surface_dark']};
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
        padding: 8px 12px;
        color: {COLORS['text']};
        font-size: 13px;
        min-height: 20px;
    }}
    
    QComboBox:hover {{
        border-color: {COLORS['border_light']};
    }}
    
    QComboBox::drop-down {{
        border: none;
        width: 20px;
        subcontrol-origin: padding;
        subcontrol-position: top right;
    }}
    
    QComboBox::down-arrow {{
        width: 0px;
        height: 0px;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 6px solid {COLORS['text_secondary']};
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {COLORS['surface_dark']};
        border: 1px solid {COLORS['border_light']};
        selection-background-color: {COLORS['border']};
        color: {COLORS['text']};
        outline: none;
    }}
    
    QLineEdit {{
        background-color: {COLORS['surface_dark']};
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
        padding: 8px 12px;
        color: {COLORS['text']};
        font-size: 13px;
        min-height: 20px;
    }}
    
    QLineEdit:focus {{
        border-color: {COLORS['primary']};
        outline: none;
    }}
    
    QSlider::groove:horizontal {{
        border: 1px solid {COLORS['border']};
        height: 6px;
        background: {COLORS['surface_dark']};
        border-radius: 3px;
        margin: 0px;
    }}
    
    QSlider::handle:horizontal {{
        background: {COLORS['primary']};
        border: 2px solid {COLORS['primary_dark']};
        width: 16px;
        height: 16px;
        margin: -6px 0px;
        border-radius: 8px;
    }}
    
    QSlider::handle:horizontal:hover {{
        background: {COLORS['primary_dark']};
    }}
    
    QPushButton#quick_button {{
        background-color: {COLORS['border']};
        color: {COLORS['text']};
        border: none;
        border-radius: 3px;
        font-size: 11px;
        min-height: 20px;
        padding: 4px 8px;
    }}
    
    QPushButton#quick_button:hover {{
        background-color: {COLORS['border_light']};
    }}
    
    QProgressBar {{
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
        background-color: {COLORS['surface_dark']};
        text-align: center;
        color: {COLORS['text']};
        font-weight: bold;
        min-height: 18px;
    }}
    
    QProgressBar::chunk {{
        background-color: {COLORS['primary']};
        border-radius: 3px;
        margin: 1px;
    }}
"""

# Button styles
BUTTON_STYLES = {
    'start': get_button_style(COLORS['primary'], COLORS['primary_dark']),
    'pause': get_button_style(COLORS['warning'], '#F57C00'),
    'stop': get_button_style(COLORS['danger'], '#D32F2F'),
    'export': get_button_style(COLORS['success'], '#388E3C'),
    'browse': get_button_style(COLORS['border'], COLORS['border_light']),
}