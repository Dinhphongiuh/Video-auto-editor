#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Folder Manager Action
Xử lý quản lý thư mục input và output với tính năng lưu trữ settings
"""

import os
import json
import glob
from datetime import datetime
from pathlib import Path
from .base_action import BaseAction


class FolderManagerAction(BaseAction):
    """Xử lý quản lý thư mục input và output với persistent settings"""

    def __init__(self):
        super().__init__()
        self.settings_file = "folder_settings.json"
        self.input_folder = ""
        self.output_folder = ""
        self.recent_folders = {"input": [], "output": []}
        self.last_used = None

        # Load settings từ file nếu có
        self.load_settings()

    def execute(self):
        """Thiết lập thư mục input và output với enhanced features"""
        print("\n🔧 THIẾT LẬP THỦ MỤC - Enhanced Version")
        print("-" * 50)

        # Hiển thị settings hiện tại nếu có
        self._show_current_settings()

        # Menu lựa chọn
        print("\n📋 LỰA CHỌN:")
        print("1. Thiết lập thư mục Input")
        print("2. Thiết lập thư mục Output")
        print("3. Thiết lập cả hai thư mục")
        print("4. Xem lịch sử thư mục gần đây")
        print("5. Xóa settings hiện tại")
        print("6. Xuất/Nhập settings")
        print("0. Quay lại")

        choice = input("\n👉 Nhập lựa chọn: ").strip()

        if choice == "1":
            self._set_input_folder()
        elif choice == "2":
            self._set_output_folder()
        elif choice == "3":
            self._set_input_folder()
            if self.input_folder:  # Chỉ thiết lập output nếu input thành công
                self._set_output_folder()
        elif choice == "4":
            self._show_recent_folders()
        elif choice == "5":
            self._clear_settings()
        elif choice == "6":
            self._settings_management()
        elif choice == "0":
            return
        else:
            print("❌ Lựa chọn không hợp lệ!")

        # Lưu settings sau khi thay đổi
        self.save_settings()

        print("\n✅ Hoàn thành thiết lập thư mục!")
        input("Nhấn Enter để tiếp tục...")

    def load_settings(self):
        """Load settings từ file JSON"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                self.input_folder = data.get("input_folder", "")
                self.output_folder = data.get("output_folder", "")
                self.recent_folders = data.get(
                    "recent_folders", {"input": [], "output": []}
                )
                self.last_used = data.get("last_used", None)

                # Validate các thư mục có tồn tại không
                if self.input_folder and not os.path.exists(self.input_folder):
                    print(f"⚠️  Thư mục input đã lưu không tồn tại: {self.input_folder}")
                    self.input_folder = ""

                if self.output_folder and not os.path.exists(self.output_folder):
                    print(
                        f"⚠️  Thư mục output đã lưu không tồn tại: {self.output_folder}"
                    )
                    self.output_folder = ""

                if self.input_folder and self.output_folder:
                    print(
                        f"✅ Đã load settings: Input={self.input_folder}, Output={self.output_folder}"
                    )

        except Exception as e:
            print(f"⚠️  Lỗi khi load settings: {e}")
            self._reset_settings()

    def save_settings(self):
        """Lưu settings vào file JSON"""
        try:
            data = {
                "input_folder": self.input_folder,
                "output_folder": self.output_folder,
                "recent_folders": self.recent_folders,
                "last_used": datetime.now().isoformat(),
                "version": "1.0",
                "created_by": "VideoForge Enhanced Folder Manager",
            }

            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"💾 Đã lưu settings vào {self.settings_file}")

        except Exception as e:
            print(f"❌ Lỗi khi lưu settings: {e}")

    def get_folders(self):
        """Lấy thông tin thư mục hiện tại"""
        return {"input": self.input_folder, "output": self.output_folder}

    def _show_current_settings(self):
        """Hiển thị settings hiện tại"""
        if self.input_folder or self.output_folder:
            print("\n📊 SETTINGS HIỆN TẠI:")
            print(f"📥 Input : {self.input_folder or 'Chưa thiết lập'}")
            print(f"📤 Output: {self.output_folder or 'Chưa thiết lập'}")

            if self.last_used:
                try:
                    last_used_dt = datetime.fromisoformat(self.last_used)
                    print(f"🕒 Lần cuối: {last_used_dt.strftime('%d/%m/%Y %H:%M:%S')}")
                except:
                    print(f"🕒 Lần cuối: {self.last_used}")

            # Hiển thị thống kê nhanh
            if self.input_folder and os.path.exists(self.input_folder):
                video_count = len(self.get_video_files(self.input_folder))
                print(f"📹 Video trong input: {video_count} files")
        else:
            print("\n📊 Chưa có settings nào được lưu trữ")

    def _set_input_folder(self):
        """Thiết lập thư mục input với enhanced features"""
        print(f"\n📥 THIẾT LẬP THƯ MỤC INPUT")
        print("-" * 30)

        # Hiển thị recent folders nếu có
        recent_inputs = self.recent_folders.get("input", [])
        if recent_inputs:
            print("📚 Thư mục gần đây:")
            for i, folder in enumerate(recent_inputs[:5], 1):
                exists = "✅" if os.path.exists(folder) else "❌"
                print(f"   {i}. {exists} {folder}")
            print("   0. Nhập thư mục mới")

            choice = input("👉 Chọn thư mục (0 để nhập mới): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(recent_inputs[:5]):
                selected_folder = recent_inputs[int(choice) - 1]
                if os.path.exists(selected_folder):
                    self.input_folder = selected_folder
                    self._add_to_recent("input", selected_folder)
                    print(f"✅ Đã chọn thư mục: {selected_folder}")
                    return
                else:
                    print("❌ Thư mục không tồn tại, vui lòng nhập thư mục mới")

        while True:
            current = f" (hiện tại: {self.input_folder})" if self.input_folder else ""
            input_path = (
                input(f"📥 Nhập đường dẫn thư mục input{current}: ").strip().strip('"')
            )

            if not input_path and self.input_folder:
                print(f"🔄 Giữ nguyên thư mục hiện tại: {self.input_folder}")
                break

            if not input_path:
                print("❌ Vui lòng nhập đường dẫn!")
                continue

            # Expand path tương đối và home directory
            input_path = os.path.expanduser(input_path)
            input_path = os.path.abspath(input_path)

            if not os.path.exists(input_path):
                print("❌ Thư mục không tồn tại!")
                create = input("Bạn có muốn tạo thư mục này không? (y/n): ").lower()
                if create == "y":
                    try:
                        os.makedirs(input_path, exist_ok=True)
                        print(f"✅ Đã tạo thư mục: {input_path}")
                    except Exception as e:
                        print(f"❌ Không thể tạo thư mục: {e}")
                        continue
                else:
                    retry = input("Bạn có muốn thử lại không? (y/n): ").lower()
                    if retry != "y":
                        break
                    continue

            # Kiểm tra và hiển thị video files
            video_files = self.get_video_files(input_path)
            if not video_files:
                print("⚠️  Không tìm thấy file video nào trong thư mục!")
                print("Các định dạng được hỗ trợ: MP4, AVI, MOV, WMV, FLV, MKV, WEBM")
                choice = input("Bạn có muốn tiếp tục không? (y/n): ").lower()
                if choice != "y":
                    continue
            else:
                print(f"✅ Tìm thấy {len(video_files)} file video:")
                self._show_video_preview(video_files)

            self.input_folder = input_path
            self._add_to_recent("input", input_path)
            print(f"✅ Đã thiết lập thư mục input: {input_path}")
            break

    def _set_output_folder(self):
        """Thiết lập thư mục output với enhanced features"""
        print(f"\n📤 THIẾT LẬP THƯ MỤC OUTPUT")
        print("-" * 30)

        # Hiển thị recent folders nếu có
        recent_outputs = self.recent_folders.get("output", [])
        if recent_outputs:
            print("📚 Thư mục gần đây:")
            for i, folder in enumerate(recent_outputs[:5], 1):
                exists = "✅" if os.path.exists(folder) else "❌"
                print(f"   {i}. {exists} {folder}")
            print("   0. Nhập thư mục mới")

            choice = input("👉 Chọn thư mục (0 để nhập mới): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(recent_outputs[:5]):
                selected_folder = recent_outputs[int(choice) - 1]
                if os.path.exists(selected_folder) or self._create_output_folder(
                    selected_folder
                ):
                    self.output_folder = selected_folder
                    self._add_to_recent("output", selected_folder)
                    print(f"✅ Đã chọn thư mục: {selected_folder}")
                    return

        while True:
            current = f" (hiện tại: {self.output_folder})" if self.output_folder else ""
            output_path = (
                input(f"📤 Nhập đường dẫn thư mục output{current}: ").strip().strip('"')
            )

            if not output_path and self.output_folder:
                print(f"🔄 Giữ nguyên thư mục hiện tại: {self.output_folder}")
                break

            if not output_path:
                print("❌ Vui lòng nhập đường dẫn!")
                continue

            # Expand path
            output_path = os.path.expanduser(output_path)
            output_path = os.path.abspath(output_path)

            if self._create_output_folder(output_path):
                self.output_folder = output_path
                self._add_to_recent("output", output_path)
                print(f"✅ Đã thiết lập thư mục output: {output_path}")
                break
            else:
                retry = input("Bạn có muốn thử lại không? (y/n): ").lower()
                if retry != "y":
                    break

    def _create_output_folder(self, output_path):
        """Tạo và validate thư mục output"""
        try:
            # Tạo thư mục nếu chưa tồn tại
            os.makedirs(output_path, exist_ok=True)

            # Kiểm tra quyền ghi
            test_file = os.path.join(output_path, ".test_write")
            try:
                with open(test_file, "w") as f:
                    f.write("test")
                os.remove(test_file)

                # Hiển thị thông tin thư mục
                self._show_output_folder_info(output_path)
                return True

            except PermissionError:
                print("❌ Không có quyền ghi vào thư mục này!")
                return False

        except Exception as e:
            print(f"❌ Không thể tạo thư mục: {e}")
            return False

    def _show_video_preview(self, video_files, max_display=10):
        """Hiển thị preview danh sách video"""
        display_count = min(len(video_files), max_display)
        total_size = 0

        for i, video_file in enumerate(video_files[:display_count], 1):
            filename = os.path.basename(video_file)
            try:
                file_size = os.path.getsize(video_file) / (1024 * 1024)  # MB
                total_size += file_size
                print(f"   {i}. {filename} ({file_size:.2f} MB)")
            except:
                print(f"   {i}. {filename} (? MB)")

        if len(video_files) > max_display:
            print(f"   ... và {len(video_files) - max_display} file khác")

        print(f"💾 Tổng dung lượng: {total_size:.2f} MB")

    def _show_output_folder_info(self, output_path):
        """Hiển thị thông tin chi tiết về thư mục output"""
        try:
            # Kiểm tra không gian trống
            if hasattr(os, "statvfs"):  # Unix/Linux
                statvfs = os.statvfs(output_path)
                free_space = statvfs.f_frsize * statvfs.f_bavail / (1024**3)  # GB
            else:  # Windows
                import shutil

                total, used, free = shutil.disk_usage(output_path)
                free_space = free / (1024**3)  # GB

            print(f"💾 Không gian trống: {free_space:.2f} GB")

            # Kiểm tra file existing
            existing_files = self.get_video_files(output_path)

            if existing_files:
                print(f"📁 Thư mục đã có {len(existing_files)} file video")
                print("📋 Preview file có sẵn:")
                self._show_video_preview(existing_files, 5)

                choice = input("⚠️  File cũ có thể bị ghi đè. Tiếp tục? (y/n): ").lower()
                if choice != "y":
                    print("❌ Đã hủy thiết lập thư mục output")
                    return False

        except Exception as e:
            print(f"⚠️  Không thể kiểm tra thông tin thư mục: {e}")

        return True

    def _add_to_recent(self, folder_type, path):
        """Thêm thư mục vào danh sách recent"""
        if folder_type not in self.recent_folders:
            self.recent_folders[folder_type] = []

        # Remove if already exists
        if path in self.recent_folders[folder_type]:
            self.recent_folders[folder_type].remove(path)

        # Add to beginning
        self.recent_folders[folder_type].insert(0, path)

        # Keep only last 10
        self.recent_folders[folder_type] = self.recent_folders[folder_type][:10]

    def _show_recent_folders(self):
        """Hiển thị lịch sử thư mục gần đây"""
        print("\n📚 LỊCH SỬ THƯ MỤC GẦN ĐÂY")
        print("-" * 40)

        print("📥 INPUT FOLDERS:")
        recent_inputs = self.recent_folders.get("input", [])
        if recent_inputs:
            for i, folder in enumerate(recent_inputs, 1):
                exists = "✅" if os.path.exists(folder) else "❌"
                print(f"   {i}. {exists} {folder}")
        else:
            print("   Chưa có lịch sử")

        print("\n📤 OUTPUT FOLDERS:")
        recent_outputs = self.recent_folders.get("output", [])
        if recent_outputs:
            for i, folder in enumerate(recent_outputs, 1):
                exists = "✅" if os.path.exists(folder) else "❌"
                print(f"   {i}. {exists} {folder}")
        else:
            print("   Chưa có lịch sử")

        input("\nNhấn Enter để tiếp tục...")

    def _clear_settings(self):
        """Xóa tất cả settings"""
        print("\n🗑️  XÓA SETTINGS")
        print("-" * 20)

        print("⚠️  Thao tác này sẽ xóa:")
        print("   • Thư mục input và output hiện tại")
        print("   • Lịch sử thư mục gần đây")
        print("   • File settings.json")

        confirm = input("\nBạn có chắc chắn muốn xóa? (yes/no): ").lower()
        if confirm == "yes":
            self._reset_settings()

            # Xóa file settings
            try:
                if os.path.exists(self.settings_file):
                    os.remove(self.settings_file)
                    print(f"🗑️  Đã xóa file {self.settings_file}")
            except Exception as e:
                print(f"❌ Lỗi khi xóa file settings: {e}")

            print("✅ Đã xóa tất cả settings!")
        else:
            print("❌ Đã hủy thao tác xóa")

    def _settings_management(self):
        """Quản lý import/export settings"""
        print("\n📁 QUẢN LÝ SETTINGS")
        print("-" * 25)
        print("1. Xuất settings ra file")
        print("2. Nhập settings từ file")
        print("3. Xem thông tin settings file")
        print("0. Quay lại")

        choice = input("👉 Chọn tùy chọn: ").strip()

        if choice == "1":
            self._export_settings()
        elif choice == "2":
            self._import_settings()
        elif choice == "3":
            self._show_settings_info()
        elif choice == "0":
            return
        else:
            print("❌ Lựa chọn không hợp lệ!")

    def _export_settings(self):
        """Xuất settings ra file backup"""
        try:
            backup_name = f"folder_settings_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            with open(backup_name, "w", encoding="utf-8") as f:
                data = {
                    "input_folder": self.input_folder,
                    "output_folder": self.output_folder,
                    "recent_folders": self.recent_folders,
                    "exported_at": datetime.now().isoformat(),
                    "version": "1.0",
                }
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"✅ Đã xuất settings ra file: {backup_name}")

        except Exception as e:
            print(f"❌ Lỗi khi xuất settings: {e}")

    def _import_settings(self):
        """Nhập settings từ file backup"""
        backup_file = input("📥 Nhập tên file backup: ").strip()

        if not os.path.exists(backup_file):
            print("❌ File không tồn tại!")
            return

        try:
            with open(backup_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Backup current settings
            current_backup = {
                "input_folder": self.input_folder,
                "output_folder": self.output_folder,
                "recent_folders": self.recent_folders,
            }

            # Import new settings
            self.input_folder = data.get("input_folder", "")
            self.output_folder = data.get("output_folder", "")
            self.recent_folders = data.get(
                "recent_folders", {"input": [], "output": []}
            )

            # Validate imported paths
            if self.input_folder and not os.path.exists(self.input_folder):
                print(f"⚠️  Thư mục input không tồn tại: {self.input_folder}")

            if self.output_folder and not os.path.exists(self.output_folder):
                print(f"⚠️  Thư mục output không tồn tại: {self.output_folder}")

            print("✅ Đã import settings thành công!")
            print("💾 Settings cũ đã được backup trong memory")

        except Exception as e:
            print(f"❌ Lỗi khi import settings: {e}")

    def _show_settings_info(self):
        """Hiển thị thông tin chi tiết về settings file"""
        print(f"\n📄 THÔNG TIN SETTINGS FILE")
        print("-" * 35)

        if os.path.exists(self.settings_file):
            try:
                # File info
                file_size = os.path.getsize(self.settings_file)
                file_mtime = os.path.getmtime(self.settings_file)
                mtime_str = datetime.fromtimestamp(file_mtime).strftime(
                    "%d/%m/%Y %H:%M:%S"
                )

                print(f"📁 File: {self.settings_file}")
                print(f"📊 Size: {file_size} bytes")
                print(f"🕒 Modified: {mtime_str}")

                # Content preview
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                print(f"\n📋 NỘI DUNG:")
                print(f"   Input folder: {data.get('input_folder', 'N/A')}")
                print(f"   Output folder: {data.get('output_folder', 'N/A')}")
                print(
                    f"   Recent input: {len(data.get('recent_folders', {}).get('input', []))} items"
                )
                print(
                    f"   Recent output: {len(data.get('recent_folders', {}).get('output', []))} items"
                )
                print(f"   Last used: {data.get('last_used', 'N/A')}")
                print(f"   Version: {data.get('version', 'N/A')}")

            except Exception as e:
                print(f"❌ Lỗi khi đọc file: {e}")
        else:
            print(f"❌ File {self.settings_file} không tồn tại")
            print("💡 File sẽ được tạo tự động khi bạn lưu settings")

    def _reset_settings(self):
        """Reset tất cả settings về mặc định"""
        self.input_folder = ""
        self.output_folder = ""
        self.recent_folders = {"input": [], "output": []}
        self.last_used = None

    def validate_setup(self):
        """Kiểm tra xem thư mục đã được thiết lập chưa"""
        if not self.input_folder or not self.output_folder:
            print("❌ Vui lòng thiết lập thư mục input và output trước!")
            print("   Chọn menu '11. Thay đổi thư mục Input/Output' để thiết lập.")
            return False

        if not os.path.exists(self.input_folder):
            print(f"❌ Thư mục input không tồn tại: {self.input_folder}")
            print("   Vui lòng thiết lập lại thư mục input.")
            return False

        if not os.path.exists(self.output_folder):
            print(f"❌ Thư mục output không tồn tại: {self.output_folder}")
            print("   Vui lòng thiết lập lại thư mục output.")
            return False

        return True

    def get_input_videos(self):
        """Lấy danh sách video trong thư mục input"""
        if not self.input_folder:
            return []
        return self.get_video_files(self.input_folder)

    def get_stats(self):
        """Lấy thống kê chi tiết về thư mục"""
        stats = {
            "input_folder": self.input_folder,
            "output_folder": self.output_folder,
            "input_videos": 0,
            "input_size_mb": 0,
            "output_videos": 0,
            "output_size_mb": 0,
            "recent_input_count": len(self.recent_folders.get("input", [])),
            "recent_output_count": len(self.recent_folders.get("output", [])),
            "settings_file_exists": os.path.exists(self.settings_file),
            "last_used": self.last_used,
        }

        try:
            # Thống kê input
            if self.input_folder and os.path.exists(self.input_folder):
                input_videos = self.get_video_files(self.input_folder)
                stats["input_videos"] = len(input_videos)

                total_size = 0
                for video in input_videos:
                    if os.path.exists(video):
                        total_size += os.path.getsize(video)
                stats["input_size_mb"] = total_size / (1024 * 1024)

            # Thống kê output
            if self.output_folder and os.path.exists(self.output_folder):
                output_videos = self.get_video_files(self.output_folder)
                stats["output_videos"] = len(output_videos)

                total_size = 0
                for video in output_videos:
                    if os.path.exists(video):
                        total_size += os.path.getsize(video)
                stats["output_size_mb"] = total_size / (1024 * 1024)

        except Exception as e:
            print(f"⚠️  Lỗi khi tính thống kê: {e}")

        return stats

    def quick_setup(self, input_path=None, output_path=None):
        """Quick setup cho automation hoặc command line usage"""
        success = True

        if input_path:
            input_path = os.path.expanduser(os.path.abspath(input_path))
            if os.path.exists(input_path):
                self.input_folder = input_path
                self._add_to_recent("input", input_path)
                print(f"✅ Quick setup input: {input_path}")
            else:
                print(f"❌ Input path không tồn tại: {input_path}")
                success = False

        if output_path:
            output_path = os.path.expanduser(os.path.abspath(output_path))
            try:
                os.makedirs(output_path, exist_ok=True)
                self.output_folder = output_path
                self._add_to_recent("output", output_path)
                print(f"✅ Quick setup output: {output_path}")
            except Exception as e:
                print(f"❌ Không thể tạo output path: {e}")
                success = False

        if success:
            self.save_settings()

        return success

    def auto_detect_folders(self):
        """Tự động detect thư mục input/output từ current directory"""
        current_dir = os.getcwd()

        # Tìm thư mục có chứa video files
        video_dirs = []
        for item in os.listdir(current_dir):
            item_path = os.path.join(current_dir, item)
            if os.path.isdir(item_path):
                videos = self.get_video_files(item_path)
                if videos:
                    video_dirs.append((item_path, len(videos)))

        if video_dirs:
            # Sort by video count
            video_dirs.sort(key=lambda x: x[1], reverse=True)
            suggested_input = video_dirs[0][0]

            print(f"\n🔍 TỰ ĐỘNG PHÁT HIỆN THƯ MỤC")
            print(f"📥 Gợi ý input: {suggested_input} ({video_dirs[0][1]} videos)")

            # Suggest output folder
            suggested_output = os.path.join(current_dir, "output")
            print(f"📤 Gợi ý output: {suggested_output}")

            use_suggested = input("\nSử dụng gợi ý này? (y/n): ").lower()
            if use_suggested == "y":
                return self.quick_setup(suggested_input, suggested_output)

        return False

    def get_folder_summary(self):
        """Lấy summary ngắn gọn về folders"""
        summary = []

        if self.input_folder:
            video_count = (
                len(self.get_video_files(self.input_folder))
                if os.path.exists(self.input_folder)
                else 0
            )
            summary.append(
                f"Input: {os.path.basename(self.input_folder)} ({video_count} videos)"
            )
        else:
            summary.append("Input: Chưa thiết lập")

        if self.output_folder:
            summary.append(f"Output: {os.path.basename(self.output_folder)}")
        else:
            summary.append("Output: Chưa thiết lập")

        return " | ".join(summary)

    def cleanup_recent_folders(self):
        """Dọn dẹp danh sách recent folders - xóa các thư mục không tồn tại"""
        cleaned = False

        for folder_type in ["input", "output"]:
            if folder_type in self.recent_folders:
                original_count = len(self.recent_folders[folder_type])
                self.recent_folders[folder_type] = [
                    folder
                    for folder in self.recent_folders[folder_type]
                    if os.path.exists(folder)
                ]
                new_count = len(self.recent_folders[folder_type])

                if new_count < original_count:
                    removed = original_count - new_count
                    print(f"🧹 Đã xóa {removed} thư mục {folder_type} không tồn tại")
                    cleaned = True

        if cleaned:
            self.save_settings()
            print("✅ Đã dọn dẹp danh sách recent folders")
        else:
            print("✅ Danh sách recent folders đã sạch")

        return cleaned
