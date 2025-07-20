#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Combo Processor Action - Main Controller
Gắn kết nhiều chức năng xử lý video theo thứ tự - Modular approach
"""

import os
import tempfile
from ..base_action import BaseAction
from ..format_converter import VideoFormatConverter
from ..compressor import VideoCompressor
from ..speed_adjuster import VideoSpeedAdjuster
from ..resolution_changer import VideoResolutionChanger
from ..filter_applier import VideoFilterApplier
from ..voice_changer import VoiceChangerAction
from ..video_trimmer import VideoTrimmerAction

from .function_selector import FunctionSelector
from .config_manager import ConfigManager
from .pipeline_executor import PipelineExecutor


class ComboProcessorAction(BaseAction):
    """Action để xử lý video qua nhiều chức năng kết hợp - Modular architecture"""
    
    def __init__(self):
        super().__init__()
        
        # Khởi tạo các action instances
        self.actions = {
            "format_converter": VideoFormatConverter(),
            "compressor": VideoCompressor(),
            "speed_adjuster": VideoSpeedAdjuster(), 
            "resolution_changer": VideoResolutionChanger(),
            "filter_applier": VideoFilterApplier(),
            "voice_changer": VoiceChangerAction(),
            "video_trimmer": VideoTrimmerAction()
        }
        
        # Khởi tạo các module components
        self.function_selector = FunctionSelector()
        self.config_manager = ConfigManager()
        self.pipeline_executor = PipelineExecutor(self.actions)
    
    def select_functions(self):
        """Main function để chọn các chức năng"""
        print("🎯 === COMBO PROCESSOR - KẾT HỢP CÁC CHỨC NĂNG ===")
        print("💡 Chọn nhiều chức năng để xử lý video theo thứ tự")
        
        while True:
            # Hiển thị chức năng đã chọn
            self.function_selector.show_selected_functions()
            
            # Hiển thị chức năng có thể chọn
            if not self.function_selector.show_available_functions():
                break
            
            # Lấy lựa chọn
            choice = self.function_selector.get_function_choice()
            
            if choice == "done":
                if self.function_selector.has_selected_functions():
                    break
                else:
                    print("❌ Phải chọn ít nhất 1 chức năng!")
                    continue
            elif choice == "cancel":
                self.function_selector.clear_selected_functions()
                return False
            else:
                # Cấu hình chức năng
                func_config = self.config_manager.configure_function(choice, self.function_selector.available_functions)
                if func_config:
                    self.function_selector.add_selected_function(func_config)
                    print(f"✅ Đã thêm: {self.function_selector.available_functions[choice]['name']}")
        
        return self.function_selector.has_selected_functions()
    
    def execute(self, input_folder, output_folder):
        """Thực thi combo processing"""
        print("\n🎯 === COMBO PROCESSOR ===")
        
        # Kiểm tra thư mục
        if not self.validate_folders(input_folder, output_folder):
            return
        
        # Chọn các chức năng
        if not self.select_functions():
            print("🚫 Đã hủy combo processing")
            input("Nhấn Enter để tiếp tục...")
            return
        
        # Lấy danh sách video
        video_files = self.get_video_files(input_folder)
        if not video_files:
            print(f"❌ Không tìm thấy file video nào trong: {input_folder}")
            input("Nhấn Enter để tiếp tục...")
            return
        
        selected_functions = self.function_selector.get_selected_functions()
        
        # Hiển thị tổng quan
        print(f"\n📊 TỔNG QUAN COMBO PROCESSING:")
        print(f"🎬 Số video: {len(video_files)}")
        print(f"🔧 Số chức năng: {len(selected_functions)}")
        print(f"📁 Thư mục output: {output_folder}")
        
        print(f"\n📋 CÁC BƯỚC XỬ LÝ:")
        for i, func_config in enumerate(selected_functions, 1):
            func_info = self.function_selector.available_functions[func_config['key']]
            print(f"  {i}. {func_info['name']} - {func_config['config_summary']}")
        
        # Xác nhận
        confirm = input(f"\n❓ Bắt đầu xử lý {len(video_files)} video qua {len(selected_functions)} bước? (y/n): ").strip().lower()
        if confirm != 'y':
            print("🚫 Đã hủy thao tác")
            input("Nhấn Enter để tiếp tục...")
            return
        
        # Xử lý từng video
        success_count = 0
        total_count = len(video_files)
        
        print(f"\n🚀 BẮT ĐẦU COMBO PROCESSING...")
        print("=" * 80)
        
        with tempfile.TemporaryDirectory() as temp_folder:
            print(f"📂 Sử dụng temp folder: {temp_folder}")
            
            for i, video_file in enumerate(video_files, 1):
                print(f"\n🎥 [{i}/{total_count}] Video: {os.path.basename(video_file)}")
                
                success = self.pipeline_executor.process_single_video(
                    video_file, 
                    selected_functions, 
                    self.function_selector.available_functions,
                    temp_folder, 
                    output_folder
                )
                
                if success:
                    success_count += 1
                    print(f"✅ Video {i} hoàn thành")
                else:
                    print(f"❌ Video {i} thất bại")
                
                print("-" * 60)
        
        # Kết quả
        print(f"\n🎊 KẾT QUẢ COMBO PROCESSING:")
        print(f"✅ Thành công: {success_count}/{total_count}")
        print(f"❌ Thất bại: {total_count - success_count}/{total_count}")
        print(f"📁 Thư mục output: {output_folder}")
        
        if success_count > 0:
            print(f"🎉 Đã xử lý thành công {success_count} video qua {len(selected_functions)} bước!")
            print("💡 Tất cả video đã được xử lý theo combo và lưu với suffix '_combo_processed'")
        
        input("\nNhấn Enter để tiếp tục...")