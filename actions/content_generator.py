#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikTok Content Generator
Tự động tạo nội dung cho TikTok từ YouTube video
"""

import os
import re
import json
import tempfile
from datetime import datetime


class TikTokContentGenerator:
    """Tạo nội dung TikTok từ YouTube video"""
    
    def __init__(self):
        # Hashtags phổ biến cho TikTok
        self.popular_hashtags = [
            "#fyp", "#foryou", "#viral", "#trending", "#xuhuong",
            "#video", "#funny", "#entertainment", "#tiktok", "#reels"
        ]
        
        # Hashtags theo chủ đề
        self.topic_hashtags = {
            "music": ["#music", "#nhac", "#beat", "#song", "#cover"],
            "dance": ["#dance", "#mua", "#choreography", "#dancer"],
            "comedy": ["#funny", "#hài", "#laugh", "#comedy", "#vui"],
            "food": ["#food", "#cooking", "#recipe", "#ăn", "#nấuăn"],
            "beauty": ["#beauty", "#makeup", "#skincare", "#làmđẹp"],
            "fashion": ["#fashion", "#outfit", "#style", "#thờitrang"],
            "travel": ["#travel", "#dulich", "#explore", "#adventure"],
            "tech": ["#tech", "#technology", "#công_nghệ", "#gadget"],
            "education": ["#learn", "#education", "#học", "#kiến_thức"],
            "gaming": ["#gaming", "#game", "#gamer", "#esports"],
            "sport": ["#sport", "#fitness", "#workout", "#thể_thao"],
            "lifestyle": ["#lifestyle", "#daily", "#life", "#cuộc_sống"]
        }
    
    def extract_keywords_from_title(self, title):
        """Trích xuất keywords từ tiêu đề video"""
        # Loại bỏ ký tự đặc biệt và chuyển thành lowercase
        clean_title = re.sub(r'[^\w\sÀ-ỹ]', ' ', title.lower())
        
        # Tách từ
        words = clean_title.split()
        
        # Loại bỏ stop words tiếng Việt và tiếng Anh
        stop_words = {
            'và', 'của', 'trong', 'với', 'để', 'cho', 'từ', 'về', 'theo',
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'by', 'how', 'what', 'when', 'where', 'why'
        }
        
        keywords = [word for word in words if len(word) > 2 and word not in stop_words]
        
        return keywords[:10]  # Lấy 10 từ khóa đầu tiên
    
    def detect_video_category(self, title, description, tags):
        """Phát hiện thể loại video"""
        content = f"{title} {description}".lower()
        
        # Đếm keyword cho mỗi category
        category_scores = {}
        
        for category, keywords in self.topic_hashtags.items():
            score = 0
            for keyword in keywords:
                clean_keyword = keyword.replace('#', '')
                if clean_keyword in content:
                    score += 2
            
            # Kiểm tra trong tags YouTube
            for tag in tags:
                if any(keyword.replace('#', '') in tag.lower() for keyword in keywords):
                    score += 1
            
            category_scores[category] = score
        
        # Trả về category có điểm cao nhất
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            if category_scores[best_category] > 0:
                return best_category
        
        return "entertainment"  # Default category
    
    def generate_tiktok_title(self, youtube_title, category):
        """Tạo tiêu đề TikTok từ tiêu đề YouTube"""
        # Rút gọn tiêu đề nếu quá dài
        if len(youtube_title) > 80:
            # Cắt ngắn và thêm "..."
            short_title = youtube_title[:77] + "..."
        else:
            short_title = youtube_title
        
        # Thêm prefix thu hút dựa trên category
        category_prefixes = {
            "music": ["🎵 ", "🎶 ", "Nhạc hay: "],
            "dance": ["💃 ", "🕺 ", "Vũ điệu: "],
            "comedy": ["😂 ", "🤣 ", "Hài hước: "],
            "food": ["🍔 ", "👨‍🍳 ", "Món ngon: "],
            "beauty": ["💄 ", "✨ ", "Làm đẹp: "],
            "fashion": ["👗 ", "💅 ", "Thời trang: "],
            "travel": ["✈️ ", "🌍 ", "Du lịch: "],
            "tech": ["📱 ", "💻 ", "Công nghệ: "],
            "education": ["📚 ", "🧠 ", "Học hỏi: "],
            "gaming": ["🎮 ", "🕹️ ", "Gaming: "],
            "sport": ["⚽ ", "🏃‍♂️ ", "Thể thao: "],
            "lifestyle": ["🌟 ", "💫 ", "Cuộc sống: "]
        }
        
        prefixes = category_prefixes.get(category, ["🔥 ", "✨ ", ""])
        prefix = prefixes[0] if prefixes else ""
        
        return f"{prefix}{short_title}"
    
    def generate_hashtags(self, video_info, category, keywords):
        """Tạo hashtags cho TikTok"""
        hashtags = []
        
        # Thêm hashtags phổ biến (2-3 cái)
        hashtags.extend(self.popular_hashtags[:3])
        
        # Thêm hashtags theo category (3-4 cái)
        category_tags = self.topic_hashtags.get(category, [])
        hashtags.extend(category_tags[:4])
        
        # Tạo hashtags từ keywords (3-5 cái)
        for keyword in keywords[:5]:
            if len(keyword) > 2:
                hashtag = f"#{keyword.replace(' ', '')}"
                if hashtag not in hashtags:
                    hashtags.append(hashtag)
        
        # Thêm hashtags từ YouTube tags (2-3 cái)
        youtube_tags = video_info.get('tags', [])
        for tag in youtube_tags[:3]:
            clean_tag = re.sub(r'[^\w]', '', tag.lower())
            if len(clean_tag) > 2:
                hashtag = f"#{clean_tag}"
                if hashtag not in hashtags and len(hashtags) < 15:
                    hashtags.append(hashtag)
        
        # Thêm hashtag về channel (nếu nổi tiếng)
        channel = video_info.get('uploader', '')
        if channel and len(channel) < 20:
            clean_channel = re.sub(r'[^\w]', '', channel.lower())
            if clean_channel:
                hashtags.append(f"#{clean_channel}")
        
        # Giới hạn số lượng hashtags (TikTok recommend không quá 20)
        return hashtags[:18]
    
    def generate_description(self, video_info, tiktok_title, hashtags):
        """Tạo mô tả cho TikTok"""
        youtube_desc = video_info.get('description', '')
        
        # Lấy câu đầu tiên của description YouTube (nếu có)
        first_sentence = ""
        if youtube_desc:
            sentences = youtube_desc.split('.')
            if sentences:
                first_sentence = sentences[0].strip()
                if len(first_sentence) > 100:
                    first_sentence = first_sentence[:97] + "..."
        
        # Tạo description structure
        description_parts = []
        
        # Title
        description_parts.append(tiktok_title)
        
        # Thêm mô tả ngắn nếu có
        if first_sentence and len(first_sentence) > 10:
            description_parts.append(f"\n{first_sentence}")
        
        # Call to action
        cta_options = [
            "\n👀 Xem đầy đủ trên YouTube!",
            "\n💝 Like nếu bạn thích!",
            "\n🔔 Follow để xem thêm!",
            "\n💬 Comment ý kiến của bạn!"
        ]
        description_parts.append(cta_options[0])
        
        # Hashtags
        hashtag_text = " ".join(hashtags)
        description_parts.append(f"\n\n{hashtag_text}")
        
        return "".join(description_parts)
    
    def _estimate_engagement(self, category, hashtag_count):
        """Ước tính mức độ engagement dựa trên category và hashtags"""
        base_scores = {
            "music": 85,
            "dance": 90,
            "comedy": 88,
            "food": 82,
            "beauty": 80,
            "fashion": 78,
            "travel": 75,
            "tech": 70,
            "education": 65,
            "gaming": 83,
            "sport": 77,
            "lifestyle": 73
        }
        
        base_score = base_scores.get(category, 70)
        hashtag_bonus = min(hashtag_count * 2, 20)  # Max 20 points from hashtags
        
        return min(base_score + hashtag_bonus, 100)
    
    def create_content_file(self, video_info, video_file, output_folder):
        """Tạo file txt chứa content TikTok với logging chi tiết"""
        try:
            print("🔍 Bắt đầu phân tích và tạo content...")
            
            # Phân tích video
            print("📊 Đang trích xuất keywords từ tiêu đề...")
            keywords = self.extract_keywords_from_title(video_info['title'])
            print(f"   ✅ Tìm thấy {len(keywords)} keywords: {', '.join(keywords)}")
            
            print("🎯 Đang phát hiện thể loại video...")
            category = self.detect_video_category(
                video_info['title'], 
                video_info.get('description', ''), 
                video_info.get('tags', [])
            )
            print(f"   ✅ Thể loại được phát hiện: {category.title()}")
            
            # Tạo content
            print("🎬 Đang tạo tiêu đề TikTok...")
            tiktok_title = self.generate_tiktok_title(video_info['title'], category)
            print(f"   ✅ Tiêu đề TikTok: {tiktok_title}")
            
            print("🏷️ Đang tạo hashtags...")
            hashtags = self.generate_hashtags(video_info, category, keywords)
            print(f"   ✅ Tạo được {len(hashtags)} hashtags")
            print(f"   📋 Preview: {' '.join(hashtags[:8])}{'...' if len(hashtags) > 8 else ''}")
            
            print("📝 Đang tạo mô tả đầy đủ...")
            description = self.generate_description(video_info, tiktok_title, hashtags)
            print(f"   ✅ Mô tả: {len(description)} ký tự")
            
            # Tạo tên file
            print("📁 Đang chuẩn bị file output...")
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', video_info['title'])
            safe_title = safe_title[:50]  # Giới hạn độ dài
            content_filename = f"{safe_title}_TikTok_Content.txt"
            content_path = os.path.join(output_folder, content_filename)
            print(f"   📄 Tên file: {content_filename}")
            
            # Tạo nội dung file với logging chi tiết
            print("✍️ Đang ghi nội dung vào file TXT...")
            
            content_lines = []
            content_lines.append("=====================================")
            content_lines.append("TIKTOK CONTENT GENERATOR")
            content_lines.append("Generated by VideoForge")
            content_lines.append("=====================================")
            print("   ✅ Header section")
            
            content_lines.append("")
            content_lines.append("📹 VIDEO NGUỒN:")
            content_lines.append(f"Tiêu đề: {video_info['title']}")
            content_lines.append(f"Kênh: {video_info['uploader']}")
            content_lines.append(f"Thời lượng: {video_info['duration']} giây")
            content_lines.append(f"Lượt xem: {video_info.get('view_count', 0):,}")
            content_lines.append(f"URL: {video_info['webpage_url']}")
            print("   ✅ Video info section")
            
            content_lines.append("")
            content_lines.append("📱 CONTENT CHO TIKTOK:")
            content_lines.append("=====================================")
            print("   ✅ TikTok content header")
            
            content_lines.append("")
            content_lines.append("🎬 TIÊU ĐỀ TIKTOK:")
            content_lines.append(tiktok_title)
            print("   ✅ TikTok title section")
            
            content_lines.append("")
            content_lines.append("📝 MÔ TẢ ĐẦY ĐỦ:")
            content_lines.append(description)
            print("   ✅ Description section")
            
            content_lines.append("")
            content_lines.append(f"🏷️ HASHTAGS ({len(hashtags)} tags):")
            content_lines.append(' '.join(hashtags))
            print(f"   ✅ Hashtags section ({len(hashtags)} tags)")
            
            content_lines.append("")
            content_lines.append("📊 PHÂN TÍCH:")
            content_lines.append(f"Thể loại: {category.title()}")
            content_lines.append(f"Keywords: {', '.join(keywords)}")
            content_lines.append(f"Ước tính độ dài mô tả: {len(description)} ký tự")
            print("   ✅ Analysis section")
            
            content_lines.append("")
            content_lines.append("💡 GỢI Ý ĐĂNG BÀI:")
            content_lines.append("- Đăng vào khung giờ vàng: 18:00-22:00")
            content_lines.append("- Sử dụng trending sounds nếu có")
            content_lines.append("- Thêm subtitle cho video")
            content_lines.append("- Tương tác với comments trong 1-2 giờ đầu")
            content_lines.append("- Có thể cắt thành nhiều phần nếu video dài")
            print("   ✅ Tips section")
            
            content_lines.append("")
            content_lines.append("=====================================")
            content_lines.append(f"📅 Ngày tạo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            content_lines.append(f"📁 Video file: {os.path.basename(video_file)}")
            content_lines.append("🔧 Tool: VideoForge YouTube Downloader")
            content_lines.append("=====================================")
            print("   ✅ Footer section")
            
            # Ghi file
            print("💾 Đang lưu file TXT...")
            content = "\n".join(content_lines)
            
            with open(content_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            file_size = os.path.getsize(content_path)
            print(f"   ✅ Đã lưu: {content_filename}")
            print(f"   📊 Kích thước: {file_size} bytes")
            print(f"   📝 Tổng dòng: {len(content_lines)} dòng")
            
            # Tạo JSON file cho dữ liệu structured
            print("📄 Đang tạo JSON data file...")
            json_filename = f"{safe_title}_TikTok_Data.json"
            json_path = os.path.join(output_folder, json_filename)
            
            json_data = {
                "youtube_info": video_info,
                "tiktok_content": {
                    "title": tiktok_title,
                    "description": description,
                    "hashtags": hashtags,
                    "category": category,
                    "keywords": keywords
                },
                "analysis": {
                    "total_hashtags": len(hashtags),
                    "total_keywords": len(keywords),
                    "description_length": len(description),
                    "estimated_engagement": self._estimate_engagement(category, len(hashtags))
                },
                "generated_at": datetime.now().isoformat(),
                "video_file": os.path.basename(video_file)
            }
            
            print("   🔗 Đang ghi structured data...")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            
            json_size = os.path.getsize(json_path)
            print(f"   ✅ Đã lưu: {json_filename}")
            print(f"   📊 Kích thước: {json_size} bytes")
            
            # Summary
            print("\n📋 SUMMARY CONTENT FILES:")
            print(f"   📄 {content_filename} - {file_size} bytes")
            print(f"   📊 {json_filename} - {json_size} bytes")
            print(f"   🎯 Category: {category.title()}")
            print(f"   🏷️ Hashtags: {len(hashtags)} tags")
            print(f"   🔤 Keywords: {len(keywords)} từ khóa")
            
            return True
            
        except Exception as e:
            print(f"❌ Lỗi tạo content file: {e}")
            import traceback
            print(f"🔍 Chi tiết lỗi: {traceback.format_exc()}")
            return False
    
    def generate_tiktok_content(self, video_info, video_file, output_folder):
        """Main function để tạo TikTok content với logging chi tiết"""
        try:
            print("🤖 TikTok Content Generator đã khởi động")
            print("📊 Đang chuẩn bị phân tích video...")
            
            # Hiển thị thông tin input
            print(f"📹 Input video: {os.path.basename(video_file)}")
            print(f"📁 Output folder: {output_folder}")
            print(f"🎬 Video title: {video_info['title'][:60]}{'...' if len(video_info['title']) > 60 else ''}")
            
            # Tạo content file
            success = self.create_content_file(video_info, video_file, output_folder)
            
            if success:
                print("\n🎉 CONTENT GENERATION HOÀN THÀNH!")
                print("="*50)
                print("✅ TikTok content đã được tạo thành công")
                print("✅ Files đã sẵn sàng sử dụng")
                print("💡 Bạn có thể copy content để đăng TikTok ngay!")
                
                # List output files
                txt_files = [f for f in os.listdir(output_folder) if f.endswith('_TikTok_Content.txt')]
                json_files = [f for f in os.listdir(output_folder) if f.endswith('_TikTok_Data.json')]
                
                print(f"\n📁 FILES CREATED:")
                for txt_file in txt_files:
                    if video_info['title'][:20] in txt_file:
                        print(f"   📄 {txt_file}")
                for json_file in json_files:
                    if video_info['title'][:20] in json_file:
                        print(f"   📊 {json_file}")
                
                return True
            else:
                print("❌ Content generation thất bại")
                return False
                
        except Exception as e:
            print(f"❌ Lỗi generate TikTok content: {e}")
            import traceback
            print(f"🔍 Chi tiết lỗi: {traceback.format_exc()}")
            return False