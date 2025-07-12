#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
System Info Action
Xử lý hiển thị thông tin hệ thống
"""

import os
import subprocess
import platform
from .base_action import BaseAction

# Thử import psutil, nếu không có thì skip
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class SystemInfoAction(BaseAction):
    """Xử lý hiển thị thông tin hệ thống"""
    
    def execute(self):
        """Hiển thị thông tin hệ thống"""
        print("\n📊 THÔNG TIN HỆ THỐNG")
        print("-" * 30)
        
        try:
            # Kiểm tra FFmpeg
            self._check_ffmpeg()
            
            # Kiểm tra Python
            self._check_python()
            
            # Kiểm tra VideoForge
            self._check_videoforge()
            
            # Thông tin hệ thống
            self._show_system_details()
            
            # Thông tin phần cứng
            self._show_hardware_info()
            
        except Exception as e:
            print(f"❌ Lỗi khi lấy thông tin hệ thống: {e}")
        
        input("Nhấn Enter để tiếp tục...")
    
    def _check_ffmpeg(self):
        """Kiểm tra FFmpeg"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                print(f"✅ FFmpeg: {version_line}")
            else:
                print("❌ FFmpeg: Không tìm thấy")
        except:
            print("❌ FFmpeg: Không tìm thấy")
    
    def _check_python(self):
        """Kiểm tra Python"""
        import sys
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        print(f"✅ Python: {python_version}")
    
    def _check_videoforge(self):
        """Kiểm tra VideoForge"""
        try:
            # Kiểm tra module VideoForge
            venv_python = os.path.join("D:", "VideoForge", "videoforge-core", "venv", "Scripts", "python.exe")
            
            if os.path.exists(venv_python):
                result = subprocess.run([venv_python, "-m", "videoforge", "--version"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ VideoForge: {result.stdout.strip()}")
                else:
                    print("❌ VideoForge: Lỗi khi kiểm tra version")
            else:
                print("❌ VideoForge: Virtual environment không tồn tại")
                
        except Exception as e:
            print(f"❌ VideoForge: Lỗi - {e}")
    
    def _show_system_details(self):
        """Hiển thị chi tiết hệ thống"""
        print("\n🖥️ Thông tin hệ thống:")
        print(f"  OS: {platform.system()} {platform.release()}")
        print(f"  Architecture: {platform.architecture()[0]}")
        print(f"  Processor: {platform.processor()}")
        print(f"  Machine: {platform.machine()}")
    
    def _show_hardware_info(self):
        """Hiển thị thông tin phần cứng"""
        if not PSUTIL_AVAILABLE:
            print("\n💻 Thông tin phần cứng:")
            print("  ⚠️  psutil chưa được cài đặt")
            print("  🛠️  Chạy: pip install psutil để xem thêm thông tin")
            return
            
        try:
            print("\n💻 Thông tin phần cứng:")
            
            # CPU
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            print(f"  CPU Cores: {cpu_count}")
            if cpu_freq:
                print(f"  CPU Frequency: {cpu_freq.current:.2f} MHz")
            
            # Memory
            memory = psutil.virtual_memory()
            print(f"  RAM: {memory.total / (1024**3):.2f} GB")
            print(f"  RAM Available: {memory.available / (1024**3):.2f} GB")
            print(f"  RAM Usage: {memory.percent}%")
            
            # Disk
            try:
                if os.name == 'nt':  # Windows
                    disk = psutil.disk_usage('C:\\')
                else:  # Unix/Linux
                    disk = psutil.disk_usage('/')
                print(f"  Disk Total: {disk.total / (1024**3):.2f} GB")
                print(f"  Disk Free: {disk.free / (1024**3):.2f} GB")
                print(f"  Disk Usage: {(disk.used / disk.total) * 100:.1f}%")
            except:
                print("  Disk: Không thể lấy thông tin disk")
            
        except Exception as e:
            print(f"\n💻 Thông tin phần cứng: Lỗi - {e}")
