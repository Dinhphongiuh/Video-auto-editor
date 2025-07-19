#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Voice Effects
Các hiệu ứng giọng nói chuyên dụng
"""

import os
import subprocess
import tempfile


class VoiceEffects:
    """Lớp xử lý các hiệu ứng giọng nói"""
    
    def __init__(self):
        self.ffmpeg_path = "ffmpeg"
        self.sox_path = "sox"  # SoX cho voice processing tốt hơn
    
    def check_sox(self):
        """Kiểm tra SoX có sẵn không"""
        try:
            result = subprocess.run([self.sox_path, "--version"], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def apply_voice_effect(self, input_file, output_file, config):
        """Áp dụng hiệu ứng giọng nói"""
        try:
            # Lấy các thông số
            pitch = config.get('pitch', '0')
            tempo = config.get('tempo', '1.0')
            formant = config.get('formant', '1.0')
            effect = config.get('effect', None)
            
            # Nếu có SoX, dùng SoX cho chất lượng tốt hơn
            if self.check_sox() and effect not in ['robot', 'telephone']:
                return self._apply_sox_effect(input_file, output_file, config)
            else:
                return self._apply_ffmpeg_effect(input_file, output_file, config)
                
        except Exception as e:
            print(f"❌ Lỗi áp dụng voice effect: {e}")
            return False
    
    def _apply_sox_effect(self, input_file, output_file, config):
        """Sử dụng SoX để xử lý voice effect"""
        try:
            pitch = config.get('pitch', '0')
            tempo = config.get('tempo', '1.0')
            effect = config.get('effect', None)
            
            # Xây dựng lệnh SoX
            cmd = [self.sox_path, input_file, output_file]
            
            # Pitch shifting
            if pitch != '0':
                pitch_cents = int(pitch) if pitch.lstrip('+-').isdigit() else 0
                cmd.extend(['pitch', str(pitch_cents)])
            
            # Tempo change (không thay đổi pitch)
            if tempo != '1.0':
                cmd.extend(['tempo', tempo])
            
            # Các hiệu ứng đặc biệt
            if effect == 'echo':
                cmd.extend(['echo', '0.8', '0.9', '1000', '0.3'])
            elif effect == 'reverb':
                cmd.extend(['reverb', '50'])
            elif effect == 'monster':
                cmd.extend(['pitch', '-400', 'echo', '0.5', '0.7', '100', '0.25'])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Lỗi SoX: {result.stderr}")
                return False
            
            return os.path.exists(output_file)
            
        except Exception as e:
            print(f"❌ Lỗi SoX processing: {e}")
            return False
    
    def _apply_ffmpeg_effect(self, input_file, output_file, config):
        """Sử dụng FFmpeg để xử lý voice effect"""
        try:
            pitch = config.get('pitch', '0')
            tempo = config.get('tempo', '1.0')
            effect = config.get('effect', None)
            
            # Xây dựng filter chain
            filters = []
            
            # Pitch shifting với rubberband (nếu có) hoặc asetrate
            if pitch != '0':
                pitch_cents = int(pitch) if pitch.lstrip('+-').isdigit() else 0
                # Chuyển cents thành ratio
                pitch_ratio = 2 ** (pitch_cents / 1200.0)
                
                # Dùng asetrate + atempo để thay đổi pitch
                if pitch_ratio != 1.0:
                    new_rate = int(44100 * pitch_ratio)
                    filters.append(f"asetrate={new_rate}")
                    filters.append(f"atempo={1/pitch_ratio}")
            
            # Tempo change
            if tempo != '1.0':
                filters.append(f"atempo={tempo}")
            
            # Hiệu ứng đặc biệt
            if effect == 'robot':
                # Robot effect với phaser và distortion
                filters.extend([
                    "aphaser=in_gain=0.4",
                    "afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=512:overlap=0.75"
                ])
            elif effect == 'echo':
                filters.append("aecho=0.8:0.9:1000:0.3")
            elif effect == 'reverb':
                filters.append("aecho=0.8:0.88:60:0.4")
            elif effect == 'telephone':
                # Telephone effect với bandpass filter
                filters.extend([
                    "highpass=f=300",
                    "lowpass=f=3000",
                    "volume=1.5"
                ])
            elif effect == 'monster':
                # Monster effect với pitch down và distortion
                filters.extend([
                    "asetrate=22050",
                    "atempo=2.0",
                    "volume=1.2"
                ])
            
            # Nếu không có filter nào, chỉ copy
            if not filters:
                filter_string = "acopy"
            else:
                filter_string = ",".join(filters)
            
            cmd = [
                self.ffmpeg_path,
                "-i", input_file,
                "-af", filter_string,
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                "-ac", "2",
                "-y",
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Lỗi FFmpeg: {result.stderr}")
                return False
            
            return os.path.exists(output_file)
            
        except Exception as e:
            print(f"❌ Lỗi FFmpeg processing: {e}")
            return False
    
    def create_robot_voice(self, input_file, output_file):
        """Tạo giọng robot chuyên dụng"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", input_file,
                "-af", "aphaser=in_gain=0.4:out_gain=0.74:delay=3:decay=0.4:speed=0.5:type=t",
                "-y",
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0 and os.path.exists(output_file)
            
        except Exception as e:
            print(f"❌ Lỗi tạo robot voice: {e}")
            return False
    
    def create_chipmunk_voice(self, input_file, output_file):
        """Tạo giọng chipmunk"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", input_file,
                "-af", "asetrate=44100*1.5,atempo=1/1.5,atempo=1.3",
                "-y",
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0 and os.path.exists(output_file)
            
        except Exception as e:
            print(f"❌ Lỗi tạo chipmunk voice: {e}")
            return False
    
    def create_deep_voice(self, input_file, output_file):
        """Tạo giọng trầm/sâu"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", input_file,
                "-af", "asetrate=44100*0.8,atempo=1/0.8,atempo=0.9",
                "-y",
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0 and os.path.exists(output_file)
            
        except Exception as e:
            print(f"❌ Lỗi tạo deep voice: {e}")
            return False
    
    def add_echo_effect(self, input_file, output_file, delay=1000, decay=0.3):
        """Thêm hiệu ứng echo"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", input_file,
                "-af", f"aecho=0.8:0.9:{delay}:{decay}",
                "-y",
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0 and os.path.exists(output_file)
            
        except Exception as e:
            print(f"❌ Lỗi thêm echo: {e}")
            return False
    
    def add_reverb_effect(self, input_file, output_file):
        """Thêm hiệu ứng reverb"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", input_file,
                "-af", "aecho=0.8:0.88:60:0.4,aecho=0.8:0.88:120:0.3",
                "-y",
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0 and os.path.exists(output_file)
            
        except Exception as e:
            print(f"❌ Lỗi thêm reverb: {e}")
            return False
    
    def gender_swap(self, input_file, output_file, direction="male_to_female"):
        """Chuyển đổi giới tính giọng nói"""
        try:
            if direction == "male_to_female":
                # Nam -> Nữ: tăng pitch, tăng formant
                filter_str = "asetrate=44100*1.3,atempo=1/1.3,atempo=1.1"
            else:
                # Nữ -> Nam: giảm pitch, giảm formant  
                filter_str = "asetrate=44100*0.8,atempo=1/0.8,atempo=0.9"
            
            cmd = [
                self.ffmpeg_path,
                "-i", input_file,
                "-af", filter_str,
                "-y",
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0 and os.path.exists(output_file)
            
        except Exception as e:
            print(f"❌ Lỗi gender swap: {e}")
            return False
    
    def apply_distortion(self, input_file, output_file, gain=20):
        """Áp dụng hiệu ứng méo tiếng"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", input_file,
                "-af", f"volume={gain}dB,alimiter=level_in=1:level_out=0.8:limit=0.7",
                "-y",
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0 and os.path.exists(output_file)
            
        except Exception as e:
            print(f"❌ Lỗi distortion: {e}")
            return False
    
    def apply_chorus(self, input_file, output_file):
        """Áp dụng hiệu ứng chorus"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", input_file,
                "-af", "chorus=0.5:0.9:50|60|40:0.4|0.32|0.3:0.25|0.4|0.3:2|2.3|1.3",
                "-y",
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0 and os.path.exists(output_file)
            
        except Exception as e:
            print(f"❌ Lỗi chorus: {e}")
            return False
    
    def create_whisper_voice(self, input_file, output_file):
        """Tạo giọng thì thầm"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", input_file,
                "-af", "volume=0.3,highpass=f=200,lowpass=f=8000",
                "-y",
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0 and os.path.exists(output_file)
            
        except Exception as e:
            print(f"❌ Lỗi whisper voice: {e}")
            return False
    
    def create_vintage_radio(self, input_file, output_file):
        """Tạo hiệu ứng radio cổ"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", input_file,
                "-af", "highpass=f=500,lowpass=f=2000,volume=1.2,aecho=0.8:0.88:40:0.2",
                "-y",
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0 and os.path.exists(output_file)
            
        except Exception as e:
            print(f"❌ Lỗi vintage radio: {e}")
            return False