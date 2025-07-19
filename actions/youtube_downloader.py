#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube Downloader Action
Download video từ YouTube và tự động tạo content cho TikTok
"""

import os
import re
import json
import tempfile
from datetime import datetime
from .base_action import BaseAction
from .content_generator import TikTokContentGenerator


class YouTubeDownloaderAction(BaseAction):
    """Action để download video từ YouTube và tạo TikTok content"""
    
    def __init__(self):
        super().__init__()
        self.content_generator = TikTokContentGenerator()
        
        # Supported video qualities
        self.quality_options = {
            "1": {"name": "720p (Recommended)", "format": "best[height<=720]"},
            "2": {"name": "1080p (High Quality)", "format": "best[height<=1080]"},
            "3": {"name": "480p (Fast Download)", "format": "best[height<=480]"},
            "4": {"name": "Best Available", "format": "best"},
            "5": {"name": "Audio Only (MP3)", "format": "bestaudio"}
        }
    
    def check_dependencies(self):
        """Kiểm tra các dependencies cần thiết"""
        try:
            import yt_dlp
            return True
        except ImportError:
            print("❌ Thiếu thư viện yt-dlp!")
            print("📋 Cài đặt bằng lệnh: pip install yt-dlp")
            return False
    
    def extract_video_id(self, url):
        """Extract video ID từ YouTube URL"""
        patterns = [
            r'[?&]v=([^&\n?#]+)',  # ?v= hoặc &v=
            r'youtu\.be/([^&\n?#]+)',  # youtu.be/VIDEO_ID
            r'youtube\.com/embed/([^&\n?#]+)',  # embed/VIDEO_ID
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                print(f"🎯 Extracted video ID: {video_id}")
                return video_id
        
        return None
    
    def clean_video_url(self, url):
        """Clean URL để chỉ lấy video, bỏ playlist parameters"""
        video_id = self.extract_video_id(url)
        
        if video_id:
            # Tạo clean URL chỉ có video ID
            clean_url = f"https://www.youtube.com/watch?v={video_id}"
            print(f"🧹 Clean URL: {clean_url}")
            return clean_url
        
        return url
    
    def validate_youtube_url(self, url):
        """Validate YouTube URL và phát hiện playlist"""
        youtube_patterns = [
            r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)',
            r'(https?://)?(www\.)?youtube\.com/.*[?&]v=',
            r'(https?://)?(www\.)?youtu\.be/'
        ]
        
        # Kiểm tra playlist URL
        playlist_patterns = [
            r'(https?://)?(www\.)?youtube\.com/playlist\?list=',
        ]
        
        # Kiểm tra nếu là playlist URL thuần túy (không có video ID)
        for pattern in playlist_patterns:
            if re.search(pattern, url) and 'v=' not in url:
                print("⚠️ Phát hiện Playlist URL thuần túy!")
                print("💡 Chức năng này chỉ hỗ trợ single video")
                print("🔗 Vui lòng sử dụng URL của 1 video cụ thể")
                print("📋 Ví dụ: https://www.youtube.com/watch?v=VIDEO_ID")
                return False
        
        # Kiểm tra video URL hợp lệ
        for pattern in youtube_patterns:
            if re.search(pattern, url):
                return True
        
        return False
    
    def get_video_info(self, url):
        """Lấy thông tin video từ YouTube URL với logging chi tiết"""
        try:
            import yt_dlp
            
            print("🔍 Đang kết nối đến YouTube...")
            print("📡 Đang gửi request...")
            
            # Clean URL trước khi xử lý
            original_url = url
            clean_url = self.clean_video_url(url)
            
            if clean_url != original_url:
                print("🧹 Đã clean URL (loại bỏ playlist parameters)")
                print(f"   Original: {original_url}")
                print(f"   Clean: {clean_url}")
                url = clean_url
            
            # Extract video ID để verify
            video_id = self.extract_video_id(url)
            if video_id:
                print(f"🎯 Video ID: {video_id}")
            else:
                print("⚠️ Không extract được video ID")
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,  # Đảm bảo extract full info
                'noplaylist': True,     # QUAN TRỌNG: Chỉ lấy video, không lấy playlist
            }
            
            print("⏳ Đang chờ phản hồi từ server...")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("🔄 Đang extract metadata cho video cụ thể...")
                info = ydl.extract_info(url, download=False)
                
                # Debug: In type của response
                response_type = info.get('_type', 'video')
                print(f"🔍 Response type: {response_type}")
                
                # Kiểm tra nếu vẫn là playlist
                if response_type == 'playlist':
                    print("❌ Vẫn nhận được playlist thay vì video!")
                    print("🔄 Thử force extract video...")
                    
                    # Thử lần nữa với video ID trực tiếp
                    if video_id:
                        video_url = f"https://www.youtube.com/watch?v={video_id}"
                        info = ydl.extract_info(video_url, download=False)
                        response_type = info.get('_type', 'video')
                        print(f"🔄 Retry response type: {response_type}")
                    
                    if response_type == 'playlist':
                        print("❌ Không thể lấy thông tin video cụ thể")
                        return None
                
                print("✅ Nhận được dữ liệu video từ YouTube")
                print("🔍 Đang parse thông tin video...")
                
                # Parse từng thông tin với validation tốt hơn
                title = info.get('title', '').strip()
                if not title:
                    # Thử lấy từ các field khác
                    title = info.get('fulltitle', '') or info.get('display_title', '') or 'Unknown Title'
                
                print(f"   📝 Title: {title}")
                
                duration = info.get('duration', 0)
                if duration and duration > 0:
                    duration_str = f"{duration//60}:{duration%60:02d}"
                    print(f"   ⏱️ Duration: {duration_str} ({duration} giây)")
                else:
                    print("   ⚠️ Duration không có hoặc = 0")
                    duration = 0
                
                uploader = info.get('uploader', '') or info.get('channel', '') or 'Unknown Channel'
                print(f"   👤 Channel: {uploader}")
                
                upload_date = info.get('upload_date', '')
                if upload_date and len(upload_date) == 8:
                    formatted_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
                    print(f"   📅 Upload date: {formatted_date}")
                else:
                    print(f"   📅 Upload date: {upload_date or 'Unknown'}")
                
                view_count = info.get('view_count', 0) or 0
                print(f"   👀 Views: {view_count:,}")
                
                description = info.get('description', '') or ''
                desc_length = len(description)
                print(f"   📝 Description: {desc_length} characters")
                if desc_length > 0:
                    # Preview description
                    desc_preview = description[:100].replace('\n', ' ') + '...' if len(description) > 100 else description
                    print(f"       Preview: {desc_preview}")
                
                tags = info.get('tags', []) or []
                print(f"   🏷️ Tags: {len(tags)} tags")
                if tags:
                    print(f"       Preview: {', '.join(tags[:5])}{'...' if len(tags) > 5 else ''}")
                
                thumbnail = info.get('thumbnail', '')
                print(f"   🖼️ Thumbnail: {'Available' if thumbnail else 'N/A'}")
                
                # Verify video ID
                extracted_id = info.get('id', '') or video_id
                print(f"   🆔 Confirmed Video ID: {extracted_id}")
                
                # Tạo video_info object
                video_info = {
                    'title': title,
                    'duration': duration,
                    'uploader': uploader,
                    'upload_date': upload_date,
                    'view_count': view_count,
                    'description': description,
                    'tags': tags,
                    'thumbnail': thumbnail,
                    'webpage_url': f"https://www.youtube.com/watch?v={extracted_id}",
                    'video_id': extracted_id
                }
                
                print("✅ Hoàn thành parse thông tin video")
                print(f"📊 Dữ liệu hợp lệ: {len([k for k, v in video_info.items() if v])} trường")
                
                # Validation cuối cùng
                if not title or title == 'Unknown Title':
                    print("❌ Title không hợp lệ")
                    return None
                
                if duration == 0:
                    print("⚠️ Duration = 0, có thể có vấn đề với video")
                    # Vẫn tiếp tục nhưng cảnh báo
                
                return video_info
                
        except Exception as e:
            print(f"❌ Lỗi lấy thông tin video: {e}")
            print("🔍 Kiểm tra:")
            print("   - URL có đúng format không?")
            print("   - Video có public không?")
            print("   - Video có bị age-restricted không?")
            print("   - Kết nối internet ổn định không?")
            import traceback
            print(f"🔍 Chi tiết lỗi: {traceback.format_exc()}")
            return None
    
    def show_quality_menu(self):
        """Hiển thị menu chọn chất lượng"""
        print("\n📺 CHỌN CHẤT LƯỢNG VIDEO:")
        print("-" * 40)
        for key, option in self.quality_options.items():
            print(f"{key}. {option['name']}")
        print("0. ← Quay lại")
        print("-" * 40)
    
    def get_quality_choice(self):
        """Lấy lựa chọn chất lượng từ user"""
        while True:
            choice = input("👉 Chọn chất lượng (0-5): ").strip()
            if choice == "0":
                return None
            elif choice in self.quality_options:
                return choice
            else:
                print("❌ Lựa chọn không hợp lệ! Vui lòng chọn từ 0-5.")
    
    def download_video(self, url, output_folder, quality_format, video_info):
        """Download video từ YouTube với progress logging chi tiết"""
        try:
            import yt_dlp
            
            # Sử dụng clean URL cho download
            clean_url = self.clean_video_url(url)
            
            # Tạo tên file an toàn
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', video_info['title'])
            safe_title = safe_title[:100]  # Giới hạn độ dài
            
            print("\n" + "="*60)
            print("🚀 BẮT ĐẦU QUÁ TRÌNH DOWNLOAD")
            print("="*60)
            print(f"📺 Video: {video_info['title']}")
            print(f"👤 Kênh: {video_info['uploader']}")
            print(f"⏱️ Thời lượng: {video_info['duration']} giây")
            print(f"👀 Lượt xem: {video_info['view_count']:,}")
            print(f"🎯 Chất lượng: {quality_format}")
            print(f"📁 Đích: {output_folder}")
            print(f"🔗 URL: {clean_url}")  # Show clean URL
            print("-"*60)
            
            # Progress hook function
            def progress_hook(d):
                if d['status'] == 'downloading':
                    if 'total_bytes' in d and d['total_bytes']:
                        percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                        speed = d.get('speed', 0)
                        eta = d.get('eta', 0)
                        
                        # Format speed
                        if speed:
                            if speed > 1024*1024:
                                speed_str = f"{speed/(1024*1024):.1f}MB/s"
                            elif speed > 1024:
                                speed_str = f"{speed/1024:.1f}KB/s"
                            else:
                                speed_str = f"{speed:.0f}B/s"
                        else:
                            speed_str = "N/A"
                        
                        # Format ETA
                        if eta:
                            eta_min = eta // 60
                            eta_sec = eta % 60
                            eta_str = f"{eta_min}:{eta_sec:02d}"
                        else:
                            eta_str = "N/A"
                        
                        # Progress bar
                        bar_length = 30
                        filled_length = int(bar_length * percent / 100)
                        bar = '█' * filled_length + '░' * (bar_length - filled_length)
                        
                        print(f"\r📥 Download: [{bar}] {percent:.1f}% | {speed_str} | ETA: {eta_str}", end='', flush=True)
                    
                    elif 'total_bytes_estimate' in d and d['total_bytes_estimate']:
                        percent = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
                        print(f"\r📥 Download: {percent:.1f}% (ước tính)", end='', flush=True)
                    else:
                        # Không có thông tin tổng size
                        downloaded_mb = d['downloaded_bytes'] / (1024*1024)
                        print(f"\r📥 Download: {downloaded_mb:.1f}MB", end='', flush=True)
                
                elif d['status'] == 'finished':
                    print(f"\n✅ Download hoàn thành: {os.path.basename(d['filename'])}")
                    print(f"📊 Kích thước file: {os.path.getsize(d['filename'])/(1024*1024):.1f}MB")
            
            # Thiết lập yt-dlp options với clean URL
            ydl_opts = {
                'format': quality_format,
                'outtmpl': os.path.join(output_folder, f"{safe_title}.%(ext)s"),
                'writeinfojson': True,  # Lưu metadata
                'writesubtitles': True,  # Download subtitles nếu có
                'writeautomaticsub': True,  # Download auto-generated subtitles
                'subtitleslangs': ['vi', 'en'],  # Vietnamese và English subtitles
                'ignoreerrors': True,
                'progress_hooks': [progress_hook],  # Progress tracking
                'noplaylist': True,  # QUAN TRỌNG: Chỉ download video, không download playlist
            }
            
            print("🔍 Đang phân tích video và chuẩn bị download...")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("📡 Kết nối đến YouTube...")
                print("🎯 Tìm thấy video, bắt đầu download...")
                ydl.download([clean_url])  # Sử dụng clean URL
            
            print()  # New line sau progress bar
            print("🔍 Đang tìm file đã download...")
            
            # Tìm file đã download
            downloaded_files = []
            for file in os.listdir(output_folder):
                if file.startswith(safe_title) and not file.endswith('.json') and not file.endswith('.vtt'):
                    downloaded_files.append(os.path.join(output_folder, file))
            
            if downloaded_files:
                video_file = downloaded_files[0]  # Lấy file đầu tiên
                file_size = os.path.getsize(video_file) / (1024*1024)
                print(f"✅ Tìm thấy file video: {os.path.basename(video_file)}")
                print(f"📊 Kích thước: {file_size:.1f}MB")
                print(f"📁 Đường dẫn: {video_file}")
                
                # Kiểm tra subtitle files
                subtitle_files = [f for f in os.listdir(output_folder) 
                                if f.startswith(safe_title) and (f.endswith('.vtt') or f.endswith('.srt'))]
                if subtitle_files:
                    print(f"📝 Tìm thấy {len(subtitle_files)} subtitle file(s)")
                    for sub_file in subtitle_files:
                        print(f"   └── {sub_file}")
                
                return video_file
            else:
                print("❌ Không tìm thấy file video đã download")
                return None
                
        except Exception as e:
            print(f"\n❌ Lỗi download video: {e}")
            import traceback
            print(f"🔍 Chi tiết lỗi: {traceback.format_exc()}")
            return None
    
    def process_youtube_url(self, url, output_folder, quality_choice):
        """Xử lý toàn bộ quy trình download và tạo content với logging chi tiết"""
        try:
            print("\n" + "="*70)
            print("🎬 YOUTUBE TO TIKTOK PROCESSOR")
            print("="*70)
            
            # Lấy thông tin video
            print("🔍 GIAI ĐOẠN 1: PHÂN TÍCH VIDEO")
            print("-"*40)
            print("📡 Đang kết nối đến YouTube...")
            print("🔍 Đang lấy thông tin video...")
            
            video_info = self.get_video_info(url)
            
            if not video_info:
                print("❌ Không thể lấy thông tin video")
                return False
            
            print("✅ Lấy thông tin thành công!")
            print("📋 Thông tin video đã thu thập:")
            
            # Hiển thị thông tin video với logging chi tiết
            print(f"   🎬 Tiêu đề: {video_info['title']}")
            print(f"   👤 Kênh: {video_info['uploader']}")
            print(f"   ⏱️ Thời lượng: {video_info['duration']} giây ({video_info['duration']//60}:{video_info['duration']%60:02d})")
            print(f"   👀 Lượt xem: {video_info['view_count']:,}")
            print(f"   📅 Ngày tải lên: {video_info.get('upload_date', 'N/A')}")
            print(f"   🏷️ Tags: {len(video_info.get('tags', []))} tags")
            print(f"   📝 Mô tả: {len(video_info.get('description', ''))} ký tự")
            print(f"   🔗 URL: {video_info['webpage_url']}")
            
            # Xác nhận download
            print("\n" + "-"*40)
            confirm = input("❓ Tiếp tục download và tạo TikTok content? (y/n): ").strip().lower()
            if confirm != 'y':
                print("🚫 Đã hủy thao tác")
                return False
            
            # Download video
            print("\n🔍 GIAI ĐOẠN 2: DOWNLOAD VIDEO")
            print("-"*40)
            quality_format = self.quality_options[quality_choice]['format']
            quality_name = self.quality_options[quality_choice]['name']
            print(f"🎯 Chế độ download: {quality_name}")
            
            video_file = self.download_video(url, output_folder, quality_format, video_info)
            
            if not video_file:
                print("❌ Download thất bại")
                return False
            
            # Tạo TikTok content
            print("\n🔍 GIAI ĐOẠN 3: TẠO TIKTOK CONTENT")
            print("-"*40)
            print("🤖 Khởi động content generator...")
            print("📊 Đang phân tích nội dung video...")
            
            content_success = self.content_generator.generate_tiktok_content(
                video_info, video_file, output_folder
            )
            
            if content_success:
                print("\n" + "="*70)
                print("🎉 HOÀN THÀNH THÀNH CÔNG!")
                print("="*70)
                print("✅ Video đã được download")
                print("✅ TikTok content đã được tạo")
                print(f"📁 Tất cả files đã lưu trong: {output_folder}")
                print("💡 Bạn có thể sử dụng content để đăng TikTok ngay!")
            else:
                print("\n⚠️ Video download thành công nhưng có lỗi tạo content TikTok")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Lỗi xử lý: {e}")
            import traceback
            print(f"🔍 Chi tiết lỗi: {traceback.format_exc()}")
            return False
    
    def execute(self, input_folder, output_folder):
        """Thực thi chức năng YouTube downloader với complete logging"""
        print("\n" + "="*80)
        print("🎬 YOUTUBE TO TIKTOK CONTENT GENERATOR")
        print("📺 VideoForge Professional Video Processing Suite")
        print("="*80)
        
        # Kiểm tra dependencies
        print("\n🔍 BƯỚC 1: KIỂM TRA HỆ THỐNG")
        print("-"*50)
        print("🔧 Đang kiểm tra dependencies...")
        
        if not self.check_dependencies():
            print("❌ System check thất bại!")
            print("\n💡 HƯỚNG DẪN CÀI ĐẶT:")
            print("pip install yt-dlp")
            print("pip install openai-whisper")
            print("\n🔄 Sau khi cài đặt, hãy chạy lại chức năng này")
            input("Nhấn Enter để tiếp tục...")
            return
        
        print("✅ yt-dlp library đã sẵn sàng")
        print("✅ System requirements OK")
        
        # Kiểm tra thư mục output
        print("\n🔍 BƯỚC 2: KIỂM TRA THƯ MỤC")
        print("-"*50)
        print("📁 Đang kiểm tra thư mục output...")
        
        if not output_folder:
            print("❌ Thư mục output chưa được thiết lập!")
            print("💡 Vui lòng chọn menu '10. ⚙️ Thay đổi thư mục Input/Output' trước")
            input("Nhấn Enter để tiếp tục...")
            return
        
        print(f"✅ Thư mục output: {output_folder}")
        
        if not os.path.exists(output_folder):
            try:
                print("📁 Thư mục chưa tồn tại, đang tạo...")
                os.makedirs(output_folder)
                print(f"✅ Đã tạo thư mục: {output_folder}")
            except Exception as e:
                print(f"❌ Không thể tạo thư mục output: {e}")
                input("Nhấn Enter để tiếp tục...")
                return
        else:
            print("✅ Thư mục output đã tồn tại")
        
        # Kiểm tra quyền ghi
        print("🔐 Đang kiểm tra quyền ghi file...")
        try:
            test_file = os.path.join(output_folder, "test_write.tmp")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            print("✅ Quyền ghi file OK")
        except Exception as e:
            print(f"❌ Không có quyền ghi vào thư mục: {e}")
            input("Nhấn Enter để tiếp tục...")
            return
        
        # Main loop
        session_count = 0
        success_count = 0
        
        print(f"\n🎯 HỆ THỐNG SẴN SÀNG!")
        print(f"📁 Files sẽ được lưu vào: {output_folder}")
        print("-"*80)
        
        while True:
            session_count += 1
            
            print(f"\n🎬 SESSION #{session_count}")
            print("="*60)
            print(f"📊 Thống kê: {success_count} video đã xử lý thành công")
            print(f"📁 Thư mục lưu: {output_folder}")
            print("-"*60)
            
            # Nhập YouTube URL
            url = input("🔗 Nhập URL YouTube (hoặc 'q' để thoát): ").strip()
            
            if url.lower() == 'q':
                break
            
            if not url:
                print("⚠️ URL trống, vui lòng nhập lại")
                continue
            
            print(f"\n🔍 BƯỚC 3: VALIDATE URL")
            print("-"*40)
            print(f"🔗 URL nhận được: {url}")
            print("🔍 Đang kiểm tra format URL...")
            
            # Validate URL
            if not self.validate_youtube_url(url):
                print("❌ URL không hợp lệ!")
                print("💡 Định dạng hỗ trợ:")
                print("   - https://www.youtube.com/watch?v=VIDEO_ID")
                print("   - https://youtu.be/VIDEO_ID")
                print("   - youtube.com/watch?v=VIDEO_ID")
                continue
            
            print("✅ URL format hợp lệ")
            print("✅ Đã xác nhận là YouTube URL")
            
            # Hiển thị menu chất lượng
            print(f"\n🔍 BƯỚC 4: CHỌN CHẤT LƯỢNG")
            print("-"*40)
            self.show_quality_menu()
            quality_choice = self.get_quality_choice()
            
            if quality_choice is None:
                print("🚫 Đã hủy chọn chất lượng")
                continue
            
            quality_name = self.quality_options[quality_choice]['name']
            print(f"✅ Đã chọn: {quality_name}")
            
            # Bắt đầu processing
            print(f"\n🚀 BƯỚC 5: BẮT ĐẦU XỬ LÝ")
            print("-"*40)
            print(f"⏰ Thời gian bắt đầu: {datetime.now().strftime('%H:%M:%S')}")
            
            # Xử lý download và tạo content
            start_time = datetime.now()
            success = self.process_youtube_url(url, output_folder, quality_choice)
            end_time = datetime.now()
            
            processing_time = (end_time - start_time).total_seconds()
            
            if success:
                success_count += 1
                print(f"\n🎉 SESSION #{session_count} HOÀN THÀNH!")
                print("="*60)
                print(f"✅ Thời gian xử lý: {processing_time:.1f} giây")
                print(f"✅ Video và content đã được tạo thành công")
                print(f"📁 Location: {output_folder}")
                
                # List files được tạo
                print(f"\n📋 FILES TẠO TRONG SESSION #{session_count}:")
                recent_files = []
                for file in os.listdir(output_folder):
                    file_path = os.path.join(output_folder, file)
                    file_time = os.path.getctime(file_path)
                    if datetime.fromtimestamp(file_time) >= start_time:
                        recent_files.append(file)
                
                for file in sorted(recent_files):
                    file_path = os.path.join(output_folder, file)
                    file_size = os.path.getsize(file_path)
                    if file_size > 1024*1024:
                        size_str = f"{file_size/(1024*1024):.1f}MB"
                    elif file_size > 1024:
                        size_str = f"{file_size/1024:.1f}KB"
                    else:
                        size_str = f"{file_size}B"
                    
                    if file.endswith('.mp4') or file.endswith('.mkv') or file.endswith('.webm'):
                        print(f"   🎬 {file} ({size_str})")
                    elif file.endswith('.txt'):
                        print(f"   📄 {file} ({size_str})")
                    elif file.endswith('.json'):
                        print(f"   📊 {file} ({size_str})")
                    else:
                        print(f"   📁 {file} ({size_str})")
                
                # Hỏi có muốn download thêm không
                another = input(f"\n❓ Download video khác? (y/n): ").strip().lower()
                if another != 'y':
                    break
            else:
                print(f"\n❌ SESSION #{session_count} THẤT BẠI!")
                print("="*60)
                print(f"⏱️ Thời gian thử: {processing_time:.1f} giây")
                print("💡 Gợi ý khắc phục:")
                print("   - Kiểm tra kết nối internet")
                print("   - Thử URL khác")
                print("   - Chọn chất lượng thấp hơn")
                print("   - Kiểm tra video có bị private không")
                
                retry = input("\n❓ Thử lại với URL khác? (y/n): ").strip().lower()
                if retry != 'y':
                    break
        
        # Session summary
        print(f"\n📊 TỔNG KẾT SESSION")
        print("="*80)
        print(f"🎬 Tổng số video đã xử lý: {success_count}/{session_count}")
        if success_count > 0:
            success_rate = (success_count / session_count) * 100
            print(f"📈 Tỷ lệ thành công: {success_rate:.1f}%")
            print(f"📁 Tất cả files đã lưu trong: {output_folder}")
            print(f"💡 Bạn có {success_count} TikTok content sẵn sàng sử dụng!")
        
        print(f"⏰ Kết thúc session: {datetime.now().strftime('%H:%M:%S')}")
        print("\n👋 Cảm ơn bạn đã sử dụng YouTube Downloader!")
        print("🎉 Chúc bạn viral trên TikTok!")
        input("Nhấn Enter để quay về menu chính...")