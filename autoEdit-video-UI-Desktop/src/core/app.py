"""
Core Application Class - Hello World Version
Main application initialization and lifecycle management
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from ..ui.windows.main_window import MainWindow


class AutoEditApp:
    """Main application class - Entry point for desktop app"""
    
    def __init__(self):
        """Initialize application"""
        self.app = None
        self.main_window = None
        
    def initialize(self):
        """Initialize PyQt application"""
        # Create QApplication instance
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("AutoEdit Video UI Desktop")
        self.app.setApplicationVersion("1.0.0")
        self.app.setOrganizationName("VideoForge Team")
        
        # Set application style
        self.app.setStyle('Fusion')
        
        # Create main window
        self.main_window = MainWindow()
        
        return True
    
    def run(self):
        """Run the application"""
        try:
            # Initialize application
            if not self.initialize():
                print("Failed to initialize application")
                return 1
            
            # Show main window
            self.main_window.show()
            
            # Start event loop
            return self.app.exec()
            
        except ImportError as e:
            print(f"Import Error: {e}")
            print("Please install PyQt6: pip install PyQt6")
            return 1
            
        except Exception as e:
            print(f"Application Error: {e}")
            return 1
    
    def cleanup(self):
        """Cleanup application resources"""
        if self.main_window:
            self.main_window.close()
        if self.app:
            self.app.quit()
