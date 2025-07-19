#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Trimmer Action
Tự động cắt video từ đầu hoặc cuối theo số giây chỉ định
"""

import os
import subprocess
from .base_action import BaseAction


class VideoTrimmerAction(BaseAction):
    """Action để cắt video tự động"""
    
    def __init__(self):
        super().__init__()
        
        # Trim options
        self.trim_options = {
            "1": {
                "name": "Cắt từ đầu video",
                "description": "Bỏ N giây đầu video",
                "type": "start"
            },
            "2": {
                "name": "Cắt từ cuối video", 
                "description": "Bỏ N giây cuối video",
                "type": "end"
            }
        }
    
    def check_ffmpeg(self):
        """Kiểm tra FFmpeg có sẵn không"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def get_video_duration(self, video_file):
        """Lấy thời lượng video bằng ffprobe"""
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                video_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                duration = float(result.stdout.strip())
                return duration
            else:
                print(f"❌ Lỗi ffprobe: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Lỗi lấy duration: {e}")
            return None
    
    def show_trim_menu(self):
        """Hiển thị menu chọn kiểu cắt"""
        print("\n✂️ CHỌN KIỂU CẮT VIDEO:")
        print("-" * 50)
        for key, option in self.trim_options.items():
            print(f"{key}. {option['name']} - {option['description']}")
        print("0. ← Quay lại")
        print("-" * 50)
    
    def get_trim_choice(self):
        """Lấy lựa chọn kiểu cắt từ user"""
        while True:
            choice = input("👉 Chọn kiểu cắt (0-2): ").strip()
            if choice == "0":
                return None
            elif choice in self.trim_options:
                return choice
            else:
                print("❌ Lựa chọn không hợp lệ! Vui lòng chọn từ 0-2.")
    
    def get_trim_seconds(self, trim_type, max_duration):
        """Lấy số giây cần cắt từ user"""
        while True:
            if trim_type == "start":
                prompt = f"⏱️ Nhập số giây cần bỏ từ đầu video (1-{int(max_duration-1)}): "
            else:
                prompt = f"⏱️ Nhập số giây cần bỏ từ cuối video (1-{int(max_duration-1)}): "
            
            try:
                seconds_input = input(prompt).strip()
                if not seconds_input:
                    print("❌ Vui lòng nhập số giây")
                    continue
                
                seconds = float(seconds_input)
                
                if seconds <= 0:
                    print("❌ Số giây phải lớn hơn 0")
                    continue
                elif seconds >= max_duration:
                    print(f"❌ Số giây không được >= thời lượng video ({max_duration:.1f}s)")
                    continue
                else:
                    return seconds
                    
            except ValueError:
                print("❌ Vui lòng nhập số hợp lệ")
    
    def trim_video_start(self, input_file, output_file, skip_seconds):
        """Cắt video từ đầu (bỏ N giây đầu)"""
        try:
            print(f"✂️ Đang cắt {skip_seconds} giây đầu video...")
            
            cmd = [
                'ffmpeg',
                '-i', input_file,
                '-ss', str(skip_seconds),  # Skip first N seconds
                '-c', 'copy',  # Copy streams without re-encoding (faster)
                '-avoid_negative_ts', 'make_zero',
                '-y',  # Overwrite output
                output_file
            ]
            
            print(f"🚀 Command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Cắt video thành công!")
                return True
            else:
                print(f"❌ Lỗi FFmpeg: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Lỗi trim video start: {e}")
            return False
    
    def trim_video_end(self, input_file, output_file, duration, cut_seconds):
        """Cắt video từ cuối (bỏ N giây cuối)"""
        try:
            print(f"✂️ Đang cắt {cut_seconds} giây cuối video...")
            
            # Tính thời lượng output = duration - cut_seconds
            output_duration = duration - cut_seconds
            
            cmd = [
                'ffmpeg',
                '-i', input_file,
                '-t', str(output_duration),  # Duration of output
                '-c', 'copy',  # Copy streams without re-encoding (faster)
                '-y',  # Overwrite output
                output_file
            ]
            
            print(f"🚀 Command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Cắt video thành công!")
                return True
            else:
                print(f"❌ Lỗi FFmpeg: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Lỗi trim video end: {e}")
            return False
    
    def trim_single_video(self, video_file, output_folder, trim_type, trim_seconds):
        """Cắt một video đơn lẻ"""
        try:
            print(f"\n🎬 Đang xử lý: {os.path.basename(video_file)}")
            
            # Lấy thời lượng video
            print("📊 Đang lấy thông tin video...")
            duration = self.get_video_duration(video_file)
            
            if duration is None:
                print("❌ Không thể lấy thời lượng video")
                return False
            
            duration_str = f"{int(duration//60)}:{int(duration%60):02d}"
            print(f"⏱️ Thời lượng: {duration_str} ({duration:.1f}s)")
            
            # Kiểm tra trim_seconds hợp lệ
            if trim_seconds >= duration:
                print(f"❌ Không thể cắt {trim_seconds}s từ video {duration:.1f}s")
                return False
            
            # Tạo tên file output
            base_name = os.path.splitext(os.path.basename(video_file))[0]
            extension = os.path.splitext(video_file)[1]
            
            if trim_type == "start":
                output_filename = f"{base_name}_trimmed_start_{int(trim_seconds)}s{extension}"
                action_desc = f"Bỏ {trim_seconds}s đầu"
            else:
                output_filename = f"{base_name}_trimmed_end_{int(trim_seconds)}s{extension}"
                action_desc = f"Bỏ {trim_seconds}s cuối"
            
            output_path = os.path.join(output_folder, output_filename)
            
            print(f"🎯 Hành động: {action_desc}")
            print(f"📁 Output: {output_filename}")
            
            # Thực hiện cắt video
            if trim_type == "start":
                success = self.trim_video_start(video_file, output_path, trim_seconds)
            else:
                success = self.trim_video_end(video_file, output_path, duration, trim_seconds)
            
            if success:
                # Kiểm tra file output
                if os.path.exists(output_path):
                    output_size = os.path.getsize(output_path) / (1024*1024)
                    output_duration = self.get_video_duration(output_path)
                    
                    print(f"✅ Hoàn thành: {output_filename}")
                    print(f"📊 Kích thước: {output_size:.1f}MB")
                    if output_duration:
                        output_duration_str = f"{int(output_duration//60)}:{int(output_duration%60):02d}"
                        print(f"⏱️ Thời lượng mới: {output_duration_str} ({output_duration:.1f}s)")
                    return True
                else:
                    print("❌ File output không tồn tại")
                    return False
            else:
                return False
                
        except Exception as e:
            print(f"❌ Lỗi xử lý video: {e}")
            return False
    
    def execute(self, input_folder, output_folder):
        """Thực thi chức năng cắt video"""
        print("\n✂️ === VIDEO TRIMMER - TỰ ĐỘNG CẮT VIDEO ===")
        
        # Kiểm tra FFmpeg
        print("🔧 Đang kiểm tra FFmpeg...")
        if not self.check_ffmpeg():
            print("❌ FFmpeg không được tìm thấy!")
            print("💡 Vui lòng cài đặt FFmpeg để sử dụng chức năng này")
            print("🔗 Download tại: https://ffmpeg.org/download.html")
            input("Nhấn Enter để tiếp tục...")
            return
        
        print("✅ FFmpeg đã sẵn sàng")
        
        # Kiểm tra thư mục
        if not self.validate_folders(input_folder, output_folder):
            return
        
        # Lấy danh sách video
        video_files = self.get_video_files(input_folder)
        if not video_files:
            print(f"❌ Không tìm thấy file video nào trong thư mục: {input_folder}")
            input("Nhấn Enter để tiếp tục...")
            return
        
        print(f"📁 Tìm thấy {len(video_files)} video(s):")
        for i, file in enumerate(video_files, 1):
            print(f"  {i}. {os.path.basename(file)}")
        
        # Hiển thị menu trim options
        self.show_trim_menu()
        
        # Lấy lựa chọn kiểu cắt
        trim_choice = self.get_trim_choice()
        if trim_choice is None:
            print("🚫 Đã hủy thao tác")
            input("Nhấn Enter để tiếp tục...")
            return
        
        trim_config = self.trim_options[trim_choice]
        trim_type = trim_config['type']
        
        print(f"✅ Đã chọn: {trim_config['name']}")
        
        # Lấy thời lượng của video đầu tiên để estimate max duration
        print("\n📊 Đang phân tích video mẫu...")
        sample_duration = self.get_video_duration(video_files[0])
        
        if sample_duration is None:
            print("❌ Không thể phân tích video mẫu")
            input("Nhấn Enter để tiếp tục...")
            return
        
        print(f"📋 Video mẫu: {sample_duration:.1f}s")
        
        # Lấy số giây cần cắt
        trim_seconds = self.get_trim_seconds(trim_type, sample_duration)
        
        # Xác nhận thông tin
        print(f"\n📋 THÔNG TIN CẮT VIDEO:")
        print(f"🎬 Số video: {len(video_files)}")
        print(f"✂️ Kiểu cắt: {trim_config['name']}")
        print(f"⏱️ Số giây: {trim_seconds}")
        print(f"📁 Thư mục output: {output_folder}")
        
        confirm = input("\n❓ Bắt đầu cắt video? (y/n): ").strip().lower()
        if confirm != 'y':
            print("🚫 Đã hủy thao tác")
            input("Nhấn Enter để tiếp tục...")
            return
        
        # Xử lý từng video
        success_count = 0
        total_count = len(video_files)
        
        print(f"\n🚀 Bắt đầu cắt {total_count} video(s)...")
        print("=" * 70)
        
        for i, video_file in enumerate(video_files, 1):
            print(f"\n📹 [{i}/{total_count}] Đang xử lý video...")
            
            success = self.trim_single_video(video_file, output_folder, trim_type, trim_seconds)
            
            if success:
                success_count += 1
            
            print("-" * 50)
        
        # Kết quả
        print(f"\n🎊 KẾT QUẢ XỬ LÝ:")
        print(f"✅ Thành công: {success_count}/{total_count}")
        print(f"❌ Thất bại: {total_count - success_count}/{total_count}")
        print(f"📁 Thư mục output: {output_folder}")
        
        if success_count > 0:
            print(f"🎉 Đã cắt thành công {success_count} video!")
            print("💡 Các video đã được cắt và lưu với tên mới")
        
        input("\nNhấn Enter để tiếp tục...")