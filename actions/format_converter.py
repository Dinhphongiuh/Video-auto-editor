#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Format Converter Action - Sử dụng FFmpeg trực tiếp
Xử lý chuyển đổi định dạng video
"""

import os
import subprocess
from .base_action import BaseAction


class VideoFormatConverter(BaseAction):
    """Xử lý chuyển đổi định dạng video bằng FFmpeg trực tiếp"""
    
    SUPPORTED_FORMATS = ["mp4", "avi", "mov", "wmv", "flv", "mkv", "webm"]
    
    # Format configurations for FFmpeg
    FORMAT_CONFIGS = {
        "mp4": {
            "container": "mp4",
            "video_codec": "libx264",
            "audio_codec": "aac"
        },
        "avi": {
            "container": "avi", 
            "video_codec": "libx264",
            "audio_codec": "mp3"
        },
        "mov": {
            "container": "mov",
            "video_codec": "libx264", 
            "audio_codec": "aac"
        },
        "wmv": {
            "container": "asf",
            "video_codec": "wmv2",
            "audio_codec": "wmav2"
        },
        "flv": {
            "container": "flv",
            "video_codec": "libx264",
            "audio_codec": "aac"
        },
        "mkv": {
            "container": "matroska",
            "video_codec": "libx264",
            "audio_codec": "aac"
        },
        "webm": {
            "container": "webm",
            "video_codec": "libvpx-vp9",
            "audio_codec": "libopus"
        }
    }
    
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
        
        # Kiểm tra FFmpeg
        if not self._check_ffmpeg():
            print("❌ FFmpeg không khả dụng! Vui lòng cài đặt FFmpeg.")
            input("Nhấn Enter để tiếp tục...")
            return
        
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
                
                # Chuyển đổi bằng FFmpeg trực tiếp
                if self._convert_with_ffmpeg(video_file, output_file, output_format):
                    output_size = os.path.getsize(output_file) / (1024 * 1024)
                    print(f"  ✅ Thành công! Kích thước output: {output_size:.2f} MB")
                    success_count += 1
                else:
                    print(f"  ❌ Lỗi: Không thể chuyển đổi!")
                    error_count += 1
                    
            except Exception as e:
                print(f"  ❌ Lỗi: {e}")
                error_count += 1
        
        # Hiển thị kết quả
        self._show_results(success_count, error_count, len(video_files), output_format)
        input("Nhấn Enter để tiếp tục...")
    
    def _check_ffmpeg(self):
        """Kiểm tra FFmpeg có khả dụng không"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def _convert_with_ffmpeg(self, input_file, output_file, output_format):
        """Chuyển đổi video bằng FFmpeg trực tiếp"""
        try:
            # Lấy configuration cho format
            config = self.FORMAT_CONFIGS.get(output_format, self.FORMAT_CONFIGS["mp4"])
            
            # Tạo FFmpeg command
            cmd = [
                'ffmpeg',
                '-i', input_file,
                '-c:v', config['video_codec'],
                '-c:a', config['audio_codec'],
                '-f', config['container'],
                '-y',  # Overwrite output
                output_file
            ]
            
            print(f"  🔧 FFmpeg Command: {' '.join(cmd)}")
            
            # Chạy FFmpeg
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True
            else:
                print(f"  ❌ FFmpeg Error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"  ❌ Lỗi khi chạy FFmpeg: {e}")
            return False
    
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
    
    def _show_results(self, success_count, error_count, total_count, output_format):
        """Hiển thị kết quả xử lý"""
        print("\n" + "=" * 50)
        print(f"🏁 Kết quả chuyển đổi:")
        print(f"  ✅ Thành công: {success_count}/{total_count}")
        print(f"  ❌ Lỗi: {error_count}/{total_count}")
        print(f"  📹 Định dạng: {output_format.upper()}")
        if success_count > 0:
            print(f"  📁 Vị trí output: Đã lưu với định dạng .{output_format}")
        print("=" * 50)