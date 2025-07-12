#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Resolution Changer Action
Xử lý thay đổi độ phân giải video
"""

import os
from .base_action import BaseAction


class VideoResolutionChanger(BaseAction):
    """Xử lý thay đổi độ phân giải video"""
    
    RESOLUTION_PRESETS = {
        "1": ("1920", "1080", "Full HD"),
        "2": ("1280", "720", "HD"),
        "3": ("854", "480", "SD"),
        "4": ("640", "360", "Low"),
        "5": ("custom", "custom", "Tùy chỉnh")
    }
    
    def execute(self, input_folder, output_folder):
        """Thực hiện thay đổi độ phân giải video"""
        # Kiểm tra thư mục
        if not self.validate_folders(input_folder, output_folder):
            return
        
        # Lấy danh sách video
        video_files = self.get_video_files(input_folder)
        if not video_files:
            print("❌ Không tìm thấy file video nào!")
            input("Nhấn Enter để tiếp tục...")
            return
        
        print(f"\n📐 THAY ĐỔI ĐỘ PHÂN GIẢI")
        print(f"Tìm thấy {len(video_files)} file video")
        
        # Chọn độ phân giải
        width, height = self._select_resolution()
        if not width or not height:
            return
        
        # Thực hiện thay đổi
        print(f"\n🔄 Đang thay đổi độ phân giải thành {width}x{height}...")
        print(f"Số file cần xử lý: {len(video_files)}")
        print("-" * 50)
        
        success_count = 0
        error_count = 0
        
        for i, video_file in enumerate(video_files, 1):
            filename = os.path.basename(video_file)
            name, ext = os.path.splitext(filename)
            output_file = os.path.join(output_folder, f"{name}_{width}x{height}{ext}")
            
            print(f"\n[{i}/{len(video_files)}] 📁 Xử lý: {filename}")
            print(f"  📍 Input : {video_file}")
            print(f"  📤 Output: {output_file}")
            
            # Kiểm tra file input tồn tại
            if not os.path.exists(video_file):
                print(f"  ❌ Lỗi: File input không tồn tại!")
                error_count += 1
                continue
            
            try:
                # Kiểm tra trạng thái trước khi chạy
                file_size = os.path.getsize(video_file) / (1024 * 1024)  # MB
                print(f"  📀 Kích thước file: {file_size:.2f} MB")
                print(f"  📐 Độ phân giải: {width}x{height}")
                
                # Chạy lệnh thay đổi độ phân giải
                self.run_videoforge_command([
                    "process",
                    "-i", video_file,
                    "-o", output_file,
                    "--resolution", f"{width}x{height}"
                ])
                
                # Kiểm tra kết quả
                if os.path.exists(output_file):
                    output_size = os.path.getsize(output_file) / (1024 * 1024)
                    print(f"  ✅ Thành công! Kích thước output: {output_size:.2f} MB")
                    success_count += 1
                else:
                    print(f"  ❌ Lỗi: File output không được tạo!")
                    error_count += 1
                    
            except Exception as e:
                print(f"  ❌ Lỗi: {e}")
                error_count += 1
        
        # Hiển thị kết quả
        self._show_results(success_count, error_count, len(video_files), width, height)
        input("Nhấn Enter để tiếp tục...")
    
    def _select_resolution(self):
        """Cho phép user chọn độ phân giải"""
        print("\nChọn độ phân giải:")
        for key, (width, height, name) in self.RESOLUTION_PRESETS.items():
            if key == "5":
                print(f"{key}. {name}")
            else:
                print(f"{key}. {width}x{height} ({name})")
        
        try:
            choice = input("Nhập số: ").strip()
            
            if choice in self.RESOLUTION_PRESETS:
                width, height, name = self.RESOLUTION_PRESETS[choice]
                
                if choice == "5":  # Tùy chỉnh
                    width = input("Nhập chiều rộng: ").strip()
                    height = input("Nhập chiều cao: ").strip()
                    
                    # Validate input
                    try:
                        int(width)
                        int(height)
                        return width, height
                    except ValueError:
                        print("❌ Vui lòng nhập số hợp lệ!")
                        return None, None
                
                return width, height
            else:
                print("❌ Lựa chọn không hợp lệ!")
                return None, None
                
        except ValueError:
            print("❌ Vui lòng nhập số!")
            return None, None
    
    def _show_results(self, success_count, error_count, total_count, width, height):
        """Hiển thị kết quả xử lý"""
        print("\n" + "=" * 50)
        print(f"🏁 Kết quả thay đổi độ phân giải:")
        print(f"  ✅ Thành công: {success_count}/{total_count}")
        print(f"  ❌ Lỗi: {error_count}/{total_count}")
        print(f"  📐 Độ phân giải: {width}x{height}")
        print("=" * 50)
