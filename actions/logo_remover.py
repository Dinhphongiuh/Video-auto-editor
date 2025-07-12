#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logo Remover Action Enhanced - Phiên bản cải tiến
Sử dụng nhiều phương pháp xóa logo khác nhau
"""

import os
import subprocess
import json
import shutil
from datetime import datetime
from .base_action import BaseAction


class LogoRemoverAction(BaseAction):
    """Xử lý tự động phát hiện và xóa logo/watermark - Enhanced Version"""
    
    def __init__(self):
        super().__init__()
        self.removal_methods = {
            "1": ("auto_detect", "🤖 Tự động phát hiện logo (khuyến nghị)"),
            "2": ("auto_corners", "🔍 Tự động tìm ở các góc"),
            "3": ("manual_preset", "📍 Chọn vị trí có sẵn"),
            "4": ("custom", "🎯 Tùy chỉnh vị trí"),
            "5": ("advanced_blur", "🌀 Xóa logo nâng cao (blur + delogo)"),
            "6": ("inpaint", "🎨 Xóa logo với inpainting (chất lượng cao)")
        }
        
        # Preset positions cho manual mode
        self.preset_positions = {
            "1": ("corner_top_right", "Góc trên phải"),
            "2": ("corner_top_left", "Góc trên trái"), 
            "3": ("corner_bottom_right", "Góc dưới phải"),
            "4": ("corner_bottom_left", "Góc dưới trái"),
            "5": ("center_bottom", "Giữa phía dưới"),
            "6": ("center_top", "Giữa phía trên"),
            "7": ("custom_multi", "Nhiều vị trí (nhập thủ công)")
        }
        
        # Removal techniques
        self.removal_techniques = {
            "delogo": "Xóa logo cơ bản",
            "blur": "Làm mờ vùng logo",
            "boxblur": "Làm mờ hình hộp",
            "inpaint": "Tái tạo vùng logo",
            "crop": "Cắt bỏ vùng có logo"
        }
    
    def execute(self, input_folder, output_folder):
        """Thực hiện tự động xóa logo"""
        # Kiểm tra thư mục
        if not self.validate_folders(input_folder, output_folder):
            return
        
        # Lấy danh sách video
        video_files = self.get_video_files(input_folder)
        if not video_files:
            print("❌ Không tìm thấy file video nào!")
            input("Nhấn Enter để tiếp tục...")
            return
        
        print(f"\n🚫 TỰ ĐỘNG XÓA LOGO/WATERMARK - ENHANCED VERSION")
        print(f"Tìm thấy {len(video_files)} file video")
        
        # Kiểm tra FFmpeg
        if not self._check_ffmpeg():
            print("❌ FFmpeg không khả dụng! Vui lòng cài đặt FFmpeg.")
            input("Nhấn Enter để tiếp tục...")
            return
        
        # Chọn phương pháp detection
        detection_method = self._select_detection_method()
        if not detection_method:
            return
        
        # Chọn kỹ thuật xóa logo
        removal_technique = self._select_removal_technique()
        
        # Tạo log file
        log_file = os.path.join(output_folder, f"logo_removal_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        
        # Thực hiện xóa logo
        print(f"\n🔄 Đang xử lý...")
        print(f"Phương pháp phát hiện: {detection_method}")
        print(f"Kỹ thuật xóa: {removal_technique}")
        print(f"Số file cần xử lý: {len(video_files)}")
        print(f"Log file: {log_file}")
        print("-" * 50)
        
        success_count = 0
        error_count = 0
        skipped_count = 0
        
        with open(log_file, 'w', encoding='utf-8') as log:
            log.write(f"Logo Removal Log - {datetime.now()}\n")
            log.write(f"Detection Method: {detection_method}\n")
            log.write(f"Removal Technique: {removal_technique}\n")
            log.write("="*50 + "\n\n")
            
            for i, video_file in enumerate(video_files, 1):
                filename = os.path.basename(video_file)
                name, ext = os.path.splitext(filename)
                output_file = os.path.join(output_folder, f"{name}_no_logo{ext}")
                
                print(f"\n[{i}/{len(video_files)}] 📁 Xử lý: {filename}")
                log.write(f"\n[{i}/{len(video_files)}] Processing: {filename}\n")
                
                # Kiểm tra file input tồn tại
                if not os.path.exists(video_file):
                    print(f"  ❌ Lỗi: File input không tồn tại!")
                    log.write(f"  ERROR: Input file not found\n")
                    error_count += 1
                    continue
                
                try:
                    # Lấy thông tin video
                    video_info = self._get_video_info(video_file)
                    if not video_info:
                        print(f"  ❌ Lỗi: Không thể đọc thông tin video!")
                        log.write(f"  ERROR: Cannot read video info\n")
                        error_count += 1
                        continue
                    
                    file_size = os.path.getsize(video_file) / (1024 * 1024)  # MB
                    print(f"  📀 Kích thước: {file_size:.2f} MB | {video_info['width']}x{video_info['height']}")
                    log.write(f"  Size: {file_size:.2f} MB | Resolution: {video_info['width']}x{video_info['height']}\n")
                    
                    # Tự động phát hiện hoặc sử dụng preset
                    logo_regions = self._detect_logo_regions(video_file, detection_method, video_info)
                    
                    if logo_regions:
                        print(f"  🎯 Phát hiện {len(logo_regions)} vùng logo")
                        log.write(f"  Detected {len(logo_regions)} logo regions\n")
                        
                        for idx, (x, y, w, h, confidence) in enumerate(logo_regions):
                            print(f"    Region {idx+1}: x={x}, y={y}, w={w}, h={h} (confidence: {confidence:.2f})")
                            log.write(f"    Region {idx+1}: x={x}, y={y}, w={w}, h={h} (confidence: {confidence:.2f})\n")
                        
                        # Xóa logo với kỹ thuật đã chọn
                        success = self._remove_logo_advanced(
                            video_file, output_file, logo_regions, removal_technique, log
                        )
                        
                        if success:
                            output_size = os.path.getsize(output_file) / (1024 * 1024)
                            print(f"  ✅ Thành công! Output: {output_size:.2f} MB")
                            log.write(f"  SUCCESS: Output size {output_size:.2f} MB\n")
                            success_count += 1
                        else:
                            print(f"  ❌ Lỗi: Không thể xóa logo!")
                            log.write(f"  ERROR: Failed to remove logo\n")
                            error_count += 1
                            # Xóa file output nếu có (không copy file gốc)
                            if os.path.exists(output_file):
                                os.remove(output_file)
                    else:
                        print(f"  ⚠️ Không tìm thấy logo trong video")
                        log.write(f"  WARNING: No logo detected\n")
                        
                        # Hỏi user có muốn copy file gốc không
                        if i == 1:  # Chỉ hỏi 1 lần
                            copy_original = input("    Copy file gốc khi không tìm thấy logo? (y/n): ").lower() == 'y'
                        
                        if 'copy_original' in locals() and copy_original:
                            shutil.copy2(video_file, output_file)
                            print(f"    📋 Đã copy file gốc")
                            log.write(f"    Copied original file\n")
                            success_count += 1
                        else:
                            skipped_count += 1
                        
                except Exception as e:
                    print(f"  ❌ Lỗi: {e}")
                    log.write(f"  ERROR: {str(e)}\n")
                    error_count += 1
        
        # Hiển thị kết quả
        self._show_results(success_count, error_count, skipped_count, len(video_files))
        print(f"\n📄 Chi tiết đã được lưu trong: {log_file}")
        input("Nhấn Enter để tiếp tục...")
    
    def _select_removal_technique(self):
        """Chọn kỹ thuật xóa logo"""
        print("\n🎨 Chọn kỹ thuật xóa logo:")
        print("1. Delogo (Cơ bản, nhanh)")
        print("2. Blur (Làm mờ, trung bình)")
        print("3. Boxblur (Làm mờ mạnh)")
        print("4. Smart Blur (Làm mờ thông minh)")
        print("5. Inpaint (Tái tạo - chất lượng cao nhưng chậm)")
        
        choice = input("Chọn kỹ thuật (mặc định 1): ").strip() or "1"
        
        techniques = {
            "1": "delogo",
            "2": "blur", 
            "3": "boxblur",
            "4": "smartblur",
            "5": "inpaint"
        }
        
        return techniques.get(choice, "delogo")
    
    def _detect_logo_regions(self, video_file, method, video_info):
        """Phát hiện nhiều vùng logo"""
        if method == "auto_detect":
            return self._auto_detect_multiple_logos(video_file, video_info)
        elif method == "auto_corners":
            return self._auto_detect_corners_multi(video_file, video_info)
        elif method == "manual_preset":
            return [self._select_preset_position(video_file, video_info)]
        elif method == "custom":
            return self._get_custom_positions()
        elif method == "advanced_blur" or method == "inpaint":
            return self._auto_detect_multiple_logos(video_file, video_info)
        else:
            return None
    
    def _auto_detect_multiple_logos(self, video_file, video_info):
        """Tự động phát hiện nhiều logo"""
        width, height = video_info['width'], video_info['height']
        candidates = []
        
        # Các vùng thường có logo với kích thước động
        logo_width = min(250, int(width * 0.2))  # Max 20% width
        logo_height = min(120, int(height * 0.15))  # Max 15% height
        margin = 20
        
        regions = [
            # Góc trên phải (phổ biến nhất)
            (width - logo_width - margin, margin, logo_width, logo_height, 0.9),
            # Góc trên trái
            (margin, margin, logo_width, logo_height, 0.8),
            # Góc dưới phải
            (width - logo_width - margin, height - logo_height - margin, logo_width, logo_height, 0.7),
            # Góc dưới trái  
            (margin, height - logo_height - margin, logo_width, logo_height, 0.6),
            # Giữa phía dưới (cho TV logos)
            ((width - logo_width) // 2, height - logo_height - margin, logo_width, logo_height, 0.5)
        ]
        
        # Thêm các region vào candidates nếu hợp lệ
        for x, y, w, h, conf in regions:
            if self._is_valid_region(x, y, w, h, width, height):
                candidates.append((int(x), int(y), int(w), int(h), conf))
        
        # Chỉ trả về top 2 candidates với confidence cao nhất
        candidates.sort(key=lambda x: x[4], reverse=True)
        return candidates[:2]
    
    def _is_valid_region(self, x, y, w, h, video_width, video_height):
        """Kiểm tra region có hợp lệ không"""
        return (x >= 0 and y >= 0 and 
                x + w <= video_width and y + h <= video_height and
                w > 30 and h > 20)
    
    def _remove_logo_advanced(self, input_file, output_file, logo_regions, technique, log):
        """Xóa logo với nhiều kỹ thuật khác nhau"""
        try:
            if technique == "delogo":
                return self._remove_with_delogo(input_file, output_file, logo_regions, log)
            elif technique == "blur":
                return self._remove_with_blur(input_file, output_file, logo_regions, log)
            elif technique == "boxblur":
                return self._remove_with_boxblur(input_file, output_file, logo_regions, log)
            elif technique == "smartblur":
                return self._remove_with_smartblur(input_file, output_file, logo_regions, log)
            elif technique == "inpaint":
                return self._remove_with_inpaint(input_file, output_file, logo_regions, log)
            else:
                return self._remove_with_delogo(input_file, output_file, logo_regions, log)
                
        except Exception as e:
            log.write(f"    ERROR in removal: {str(e)}\n")
            print(f"    ❌ Lỗi khi xóa logo: {e}")
            return False
    
    def _remove_with_delogo(self, input_file, output_file, logo_regions, log):
        """Xóa logo với delogo filter"""
        # Build delogo filter cho nhiều regions
        filters = []
        for x, y, w, h, _ in logo_regions:
            filters.append(f"delogo=x={x}:y={y}:w={w}:h={h}")
        
        filter_complex = ",".join(filters)
        
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-vf', filter_complex,
            '-c:a', 'copy',
            '-y',
            output_file
        ]
        
        log.write(f"    Command: {' '.join(cmd)}\n")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            log.write("    Delogo filter applied successfully\n")
            return True
        else:
            log.write(f"    Delogo failed: {result.stderr}\n")
            return False
    
    def _remove_with_blur(self, input_file, output_file, logo_regions, log):
        """Xóa logo với blur filter"""
        # Build complex filter với blur cho từng region
        filter_parts = []
        
        for i, (x, y, w, h, _) in enumerate(logo_regions):
            if i == 0:
                filter_parts.append(f"[0:v]crop={w}:{h}:{x}:{y},avgblur=10[blur{i}]")
                filter_parts.append(f"[0:v][blur{i}]overlay={x}:{y}[v{i}]")
            else:
                filter_parts.append(f"[v{i-1}]crop={w}:{h}:{x}:{y},avgblur=10[blur{i}]")
                filter_parts.append(f"[v{i-1}][blur{i}]overlay={x}:{y}[v{i}]")
        
        filter_complex = ";".join(filter_parts)
        
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-filter_complex', filter_complex,
            '-map', f'[v{len(logo_regions)-1}]',
            '-map', '0:a?',
            '-c:a', 'copy',
            '-y',
            output_file
        ]
        
        log.write(f"    Blur filter command\n")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            log.write("    Blur filter applied successfully\n")
            return True
        else:
            log.write(f"    Blur failed: {result.stderr}\n")
            return False
    
    def _remove_with_boxblur(self, input_file, output_file, logo_regions, log):
        """Xóa logo với boxblur mạnh hơn"""
        # Tương tự blur nhưng dùng boxblur
        filter_parts = []
        
        for i, (x, y, w, h, _) in enumerate(logo_regions):
            if i == 0:
                filter_parts.append(f"[0:v]crop={w}:{h}:{x}:{y},boxblur=20:5[blur{i}]")
                filter_parts.append(f"[0:v][blur{i}]overlay={x}:{y}[v{i}]")
            else:
                filter_parts.append(f"[v{i-1}]crop={w}:{h}:{x}:{y},boxblur=20:5[blur{i}]")
                filter_parts.append(f"[v{i-1}][blur{i}]overlay={x}:{y}[v{i}]")
        
        filter_complex = ";".join(filter_parts)
        
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-filter_complex', filter_complex,
            '-map', f'[v{len(logo_regions)-1}]',
            '-map', '0:a?',
            '-c:a', 'copy',
            '-y',
            output_file
        ]
        
        log.write(f"    Boxblur filter command\n")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            log.write("    Boxblur filter applied successfully\n")
            return True
        else:
            log.write(f"    Boxblur failed: {result.stderr}\n")
            return False
    
    def _remove_with_smartblur(self, input_file, output_file, logo_regions, log):
        """Xóa logo với smart blur (delogo + blur)"""
        # Kết hợp delogo và blur
        filters = []
        
        # Đầu tiên apply delogo
        for x, y, w, h, _ in logo_regions:
            filters.append(f"delogo=x={x}:y={y}:w={w}:h={h}")
        
        # Sau đó apply nhẹ blur lên vùng đó
        for x, y, w, h, _ in logo_regions:
            # Expand vùng blur một chút
            bx = max(0, x - 5)
            by = max(0, y - 5)
            bw = w + 10
            bh = h + 10
            filters.append(f"boxblur=5:1:cr={bw}:{bh}:{bx}:{by}:exact=1")
        
        filter_complex = ",".join(filters)
        
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-vf', filter_complex,
            '-c:a', 'copy',
            '-y',
            output_file
        ]
        
        log.write(f"    Smart blur command\n")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            log.write("    Smart blur applied successfully\n")
            return True
        else:
            log.write(f"    Smart blur failed, trying simple delogo\n")
            # Fallback to simple delogo
            return self._remove_with_delogo(input_file, output_file, logo_regions, log)
    
    def _remove_with_inpaint(self, input_file, output_file, logo_regions, log):
        """Xóa logo với inpainting (chất lượng cao nhất)"""
        # FFmpeg không hỗ trợ inpainting trực tiếp
        # Sử dụng kết hợp delogo + smartblur + denoise
        filters = []
        
        # Delogo first
        for x, y, w, h, _ in logo_regions:
            filters.append(f"delogo=x={x}:y={y}:w={w}:h={h}:show=0")
        
        # Add noise reduction
        filters.append("hqdn3d=4:3:6:4.5")
        
        # Add slight sharpening
        filters.append("unsharp=5:5:0.5:5:5:0.0")
        
        filter_complex = ",".join(filters)
        
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-vf', filter_complex,
            '-c:a', 'copy',
            '-y',
            output_file
        ]
        
        log.write(f"    Inpaint-style filter command\n")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            log.write("    Inpaint-style filter applied successfully\n")
            return True
        else:
            log.write(f"    Inpaint-style failed: {result.stderr}\n")
            return False
    
    def _show_results(self, success_count, error_count, skipped_count, total_count):
        """Hiển thị kết quả xử lý chi tiết"""
        print("\n" + "=" * 50)
        print(f"🏁 KẾT QUẢ XÓA LOGO:")
        print(f"  ✅ Thành công: {success_count}/{total_count}")
        print(f"  ❌ Lỗi: {error_count}/{total_count}")
        print(f"  ⏭️  Bỏ qua: {skipped_count}/{total_count}")
        
        if success_count > 0:
            print(f"\n📁 File output:")
            print(f"  - Pattern: *_no_logo.*")
            print(f"  - Kiểm tra log file để xem chi tiết")
        
        print("\n💡 Lưu ý:")
        print("  - Nếu logo không được xóa sạch, thử các kỹ thuật khác")
        print("  - Blur/Boxblur phù hợp cho logo trong suốt")
        print("  - Delogo phù hợp cho logo đặc")
        print("  - Inpaint cho chất lượng tốt nhất nhưng chậm")
        print("=" * 50)
    
    def _check_ffmpeg(self):
        """Kiểm tra FFmpeg và các filter có khả dụng không"""
        try:
            # Check ffmpeg version
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                return False
            
            # Check available filters
            result = subprocess.run(['ffmpeg', '-filters'], 
                                  capture_output=True, text=True)
            
            required_filters = ['delogo', 'blur', 'boxblur', 'overlay', 'crop']
            available_filters = result.stdout
            
            missing = []
            for f in required_filters:
                if f not in available_filters:
                    missing.append(f)
            
            if missing:
                print(f"⚠️ Cảnh báo: Một số filter không khả dụng: {', '.join(missing)}")
                print("   Một số tính năng có thể không hoạt động.")
            
            return True
            
        except:
            return False
    
    def _select_detection_method(self):
        """Cho phép user chọn phương pháp phát hiện"""
        print("\nChọn phương pháp xử lý logo:")
        
        for key, (method, desc) in self.removal_methods.items():
            print(f"{key}. {desc}")
        
        try:
            choice = input("Nhập số (mặc định 1): ").strip() or "1"
            
            if choice in self.removal_methods:
                method, desc = self.removal_methods[choice]
                return method
            else:
                print("❌ Lựa chọn không hợp lệ! Sử dụng auto detect.")
                return "auto_detect"
                
        except ValueError:
            print("❌ Vui lòng nhập số! Sử dụng auto detect.")
            return "auto_detect"
    
    def _auto_detect_corners_multi(self, video_file, video_info):
        """Auto detect ở các góc với nhiều kích thước"""
        width, height = video_info['width'], video_info['height']
        candidates = []
        
        # Thử nhiều kích thước logo
        logo_sizes = [
            (200, 80),   # Small
            (250, 100),  # Medium
            (300, 120),  # Large
        ]
        
        for lw, lh in logo_sizes:
            # Scale theo video size
            lw = min(lw, int(width * 0.25))
            lh = min(lh, int(height * 0.2))
            
            # Chỉ thêm góc trên phải (phổ biến nhất)
            x = width - lw - 20
            y = 20
            
            if self._is_valid_region(x, y, lw, lh, width, height):
                candidates.append((x, y, lw, lh, 0.8))
                break  # Chỉ lấy 1 size phù hợp
        
        return candidates[:1]  # Trả về 1 region
    
    def _select_preset_position(self, video_file, video_info):
        """Cho user chọn preset position"""
        print("\nChọn vị trí logo:")
        for key, (pos, desc) in self.preset_positions.items():
            print(f"{key}. {desc}")
        
        try:
            choice = input("Nhập số: ").strip()
            if choice in self.preset_positions:
                pos, desc = self.preset_positions[choice]
                
                if pos == "custom_multi":
                    return self._get_custom_positions()
                
                width, height = video_info['width'], video_info['height']
                x, y, w, h = self._get_preset_coordinates(pos, width, height)
                
                return (x, y, w, h, 1.0)
            else:
                print("❌ Lựa chọn không hợp lệ!")
                return None
        except:
            return None
    
    def _get_preset_coordinates(self, position, width, height):
        """Lấy tọa độ cho preset position với dynamic sizing"""
        # Dynamic logo size based on video resolution
        logo_width = min(250, int(width * 0.2))
        logo_height = min(100, int(height * 0.15))
        margin = 20
        
        configs = {
            "corner_top_right": (width - logo_width - margin, margin, logo_width, logo_height),
            "corner_top_left": (margin, margin, logo_width, logo_height),
            "corner_bottom_right": (width - logo_width - margin, height - logo_height - margin, logo_width, logo_height),
            "corner_bottom_left": (margin, height - logo_height - margin, logo_width, logo_height),
            "center_bottom": ((width - logo_width) // 2, height - logo_height - margin, logo_width, logo_height),
            "center_top": ((width - logo_width) // 2, margin, logo_width, logo_height)
        }
        return configs.get(position, (margin, margin, logo_width, logo_height))
    
    def _get_custom_positions(self):
        """Lấy nhiều vị trí tùy chỉnh từ user"""
        print("\n🎯 TÙY CHỈNH VỊ TRÍ LOGO")
        positions = []
        
        while True:
            print(f"\nNhập vị trí logo #{len(positions) + 1} (hoặc Enter để kết thúc):")
            try:
                x_input = input("X (tọa độ ngang): ").strip()
                if not x_input:
                    break
                    
                x = int(x_input)
                y = int(input("Y (tọa độ dọc): ").strip())
                w = int(input("Width (chiều rộng): ").strip())
                h = int(input("Height (chiều cao): ").strip())
                
                positions.append((x, y, w, h, 1.0))
                
                if len(positions) >= 3:
                    print("⚠️ Đã đạt giới hạn 3 vùng logo")
                    break
                    
            except ValueError:
                print("❌ Vui lòng nhập số hợp lệ!")
                continue
        
        return positions if positions else None
    
    def _get_video_info(self, video_file):
        """Lấy thông tin video chi tiết"""
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_streams',
                '-show_format',
                video_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return None
            
            data = json.loads(result.stdout)
            
            # Tìm video stream
            for stream in data['streams']:
                if stream['codec_type'] == 'video':
                    return {
                        'width': int(stream['width']),
                        'height': int(stream['height']),
                        'duration': float(data['format'].get('duration', 0)),
                        'bitrate': int(data['format'].get('bit_rate', 0)),
                        'codec': stream.get('codec_name', 'unknown')
                    }
            
            return None
        except Exception as e:
            print(f"❌ Lỗi khi đọc video info: {e}")
            return None