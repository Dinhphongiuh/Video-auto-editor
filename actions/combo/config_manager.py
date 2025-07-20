#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Config Manager
Quản lý cấu hình cho các chức năng combo
"""


class ConfigManager:
    """Class để cấu hình từng chức năng trong combo"""
    
    def configure_function(self, function_key, available_functions):
        """Cấu hình chi tiết cho từng chức năng"""
        func_info = available_functions[function_key]
        action_name = func_info['action']
        
        print(f"\n⚙️ CẤU HÌNH: {func_info['name']}")
        print("-" * 50)
        
        config = {}
        config_summary = ""
        
        if action_name == "format_converter":
            config, config_summary = self._configure_format_converter()
        elif action_name == "compressor":
            config, config_summary = self._configure_compressor()
        elif action_name == "speed_adjuster":
            config, config_summary = self._configure_speed_adjuster()
        elif action_name == "resolution_changer":
            config, config_summary = self._configure_resolution_changer()
        elif action_name == "filter_applier":
            config, config_summary = self._configure_filter_applier()
        elif action_name == "voice_changer":
            config, config_summary = self._configure_voice_changer()
        elif action_name == "video_trimmer":
            config, config_summary = self._configure_video_trimmer()
        
        if config:
            return {
                'key': function_key,
                'action': action_name,
                'config': config,
                'config_summary': config_summary
            }
        else:
            print("🚫 Đã hủy cấu hình chức năng này")
            return None
    
    def _configure_format_converter(self):
        """Cấu hình format converter"""
        print("📹 Chọn định dạng output:")
        print("1. MP4 (Recommended)")
        print("2. AVI")
        print("3. MOV")
        print("4. MKV")
        print("0. Hủy")
        
        choice = input("👉 Chọn (0-4): ").strip()
        format_map = {"1": "mp4", "2": "avi", "3": "mov", "4": "mkv"}
        
        if choice in format_map:
            format_type = format_map[choice]
            return {"format": format_type, "choice": choice}, f"Format: {format_type.upper()}"
        return None, ""
    
    def _configure_compressor(self):
        """Cấu hình compressor"""
        print("🗜️ Chọn mức nén:")
        print("1. Nén nhẹ (chất lượng cao)")
        print("2. Nén vừa (cân bằng)")
        print("3. Nén mạnh (dung lượng nhỏ)")
        print("0. Hủy")
        
        choice = input("👉 Chọn (0-3): ").strip()
        quality_map = {"1": "high", "2": "medium", "3": "low"}
        
        if choice in quality_map:
            quality = quality_map[choice]
            return {"quality": quality, "choice": choice}, f"Chất lượng: {quality}"
        return None, ""
    
    def _configure_speed_adjuster(self):
        """Cấu hình speed adjuster"""
        print("⚡ Chọn tốc độ:")
        print("1. 0.5x (Chậm)")
        print("2. 1.5x (Nhanh vừa)")
        print("3. 2.0x (Nhanh)")
        print("4. Tùy chỉnh")
        print("0. Hủy")
        
        choice = input("👉 Chọn (0-4): ").strip()
        
        if choice == "1":
            return {"speed": 0.5, "choice": "1"}, "Tốc độ: 0.5x"
        elif choice == "2":
            return {"speed": 1.5, "choice": "2"}, "Tốc độ: 1.5x"
        elif choice == "3":
            return {"speed": 2.0, "choice": "3"}, "Tốc độ: 2.0x"
        elif choice == "4":
            try:
                speed = float(input("Nhập tốc độ (0.1-4.0): "))
                if 0.1 <= speed <= 4.0:
                    return {"speed": speed, "choice": "4", "custom_speed": speed}, f"Tốc độ: {speed}x"
                else:
                    print("❌ Tốc độ không hợp lệ")
            except ValueError:
                print("❌ Vui lòng nhập số")
        
        return None, ""
    
    def _configure_resolution_changer(self):
        """Cấu hình resolution changer"""
        print("📐 Chọn độ phân giải:")
        print("1. 720p (HD)")
        print("2. 1080p (Full HD)")
        print("3. 480p (SD)")
        print("0. Hủy")
        
        choice = input("👉 Chọn (0-3): ").strip()
        resolution_map = {"1": "720p", "2": "1080p", "3": "480p"}
        
        if choice in resolution_map:
            resolution = resolution_map[choice]
            return {"resolution": resolution, "choice": choice}, f"Độ phân giải: {resolution}"
        return None, ""
    
    def _configure_filter_applier(self):
        """Cấu hình filter applier"""
        print("🎨 Chọn bộ lọc:")
        print("1. Vintage (Cổ điển)")
        print("2. Cinematic (Điện ảnh)")
        print("3. Vibrant (Sống động)")
        print("4. Black & White (Đen trắng)")
        print("0. Hủy")
        
        choice = input("👉 Chọn (0-4): ").strip()
        filter_map = {"1": "vintage", "2": "cinematic", "3": "vibrant", "4": "black_white"}
        
        if choice in filter_map:
            filter_type = filter_map[choice]
            return {"filter": filter_type, "choice": choice}, f"Bộ lọc: {filter_type}"
        return None, ""
    
    def _configure_voice_changer(self):
        """Cấu hình voice changer"""
        print("🎤 Chọn hiệu ứng giọng:")
        print("1. Nam → Nữ")
        print("2. Nữ → Nam")
        print("3. Robot")
        print("4. Chipmunk")
        print("0. Hủy")
        
        choice = input("👉 Chọn (0-4): ").strip()
        voice_names = {"1": "Nam→Nữ", "2": "Nữ→Nam", "3": "Robot", "4": "Chipmunk"}
        
        if choice in voice_names:
            return {"voice_preset": choice, "choice": choice}, f"Giọng: {voice_names[choice]}"
        return None, ""
    
    def _configure_video_trimmer(self):
        """Cấu hình video trimmer"""
        print("✂️ Chọn kiểu cắt:")
        print("1. Cắt từ đầu video")
        print("2. Cắt từ cuối video")
        print("0. Hủy")
        
        trim_choice = input("👉 Chọn (0-2): ").strip()
        
        if trim_choice in ["1", "2"]:
            try:
                seconds = float(input("Nhập số giây cần cắt: "))
                if seconds > 0:
                    trim_type = "start" if trim_choice == "1" else "end"
                    return {
                        "trim_type": trim_type, 
                        "seconds": seconds,
                        "choice": trim_choice
                    }, f"Cắt {seconds}s từ {'đầu' if trim_type == 'start' else 'cuối'}"
                else:
                    print("❌ Số giây phải > 0")
            except ValueError:
                print("❌ Vui lòng nhập số")
        
        return None, ""