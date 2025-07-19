#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audio Processor
Xử lý audio cho voice changer
"""

import os
import subprocess
import tempfile


class AudioProcessor:
    """Lớp xử lý audio cơ bản"""
    
    def __init__(self):
        self.ffmpeg_path = "ffmpeg"  # Có thể thay đổi path nếu cần
    
    def check_ffmpeg(self):
        """Kiểm tra FFmpeg có sẵn không"""
        try:
            result = subprocess.run([self.ffmpeg_path, "-version"], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def extract_audio(self, video_file, audio_output):
        """Trích xuất audio từ video"""
        try:
            if not self.check_ffmpeg():
                print("❌ FFmpeg không được tìm thấy! Vui lòng cài đặt FFmpeg.")
                return False
            
            cmd = [
                self.ffmpeg_path,
                "-i", video_file,
                "-vn",  # Không copy video
                "-acodec", "pcm_s16le",  # Audio codec
                "-ar", "44100",  # Sample rate
                "-ac", "2",  # Stereo
                "-y",  # Overwrite output
                audio_output
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Lỗi FFmpeg: {result.stderr}")
                return False
            
            return os.path.exists(audio_output)
            
        except Exception as e:
            print(f"❌ Lỗi trích xuất audio: {e}")
            return False
    
    def combine_audio_video(self, video_file, audio_file, output_file):
        """Kết hợp audio mới với video gốc"""
        try:
            if not self.check_ffmpeg():
                print("❌ FFmpeg không được tìm thấy!")
                return False
            
            cmd = [
                self.ffmpeg_path,
                "-i", video_file,  # Video gốc
                "-i", audio_file,  # Audio đã xử lý
                "-c:v", "copy",    # Copy video stream
                "-c:a", "aac",     # Encode audio as AAC
                "-map", "0:v:0",   # Map video từ input đầu tiên
                "-map", "1:a:0",   # Map audio từ input thứ hai
                "-shortest",       # Dừng khi stream ngắn nhất kết thúc
                "-y",              # Overwrite output
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Lỗi FFmpeg: {result.stderr}")
                return False
            
            return os.path.exists(output_file)
            
        except Exception as e:
            print(f"❌ Lỗi kết hợp audio-video: {e}")
            return False
    
    def get_audio_info(self, audio_file):
        """Lấy thông tin audio file"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", audio_file,
                "-f", "null",
                "-"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Parse thông tin từ stderr
            info = {
                "duration": "Unknown",
                "bitrate": "Unknown", 
                "sample_rate": "Unknown",
                "channels": "Unknown"
            }
            
            if result.stderr:
                lines = result.stderr.split('\n')
                for line in lines:
                    if "Duration:" in line:
                        parts = line.split(',')
                        for part in parts:
                            if "Duration:" in part:
                                info["duration"] = part.split("Duration:")[1].strip()
                            elif "bitrate:" in part:
                                info["bitrate"] = part.split("bitrate:")[1].strip()
                    elif "Audio:" in line:
                        # Parse sample rate và channels
                        if "Hz" in line:
                            hz_part = line.split("Hz")[0].split()[-1]
                            info["sample_rate"] = f"{hz_part} Hz"
                        if "stereo" in line:
                            info["channels"] = "2 (stereo)"
                        elif "mono" in line:
                            info["channels"] = "1 (mono)"
            
            return info
            
        except Exception as e:
            print(f"❌ Lỗi lấy thông tin audio: {e}")
            return None
    
    def normalize_audio(self, input_file, output_file, target_db=-23):
        """Chuẩn hóa âm lượng audio"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", input_file,
                "-af", f"loudnorm=I={target_db}:LRA=11:TP=-1.5",
                "-y",
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Lỗi normalize: {result.stderr}")
                return False
            
            return os.path.exists(output_file)
            
        except Exception as e:
            print(f"❌ Lỗi chuẩn hóa audio: {e}")
            return False
    
    def convert_audio_format(self, input_file, output_file, format="wav"):
        """Chuyển đổi định dạng audio"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", input_file,
                "-acodec", "pcm_s16le" if format == "wav" else "mp3",
                "-ar", "44100",
                "-ac", "2",
                "-y",
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Lỗi convert: {result.stderr}")
                return False
            
            return os.path.exists(output_file)
            
        except Exception as e:
            print(f"❌ Lỗi chuyển đổi định dạng: {e}")
            return False
    
    def apply_audio_filter(self, input_file, output_file, filter_string):
        """Áp dụng filter audio tùy chỉnh"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", input_file,
                "-af", filter_string,
                "-y",
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Lỗi apply filter: {result.stderr}")
                return False
            
            return os.path.exists(output_file)
            
        except Exception as e:
            print(f"❌ Lỗi áp dụng filter: {e}")
            return False
    
    def adjust_volume(self, input_file, output_file, volume_factor=1.0):
        """Điều chỉnh âm lượng"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", input_file,
                "-af", f"volume={volume_factor}",
                "-y",
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Lỗi adjust volume: {result.stderr}")
                return False
            
            return os.path.exists(output_file)
            
        except Exception as e:
            print(f"❌ Lỗi điều chỉnh âm lượng: {e}")
            return False