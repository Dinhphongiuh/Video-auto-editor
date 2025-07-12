#!/usr/bin/env python3
"""
AutoEdit Video UI Desktop - Main Entry Point
Professional video editing interface for VideoForge
"""

import sys
import os
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Main application entry point"""
    try:
        from src.core.app import AutoEditApp
        
        # Initialize and run application
        app = AutoEditApp()
        return app.run()
        
    except ImportError as e:
        print(f"Import Error: {e}")
        print("Please install required dependencies: pip install -r requirements.txt")
        return 1
        
    except Exception as e:
        print(f"Application Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
