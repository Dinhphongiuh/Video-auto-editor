#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Filter Applier Action - Sử dụng FFmpeg trực tiếp
Xử lý áp dụng bộ lọc video
"""

import os
import json
import subprocess
from .base_action import BaseAction


class VideoFilterApplier(BaseAction):
    """Xử lý áp dụng bộ lọc video bằng FFmpeg trực tiếp"""
    
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
                    "brightness": -0.1,
                    "contrast": 1.15,
                    "saturation": 0.8
                },
                "cinematic": {
                    "name": "Cinematic",
                    "description": "Hiệu ứng điện ảnh",
                    "brightness": 0.05,
                    "contrast": 1.25,
                    "saturation": 1.1
                },
                "vibrant": {
                    "name": "Vibrant",
                    "description": "Màu sắc sống động",
                    "brightness": 0.1,
                    "contrast": 1.2,
                    "saturation": 1.3
                },
                "black_white": {
                    "name": "Black & White",
                    "description": "Đen trắng",
                    "brightness": 0.0,
                    "contrast": 1.2,
                    "saturation": 0.0
                },
                "warm": {
                    "name": "Warm",
                    "description": "Tông màu ấm",
                    "brightness": 0.05,
                    "contrast": 1.1,
                    "saturation": 1.15
                },
                "cool": {
                    "name": "Cool",
                    "description": "Tông màu lạnh",
                    "brightness": 0.0,
                    "contrast": 1.15,
                    "saturation": 1.1
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
        
        # Kiểm tra FFmpeg
        if not self._check_ffmpeg():
            print("❌ FFmpeg không khả dụng! Vui lòng cài đặt FFmpeg.")
            input("Nhấn Enter để tiếp tục...")
            return
        
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
                
                # Áp dụng filter bằng FFmpeg trực tiếp
                if self._apply_ffmpeg_filter(video_file, output_file, filter_config):
                    output_size = os.path.getsize(output_file) / (1024 * 1024)
                    print(f"  ✅ Thành công! Kích thước output: {output_size:.2f} MB")
                    success_count += 1
                else:
                    print(f"  ❌ Lỗi: Không thể áp dụng filter!")
                    error_count += 1
                    
            except Exception as e:
                print(f"  ❌ Lỗi: {e}")
                error_count += 1
        
        # Hiển thị kết quả
        self._show_results(success_count, error_count, len(video_files), filter_name)
        input("Nhấn Enter để tiếp tục...")
    
    def _check_ffmpeg(self):
        """Kiểm tra FFmpeg có khả dụng không"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def _apply_ffmpeg_filter(self, input_file, output_file, filter_config):
        """Áp dụng filter bằng FFmpeg trực tiếp"""
        try:
            # Tạo filter string cho FFmpeg
            filter_parts = []
            
            # Brightness
            if 'brightness' in filter_config:
                brightness = filter_config['brightness']
                filter_parts.append(f"brightness={brightness}")
            
            # Contrast  
            if 'contrast' in filter_config:
                contrast = filter_config['contrast']
                filter_parts.append(f"contrast={contrast}")
            
            # Saturation
            if 'saturation' in filter_config:
                saturation = filter_config['saturation']
                filter_parts.append(f"saturation={saturation}")
            
            if not filter_parts:
                # Không có filter nào, chỉ copy file
                filter_string = "copy"
            else:
                # Tạo eq filter
                filter_string = f"eq={':'.join(filter_parts)}"
            
            # Tạo FFmpeg command
            cmd = [
                'ffmpeg',
                '-i', input_file,
                '-vf', filter_string,
                '-c:a', 'copy',  # Copy audio stream
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
        print("Brightness: -1.0 đến 1.0 (0 = không thay đổi)")
        print("Contrast: 0.0 đến 3.0 (1 = không thay đổi)")
        print("Saturation: 0.0 đến 3.0 (1 = không thay đổi)")
        
        filter_config = {"name": "Custom"}
        
        try:
            # Brightness
            brightness = input("Độ sáng (-1.0 đến 1.0): ").strip()
            if brightness:
                brightness_val = float(brightness)
                if -1.0 <= brightness_val <= 1.0:
                    filter_config['brightness'] = brightness_val
                else:
                    print("⚠️ Brightness ngoài phạm vi, sử dụng 0")
            
            # Contrast
            contrast = input("Độ tương phản (0.0 đến 3.0): ").strip()
            if contrast:
                contrast_val = float(contrast)
                if 0.0 <= contrast_val <= 3.0:
                    filter_config['contrast'] = contrast_val
                else:
                    print("⚠️ Contrast ngoài phạm vi, sử dụng 1.0")
            
            # Saturation
            saturation = input("Độ bão hòa (0.0 đến 3.0): ").strip()
            if saturation:
                saturation_val = float(saturation)
                if 0.0 <= saturation_val <= 3.0:
                    filter_config['saturation'] = saturation_val
                else:
                    print("⚠️ Saturation ngoài phạm vi, sử dụng 1.0")
            
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
        if success_count > 0:
            print(f"  📁 Vị trí output: Đã lưu với tên *_filtered_{filter_name.lower()}*")
        print("=" * 50)