#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Function Selector
Quản lý việc chọn và hiển thị các chức năng combo
"""


class FunctionSelector:
    """Class để chọn và quản lý các chức năng combo"""
    
    def __init__(self):
        # Danh sách các chức năng có thể combo
        self.available_functions = {
            "1": {
                "name": "📹 Chuyển đổi định dạng",
                "action": "format_converter",
                "description": "Thay đổi format video (MP4, AVI, MOV...)"
            },
            "2": {
                "name": "🗜️ Nén video",
                "action": "compressor", 
                "description": "Giảm dung lượng file video"
            },
            "3": {
                "name": "⚡ Tăng/giảm tốc độ",
                "action": "speed_adjuster",
                "description": "Thay đổi tốc độ phát video"
            },
            "4": {
                "name": "📐 Thay đổi độ phân giải",
                "action": "resolution_changer", 
                "description": "Resize video resolution"
            },
            "5": {
                "name": "🎨 Áp dụng bộ lọc",
                "action": "filter_applier",
                "description": "Thêm hiệu ứng màu sắc"
            },
            "6": {
                "name": "🎤 Thay đổi giọng nói",
                "action": "voice_changer",
                "description": "Biến đổi âm thanh giọng nói"
            },
            "7": {
                "name": "✂️ Cắt video",
                "action": "video_trimmer",
                "description": "Cắt đầu/cuối video"
            }
        }
        
        self.selected_functions = []
    
    def show_available_functions(self):
        """Hiển thị danh sách chức năng có thể chọn"""
        print("\n🎯 CHỌN CÁC CHỨC NĂNG XỬ LÝ:")
        print("-" * 60)
        
        available_keys = [k for k in self.available_functions.keys() 
                         if k not in [item['key'] for item in self.selected_functions]]
        
        if not available_keys:
            print("❌ Không còn chức năng nào để chọn!")
            return False
        
        for key in available_keys:
            func = self.available_functions[key]
            print(f"{key}. {func['name']} - {func['description']}")
        
        print("0. ✅ Hoàn thành chọn chức năng")
        print("9. 🚫 Hủy và quay lại")
        print("-" * 60)
        return True
    
    def show_selected_functions(self):
        """Hiển thị danh sách chức năng đã chọn"""
        if not self.selected_functions:
            return
        
        print(f"\n📋 ĐÃ CHỌN ({len(self.selected_functions)} chức năng):")
        print("-" * 40)
        for i, func in enumerate(self.selected_functions, 1):
            func_info = self.available_functions[func['key']]
            print(f"  {i}. {func_info['name']}")
            if 'config_summary' in func:
                print(f"     └── {func['config_summary']}")
        print("-" * 40)
    
    def get_function_choice(self):
        """Lấy lựa chọn chức năng từ user"""
        while True:
            choice = input("👉 Chọn chức năng (0-9): ").strip()
            
            if choice == "0":
                return "done"
            elif choice == "9":
                return "cancel"
            elif choice in self.available_functions:
                # Kiểm tra đã chọn chưa
                if choice in [item['key'] for item in self.selected_functions]:
                    print("❌ Chức năng này đã được chọn!")
                    continue
                return choice
            else:
                print("❌ Lựa chọn không hợp lệ!")
    
    def add_selected_function(self, func_config):
        """Thêm chức năng đã được configure"""
        self.selected_functions.append(func_config)
    
    def clear_selected_functions(self):
        """Xóa tất cả chức năng đã chọn"""
        self.selected_functions = []
    
    def has_selected_functions(self):
        """Kiểm tra có chức năng nào được chọn không"""
        return len(self.selected_functions) > 0
    
    def get_selected_functions(self):
        """Lấy danh sách các chức năng đã chọn"""
        return self.selected_functions