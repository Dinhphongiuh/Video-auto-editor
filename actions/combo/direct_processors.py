#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct Processors
Chỉ xử lý những actions có vấn đề với CLI (như speed_adjuster)
"""

import subprocess


class DirectProcessors:
    """Class xử lý trực tiếp với FFmpeg cho những action có vấn đề CLI"""
    
    def process_action(self, action_name, input_file, output_file, config):
        """Router cho các action processors - chỉ cho những action cần thiết"""
        if action_name == "speed_adjuster":
            return self._direct_speed_adjust(input_file, output_file, config)
        else:
            print(f"❌ Direct processor không hỗ trợ {action_name}")
            return False
    
    def _direct_speed_adjust(self, input_file, output_file, config):
        """Xử lý speed adjustment trực tiếp với FFmpeg"""
        try:
            speed = config.get('speed', 1.0)
            print(f"⚡ Đang thay đổi tốc độ thành {speed}x (Direct FFmpeg)...")
            
            cmd = [
                'ffmpeg',
                '-i', input_file,
                '-filter:v', f'setpts={1/speed}*PTS',
                '-filter:a', f'atempo={speed}',
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-y',
                output_file
            ]
            
            print(f"🚀 FFmpeg command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Speed adjustment thành công")
                return True
            else:
                print(f"❌ FFmpeg error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Lỗi speed adjustment: {e}")
            return False