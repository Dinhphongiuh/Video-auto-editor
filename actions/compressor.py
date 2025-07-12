#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Compressor Action
Xử lý nén video với các mức chất lượng khác nhau
"""

import os
from .base_action import BaseAction


class VideoCompressor(BaseAction):
    """Xử lý nén video"""
    
    QUALITY_LEVELS = {
        1: ("ultra", "Chất lượng cao nhất"),
        2: ("high", "Chất lượng cao"),
        3: ("medium", "Chất lượng trung bình"),
        4: ("low", "Chất lượng thấp, file nhỏ")
    }
    
    def execute(self, input_folder, output_folder):
        """Thực hiện nén video"""
        # Kiểm tra thư mục
        if not self.validate_folders(input_folder, output_folder):
            return
        
        # Lấy danh sách video
        video_files = self.get_video_files(input_folder)
        if not video_files:
            print("❌ Không tìm thấy file video nào!")
            input("Nhấn Enter để tiếp tục...")
            return
        
        print(f"\n🗜️ NÉN VIDEO")
        print(f"Tìm thấy {len(video_files)} file video")
        
        # Chọn mức nén
        quality = self._select_quality_level()
        if not quality:
            return
        
        # Thực hiện nén
        self._compress_videos(video_files, output_folder, quality)
        
        input("Nhấn Enter để tiếp tục...")
    
    def _select_quality_level(self):
        """Cho phép user chọn mức chất lượng"""
        print("\nChọn mức nén:")
        for key, (_, desc) in self.QUALITY_LEVELS.items():
            print(f"{key}. {desc}")
        
        try:
            choice = int(input("Nhập số: "))
            
            if choice in self.QUALITY_LEVELS:
                quality, desc = self.QUALITY_LEVELS[choice]
                return quality
            else:
                print("❌ Lựa chọn không hợp lệ!")
                input("Nhấn Enter để tiếp tục...")
                return None
                
        except ValueError:
            print("❌ Vui lòng nhập số!")
            input("Nhấn Enter để tiếp tục...")
            return None
    
    def _compress_videos(self, video_files, output_folder, quality):
        """Nén các video với chất lượng đã chọn"""
        print(f"\n🔄 Đang nén video với chất lượng {quality.upper()}...")
        print(f"Số file cần xử lý: {len(video_files)}")
        print("-" * 50)
        
        success_count = 0
        error_count = 0
        total_saved = 0  # Tổng dung lượng đã tiết kiệm
        
        for i, video_file in enumerate(video_files, 1):
            filename = os.path.basename(video_file)
            name, ext = os.path.splitext(filename)
            output_file = os.path.join(output_folder, f"{name}_compressed{ext}")
            
            print(f"\n[{i}/{len(video_files)}] 📁 Xử lý: {filename}")
            
            try:
                # Kích thước file gốc
                original_size = os.path.getsize(video_file) / (1024 * 1024)  # MB
                print(f"  📀 Kích thước gốc: {original_size:.2f} MB")
                
                # Chạy lệnh nén
                self.run_videoforge_command([
                    "process",
                    "-i", video_file,
                    "-o", output_file,
                    "--quality", quality
                ])
                
                # Kiểm tra kết quả
                if os.path.exists(output_file):
                    compressed_size = os.path.getsize(output_file) / (1024 * 1024)
                    saved = original_size - compressed_size
                    saved_percent = (saved / original_size) * 100
                    
                    print(f"  ✅ Thành công!")
                    print(f"  📉 Kích thước sau nén: {compressed_size:.2f} MB")
                    print(f"  💾 Đã tiết kiệm: {saved:.2f} MB ({saved_percent:.1f}%)")
                    
                    success_count += 1
                    total_saved += saved
                else:
                    print(f"  ❌ Lỗi: File output không được tạo!")
                    error_count += 1
                    
            except Exception as e:
                print(f"  ❌ Lỗi: {e}")
                error_count += 1
        
        # Hiển thị kết quả tổng hợp
        print("\n" + "=" * 50)
        print(f"🏁 Kết quả nén video:")
        print(f"  ✅ Thành công: {success_count}/{len(video_files)}")
        print(f"  ❌ Lỗi: {error_count}/{len(video_files)}")
        print(f"  💾 Tổng dung lượng tiết kiệm: {total_saved:.2f} MB")
        print(f"  🗜️ Chất lượng áp dụng: {quality.upper()}")
        print("=" * 50)
