#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Speed Adjuster Action
Xử lý tăng/giảm tốc độ video
"""

import os
from .base_action import BaseAction


class VideoSpeedAdjuster(BaseAction):
    """Xử lý tăng/giảm tốc độ video"""
    
    MIN_SPEED = 0.25
    MAX_SPEED = 4.0
    
    def execute(self, input_folder, output_folder):
        """Thực hiện thay đổi tốc độ video"""
        # Kiểm tra thư mục
        if not self.validate_folders(input_folder, output_folder):
            return
        
        # Lấy danh sách video
        video_files = self.get_video_files(input_folder)
        if not video_files:
            print("❌ Không tìm thấy file video nào!")
            input("Nhấn Enter để tiếp tục...")
            return
        
        print(f"\n⚡ TĂNG/GIẢM TỐC ĐỘ VIDEO")
        print(f"Tìm thấy {len(video_files)} file video")
        
        # Nhập tốc độ
        speed = self._get_speed_input()
        if speed is None:
            return
        
        # Thực hiện thay đổi tốc độ
        self._process_videos(video_files, output_folder, speed)
        
        input("Nhấn Enter để tiếp tục...")
    
    def _get_speed_input(self):
        """Lấy input tốc độ từ user"""
        print("\n🟢 Tốc độ gợi ý:")
        print("0.25x - Chậm 4 lần")
        print("0.5x  - Chậm 2 lần")
        print("0.75x - Chậm 1.3 lần")
        print("1.0x  - Tốc độ bình thường")
        print("1.25x - Nhanh hơn 25%")
        print("1.5x  - Nhanh 1.5 lần")
        print("2.0x  - Nhanh 2 lần")
        print("3.0x  - Nhanh 3 lần")
        
        try:
            speed_input = input(f"\n🎯 Nhập tốc độ mong muốn ({self.MIN_SPEED}-{self.MAX_SPEED}): ").strip()
            speed = float(speed_input)
            
            if speed < self.MIN_SPEED or speed > self.MAX_SPEED:
                print(f"❌ Tốc độ phải từ {self.MIN_SPEED} đến {self.MAX_SPEED}!")
                input("Nhấn Enter để tiếp tục...")
                return None
            
            return speed
            
        except ValueError:
            print("❌ Vui lòng nhập số hợp lệ!")
            input("Nhấn Enter để tiếp tục...")
            return None
    
    def _process_videos(self, video_files, output_folder, speed):
        """Xử lý thay đổi tốc độ cho các video"""
        # Mô tả tốc độ
        if speed < 1.0:
            speed_desc = f"chậm hơn {1/speed:.1f} lần"
        elif speed > 1.0:
            speed_desc = f"nhanh hơn {speed:.1f} lần"
        else:
            speed_desc = "tốc độ bình thường"
        
        print(f"\n🔄 Đang thay đổi tốc độ thành {speed}x ({speed_desc})...")
        print(f"Số file cần xử lý: {len(video_files)}")
        print("-" * 50)
        
        success_count = 0
        error_count = 0
        
        for i, video_file in enumerate(video_files, 1):
            filename = os.path.basename(video_file)
            name, ext = os.path.splitext(filename)
            output_file = os.path.join(output_folder, f"{name}_speed_{speed}x{ext}")
            
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
                print(f"  ⚡ Tốc độ: {speed}x ({speed_desc})")
                
                # Chạy lệnh videoforge process với tốc độ
                self.run_videoforge_command([
                    "process",
                    "-i", video_file,
                    "-o", output_file,
                    "--speed", str(speed)
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
        print("\n" + "=" * 50)
        print(f"🏁 Kết quả thay đổi tốc độ:")
        print(f"  ✅ Thành công: {success_count}/{len(video_files)}")
        print(f"  ❌ Lỗi: {error_count}/{len(video_files)}")
        print(f"  ⚡ Tốc độ áp dụng: {speed}x")
        print("=" * 50)
