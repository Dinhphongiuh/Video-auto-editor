#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Voice Changer Action
Chức năng auto thay đổi giọng nói cho video
"""

import os
import tempfile
from .base_action import BaseAction
from .audio_processor import AudioProcessor
from .voice_effects import VoiceEffects


class VoiceChangerAction(BaseAction):
    """Action để thay đổi giọng nói trong video"""
    
    def __init__(self):
        super().__init__()
        self.audio_processor = AudioProcessor()
        self.voice_effects = VoiceEffects()
        
        # Các preset giọng nói
        self.voice_presets = {
            "1": {
                "name": "Nam → Nữ",
                "description": "Chuyển giọng nam thành nữ",
                "pitch": "+300",
                "tempo": "1.1",
                "formant": "1.2"
            },
            "2": {
                "name": "Nữ → Nam", 
                "description": "Chuyển giọng nữ thành nam",
                "pitch": "-200",
                "tempo": "0.9",
                "formant": "0.8"
            },
            "3": {
                "name": "Robot",
                "description": "Giọng robot/máy móc",
                "pitch": "0",
                "tempo": "1.0",
                "formant": "1.0",
                "effect": "robot"
            },
            "4": {
                "name": "Chipmunk",
                "description": "Giọng sóc chuột vui nhộn",
                "pitch": "+500",
                "tempo": "1.3",
                "formant": "1.5"
            },
            "5": {
                "name": "Quái vật",
                "description": "Giọng quái vật đáng sợ",
                "pitch": "-400",
                "tempo": "0.8",
                "formant": "0.6",
                "effect": "monster"
            },
            "6": {
                "name": "Echo",
                "description": "Thêm hiệu ứng echo",
                "pitch": "0",
                "tempo": "1.0", 
                "formant": "1.0",
                "effect": "echo"
            },
            "7": {
                "name": "Telephone",
                "description": "Giọng qua điện thoại",
                "pitch": "0",
                "tempo": "1.0",
                "formant": "1.0",
                "effect": "telephone"
            },
            "8": {
                "name": "Reverb",
                "description": "Thêm hiệu ứng reverb",
                "pitch": "0",
                "tempo": "1.0",
                "formant": "1.0", 
                "effect": "reverb"
            },
            "custom": {
                "name": "Tùy chỉnh",
                "description": "Tự điều chỉnh các thông số"
            }
        }
    
    def show_voice_menu(self):
        """Hiển thị menu chọn giọng nói"""
        print("\n🎤 CHỌN KIỂU GIỌNG NÓI:")
        print("-" * 50)
        
        for key, preset in self.voice_presets.items():
            if key != "custom":
                print(f"{key}. {preset['name']} - {preset['description']}")
        
        print(f"9. {self.voice_presets['custom']['name']} - {self.voice_presets['custom']['description']}")
        print("0. ← Quay lại")
        print("-" * 50)
    
    def get_voice_choice(self):
        """Lấy lựa chọn giọng nói từ user"""
        while True:
            choice = input("👉 Chọn kiểu giọng (0-9): ").strip()
            
            if choice == "0":
                return None
            elif choice in self.voice_presets:
                return choice
            elif choice == "9":
                return "custom"
            else:
                print("❌ Lựa chọn không hợp lệ! Vui lòng chọn từ 0-9.")
    
    def get_custom_settings(self):
        """Lấy thông số tùy chỉnh từ user"""
        print("\n🎛️ TÙY CHỈNH THÔNG SỐ GIỌNG NÓI:")
        print("-" * 40)
        
        # Pitch (cao độ)
        while True:
            try:
                pitch_input = input("🎵 Pitch (-1000 đến +1000, 0=không đổi): ").strip()
                if not pitch_input:
                    pitch = "0"
                    break
                pitch_value = int(pitch_input)
                if -1000 <= pitch_value <= 1000:
                    pitch = f"{pitch_value:+d}" if pitch_value != 0 else "0"
                    break
                else:
                    print("❌ Pitch phải từ -1000 đến +1000")
            except ValueError:
                print("❌ Vui lòng nhập số nguyên")
        
        # Tempo (tốc độ)
        while True:
            try:
                tempo_input = input("⚡ Tempo (0.5 đến 2.0, 1.0=bình thường): ").strip()
                if not tempo_input:
                    tempo = "1.0"
                    break
                tempo_value = float(tempo_input)
                if 0.5 <= tempo_value <= 2.0:
                    tempo = str(tempo_value)
                    break
                else:
                    print("❌ Tempo phải từ 0.5 đến 2.0")
            except ValueError:
                print("❌ Vui lòng nhập số thập phân")
        
        # Formant (âm vực)
        while True:
            try:
                formant_input = input("🎭 Formant (0.5 đến 2.0, 1.0=bình thường): ").strip()
                if not formant_input:
                    formant = "1.0"
                    break
                formant_value = float(formant_input)
                if 0.5 <= formant_value <= 2.0:
                    formant = str(formant_value)
                    break
                else:
                    print("❌ Formant phải từ 0.5 đến 2.0")
            except ValueError:
                print("❌ Vui lòng nhập số thập phân")
        
        # Hiệu ứng đặc biệt
        print("\n🎨 HIỆU ỨNG ĐẶC BIỆT:")
        print("1. Không có")
        print("2. Robot")
        print("3. Echo")
        print("4. Reverb")
        print("5. Telephone")
        print("6. Monster")
        
        while True:
            effect_choice = input("👉 Chọn hiệu ứng (1-6): ").strip()
            effect_map = {
                "1": None,
                "2": "robot",
                "3": "echo", 
                "4": "reverb",
                "5": "telephone",
                "6": "monster"
            }
            if effect_choice in effect_map:
                effect = effect_map[effect_choice]
                break
            else:
                print("❌ Lựa chọn không hợp lệ!")
        
        return {
            "name": "Tùy chỉnh",
            "description": f"Pitch: {pitch}, Tempo: {tempo}, Formant: {formant}",
            "pitch": pitch,
            "tempo": tempo,
            "formant": formant,
            "effect": effect
        }
    
    def apply_voice_change(self, input_file, output_file, preset_config):
        """Áp dụng thay đổi giọng nói cho một video"""
        try:
            print(f"\n🎤 Đang xử lý: {os.path.basename(input_file)}")
            print(f"🎭 Hiệu ứng: {preset_config['name']}")
            
            # Tạo tên file tạm
            with tempfile.TemporaryDirectory() as temp_dir:
                # Trích xuất audio
                audio_file = os.path.join(temp_dir, "audio.wav")
                print("📤 Đang trích xuất audio...")
                
                if not self.audio_processor.extract_audio(input_file, audio_file):
                    print("❌ Lỗi khi trích xuất audio")
                    return False
                
                # Xử lý voice effect
                processed_audio = os.path.join(temp_dir, "processed_audio.wav")
                print("🎛️ Đang xử lý giọng nói...")
                
                if not self.voice_effects.apply_voice_effect(audio_file, processed_audio, preset_config):
                    print("❌ Lỗi khi xử lý giọng nói")
                    return False
                
                # Kết hợp với video gốc
                print("🎬 Đang kết hợp audio với video...")
                
                if not self.audio_processor.combine_audio_video(input_file, processed_audio, output_file):
                    print("❌ Lỗi khi kết hợp audio với video")
                    return False
                
                print("✅ Hoàn thành!")
                return True
                
        except Exception as e:
            print(f"❌ Lỗi xử lý file {input_file}: {e}")
            return False
    
    def execute(self, input_folder, output_folder):
        """Thực thi chức năng thay đổi giọng nói"""
        print("\n🎤 === THAY ĐỔI GIỌNG NÓI VIDEO ===")
        
        # Kiểm tra thư mục
        if not self.validate_folders(input_folder, output_folder):
            return
        
        # Lấy danh sách video
        video_files = self.get_video_files(input_folder)
        if not video_files:
            print(f"❌ Không tìm thấy file video nào trong thư mục: {input_folder}")
            input("Nhấn Enter để tiếp tục...")
            return
        
        print(f"📁 Tìm thấy {len(video_files)} video(s)")
        for i, file in enumerate(video_files, 1):
            print(f"  {i}. {os.path.basename(file)}")
        
        # Hiển thị menu chọn giọng
        self.show_voice_menu()
        
        # Lấy lựa chọn từ user
        choice = self.get_voice_choice()
        if choice is None:
            print("🚫 Đã hủy thao tác")
            input("Nhấn Enter để tiếp tục...")
            return
        
        # Lấy config preset
        if choice == "custom":
            preset_config = self.get_custom_settings()
        else:
            preset_config = self.voice_presets[choice]
        
        # Xác nhận xử lý
        print(f"\n📊 SẼ XỬ LÝ:")
        print(f"🎭 Hiệu ứng: {preset_config['name']}")
        print(f"📝 Mô tả: {preset_config['description']}")
        print(f"📁 {len(video_files)} video(s)")
        
        confirm = input("\n❓ Bắt đầu xử lý? (y/n): ").strip().lower()
        if confirm != 'y':
            print("🚫 Đã hủy thao tác")
            input("Nhấn Enter để tiếp tục...")
            return
        
        # Xử lý từng video
        success_count = 0
        total_count = len(video_files)
        
        print(f"\n🚀 Bắt đầu xử lý {total_count} video(s)...")
        print("=" * 60)
        
        for i, video_file in enumerate(video_files, 1):
            print(f"\n📹 [{i}/{total_count}] Đang xử lý video...")
            
            # Tạo tên file output
            basename = os.path.splitext(os.path.basename(video_file))[0]
            extension = os.path.splitext(video_file)[1]
            voice_name = preset_config['name'].replace(' ', '_').replace('→', 'to')
            output_filename = f"{basename}_voice_{voice_name}{extension}"
            output_path = os.path.join(output_folder, output_filename)
            
            # Xử lý
            if self.apply_voice_change(video_file, output_path, preset_config):
                success_count += 1
                print(f"✅ Lưu tại: {output_filename}")
            else:
                print(f"❌ Thất bại: {os.path.basename(video_file)}")
            
            print("-" * 40)
        
        # Kết quả
        print(f"\n🎊 KẾT QUẢ XỬ LÝ:")
        print(f"✅ Thành công: {success_count}/{total_count}")
        print(f"❌ Thất bại: {total_count - success_count}/{total_count}")
        print(f"📁 Thư mục output: {output_folder}")
        
        input("\nNhấn Enter để tiếp tục...")