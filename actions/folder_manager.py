#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Folder Manager Action
Xử lý quản lý thư mục input và output
"""

import os
import glob
from .base_action import BaseAction


class FolderManagerAction(BaseAction):
    """Xử lý quản lý thư mục input và output"""
    
    def __init__(self):
        super().__init__()
        self.input_folder = ""
        self.output_folder = ""
    
    def execute(self):
        """Thiết lập thư mục input và output"""
        print("\n🔧 THIẾT LẬP THỦ MỤC")
        print("-" * 30)
        
        # Thiết lập thư mục input
        self._set_input_folder()
        
        # Thiết lập thư mục output
        self._set_output_folder()
        
        print("\n✅ Đã thiết lập xong thư mục!")
        input("Nhấn Enter để tiếp tục...")
    
    def get_folders(self):
        """Lấy thông tin thư mục hiện tại"""
        return {
            'input': self.input_folder,
            'output': self.output_folder
        }
    
    def _set_input_folder(self):
        """Thiết lập thư mục input"""
        while True:
            print(f"\n📥 Thư mục Input hiện tại: {self.input_folder or 'Chưa chọn'}")
            input_path = input("📥 Nhập đường dẫn thư mục chứa video: ").strip().strip('"')
            
            if not input_path:
                print("❌ Vui lòng nhập đường dẫn!")
                continue
            
            if not os.path.exists(input_path):
                print("❌ Thư mục không tồn tại!")
                retry = input("Bạn có muốn thử lại không? (y/n): ").lower()
                if retry != 'y':
                    break
                continue
            
            # Kiểm tra và hiển thị video files
            video_files = self.get_video_files(input_path)
            if not video_files:
                print("⚠️  Không tìm thấy file video nào trong thư mục!")
                print("Các định dạng được hỗ trợ: MP4, AVI, MOV, WMV, FLV, MKV, WEBM")
                choice = input("Bạn có muốn tiếp tục không? (y/n): ").lower()
                if choice != 'y':
                    continue
            else:
                print(f"✅ Tìm thấy {len(video_files)} file video:")
                
                # Hiển thị tối đa 10 file đầu tiên
                display_count = min(len(video_files), 10)
                for i, video_file in enumerate(video_files[:display_count], 1):
                    filename = os.path.basename(video_file)
                    file_size = os.path.getsize(video_file) / (1024 * 1024)  # MB
                    print(f"   {i}. {filename} ({file_size:.2f} MB)")
                
                if len(video_files) > 10:
                    print(f"   ... và {len(video_files) - 10} file khác")
            
            self.input_folder = input_path
            print(f"✅ Đã thiết lập thư mục input: {input_path}")
            break
    
    def _set_output_folder(self):
        """Thiết lập thư mục output"""
        while True:
            print(f"\n📤 Thư mục Output hiện tại: {self.output_folder or 'Chưa chọn'}")
            output_path = input("📤 Nhập đường dẫn thư mục xuất video: ").strip().strip('"')
            
            if not output_path:
                print("❌ Vui lòng nhập đường dẫn!")
                continue
            
            # Tạo thư mục output nếu chưa tồn tại
            try:
                os.makedirs(output_path, exist_ok=True)
                
                # Kiểm tra quyền ghi
                test_file = os.path.join(output_path, ".test_write")
                try:
                    with open(test_file, 'w') as f:
                        f.write("test")
                    os.remove(test_file)
                    
                    self.output_folder = output_path
                    print(f"✅ Đã thiết lập thư mục output: {output_path}")
                    
                    # Hiển thị thông tin thư mục
                    self._show_output_folder_info(output_path)
                    break
                    
                except PermissionError:
                    print("❌ Không có quyền ghi vào thư mục này!")
                    continue
                    
            except Exception as e:
                print(f"❌ Không thể tạo thư mục: {e}")
                retry = input("Bạn có muốn thử lại không? (y/n): ").lower()
                if retry != 'y':
                    break
                continue
    
    def _show_output_folder_info(self, output_path):
        """Hiển thị thông tin về thư mục output"""
        try:
            # Kiểm tra không gian trống
            if hasattr(os, 'statvfs'):  # Unix/Linux
                statvfs = os.statvfs(output_path)
                free_space = statvfs.f_frsize * statvfs.f_bavail / (1024**3)  # GB
            else:  # Windows
                import shutil
                total, used, free = shutil.disk_usage(output_path)
                free_space = free / (1024**3)  # GB
            
            print(f"💾 Không gian trống: {free_space:.2f} GB")
            
            # Kiểm tra file existing
            existing_files = []
            for ext in ['*.mp4', '*.avi', '*.mov', '*.wmv', '*.flv', '*.mkv', '*.webm']:
                existing_files.extend(glob.glob(os.path.join(output_path, ext)))
                existing_files.extend(glob.glob(os.path.join(output_path, ext.upper())))
            
            if existing_files:
                print(f"📁 Thư mục đã có {len(existing_files)} file video")
                choice = input("⚠️  File cũ có thể bị ghi đè. Tiếp tục? (y/n): ").lower()
                if choice != 'y':
                    print("❌ Đã hủy thiết lập thư mục output")
                    self.output_folder = ""
                    return False
            
        except Exception as e:
            print(f"⚠️  Không thể kiểm tra thông tin thư mục: {e}")
        
        return True
    
    def validate_setup(self):
        """Kiểm tra xem thư mục đã được thiết lập chưa"""
        if not self.input_folder or not self.output_folder:
            print("❌ Vui lòng thiết lập thư mục input và output trước!")
            return False
        
        if not os.path.exists(self.input_folder):
            print("❌ Thư mục input không tồn tại!")
            return False
        
        if not os.path.exists(self.output_folder):
            print("❌ Thư mục output không tồn tại!")
            return False
        
        return True
    
    def get_input_videos(self):
        """Lấy danh sách video trong thư mục input"""
        if not self.input_folder:
            return []
        return self.get_video_files(self.input_folder)
    
    def get_stats(self):
        """Lấy thống kê về thư mục"""
        stats = {
            'input_folder': self.input_folder,
            'output_folder': self.output_folder,
            'input_videos': 0,
            'input_size_mb': 0,
            'output_videos': 0,
            'output_size_mb': 0
        }
        
        try:
            # Thống kê input
            if self.input_folder and os.path.exists(self.input_folder):
                input_videos = self.get_video_files(self.input_folder)
                stats['input_videos'] = len(input_videos)
                
                total_size = 0
                for video in input_videos:
                    if os.path.exists(video):
                        total_size += os.path.getsize(video)
                stats['input_size_mb'] = total_size / (1024 * 1024)
            
            # Thống kê output
            if self.output_folder and os.path.exists(self.output_folder):
                output_videos = self.get_video_files(self.output_folder)
                stats['output_videos'] = len(output_videos)
                
                total_size = 0
                for video in output_videos:
                    if os.path.exists(video):
                        total_size += os.path.getsize(video)
                stats['output_size_mb'] = total_size / (1024 * 1024)
                
        except Exception as e:
            print(f"⚠️  Lỗi khi tính thống kê: {e}")
        
        return stats
