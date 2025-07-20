#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Filter Applier Action - Cải tiến và tối ưu hóa
Xử lý áp dụng bộ lọc video sử dụng FFmpeg trực tiếp với nhiều tính năng nâng cao
"""

import os
import json
import subprocess
import time
from pathlib import Path
from .base_action import BaseAction


class VideoFilterApplier(BaseAction):
    """Xử lý áp dụng bộ lọc video bằng FFmpeg trực tiếp - Phiên bản cải tiến"""
    
    def __init__(self):
        super().__init__()
        self.filters_file = "video_filters.json"
        self.filters = self._load_filters()
        
        # Thêm cấu hình nâng cao
        self.ffmpeg_configs = {
            'fast': ['-preset', 'fast', '-threads', '4'],
            'quality': ['-preset', 'medium', '-crf', '18'],
            'balanced': ['-preset', 'medium', '-threads', '4']
        }
        
        # Hỗ trợ GPU acceleration nếu có
        self.gpu_acceleration = self._check_gpu_support()
    
    def _load_filters(self):
        """Tải bộ lọc từ file JSON với error handling tốt hơn"""
        try:
            if os.path.exists(self.filters_file):
                with open(self.filters_file, 'r', encoding='utf-8') as f:
                    filters_data = json.load(f)
                    print(f"✅ Đã tải {len(filters_data.get('presets', {}))} bộ lọc từ {self.filters_file}")
                    return filters_data
            else:
                print(f"⚠️ File {self.filters_file} không tồn tại, sử dụng bộ lọc mặc định")
                return self._get_default_filters()
        except json.JSONDecodeError as e:
            print(f"❌ Lỗi JSON trong {self.filters_file}: {e}")
            return self._get_default_filters()
        except Exception as e:
            print(f"❌ Lỗi khi tải filters: {e}")
            return self._get_default_filters()
    
    def _get_default_filters(self):
        """Trả về bộ lọc mặc định với nhiều options hơn"""
        return {
            "presets": {
                "vintage": {
                    "name": "Vintage",
                    "description": "Hiệu ứng cổ điển với tông màu ấm",
                    "brightness": -0.1,
                    "contrast": 1.15,
                    "saturation": 0.8,
                    "gamma": 0.9,
                    "sepia": True
                },
                "cinematic": {
                    "name": "Cinematic",
                    "description": "Hiệu ứng điện ảnh chuyên nghiệp",
                    "brightness": 0.05,
                    "contrast": 1.25,
                    "saturation": 1.1,
                    "gamma": 1.1,
                    "vignette": True
                },
                "vibrant": {
                    "name": "Vibrant",
                    "description": "Màu sắc sống động và nổi bật",
                    "brightness": 0.1,
                    "contrast": 1.2,
                    "saturation": 1.3,
                    "gamma": 1.05
                },
                "black_white": {
                    "name": "Black & White",
                    "description": "Đen trắng cổ điển",
                    "brightness": 0.0,
                    "contrast": 1.2,
                    "saturation": 0.0,
                    "gamma": 1.0
                },
                "warm": {
                    "name": "Warm",
                    "description": "Tông màu ấm áp",
                    "brightness": 0.05,
                    "contrast": 1.1,
                    "saturation": 1.15,
                    "temperature": 3200
                },
                "cool": {
                    "name": "Cool",
                    "description": "Tông màu lạnh mát",
                    "brightness": 0.0,
                    "contrast": 1.15,
                    "saturation": 1.1,
                    "temperature": 6500
                },
                "dramatic": {
                    "name": "Dramatic",
                    "description": "Hiệu ứng kịch tính cao",
                    "brightness": -0.05,
                    "contrast": 1.4,
                    "saturation": 1.2,
                    "gamma": 0.85,
                    "sharpen": True
                },
                "soft": {
                    "name": "Soft",
                    "description": "Hiệu ứng mềm mại",
                    "brightness": 0.1,
                    "contrast": 0.9,
                    "saturation": 1.05,
                    "blur": 0.5
                }
            }
        }
    
    def _check_gpu_support(self):
        """Kiểm tra hỗ trợ GPU acceleration"""
        try:
            result = subprocess.run(['ffmpeg', '-hwaccels'], 
                                  capture_output=True, text=True)
            if result.returncode == 0 and 'cuda' in result.stdout:
                print("🚀 Phát hiện hỗ trợ GPU acceleration (CUDA)")
                return True
        except:
            pass
        return False
    
    def execute(self, input_folder, output_folder):
        """Thực hiện áp dụng bộ lọc video với giao diện cải tiến"""
        # Kiểm tra thư mục
        if not self.validate_folders(input_folder, output_folder):
            return
        
        # Lấy danh sách video
        video_files = self.get_video_files(input_folder)
        if not video_files:
            print("❌ Không tìm thấy file video nào!")
            input("Nhấn Enter để tiếp tục...")
            return
        
        print(f"\n🎨 ÁP DỤNG BỘ LỌC VIDEO - VideoForge Filter Engine")
        print(f"📂 Thư mục input: {input_folder}")
        print(f"📤 Thư mục output: {output_folder}")
        print(f"🎬 Tìm thấy {len(video_files)} file video")
        
        # Kiểm tra FFmpeg
        if not self._check_ffmpeg():
            print("❌ FFmpeg không khả dụng! Vui lòng cài đặt FFmpeg.")
            input("Nhấn Enter để tiếp tục...")
            return
        
        # Hiển thị thông tin hệ thống
        if self.gpu_acceleration:
            print("🚀 GPU acceleration có sẵn")
        
        # Chọn bộ lọc
        filter_config = self._select_filter()
        if not filter_config:
            return
        
        # Chọn chế độ xử lý
        processing_mode = self._select_processing_mode()
        
        # Thực hiện áp dụng bộ lọc
        self._process_videos(video_files, output_folder, filter_config, processing_mode)
    
    def _check_ffmpeg(self):
        """Kiểm tra FFmpeg có khả dụng không với thông tin chi tiết"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                # Lấy thông tin version
                version_info = result.stdout.split('\n')[0]
                print(f"✅ FFmpeg detected: {version_info}")
                return True
            return False
        except subprocess.TimeoutExpired:
            print("❌ FFmpeg timeout - có thể đang bận")
            return False
        except FileNotFoundError:
            print("❌ FFmpeg chưa được cài đặt hoặc không có trong PATH")
            return False
        except Exception as e:
            print(f"❌ Lỗi kiểm tra FFmpeg: {e}")
            return False
    
    def _select_processing_mode(self):
        """Chọn chế độ xử lý"""
        print("\n⚙️ CHỌN CHỂ ĐỘ XỬ LÝ:")
        print("1. 🏃 Fast - Xử lý nhanh (chất lượng trung bình)")
        print("2. ⚖️  Balanced - Cân bằng tốc độ và chất lượng")
        print("3. 🎯 Quality - Chất lượng cao (xử lý chậm hơn)")
        
        if self.gpu_acceleration:
            print("4. 🚀 GPU Accelerated - Sử dụng GPU (nhanh nhất)")
        
        try:
            choice = int(input("Nhập lựa chọn (1-4): "))
            mode_map = {
                1: 'fast',
                2: 'balanced', 
                3: 'quality',
                4: 'gpu' if self.gpu_acceleration else 'balanced'
            }
            return mode_map.get(choice, 'balanced')
        except ValueError:
            print("⚠️ Lựa chọn không hợp lệ, sử dụng chế độ balanced")
            return 'balanced'
    
    def _process_videos(self, video_files, output_folder, filter_config, processing_mode):
        """Xử lý danh sách video với progress tracking"""
        filter_name = filter_config.get('name', 'custom')
        print(f"\n🔄 Đang áp dụng bộ lọc '{filter_name}' - Chế độ: {processing_mode}")
        print(f"📊 Tiến độ xử lý:")
        print("-" * 70)
        
        start_time = time.time()
        success_count = 0
        error_count = 0
        total_size_before = 0
        total_size_after = 0
        
        for i, video_file in enumerate(video_files, 1):
            filename = os.path.basename(video_file)
            name, ext = os.path.splitext(filename)
            
            # Tạo tên file output với timestamp để tránh trùng
            timestamp = int(time.time()) % 10000
            output_file = os.path.join(output_folder, 
                                     f"{name}_filtered_{filter_name.lower()}_{timestamp}{ext}")
            
            print(f"\n[{i}/{len(video_files)}] 🎬 Xử lý: {filename}")
            
            # Kiểm tra file input
            if not os.path.exists(video_file):
                print(f"  ❌ Lỗi: File input không tồn tại!")
                error_count += 1
                continue
            
            try:
                # Thông tin file
                file_size = os.path.getsize(video_file)
                total_size_before += file_size
                print(f"  📀 Kích thước: {file_size / (1024*1024):.2f} MB")
                print(f"  🎨 Bộ lọc: {filter_name}")
                print(f"  ⚙️ Chế độ: {processing_mode}")
                
                # Áp dụng filter
                process_start = time.time()
                if self._apply_ffmpeg_filter_advanced(video_file, output_file, 
                                                    filter_config, processing_mode):
                    process_time = time.time() - process_start
                    
                    if os.path.exists(output_file):
                        output_size = os.path.getsize(output_file)
                        total_size_after += output_size
                        print(f"  ✅ Thành công! ({process_time:.1f}s)")
                        print(f"  📤 Output: {output_size / (1024*1024):.2f} MB")
                        success_count += 1
                    else:
                        print(f"  ❌ Lỗi: File output không được tạo")
                        error_count += 1
                else:
                    print(f"  ❌ Lỗi: Không thể áp dụng filter")
                    error_count += 1
                    
            except Exception as e:
                print(f"  ❌ Lỗi exception: {e}")
                error_count += 1
        
        # Hiển thị kết quả tổng hợp
        total_time = time.time() - start_time
        self._show_advanced_results(success_count, error_count, len(video_files), 
                                  filter_name, total_time, total_size_before, 
                                  total_size_after, processing_mode)
        input("Nhấn Enter để tiếp tục...")
    
    def _apply_ffmpeg_filter_advanced(self, input_file, output_file, filter_config, mode):
        """Áp dụng filter với nhiều tùy chọn nâng cao"""
        try:
            # Tạo filter string phức tạp
            video_filters = []
            audio_filters = []
            
            # Xây dựng eq filter cho color correction
            eq_params = []
            if 'brightness' in filter_config:
                eq_params.append(f"brightness={filter_config['brightness']}")
            if 'contrast' in filter_config:
                eq_params.append(f"contrast={filter_config['contrast']}")
            if 'saturation' in filter_config:
                eq_params.append(f"saturation={filter_config['saturation']}")
            if 'gamma' in filter_config:
                eq_params.append(f"gamma={filter_config['gamma']}")
            
            if eq_params:
                video_filters.append(f"eq={':'.join(eq_params)}")
            
            # Các effect đặc biệt
            if filter_config.get('sepia'):
                video_filters.append("colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131")
            
            if filter_config.get('vignette'):
                video_filters.append("vignette")
            
            if filter_config.get('sharpen'):
                video_filters.append("unsharp=5:5:1.0:5:5:0.0")
            
            if filter_config.get('blur'):
                blur_val = filter_config['blur']
                video_filters.append(f"boxblur={blur_val}:{blur_val}")
            
            # Temperature adjustment (simplified)
            if 'temperature' in filter_config:
                temp = filter_config['temperature']
                if temp < 5000:  # Warm
                    video_filters.append("colorbalance=rs=0.1:gs=0.0:bs=-0.1")
                elif temp > 6000:  # Cool
                    video_filters.append("colorbalance=rs=-0.1:gs=0.0:bs=0.1")
            
            # Xây dựng FFmpeg command
            cmd = ['ffmpeg', '-i', input_file]
            
            # GPU acceleration
            if mode == 'gpu' and self.gpu_acceleration:
                cmd.extend(['-hwaccel', 'cuda', '-c:v', 'h264_nvenc'])
            
            # Video filters
            if video_filters:
                cmd.extend(['-vf', ','.join(video_filters)])
            
            # Audio copy (no processing)
            cmd.extend(['-c:a', 'copy'])
            
            # Processing mode settings
            if mode in self.ffmpeg_configs:
                cmd.extend(self.ffmpeg_configs[mode])
            
            # Output settings
            cmd.extend(['-y', output_file])
            
            # Debug: in command (có thể comment out)
            # print(f"  🔧 Command: {' '.join(cmd)}")
            
            # Chạy FFmpeg với progress tracking
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True
            else:
                print(f"  ❌ FFmpeg stderr: {result.stderr[:200]}...")
                return False
                
        except Exception as e:
            print(f"  ❌ Exception trong FFmpeg: {e}")
            return False
    
    def _select_filter(self):
        """Giao diện chọn bộ lọc cải tiến"""
        presets = self.filters.get('presets', {})
        
        print("\n🎨 CHỌN BỘ LỌC VIDEO:")
        print("=" * 50)
        
        preset_keys = list(presets.keys())
        
        for i, key in enumerate(preset_keys, 1):
            preset = presets[key]
            print(f"{i:2d}. {preset['name']:15} - {preset['description']}")
            
            # Hiển thị parameters
            params = []
            if 'brightness' in preset and preset['brightness'] != 0:
                params.append(f"Brightness: {preset['brightness']:+.1f}")
            if 'contrast' in preset and preset['contrast'] != 1:
                params.append(f"Contrast: {preset['contrast']:.1f}x")
            if 'saturation' in preset and preset['saturation'] != 1:
                params.append(f"Saturation: {preset['saturation']:.1f}x")
            
            if params:
                print(f"     └─ {', '.join(params)}")
        
        print(f"{len(preset_keys) + 1:2d}. Custom Filter      - Tạo bộ lọc tùy chỉnh")
        print(f" 0. Quay lại")
        print("=" * 50)
        
        try:
            choice = int(input("👉 Nhập số để chọn bộ lọc: "))
            
            if choice == 0:
                return None
            elif 1 <= choice <= len(preset_keys):
                selected_key = preset_keys[choice - 1]
                selected_filter = presets[selected_key]
                print(f"\n✅ Đã chọn bộ lọc: {selected_filter['name']}")
                return selected_filter
            elif choice == len(preset_keys) + 1:
                return self._create_custom_filter()
            else:
                print("❌ Lựa chọn không hợp lệ!")
                return None
                
        except ValueError:
            print("❌ Vui lòng nhập số!")
            return None
    
    def _create_custom_filter(self):
        """Tạo bộ lọc tùy chỉnh với giao diện wizard"""
        print("\n🎨 TẠO BỘ LỌC TÙY CHỈNH")
        print("=" * 40)
        print("Nhập giá trị cho các tham số (Enter để bỏ qua):")
        print()
        
        filter_config = {"name": "Custom"}
        
        try:
            # Basic adjustments
            print("📝 CÁC ĐIỀU CHỈNH CƠ BẢN:")
            
            brightness = input("🔆 Độ sáng (-1.0 đến 1.0, 0=không đổi): ").strip()
            if brightness:
                val = float(brightness)
                if -1.0 <= val <= 1.0:
                    filter_config['brightness'] = val
                    print(f"   ✓ Brightness: {val:+.2f}")
                else:
                    print("   ⚠️ Giá trị ngoài phạm vi, bỏ qua")
            
            contrast = input("🔳 Độ tương phản (0.0 đến 3.0, 1.0=không đổi): ").strip()
            if contrast:
                val = float(contrast)
                if 0.0 <= val <= 3.0:
                    filter_config['contrast'] = val
                    print(f"   ✓ Contrast: {val:.2f}x")
                else:
                    print("   ⚠️ Giá trị ngoài phạm vi, bỏ qua")
            
            saturation = input("🌈 Độ bão hòa (0.0 đến 3.0, 1.0=không đổi): ").strip()
            if saturation:
                val = float(saturation)
                if 0.0 <= val <= 3.0:
                    filter_config['saturation'] = val
                    print(f"   ✓ Saturation: {val:.2f}x")
                else:
                    print("   ⚠️ Giá trị ngoài phạm vi, bỏ qua")
            
            print("\n🎭 CÁC HIỆU ỨNG ĐỘC BIỆT:")
            
            sepia = input("📸 Hiệu ứng Sepia (y/n): ").strip().lower()
            if sepia in ['y', 'yes', '1']:
                filter_config['sepia'] = True
                print("   ✓ Sepia effect enabled")
            
            vignette = input("🕳️ Hiệu ứng Vignette (y/n): ").strip().lower()
            if vignette in ['y', 'yes', '1']:
                filter_config['vignette'] = True
                print("   ✓ Vignette effect enabled")
            
            # Tóm tắt custom filter
            print(f"\n📋 TÓM TẮT BỘ LỌC TÙY CHỈNH:")
            for key, value in filter_config.items():
                if key != 'name':
                    print(f"   • {key}: {value}")
            
            confirm = input("\n✅ Xác nhận tạo bộ lọc này (y/n): ").strip().lower()
            if confirm in ['y', 'yes', '1']:
                return filter_config
            else:
                print("❌ Hủy tạo bộ lọc")
                return None
            
        except ValueError:
            print("❌ Vui lòng nhập số hợp lệ!")
            return None
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return None
    
    def _show_advanced_results(self, success_count, error_count, total_count, 
                             filter_name, total_time, size_before, size_after, mode):
        """Hiển thị kết quả chi tiết với thống kê"""
        print("\n" + "=" * 70)
        print(f"🏁 KẾT QUẢ XỬ LÝ BỘ LỌC VIDEO")
        print("=" * 70)
        
        # Thống kê cơ bản
        print(f"📊 THỐNG KÊ TỔNG QUAN:")
        print(f"   ✅ Thành công: {success_count}/{total_count} file")
        print(f"   ❌ Lỗi: {error_count}/{total_count} file")
        print(f"   🎨 Bộ lọc: {filter_name}")
        print(f"   ⚙️ Chế độ: {mode}")
        
        # Thống kê thời gian
        print(f"\n⏱️ THỐNG KÊ THỜI GIAN:")
        print(f"   ⏰ Tổng thời gian: {total_time:.1f} giây")
        if success_count > 0:
            avg_time = total_time / success_count
            print(f"   📈 Trung bình/file: {avg_time:.1f} giây")
        
        # Thống kê dung lượng
        if size_before > 0 and size_after > 0:
            print(f"\n💾 THỐNG KÊ DUNG LƯỢNG:")
            size_before_mb = size_before / (1024 * 1024)
            size_after_mb = size_after / (1024 * 1024)
            compression_ratio = (size_after / size_before) * 100
            
            print(f"   📥 Tổng input: {size_before_mb:.1f} MB")
            print(f"   📤 Tổng output: {size_after_mb:.1f} MB")
            print(f"   📊 Tỷ lệ nén: {compression_ratio:.1f}%")
            
            if compression_ratio < 100:
                savings = size_before_mb - size_after_mb
                print(f"   💰 Tiết kiệm: {savings:.1f} MB")
        
        # Thông tin output
        if success_count > 0:
            print(f"\n📁 FILES OUTPUT:")
            print(f"   📂 Vị trí: Thư mục output đã chỉ định")
            print(f"   🏷️ Định dạng tên: *_filtered_{filter_name.lower()}_*")
            print(f"   📋 Quy tắc: [tên_gốc]_filtered_[tên_filter]_[timestamp][đuôi_file]")
        
        # Khuyến nghị
        print(f"\n💡 KHUYẾN NGHỊ:")
        if error_count > 0:
            print(f"   ⚠️ {error_count} file lỗi - kiểm tra định dạng và quyền truy cập")
        
        if mode == 'fast' and success_count > 0:
            print(f"   🏃 Chế độ Fast - có thể nâng cấp lên Quality để chất lượng tốt hơn")
        elif mode == 'quality':
            print(f"   🎯 Chế độ Quality - chất lượng tối ưu đã được áp dụng")
        
        if total_time > 300:  # > 5 phút
            print(f"   🚀 Xử lý lâu - thử chế độ GPU hoặc Fast để tăng tốc")
        
        print("=" * 70)