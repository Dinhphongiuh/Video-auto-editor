#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VideoForge Controller - Phiên bản cải tiến
Giao diện điều khiển với tích hợp filter_applier.py được tối ưu hóa
"""

import os
import sys
from pathlib import Path

# Import các actions - đảm bảo sử dụng đúng filter_applier
from actions.format_converter import VideoFormatConverter
from actions.compressor import VideoCompressor
from actions.speed_adjuster import VideoSpeedAdjuster
from actions.resolution_changer import VideoResolutionChanger
from actions.filter_applier import VideoFilterApplier  # ✅ Sử dụng filter_applier.py
from actions.system_info import SystemInfoAction
from actions.api_service import APIServiceAction
from actions.folder_manager import FolderManagerAction
from actions.logo_remover import LogoRemoverAction
from actions.voice_changer import VoiceChangerAction
from actions.youtube_downloader import YouTubeDownloaderAction
from actions.video_trimmer import VideoTrimmerAction
from actions.combo import ComboProcessorAction


class VideoForgeController:
    """Controller chính - Phiên bản cải tiến với filter_applier.py tối ưu"""

    def __init__(self):
        self.version = "1.3.1"  # Tăng version để đánh dấu cải tiến
        self.folder_manager = FolderManagerAction()
        self.system_info = SystemInfoAction()
        self.api_service = APIServiceAction()

        # Khởi tạo các actions - ĐẶC BIỆT CHÚ Ý filter_applier
        self.actions = {
            "format_converter": VideoFormatConverter(),
            "compressor": VideoCompressor(),
            "speed_adjuster": VideoSpeedAdjuster(),
            "resolution_changer": VideoResolutionChanger(),
            "filter_applier": VideoFilterApplier(),  # ✅ CHÍNH THỨC sử dụng filter_applier.py
            "logo_remover": LogoRemoverAction(),
            "voice_changer": VoiceChangerAction(),
            "youtube_downloader": YouTubeDownloaderAction(),
            "video_trimmer": VideoTrimmerAction(),
            "combo_processor": ComboProcessorAction(),
        }

        # Menu mapping với filter action được cải tiến
        self.menu_actions = {
            "1": self._convert_videos,
            "2": self._compress_videos,
            "3": self._trim_videos,
            "4": self._resize_videos,
            "5": self._speed_videos,
            "6": self._apply_filters,  # ✅ Sử dụng filter_applier.py
            "7": self._remove_logos,
            "8": self._change_voice,
            "9": self._download_youtube,
            "10": self._combo_process,
            "11": self._set_folders,
            "12": self._show_system_info,
            "13": self._start_api_service,
            "14": self._filter_info,  # ✅ Thêm menu xem thông tin filter
            "0": self._exit,
        }

        # Kiểm tra filter_applier.py ngay khi khởi tạo
        self._validate_filter_applier()

    def _validate_filter_applier(self):
        """Kiểm tra và xác nhận filter_applier.py hoạt động đúng"""
        try:
            filter_applier = self.actions.get("filter_applier")
            if filter_applier:
                # Kiểm tra filters có được load không
                filters = getattr(filter_applier, "filters", {})
                presets = filters.get("presets", {})
                print(f"✅ Filter Applier: Đã tải {len(presets)} bộ lọc")

                # Kiểm tra FFmpeg
                if hasattr(filter_applier, "_check_ffmpeg"):
                    ffmpeg_status = filter_applier._check_ffmpeg()
                    if ffmpeg_status:
                        print("✅ FFmpeg: Sẵn sàng cho xử lý filter")
                    else:
                        print(
                            "⚠️ FFmpeg: Chưa sẵn sàng - một số tính năng có thể bị hạn chế"
                        )

            else:
                print("❌ Cảnh báo: Filter Applier không được khởi tạo đúng")

        except Exception as e:
            print(f"⚠️ Lỗi kiểm tra Filter Applier: {e}")

    def clear_screen(self):
        """Xóa màn hình"""
        os.system("cls" if os.name == "nt" else "clear")

    def print_banner(self):
        """In banner chào mừng với thông tin filter"""
        print("=" * 75)
        print("    🎬 VIDEO FORGE CONTROLLER v{} 🎬".format(self.version))
        print("    Công cụ xử lý video chuyên nghiệp với Advanced Filters")
        print("    ✨ Powered by filter_applier.py engine ✨")
        print("=" * 75)
        print()

    def print_menu(self):
        """In menu chính với thông tin filter cải tiến"""
        folders = self.folder_manager.get_folders()
        print("📁 Thư mục Input : {}".format(folders["input"] or "Chưa chọn"))
        print("📁 Thư mục Output: {}".format(folders["output"] or "Chưa chọn"))

        # Hiển thị thông tin filter engine
        try:
            filter_applier = self.actions.get("filter_applier")
            if filter_applier and hasattr(filter_applier, "filters"):
                preset_count = len(filter_applier.filters.get("presets", {}))
                print(f"🎨 Filter Engine: {preset_count} bộ lọc sẵn sàng")

                # Hiển thị GPU status nếu có
                if (
                    hasattr(filter_applier, "gpu_acceleration")
                    and filter_applier.gpu_acceleration
                ):
                    print("🚀 GPU Acceleration: Khả dụng")
        except:
            pass

        print("-" * 75)
        print("🎯 CHỌN TÍNH NĂNG:")
        print("1. 📹 Chuyển đổi định dạng video")
        print("2. 🗜️  Nén video")
        print("3. ✂️  Cắt video")
        print("4. 📐 Thay đổi độ phân giải")
        print("5. ⚡ Tăng/giảm tốc độ video")
        print("6. 🎨 Áp dụng bộ lọc video [ENHANCED]")  # Đánh dấu enhanced
        print("7. 🚫 Tự động xóa logo/watermark")
        print("8. 🎤 Thay đổi giọng nói")
        print("9. 📺 Download YouTube & Tạo TikTok Content")
        print("10. 🎯 Combo Processing - Kết hợp nhiều chức năng")
        print("11. ⚙️  Thay đổi thư mục Input/Output")
        print("12. 📊 Xem thông tin hệ thống")
        print("13. 🔧 Khởi động dịch vụ API")
        print("14. ℹ️  Xem thông tin bộ lọc và presets")  # Menu mới
        print("0. 🚪 Thoát")
        print("-" * 75)

    def _convert_videos(self):
        """Chuyển đổi định dạng video"""
        folders = self.folder_manager.get_folders()
        self.actions["format_converter"].execute(folders["input"], folders["output"])

    def _compress_videos(self):
        """Nén video"""
        folders = self.folder_manager.get_folders()
        self.actions["compressor"].execute(folders["input"], folders["output"])

    def _trim_videos(self):
        """Cắt video tự động"""
        folders = self.folder_manager.get_folders()
        self.actions["video_trimmer"].execute(folders["input"], folders["output"])

    def _resize_videos(self):
        """Thay đổi độ phân giải video"""
        folders = self.folder_manager.get_folders()
        self.actions["resolution_changer"].execute(folders["input"], folders["output"])

    def _speed_videos(self):
        """Tăng/giảm tốc độ video"""
        folders = self.folder_manager.get_folders()
        self.actions["speed_adjuster"].execute(folders["input"], folders["output"])

    def _apply_filters(self):
        """Áp dụng bộ lọc video - SỬ DỤNG filter_applier.py"""
        folders = self.folder_manager.get_folders()

        # Kiểm tra folders trước
        if not folders["input"] or not folders["output"]:
            print("\n❌ Vui lòng thiết lập thư mục input và output trước!")
            print("   Chọn menu 11 để thiết lập thư mục.")
            input("Nhấn Enter để tiếp tục...")
            return

        # Hiển thị thông tin trước khi xử lý
        print(f"\n🎨 CHUẨN BỊ XỬ LÝ BỘ LỌC VIDEO")
        print(f"📂 Input folder: {folders['input']}")
        print(f"📤 Output folder: {folders['output']}")

        # Kiểm tra filter_applier
        filter_applier = self.actions.get("filter_applier")
        if not filter_applier:
            print("❌ Lỗi: Filter Applier không được khởi tạo!")
            input("Nhấn Enter để tiếp tục...")
            return

        try:
            # Gọi filter_applier.py để xử lý
            print("🚀 Khởi động Filter Engine...")
            filter_applier.execute(folders["input"], folders["output"])

        except Exception as e:
            print(f"❌ Lỗi khi áp dụng filter: {e}")
            print("🔧 Hãy kiểm tra:")
            print("   - FFmpeg đã được cài đặt và có trong PATH")
            print("   - File video_filters.json có tồn tại và đúng định dạng")
            print("   - Thư mục input có chứa file video hợp lệ")
            input("Nhấn Enter để tiếp tục...")

    def _change_voice(self):
        """Thay đổi giọng nói trong video"""
        folders = self.folder_manager.get_folders()
        self.actions["voice_changer"].execute(folders["input"], folders["output"])

    def _remove_logos(self):
        """Tự động xóa logo/watermark"""
        folders = self.folder_manager.get_folders()
        self.actions["logo_remover"].execute(folders["input"], folders["output"])

    def _download_youtube(self):
        """Download YouTube video và tạo TikTok content"""
        folders = self.folder_manager.get_folders()
        # Sử dụng output folder để lưu video và content
        self.actions["youtube_downloader"].execute(folders["input"], folders["output"])

    def _combo_process(self):
        """Combo processing - kết hợp nhiều chức năng"""
        folders = self.folder_manager.get_folders()
        self.actions["combo_processor"].execute(folders["input"], folders["output"])

    def _set_folders(self):
        """Thiết lập thư mục input và output"""
        self.folder_manager.execute()

    def _show_system_info(self):
        """Hiển thị thông tin hệ thống"""
        self.system_info.execute()

    def _start_api_service(self):
        """Khởi động dịch vụ API"""
        self.api_service.execute()

    def _filter_info(self):
        """Hiển thị thông tin chi tiết về bộ lọc - MENU MỚI"""
        self.clear_screen()
        print("🎨 THÔNG TIN BỘ LỌC VIDEO")
        print("=" * 60)

        try:
            filter_applier = self.actions.get("filter_applier")
            if not filter_applier:
                print("❌ Filter Applier không khả dụng!")
                input("Nhấn Enter để tiếp tục...")
                return

            # Hiển thị thông tin engine
            print("🔧 FILTER ENGINE:")
            print(f"   📋 Module: filter_applier.py")
            print(f"   📊 Version: Enhanced with advanced features")

            # Kiểm tra FFmpeg
            if hasattr(filter_applier, "_check_ffmpeg"):
                ffmpeg_ok = filter_applier._check_ffmpeg()
                status = "✅ Sẵn sàng" if ffmpeg_ok else "❌ Không khả dụng"
                print(f"   🎬 FFmpeg: {status}")

            # Kiểm tra GPU
            if hasattr(filter_applier, "gpu_acceleration"):
                gpu_status = (
                    "✅ Khả dụng"
                    if filter_applier.gpu_acceleration
                    else "❌ Không khả dụng"
                )
                print(f"   🚀 GPU Acceleration: {gpu_status}")

            # Hiển thị danh sách bộ lọc
            filters = getattr(filter_applier, "filters", {})
            presets = filters.get("presets", {})

            print(f"\n📝 DANH SÁCH BỘ LỌC ({len(presets)} presets):")
            print("-" * 60)

            for i, (key, preset) in enumerate(presets.items(), 1):
                print(f"{i:2d}. {preset['name']:15} - {preset['description']}")

                # Hiển thị parameters chi tiết
                params = []
                for param in ["brightness", "contrast", "saturation", "gamma"]:
                    if param in preset:
                        value = preset[param]
                        if param == "brightness":
                            params.append(f"Brightness: {value:+.2f}")
                        elif param == "contrast":
                            params.append(f"Contrast: {value:.2f}x")
                        elif param == "saturation":
                            params.append(f"Saturation: {value:.2f}x")
                        elif param == "gamma":
                            params.append(f"Gamma: {value:.2f}")

                # Hiển thị special effects
                effects = []
                if preset.get("sepia"):
                    effects.append("Sepia")
                if preset.get("vignette"):
                    effects.append("Vignette")
                if preset.get("sharpen"):
                    effects.append("Sharpen")
                if preset.get("blur"):
                    effects.append(f"Blur: {preset['blur']}")

                if params:
                    print(f"     └─ {', '.join(params)}")
                if effects:
                    print(f"     └─ Effects: {', '.join(effects)}")
                print()

            # Hiển thị thông tin file cấu hình
            filters_file = getattr(filter_applier, "filters_file", "video_filters.json")
            print(f"📄 CONFIG FILE: {filters_file}")

            if os.path.exists(filters_file):
                file_size = os.path.getsize(filters_file)
                print(f"   📊 Size: {file_size} bytes")
                print(f"   ✅ Status: File exists and loaded")
            else:
                print(f"   ⚠️ Status: Using default presets (file not found)")

            # Hướng dẫn sử dụng
            print(f"\n💡 HƯỚNG DẪN SỬ DỤNG:")
            print(f"   1. Chọn menu '6. Áp dụng bộ lọc video'")
            print(f"   2. Chọn bộ lọc từ danh sách preset hoặc tạo custom")
            print(f"   3. Chọn chế độ xử lý (Fast/Balanced/Quality/GPU)")
            print(f"   4. Chờ quá trình xử lý hoàn thành")

            print(f"\n🔧 CUSTOM FILTER:")
            print(f"   • Có thể tạo bộ lọc tùy chỉnh với các tham số:")
            print(f"     - Brightness: -1.0 đến 1.0")
            print(f"     - Contrast: 0.0 đến 3.0")
            print(f"     - Saturation: 0.0 đến 3.0")
            print(f"     - Special effects: Sepia, Vignette, Sharpen, Blur")

        except Exception as e:
            print(f"❌ Lỗi khi hiển thị thông tin filter: {e}")

        print("=" * 60)
        input("Nhấn Enter để quay lại menu chính...")

    def _exit(self):
        """Thoát chương trình"""
        print("\n👋 Cảm ơn bạn đã sử dụng VideoForge!")
        print("🎨 Filter Engine được cung cấp bởi filter_applier.py")
        return True

    def run(self):
        """Chạy controller chính với error handling cải tiến"""
        print("🚀 Khởi động VideoForge Controller...")

        # Kiểm tra dependencies cơ bản
        self._check_dependencies()

        while True:
            try:
                self.clear_screen()
                self.print_banner()
                self.print_menu()

                choice = input("👉 Nhập lựa chọn của bạn: ").strip()

                if choice in self.menu_actions:
                    # Đặc biệt log cho filter action
                    if choice == "6":
                        print("🎨 Khởi động Filter Processing với filter_applier.py...")

                    if self.menu_actions[choice]():
                        break  # Thoát nếu action trả về True

                else:
                    print("❌ Lựa chọn không hợp lệ! Vui lòng chọn từ menu.")
                    input("Nhấn Enter để tiếp tục...")

            except KeyboardInterrupt:
                print("\n\n👋 Tạm biệt!")
                break
            except Exception as e:
                print(f"\n❌ Lỗi controller: {e}")
                print("🔧 Nếu lỗi liên quan đến filter, hãy kiểm tra:")
                print("   - FFmpeg installation")
                print("   - video_filters.json file")
                print("   - File permissions")
                input("Nhấn Enter để tiếp tục...")

    def _check_dependencies(self):
        """Kiểm tra dependencies cơ bản"""
        try:
            # Kiểm tra filter_applier đặc biệt
            filter_applier = self.actions.get("filter_applier")
            if filter_applier:
                print("✅ Filter Applier: Loaded successfully")
            else:
                print("⚠️ Filter Applier: Not found - filter features may not work")

            # Kiểm tra file filters
            filters_file = "video_filters.json"
            if os.path.exists(filters_file):
                print(f"✅ Filter Config: {filters_file} found")
            else:
                print(f"⚠️ Filter Config: {filters_file} not found, using defaults")

        except Exception as e:
            print(f"⚠️ Dependency check failed: {e}")


if __name__ == "__main__":
    controller = VideoForgeController()
    controller.run()
