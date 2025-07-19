#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VideoForge Controller - Refactored Version
Giao diện điều khiển tách biệt logic vào các actions
"""

import os
import sys
from pathlib import Path

# Import các actions
from actions.format_converter import VideoFormatConverter
from actions.compressor import VideoCompressor
from actions.speed_adjuster import VideoSpeedAdjuster
from actions.resolution_changer import VideoResolutionChanger
from actions.filter_applier import VideoFilterApplier
from actions.system_info import SystemInfoAction
from actions.api_service import APIServiceAction
from actions.folder_manager import FolderManagerAction
from actions.logo_remover import LogoRemoverAction
from actions.voice_changer import VoiceChangerAction
from actions.youtube_downloader import YouTubeDownloaderAction
from actions.video_trimmer import VideoTrimmerAction

class VideoForgeController:
    """Controller chính - chỉ chứa logic điều khiển và giao diện"""
    
    
    def __init__(self):
        self.version = "1.0.0"
        self.folder_manager = FolderManagerAction()
        self.system_info = SystemInfoAction()
        self.api_service = APIServiceAction()
        
        # Khởi tạo các actions
        self.actions = {
            "format_converter": VideoFormatConverter(),
            "compressor": VideoCompressor(),
            "speed_adjuster": VideoSpeedAdjuster(),
            "resolution_changer": VideoResolutionChanger(),
            "filter_applier": VideoFilterApplier(),
            "logo_remover": LogoRemoverAction(), 
            "voice_changer": VoiceChangerAction(),
            "youtube_downloader": YouTubeDownloaderAction(),
            "video_trimmer": VideoTrimmerAction(),
        }
        
        # Menu mapping
        self.menu_actions = {
            "1": self._convert_videos,
            "2": self._compress_videos,
            "3": self._trim_videos,
            "4": self._resize_videos,
            "5": self._speed_videos,
            "6": self._apply_filters,
            "7": self._remove_logos,
            "8": self._change_voice,        
            "9": self._download_youtube,       
            "10": self._set_folders,         
            "11": self._show_system_info,    
            "12": self._start_api_service,   
        }
    
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
        folders = self.folder_manager.get_folders()
        print("📁 Thư mục Input : {}".format(folders['input'] or "Chưa chọn"))
        print("📁 Thư mục Output: {}".format(folders['output'] or "Chưa chọn"))
        print("-" * 70)
        print("🎯 CHỌN TÍNH NĂNG:")
        print("1. 📹 Chuyển đổi định dạng video")
        print("2. 🗜️  Nén video")
        print("3. ✂️  Cắt video")
        print("4. 📐 Thay đổi độ phân giải")
        print("5. ⚡ Tăng/giảm tốc độ video")
        print("6. 🎨 Áp dụng bộ lọc video")
        print("7. 🚫 Tự động xóa logo/watermark") 
        print("8. 🎤 Thay đổi giọng nói")             
        print("9. 📺 Download YouTube & Tạo TikTok Content")  
        print("10. ⚙️  Thay đổi thư mục Input/Output")       
        print("11. 📊 Xem thông tin hệ thống")                 
        print("12. 🔧 Khởi động dịch vụ API")                          
        print("0. 🚪 Thoát")
        print("-" * 70)
    
    def _convert_videos(self):
        """Chuyển đổi định dạng video"""
        folders = self.folder_manager.get_folders()
        self.actions["format_converter"].execute(folders['input'], folders['output'])
    
    def _compress_videos(self):
        """Nén video"""
        folders = self.folder_manager.get_folders()
        self.actions["compressor"].execute(folders['input'], folders['output'])
    
    def _trim_videos(self):
        """Cắt video tự động"""
        folders = self.folder_manager.get_folders()
        self.actions["video_trimmer"].execute(folders['input'], folders['output'])
    
    def _resize_videos(self):
        """Thay đổi độ phân giải video"""
        folders = self.folder_manager.get_folders()
        self.actions["resolution_changer"].execute(folders['input'], folders['output'])
    
    def _speed_videos(self):
        """Tăng/giảm tốc độ video"""
        folders = self.folder_manager.get_folders()
        self.actions["speed_adjuster"].execute(folders['input'], folders['output'])
    
    def _apply_filters(self):
        """Áp dụng bộ lọc video"""
        folders = self.folder_manager.get_folders()
        self.actions["filter_applier"].execute(folders['input'], folders['output'])

    def _change_voice(self):
        """Thay đổi giọng nói trong video"""
        folders = self.folder_manager.get_folders()
        self.actions["voice_changer"].execute(folders['input'], folders['output'])

    def _remove_logos(self):
        """Tự động xóa logo/watermark"""
        folders = self.folder_manager.get_folders()
        self.actions["logo_remover"].execute(folders['input'], folders['output'])

    def _download_youtube(self):
        """Download YouTube video và tạo TikTok content"""
        folders = self.folder_manager.get_folders()
        # Sử dụng output folder để lưu video và content
        self.actions["youtube_downloader"].execute(folders['input'], folders['output'])
    
    def _set_folders(self):
        """Thiết lập thư mục input và output"""
        self.folder_manager.execute()
    
    def _show_system_info(self):
        """Hiển thị thông tin hệ thống"""
        self.system_info.execute()
    
    def _start_api_service(self):
        """Khởi động dịch vụ API"""
        self.api_service.execute()
    
    def _exit(self):
        """Thoát chương trình"""
        print("\n👋 Cảm ơn bạn đã sử dụng VideoForge!")
        return True
    
    def run(self):
        """Chạy controller chính"""
        while True:
            self.clear_screen()
            self.print_banner()
            self.print_menu()
            
            try:
                choice = input("👉 Nhập lựa chọn của bạn: ").strip()
                
                if choice in self.menu_actions:
                    if self.menu_actions[choice]():
                        break  # Thoát nếu action trả về True
                else:
                    print("❌ Lựa chọn không hợp lệ! Vui lòng chọn từ 0-10.")
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
