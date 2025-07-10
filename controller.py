#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VideoForge Controller - Giao diện điều khiển đơn giản
"""

import os
import sys
import subprocess
import glob
from pathlib import Path

class VideoForgeController:
    def __init__(self):
        self.input_folder = ""
        self.output_folder = ""
        self.version = "1.0.0"
        
    def clear_screen(self):
        """Xóa màn hình"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        """In banner chào mừng"""
        print("=" * 70)
        print("    🎬 VIDEO FORGE CONTROLLER v{} 🎬".format(self.version))
        print("    Công cụ xử lý video chuyên nghiệp")
        print("=" * 70)
        print()
    
    def print_menu(self):
        """In menu chính"""
        print("📁 Thư mục Input : {}".format(self.input_folder or "Chưa chọn"))
        print("📁 Thư mục Output: {}".format(self.output_folder or "Chưa chọn"))
        print("-" * 70)
        print("🎯 CHỌN TÍNH NĂNG:")
        print("1. 📹 Chuyển đổi định dạng video")
        print("2. 🗜️  Nén video")
        print("3. ⚠️  Cắt video (chưa hỗ trợ)")
        print("4. 📐 Thay đổi độ phân giải")
        print("5. ⚙️  Thay đổi thư mục Input/Output")
        print("6. 📊 Xem thông tin hệ thống")
        print("7. 🔧 Khởi động dịch vụ API")
        print("0. 🚪 Thoát")
        print("-" * 70)
    
    def get_video_files(self, folder_path):
        """Lấy danh sách file video trong thư mục"""
        if not folder_path or not os.path.exists(folder_path):
            return []
        
        video_extensions = ['*.mp4', '*.avi', '*.mov', '*.wmv', '*.flv', '*.mkv', '*.webm']
        video_files = []
        
        for ext in video_extensions:
            video_files.extend(glob.glob(os.path.join(folder_path, ext)))
            video_files.extend(glob.glob(os.path.join(folder_path, ext.upper())))
        
        # Loại bỏ duplicate (do Windows không phân biệt chữ hoa/thường)
        video_files = list(set(video_files))
        video_files.sort()  # Sắp xếp theo thứ tự abc
        
        return video_files
    
    def set_folders(self):
        """Thiết lập thư mục input và output"""
        print("\n🔧 THIẾT LẬP THỦ MỤC")
        print("-" * 30)
        
        # Thiết lập thư mục input
        while True:
            input_path = input("📥 Nhập đường dẫn thư mục chứa video: ").strip().strip('"')
            if not input_path:
                print("❌ Vui lòng nhập đường dẫn!")
                continue
            
            if not os.path.exists(input_path):
                print("❌ Thư mục không tồn tại!")
                continue
            
            video_files = self.get_video_files(input_path)
            if not video_files:
                print("⚠️  Không tìm thấy file video nào trong thư mục!")
                choice = input("Bạn có muốn tiếp tục không? (y/n): ").lower()
                if choice != 'y':
                    continue
            else:
                print(f"✅ Tìm thấy {len(video_files)} file video:")
                for i, video_file in enumerate(video_files, 1):
                    filename = os.path.basename(video_file)
                    print(f"   {i}. {filename}")
            
            self.input_folder = input_path
            break
        
        # Thiết lập thư mục output
        while True:
            output_path = input("📤 Nhập đường dẫn thư mục xuất video: ").strip().strip('"')
            if not output_path:
                print("❌ Vui lòng nhập đường dẫn!")
                continue
            
            # Tạo thư mục output nếu chưa tồn tại
            try:
                os.makedirs(output_path, exist_ok=True)
                self.output_folder = output_path
                print(f"✅ Đã thiết lập thư mục output: {output_path}")
                break
            except Exception as e:
                print(f"❌ Không thể tạo thư mục: {e}")
                continue
        
        input("\nNhấn Enter để tiếp tục...")
    
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
            
            # Thử chạy lệnh help trước để debug
            if command_parts[0] == "process":
                print("\n📚 Kiểm tra cú pháp lệnh process...")
                help_cmd = [venv_python, "-m", "videoforge", "process", "--help"] if os.path.exists(venv_python) else ["videoforge", "process", "--help"]
                help_result = subprocess.run(help_cmd, capture_output=True, text=True, encoding='utf-8')
                if help_result.stdout:
                    print("📖 Cú pháp lệnh:")
                    print(help_result.stdout[:500] + "..." if len(help_result.stdout) > 500 else help_result.stdout)
            
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
                    
                # Thử phân tích lỗi cụ thể
                if "Missing option" in (result.stderr or "") or "Missing option" in (result.stdout or ""):
                    print("\n⚠️  Lỗi thiếu tham số. Hãy kiểm tra cú pháp lệnh.")
                elif "not found" in (result.stderr or "").lower():
                    print("\n⚠️  Không tìm thấy file hoặc lệnh.")
                elif "permission" in (result.stderr or "").lower():
                    print("\n⚠️  Lỗi quyền truy cập.")
                    
        except Exception as e:
            print(f"❌ Lỗi khi chạy lệnh: {e}")
            import traceback
            print(f"🔍 Chi tiết lỗi: {traceback.format_exc()}")
    
    def convert_videos(self):
        """Chuyển đổi định dạng video"""
        if not self.input_folder or not self.output_folder:
            print("❌ Vui lòng thiết lập thư mục input và output trước!")
            input("Nhấn Enter để tiếp tục...")
            return
        
        video_files = self.get_video_files(self.input_folder)
        if not video_files:
            print("❌ Không tìm thấy file video nào!")
            input("Nhấn Enter để tiếp tục...")
            return
        
        print(f"\n📹 CHUYỂN ĐỔI ĐỊNH DẠNG VIDEO")
        print(f"Tìm thấy {len(video_files)} file video")
        
        # Chọn định dạng output
        formats = ["mp4", "avi", "mov", "wmv", "flv", "mkv", "webm"]
        print("\nChọn định dạng output:")
        for i, fmt in enumerate(formats, 1):
            print(f"{i}. {fmt.upper()}")
        
        try:
            choice = int(input("Nhập số: ")) - 1
            if 0 <= choice < len(formats):
                output_format = formats[choice]
                
                print(f"\n🔄 Đang chuyển đổi sang {output_format.upper()}...")
                print(f"Số file cần xử lý: {len(video_files)}")
                print("-" * 50)
                
                success_count = 0
                error_count = 0
                
                for i, video_file in enumerate(video_files, 1):
                    filename = os.path.basename(video_file)
                    name, _ = os.path.splitext(filename)
                    output_file = os.path.join(self.output_folder, f"{name}.{output_format}")
                    
                    print(f"\n[{i}/{len(video_files)}] 📁 Xử lý: {filename}")
                    print(f"  📍 Input : {video_file}")
                    print(f"  📤 Output: {output_file}")
                    
                    # Kiểm tra file input tồn tại
                    if not os.path.exists(video_file):
                        print(f"  ❌ Lỗi: File input không tồn tại!")
                        error_count += 1
                        continue
                    
                    # Chạy lệnh videoforge process với option --input và --output
                    try:
                        # Kiểm tra trạng thái trước khi chạy
                        file_size = os.path.getsize(video_file) / (1024 * 1024)  # MB
                        print(f"  📀 Kích thước file: {file_size:.2f} MB")
                        
                        self.run_videoforge_command([
                            "process",
                            "-i", video_file,
                            "-o", output_file
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
                
                print("\n" + "=" * 50)
                print(f"🏁 Kết quả chuyển đổi:")
                print(f"  ✅ Thành công: {success_count}/{len(video_files)}")
                print(f"  ❌ Lỗi: {error_count}/{len(video_files)}")
                print("=" * 50)
            else:
                print("❌ Lựa chọn không hợp lệ!")
                
        except ValueError:
            print("❌ Vui lòng nhập số!")
        
        input("Nhấn Enter để tiếp tục...")
    
    def compress_videos(self):
        """Nén video"""
        if not self.input_folder or not self.output_folder:
            print("❌ Vui lòng thiết lập thư mục input và output trước!")
            input("Nhấn Enter để tiếp tục...")
            return
        
        video_files = self.get_video_files(self.input_folder)
        if not video_files:
            print("❌ Không tìm thấy file video nào!")
            input("Nhấn Enter để tiếp tục...")
            return
        
        print(f"\n🗜️ NÉN VIDEO")
        print(f"Tìm thấy {len(video_files)} file video")
        
        # Chọn mức nén
        print("\nChọn mức nén:")
        print("1. Ultra (Chất lượng cao nhất)")
        print("2. High (Chất lượng cao)")
        print("3. Medium (Chất lượng trung bình)")
        print("4. Low (Chất lượng thấp, file nhỏ)")
        
        try:
            choice = int(input("Nhập số: "))
            
            quality_map = {
                1: "ultra",
                2: "high",
                3: "medium",
                4: "low"
            }
            
            if choice in quality_map:
                quality = quality_map[choice]
                print(f"\n🔄 Đang nén video với chất lượng {quality.upper()}...")
            else:
                print("❌ Lựa chọn không hợp lệ!")
                input("Nhấn Enter để tiếp tục...")
                return
            
            for video_file in video_files:
                filename = os.path.basename(video_file)
                name, ext = os.path.splitext(filename)
                output_file = os.path.join(self.output_folder, f"{name}_compressed{ext}")
                
                print(f"📁 Xử lý: {filename}")
                
                # Chạy lệnh videoforge process với options
                self.run_videoforge_command([
                    "process",
                    "-i", video_file,
                    "-o", output_file,
                    "--quality", quality
                ])
            
            print("✅ Hoàn thành nén video!")
            
        except ValueError:
            print("❌ Vui lòng nhập số!")
        
        input("Nhấn Enter để tiếp tục...")
    
    def trim_videos(self):
        """Đã tạm thời disable do VideoForge chưa hỗ trợ"""
        print("\n⚠️  Chức năng cắt video hiện chưa được hỗ trợ!")
        print("🔧 Chức năng này đang được phát triển và sẽ có trong phiên bản tiếp theo.")
        print("\n💡 Mẹo: Bạn có thể sử dụng chức năng Speed để thay đổi tốc độ video.")
        
        input("\nNhấn Enter để tiếp tục...")
    
    def resize_videos(self):
        """Thay đổi độ phân giải video"""
        if not self.input_folder or not self.output_folder:
            print("❌ Vui lòng thiết lập thư mục input và output trước!")
            input("Nhấn Enter để tiếp tục...")
            return
        
        video_files = self.get_video_files(self.input_folder)
        if not video_files:
            print("❌ Không tìm thấy file video nào!")
            input("Nhấn Enter để tiếp tục...")
            return
        
        print(f"\n📐 THAY ĐỔI ĐỘ PHÂN GIẢI")
        print(f"Tìm thấy {len(video_files)} file video")
        
        print("\nChọn độ phân giải:")
        print("1. 1920x1080 (Full HD)")
        print("2. 1280x720 (HD)")
        print("3. 854x480 (SD)")
        print("4. 640x360 (Low)")
        print("5. Tùy chỉnh")
        
        try:
            choice = int(input("Nhập số: "))
            
            if choice == 1:
                width, height = "1920", "1080"
            elif choice == 2:
                width, height = "1280", "720"
            elif choice == 3:
                width, height = "854", "480"
            elif choice == 4:
                width, height = "640", "360"
            elif choice == 5:
                width = input("Nhập chiều rộng: ")
                height = input("Nhập chiều cao: ")
            else:
                print("❌ Lựa chọn không hợp lệ!")
                return
            
            print(f"\n🔄 Đang thay đổi độ phân giải thành {width}x{height}...")
            
            for video_file in video_files:
                filename = os.path.basename(video_file)
                name, ext = os.path.splitext(filename)
                output_file = os.path.join(self.output_folder, f"{name}_{width}x{height}{ext}")
                
                print(f"📁 Xử lý: {filename}")
                
                # Chạy lệnh videoforge process với options
                self.run_videoforge_command([
                    "process",
                    "-i", video_file,
                    "-o", output_file,
                    "--resolution", f"{width}x{height}"
                ])
            
            print("✅ Hoàn thành thay đổi độ phân giải!")
            
        except ValueError:
            print("❌ Vui lòng nhập số!")
        
        input("Nhấn Enter để tiếp tục...")
    
    def show_system_info(self):
        """Hiển thị thông tin hệ thống"""
        print("\n📊 THÔNG TIN HỆ THỐNG")
        print("-" * 30)
        self.run_videoforge_command(["info"])
        input("Nhấn Enter để tiếp tục...")
    
    def start_api_service(self):
        """Khởi động dịch vụ API"""
        print("\n🔧 KHỞI ĐỘNG DỊCH VỤ API")
        print("-" * 30)
        print("Dịch vụ API sẽ chạy ở background...")
        self.run_videoforge_command(["serve"])
        input("Nhấn Enter để tiếp tục...")
    
    def run(self):
        """Chạy controller chính"""
        while True:
            self.clear_screen()
            self.print_banner()
            self.print_menu()
            
            try:
                choice = input("👉 Nhập lựa chọn của bạn: ").strip()
                
                if choice == "0":
                    print("\n👋 Cảm ơn bạn đã sử dụng VideoForge!")
                    break
                elif choice == "1":
                    self.convert_videos()
                elif choice == "2":
                    self.compress_videos()
                elif choice == "3":
                    self.trim_videos()
                elif choice == "4":
                    self.resize_videos()
                elif choice == "5":
                    self.set_folders()
                elif choice == "6":
                    self.show_system_info()
                elif choice == "7":
                    self.start_api_service()
                else:
                    print("❌ Lựa chọn không hợp lệ! Vui lòng chọn từ 0-7.")
                    input("Nhấn Enter để tiếp tục...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Tạm biệt!")
                break
            except Exception as e:
                print(f"\n❌ Lỗi: {e}")
                input("Nhấn Enter để tiếp tục...")

if __name__ == "__main__":
    controller = VideoForgeController()
    controller.run()
