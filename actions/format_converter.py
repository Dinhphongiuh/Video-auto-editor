#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Format Converter Action
Xử lý chuyển đổi định dạng video
"""

import os
import glob
from .base_action import BaseAction


class VideoFormatConverter(BaseAction):
    """Xử lý chuyển đổi định dạng video"""
    
    SUPPORTED_FORMATS = ["mp4", "avi", "mov", "wmv", "flv", "mkv", "webm"]
    
    def execute(self, input_folder, output_folder):
        """Thực hiện chuyển đổi định dạng video"""
        # Kiểm tra thư mục
        if not self.validate_folders(input_folder, output_folder):
            return
        
        # Lấy danh sách video
        video_files = self.get_video_files(input_folder)
        if not video_files:
            print("❌ Không tìm thấy file video nào!")
            input("Nhấn Enter để tiếp tục...")
            return
        
        print(f"\n📹 CHUYỂN ĐỔI ĐỊNH DẠNG VIDEO")
        print(f"Tìm thấy {len(video_files)} file video")
        
        # Chọn định dạng output
        output_format = self._select_output_format()
        if not output_format:
            return
        
        # Thực hiện chuyển đổi
        print(f"\n🔄 Đang chuyển đổi sang {output_format.upper()}...")
        print(f"Số file cần xử lý: {len(video_files)}")
        print("-" * 50)
        
        success_count = 0
        error_count = 0
        
        for i, video_file in enumerate(video_files, 1):
            filename = os.path.basename(video_file)
            name, _ = os.path.splitext(filename)
            output_file = os.path.join(output_folder, f"{name}.{output_format}")
            
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
                print(f"  🔄 Chuyển đổi sang định dạng: {output_format.upper()}")
                
                # Chạy lệnh chuyển đổi
                self.run_videoforge_command([
                    "process",
                    "-i", video_file,
                    "-o", output_file,
                    "--format", output_format
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
        self._show_results(success_count, error_count, len(video_files))
        input("Nhấn Enter để tiếp tục...")
    
    def _select_output_format(self):
        """Cho phép user chọn định dạng output"""
        print("\nChọn định dạng output:")
        for i, fmt in enumerate(self.SUPPORTED_FORMATS, 1):
            print(f"{i}. {fmt.upper()}")
        
        try:
            choice = int(input("Nhập số: ")) - 1
            if 0 <= choice < len(self.SUPPORTED_FORMATS):
                return self.SUPPORTED_FORMATS[choice]
            else:
                print("❌ Lựa chọn không hợp lệ!")
                return None
                
        except ValueError:
            print("❌ Vui lòng nhập số!")
            return None
    
    def _show_results(self, success_count, error_count, total_count):
        """Hiển thị kết quả xử lý"""
        print("\n" + "=" * 50)
        print(f"🏁 Kết quả chuyển đổi:")
        print(f"  ✅ Thành công: {success_count}/{total_count}")
        print(f"  ❌ Lỗi: {error_count}/{total_count}")
        print("=" * 50)
