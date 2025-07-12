#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base Action Class
Lớp cơ sở cho tất cả các action
"""

import os
import glob
import subprocess


class BaseAction:
    """Lớp cơ sở cho tất cả các action"""
    
    def __init__(self):
        self.video_extensions = ['*.mp4', '*.avi', '*.mov', '*.wmv', '*.flv', '*.mkv', '*.webm']
    
    def validate_folders(self, input_folder, output_folder):
        """Kiểm tra thư mục input và output"""
        if not input_folder or not output_folder:
            print("❌ Vui lòng thiết lập thư mục input và output trước!")
            input("Nhấn Enter để tiếp tục...")
            return False
        return True
    
    def get_video_files(self, folder_path):
        """Lấy danh sách file video trong thư mục"""
        if not folder_path or not os.path.exists(folder_path):
            return []
        
        video_files = []
        
        for ext in self.video_extensions:
            video_files.extend(glob.glob(os.path.join(folder_path, ext)))
            video_files.extend(glob.glob(os.path.join(folder_path, ext.upper())))
        
        # Loại bỏ duplicate (do Windows không phân biệt chữ hoa/thường)
        video_files = list(set(video_files))
        video_files.sort()  # Sắp xếp theo thứ tự abc
        
        return video_files
    
    def run_videoforge_command(self, command_parts):
        """Chạy lệnh videoforge"""
        try:
            # Log chi tiết các tham số
            print("\n🔍 DEBUG: Tham số lệnh:")
            for i, part in enumerate(command_parts):
                print(f"  [{i}]: {part}")
            
            # Kích hoạt virtual environment và chạy lệnh
            venv_python = os.path.join("D:", "VideoForge", "videoforge-core", "venv", "Scripts", "python.exe")
            
            if os.path.exists(venv_python):
                cmd = [venv_python, "-m", "videoforge"] + command_parts
            else:
                cmd = ["videoforge"] + command_parts
            
            print(f"\n🚀 Đang chạy: {' '.join(cmd)}")
            print(f"📝 Chi tiết lệnh: {cmd}")
            print("-" * 50)
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            print(f"\n📊 Mã trả về: {result.returncode}")
            
            if result.returncode == 0:
                print("✅ Thành công!")
                if result.stdout:
                    print("📤 Kết quả:")
                    print(result.stdout)
            else:
                print("❌ Lỗi!")
                print(f"🏁 Return code: {result.returncode}")
                
                # Hiển thị tất cả output để debug
                if result.stderr:
                    print("\n🔥 Lỗi chi tiết (stderr):")
                    print(result.stderr)
                    
                if result.stdout:
                    print("\n📤 Output (stdout):")
                    print(result.stdout)
                    
        except Exception as e:
            print(f"❌ Lỗi khi chạy lệnh: {e}")
            import traceback
            print(f"🔍 Chi tiết lỗi: {traceback.format_exc()}")
    
    def execute(self, input_folder, output_folder):
        """Phương thức abstract - các subclass phải implement"""
        raise NotImplementedError("Subclass must implement execute method")
