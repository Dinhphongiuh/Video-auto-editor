#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline Executor
Thực thi pipeline combo processing - Tái sử dụng các action có sẵn
"""

import os
import shutil
import tempfile
import builtins
from .direct_processors import DirectProcessors


class PipelineExecutor:
    """Class thực thi pipeline xử lý combo"""
    
    def __init__(self, actions):
        self.actions = actions
        self.direct_processors = DirectProcessors()
    
    def process_single_video(self, video_file, selected_functions, available_functions, temp_folder, final_output_folder):
        """Xử lý một video qua tất cả các chức năng đã chọn"""
        try:
            current_file = video_file
            base_name = os.path.splitext(os.path.basename(video_file))[0]
            
            print(f"\n🎬 Đang xử lý: {os.path.basename(video_file)}")
            print("=" * 60)
            
            for i, func_config in enumerate(selected_functions, 1):
                action_name = func_config['action']
                config = func_config['config']
                func_info = available_functions[func_config['key']]
                
                print(f"\n📍 BƯỚC {i}/{len(selected_functions)}: {func_info['name']}")
                print(f"⚙️ Cấu hình: {func_config['config_summary']}")
                print("-" * 40)
                
                # Tạo temp folders cho step này
                step_input_folder = os.path.join(temp_folder, f"step_{i}_input")
                step_output_folder = os.path.join(temp_folder, f"step_{i}_output")
                
                os.makedirs(step_input_folder, exist_ok=True)
                os.makedirs(step_output_folder, exist_ok=True)
                
                # Copy current file vào step input
                step_input_file = os.path.join(step_input_folder, os.path.basename(current_file))
                shutil.copy2(current_file, step_input_file)
                
                # Xử lý với action tương ứng
                success = self._process_with_action(action_name, step_input_folder, step_output_folder, config)
                
                if success:
                    # Tìm output file và set làm current_file cho step tiếp
                    output_files = self._get_video_files(step_output_folder)
                    if output_files:
                        current_file = output_files[0]
                        print(f"✅ Hoàn thành bước {i}")
                    else:
                        print(f"❌ Không tìm thấy output file ở bước {i}")
                        return False
                else:
                    print(f"❌ Lỗi ở bước {i}")
                    return False
            
            # Copy file cuối cùng sang output folder
            final_filename = f"{base_name}_combo_processed.mp4"
            final_output = os.path.join(final_output_folder, final_filename)
            
            print(f"\n📁 Đang lưu kết quả cuối cùng...")
            shutil.copy2(current_file, final_output)
            
            if os.path.exists(final_output):
                file_size = os.path.getsize(final_output) / (1024*1024)
                print(f"✅ Hoàn thành: {final_filename} ({file_size:.1f}MB)")
                return True
            else:
                print("❌ Lỗi lưu file cuối cùng")
                return False
                
        except Exception as e:
            print(f"❌ Lỗi xử lý video: {e}")
            import traceback
            print(f"🔍 Chi tiết: {traceback.format_exc()}")
            return False
    
    def _process_with_action(self, action_name, input_folder, output_folder, config):
        """Xử lý với action cụ thể - Tái sử dụng action gốc khi có thể"""
        try:
            # Sử dụng action gốc cho tất cả actions (trừ speed_adjuster vì có vấn đề CLI)
            if action_name in ["format_converter", "compressor", "resolution_changer", 
                             "filter_applier", "voice_changer", "video_trimmer"]:
                return self._use_original_action(action_name, input_folder, output_folder, config)
            
            # Chỉ dùng direct processor cho speed_adjuster (vì có vấn đề với VideoForge CLI)
            elif action_name == "speed_adjuster":
                return self._use_direct_processor(action_name, input_folder, output_folder, config)
            else:
                print(f"❌ Unsupported action: {action_name}")
                return False
        
        except Exception as e:
            print(f"❌ Lỗi action {action_name}: {e}")
            return False
    
    def _use_original_action(self, action_name, input_folder, output_folder, config):
        """Sử dụng action gốc với mock input"""
        try:
            print(f"🔄 Sử dụng {action_name} action gốc...")
            
            action = self.actions[action_name]
            
            # Backup original input function
            original_input = builtins.input
            
            def create_mock_input(config):
                def mock_input(prompt):
                    prompt_lower = prompt.lower()
                    
                    # Handle different prompts based on action type
                    if action_name == "format_converter":
                        if "format" in prompt_lower or "định dạng" in prompt_lower:
                            choice = config.get('choice', '1')
                            print(f"Auto selected format: {choice}")
                            return choice
                    
                    elif action_name == "compressor":
                        if "quality" in prompt_lower or "chất lượng" in prompt_lower:
                            choice = config.get('choice', '2')
                            print(f"Auto selected quality: {choice}")
                            return choice
                    
                    elif action_name == "resolution_changer":
                        if "resolution" in prompt_lower or "phân giải" in prompt_lower:
                            choice = config.get('choice', '1')
                            print(f"Auto selected resolution: {choice}")
                            return choice
                    
                    elif action_name == "filter_applier":
                        if "filter" in prompt_lower or "lọc" in prompt_lower:
                            choice = config.get('choice', '1')
                            print(f"Auto selected filter: {choice}")
                            return choice
                    
                    elif action_name == "voice_changer":
                        if "voice" in prompt_lower or "giọng" in prompt_lower:
                            choice = config.get('choice', '1')
                            print(f"Auto selected voice: {choice}")
                            return choice
                    
                    elif action_name == "video_trimmer":
                        if "trim" in prompt_lower or "cắt" in prompt_lower:
                            choice = config.get('choice', '1')
                            print(f"Auto selected trim type: {choice}")
                            return choice
                        elif "giây" in prompt_lower or "second" in prompt_lower:
                            seconds = config.get('seconds', 5)
                            print(f"Auto input seconds: {seconds}")
                            return str(seconds)
                    
                    # Default responses
                    if "y/n" in prompt_lower or "yes/no" in prompt_lower:
                        return "y"
                    elif "continue" in prompt_lower or "tiếp tục" in prompt_lower:
                        return ""
                    else:
                        return "y"
                
                return mock_input
            
            # Set mock input
            builtins.input = create_mock_input(config)
            
            try:
                # Execute action
                action.execute(input_folder, output_folder)
                return True
                
            finally:
                # Always restore original input
                builtins.input = original_input
        
        except Exception as e:
            print(f"❌ Lỗi original action {action_name}: {e}")
            # Ensure input is restored even on error
            builtins.input = original_input
            return False
    
    def _use_direct_processor(self, action_name, input_folder, output_folder, config):
        """Sử dụng direct processor cho các action có vấn đề CLI"""
        try:
            # Lấy input file
            input_files = self._get_video_files(input_folder)
            if not input_files:
                print("❌ Không tìm thấy input file")
                return False
            
            input_file = input_files[0]
            
            # Tạo output filename
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_file = os.path.join(output_folder, f"{base_name}_processed.mp4")
            
            # Xử lý với direct processor
            return self.direct_processors.process_action(action_name, input_file, output_file, config)
        
        except Exception as e:
            print(f"❌ Lỗi direct processor {action_name}: {e}")
            return False
    
    def _get_video_files(self, folder_path):
        """Lấy danh sách file video trong thư mục"""
        if not folder_path or not os.path.exists(folder_path):
            return []
        
        video_extensions = ['*.mp4', '*.avi', '*.mov', '*.wmv', '*.flv', '*.mkv', '*.webm']
        video_files = []
        
        import glob
        for ext in video_extensions:
            video_files.extend(glob.glob(os.path.join(folder_path, ext)))
            video_files.extend(glob.glob(os.path.join(folder_path, ext.upper())))
        
        # Loại bỏ duplicate
        video_files = list(set(video_files))
        video_files.sort()
        
        return video_files