#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Filter Applier Action
Xử lý áp dụng bộ lọc video
"""

import os
import json
from .base_action import BaseAction


class VideoFilterApplier(BaseAction):
    """Xử lý áp dụng bộ lọc video"""
    
    def __init__(self):
        super().__init__()
        self.filters_file = "video_filters.json"
        self.filters = self._load_filters()
    
    def _load_filters(self):
        """Tải bộ lọc từ file JSON"""
        try:
            if os.path.exists(self.filters_file):
                with open(self.filters_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return self._get_default_filters()
        except Exception as e:
            print(f"❌ Lỗi khi tải filters: {e}")
            return self._get_default_filters()
    
    def _get_default_filters(self):
        """Trả về bộ lọc mặc định"""
        return {
            "presets": {
                "vintage": {
                    "name": "Vintage",
                    "description": "Hiệu ứng cổ điển",
                    "brightness": -10,
                    "contrast": 15,
                    "saturation": -20,
                    "sepia": True
                },
                "cinematic": {
                    "name": "Cinematic",
                    "description": "Hiệu ứng điện ảnh",
                    "brightness": 5,
                    "contrast": 25,
                    "saturation": 10,
                    "vignette": True
                },
                "vibrant": {
                    "name": "Vibrant",
                    "description": "Màu sắc sống động",
                    "brightness": 10,
                    "contrast": 20,
                    "saturation": 30,
                    "sharpness": 15
                },
                "black_white": {
                    "name": "Black & White",
                    "description": "Đen trắng",
                    "brightness": 0,
                    "contrast": 20,
                    "saturation": -100,
                    "sharpness": 10
                },
                "warm": {
                    "name": "Warm",
                    "description": "Tông màu ấm",
                    "brightness": 5,
                    "contrast": 10,
                    "saturation": 15,
                    "temperature": 200
                },
                "cool": {
                    "name": "Cool",
                    "description": "Tông màu lạnh",
                    "brightness": 0,
                    "contrast": 15,
                    "saturation": 10,
                    "temperature": -200
                }
            }
        }
    
    def execute(self, input_folder, output_folder):
        """Thực hiện áp dụng bộ lọc video"""
        # Kiểm tra thư mục
        if not self.validate_folders(input_folder, output_folder):
            return
        
        # Lấy danh sách video
        video_files = self.get_video_files(input_folder)
        if not video_files:
            print("❌ Không tìm thấy file video nào!")
            input("Nhấn Enter để tiếp tục...")
            return
        
        print(f"\n🎨 ÁP DỤNG BỘ LỌC VIDEO")
        print(f"Tìm thấy {len(video_files)} file video")
        
        # Chọn bộ lọc
        filter_config = self._select_filter()
        if not filter_config:
            return
        
        # Thực hiện áp dụng bộ lọc
        filter_name = filter_config.get('name', 'custom')
        print(f"\n🔄 Đang áp dụng bộ lọc '{filter_name}'...")
        print(f"Số file cần xử lý: {len(video_files)}")
        print("-" * 50)
        
        success_count = 0
        error_count = 0
        
        for i, video_file in enumerate(video_files, 1):
            filename = os.path.basename(video_file)
            name, ext = os.path.splitext(filename)
            output_file = os.path.join(output_folder, f"{name}_filtered_{filter_name.lower()}{ext}")
            
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
                print(f"  🎨 Bộ lọc: {filter_name}")
                
                # Tạo command với filter parameters
                cmd = [
                    "process",
                    "-i", video_file,
                    "-o", output_file
                ]
                
                # Thêm các tham số filter
                if 'brightness' in filter_config:
                    cmd.extend(["--brightness", str(filter_config['brightness'])])
                if 'contrast' in filter_config:
                    cmd.extend(["--contrast", str(filter_config['contrast'])])
                if 'saturation' in filter_config:
                    cmd.extend(["--saturation", str(filter_config['saturation'])])
                
                # Chạy lệnh áp dụng bộ lọc
                self.run_videoforge_command(cmd)
                
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
        self._show_results(success_count, error_count, len(video_files), filter_name)
        input("Nhấn Enter để tiếp tục...")
    
    def _select_filter(self):
        """Cho phép user chọn bộ lọc"""
        presets = self.filters.get('presets', {})
        
        print("\nChọn bộ lọc:")
        preset_keys = list(presets.keys())
        
        for i, key in enumerate(preset_keys, 1):
            preset = presets[key]
            print(f"{i}. {preset['name']} - {preset['description']}")
        
        print(f"{len(preset_keys) + 1}. Tùy chỉnh")
        
        try:
            choice = int(input("Nhập số: ")) - 1
            
            if 0 <= choice < len(preset_keys):
                selected_key = preset_keys[choice]
                return presets[selected_key]
            elif choice == len(preset_keys):
                return self._create_custom_filter()
            else:
                print("❌ Lựa chọn không hợp lệ!")
                return None
                
        except ValueError:
            print("❌ Vui lòng nhập số!")
            return None
    
    def _create_custom_filter(self):
        """Tạo bộ lọc tùy chỉnh"""
        print("\n🎨 TẠO BỘ LỌC TÙY CHỈNH")
        print("Nhập giá trị cho các tham số (để trống để bỏ qua):")
        
        filter_config = {"name": "Custom"}
        
        try:
            # Brightness
            brightness = input("Độ sáng (-100 đến 100): ").strip()
            if brightness:
                filter_config['brightness'] = int(brightness)
            
            # Contrast
            contrast = input("Độ t대비 (-100 đến 100): ").strip()
            if contrast:
                filter_config['contrast'] = int(contrast)
            
            # Saturation
            saturation = input("Độ bão hòa (-100 đến 100): ").strip()
            if saturation:
                filter_config['saturation'] = int(saturation)
            
            return filter_config
            
        except ValueError:
            print("❌ Vui lòng nhập số hợp lệ!")
            return None
    
    def _show_results(self, success_count, error_count, total_count, filter_name):
        """Hiển thị kết quả xử lý"""
        print("\n" + "=" * 50)
        print(f"🏁 Kết quả áp dụng bộ lọc:")
        print(f"  ✅ Thành công: {success_count}/{total_count}")
        print(f"  ❌ Lỗi: {error_count}/{total_count}")
        print(f"  🎨 Bộ lọc: {filter_name}")
        print("=" * 50)
