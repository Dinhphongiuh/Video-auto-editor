#!/usr/bin/env python3
"""
Test script để kiểm tra format conversion
"""

import subprocess
import sys
from pathlib import Path

def test_format_conversion():
    """Test format conversion functionality"""
    
    # Test command
    test_video = "D:/AUTO_VIDEO_EDITOR_TEST_IP/video1.mkv"
    output_video = "D:/AUTO_VIDEO_EDITOR_TEST_IP/test_output.mp4"
    
    if not Path(test_video).exists():
        print(f"❌ Test video not found: {test_video}")
        return False
    
    print("🧪 Testing format conversion...")
    print(f"Input: {test_video}")
    print(f"Output: {output_video}")
    
    # Build command
    venv_python = Path("D:/VideoForge/videoforge-core/venv/Scripts/python.exe")
    
    if venv_python.exists():
        cmd = [
            str(venv_python), "-m", "videoforge", "process",
            "-i", test_video,
            "-o", output_video,
            "--format", "mp4"
        ]
    else:
        cmd = [
            "videoforge", "process",
            "-i", test_video,
            "-o", output_video,
            "--format", "mp4"
        ]
    
    print(f"🚀 Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        print(f"Return code: {result.returncode}")
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        # Check if output file was created
        if Path(output_video).exists():
            file_size = Path(output_video).stat().st_size
            print(f"✅ Success! Output file created: {file_size} bytes")
            return True
        else:
            print("❌ Output file was not created")
            return False
            
    except Exception as e:
        print(f"❌ Error running test: {e}")
        return False

if __name__ == "__main__":
    success = test_format_conversion()
    sys.exit(0 if success else 1)
