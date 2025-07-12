#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Service Action
Xử lý khởi động dịch vụ API
"""

import os
import subprocess
from .base_action import BaseAction


class APIServiceAction(BaseAction):
    """Xử lý khởi động dịch vụ API"""
    
    def execute(self):
        """Khởi động dịch vụ API"""
        print("\n🔧 KHỞI ĐỘNG DỊCH VỤ API")
        print("-" * 30)
        
        # Hiển thị thông tin về API service
        print("📡 VideoForge API Service sẽ được khởi động...")
        print("🌐 Service sẽ chạy tại: http://localhost:8080")
        print("📚 API Documentation: http://localhost:8080/docs")
        print()
        print("📋 Các endpoint có sẵn:")
        print("  POST /api/process/start         - Bắt đầu xử lý video")
        print("  GET  /api/process/status/{id}   - Kiểm tra trạng thái")
        print("  GET  /api/process/list          - Danh sách công việc")
        print("  POST /api/process/cancel/{id}   - Hủy công việc")
        print("  GET  /api/files/list            - Danh sách file")
        print("  POST /api/files/upload          - Upload file")
        print("  WebSocket /ws/progress          - Cập nhật real-time")
        print()
        
        # Xác nhận khởi động
        choice = input("🚀 Bạn có muốn khởi động API service không? (y/n): ").lower()
        
        if choice != 'y':
            print("❌ Đã hủy khởi động API service.")
            input("Nhấn Enter để tiếp tục...")
            return
        
        try:
            # Chạy VideoForge serve command
            print("\n🔄 Đang khởi động API service...")
            print("💡 Tip: Nhấn Ctrl+C để dừng service")
            print("-" * 50)
            
            # Kiểm tra virtual environment
            venv_python = os.path.join("D:", "VideoForge", "videoforge-core", "venv", "Scripts", "python.exe")
            
            if os.path.exists(venv_python):
                cmd = [venv_python, "-m", "videoforge", "serve", "--port", "8080"]
            else:
                cmd = ["videoforge", "serve", "--port", "8080"]
            
            print(f"🚀 Chạy lệnh: {' '.join(cmd)}")
            
            # Chạy service (blocking call)
            process = subprocess.run(cmd, text=True)
            
            if process.returncode == 0:
                print("✅ API service đã dừng thành công.")
            else:
                print(f"❌ API service dừng với lỗi. Return code: {process.returncode}")
                
        except KeyboardInterrupt:
            print("\n\n⏹️ API service đã được dừng bởi user.")
        except Exception as e:
            print(f"❌ Lỗi khi khởi động API service: {e}")
        
        input("\nNhấn Enter để tiếp tục...")
    
    def get_service_info(self):
        """Lấy thông tin về API service"""
        return {
            "name": "VideoForge API Service",
            "version": "1.0.0",
            "port": 8080,
            "host": "localhost",
            "endpoints": [
                {
                    "method": "POST",
                    "path": "/api/process/start",
                    "description": "Bắt đầu xử lý video"
                },
                {
                    "method": "GET",
                    "path": "/api/process/status/{id}",
                    "description": "Kiểm tra trạng thái xử lý"
                },
                {
                    "method": "GET",
                    "path": "/api/process/list",
                    "description": "Danh sách tất cả công việc"
                },
                {
                    "method": "POST",
                    "path": "/api/process/cancel/{id}",
                    "description": "Hủy công việc đang xử lý"
                },
                {
                    "method": "GET",
                    "path": "/api/files/list",
                    "description": "Danh sách file trong hệ thống"
                },
                {
                    "method": "POST",
                    "path": "/api/files/upload",
                    "description": "Upload file video"
                },
                {
                    "method": "WebSocket",
                    "path": "/ws/progress",
                    "description": "Cập nhật tiến độ real-time"
                }
            ]
        }
