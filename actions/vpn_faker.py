#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VPN Faker Action - Tự động tìm và kết nối VPN Mỹ cho TikTok
Tương thích với cấu trúc VideoForge
"""

import os
import sys
import time
import json
import random
import socket
import subprocess
import requests
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Base Action import
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from actions.base_action import BaseAction


class VPNFakerAction(BaseAction):
    """
    Tự động tìm kiếm và kết nối VPN Mỹ cho TikTok
    Features:
    - Tự động tìm IP Mỹ free
    - Kiểm tra chất lượng IP cho TikTok
    - Tự động kết nối hoặc cho user chọn
    """

    def __init__(self):
        super().__init__()
        self.name = "VPN Faker for TikTok"
        self.description = "Tự động tìm và kết nối VPN Mỹ cho TikTok"

        # API endpoints để lấy free proxy
        self.proxy_apis = [
            "https://www.proxy-list.download/api/v1/get?type=https&country=US",
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=US&ssl=yes&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://www.us-proxy.org/api.php?type=txt",
            "https://api.openproxylist.xyz/https.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
        ]

        # TikTok endpoints để test
        self.tiktok_test_urls = [
            "https://www.tiktok.com",
            "https://api.tiktok.com",
            "https://webcast.tiktok.com",
        ]

        # Cache file cho IP đã test
        self.cache_file = "vpn_cache.json"
        self.load_cache()

    def load_cache(self):
        """Load cache IP đã test"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, "r") as f:
                    self.cache = json.load(f)
            else:
                self.cache = {"tested_ips": {}, "last_update": None}
        except:
            self.cache = {"tested_ips": {}, "last_update": None}

    def save_cache(self):
        """Lưu cache"""
        try:
            self.cache["last_update"] = datetime.now().isoformat()
            with open(self.cache_file, "w") as f:
                json.dump(self.cache, f, indent=2)
        except:
            pass

    def fetch_us_proxies(self) -> List[Dict]:
        """Lấy danh sách proxy US từ nhiều nguồn"""
        print("\n🔍 Đang tìm kiếm IP Mỹ free...")
        all_proxies = []

        for api_url in self.proxy_apis:
            try:
                print(f"   📡 Checking: {api_url[:50]}...")
                response = requests.get(api_url, timeout=10)

                if response.status_code == 200:
                    content = response.text.strip()

                    # Parse proxies theo format
                    lines = content.split("\n")
                    for line in lines[:50]:  # Limit 50 per source
                        line = line.strip()
                        if ":" in line:
                            # Format: IP:PORT
                            parts = line.split(":")
                            if len(parts) == 2:
                                ip = parts[0]
                                port = parts[1].split()[0]  # Remove any extra info

                                # Basic IP validation
                                if self._is_valid_ip(ip):
                                    proxy = {
                                        "ip": ip,
                                        "port": int(port),
                                        "type": "http",
                                        "country": "US",
                                        "source": api_url[:30],
                                    }
                                    all_proxies.append(proxy)

            except Exception as e:
                print(f"   ⚠️ Error fetching from source: {str(e)[:50]}")
                continue

        # Remove duplicates
        unique_proxies = []
        seen = set()
        for proxy in all_proxies:
            key = f"{proxy['ip']}:{proxy['port']}"
            if key not in seen:
                seen.add(key)
                unique_proxies.append(proxy)

        print(f"\n✅ Tìm thấy {len(unique_proxies)} IP Mỹ unique")
        return unique_proxies

    def _is_valid_ip(self, ip: str) -> bool:
        """Kiểm tra IP hợp lệ"""
        try:
            parts = ip.split(".")
            if len(parts) != 4:
                return False
            for part in parts:
                if not 0 <= int(part) <= 255:
                    return False
            return True
        except:
            return False

    def test_proxy_quality(self, proxy: Dict) -> Dict:
        """
        Test chất lượng proxy cho TikTok
        Returns: Dict với score và metrics
        """
        proxy_str = f"{proxy['ip']}:{proxy['port']}"

        # Check cache first
        if proxy_str in self.cache.get("tested_ips", {}):
            cached = self.cache["tested_ips"][proxy_str]
            # Cache valid for 1 hour
            if (
                datetime.now() - datetime.fromisoformat(cached["tested_at"])
            ).seconds < 3600:
                return cached

        result = {
            "proxy": proxy_str,
            "ip": proxy["ip"],
            "port": proxy["port"],
            "score": 0,
            "latency": 999999,
            "tiktok_accessible": False,
            "speed_mbps": 0,
            "stability": 0,
            "tested_at": datetime.now().isoformat(),
        }

        proxy_dict = {"http": f"http://{proxy_str}", "https": f"http://{proxy_str}"}

        # Test 1: Basic connectivity và latency
        try:
            start = time.time()
            response = requests.get(
                "http://ip-api.com/json", proxies=proxy_dict, timeout=5
            )
            latency = (time.time() - start) * 1000  # ms

            if response.status_code == 200:
                data = response.json()
                if data.get("countryCode") != "US":
                    result["score"] = 0
                    result["error"] = "Not US IP"
                    return result

                result["latency"] = latency
                result["location"] = (
                    f"{data.get('city', '')}, {data.get('regionName', '')}"
                )
                result["isp"] = data.get("isp", "Unknown")

                # Latency score (max 25 points)
                if latency < 100:
                    result["score"] += 25
                elif latency < 300:
                    result["score"] += 20
                elif latency < 500:
                    result["score"] += 15
                elif latency < 1000:
                    result["score"] += 10
                else:
                    result["score"] += 5

        except Exception as e:
            result["error"] = f"Connection failed: {str(e)[:50]}"
            return result

        # Test 2: TikTok accessibility
        tiktok_scores = []
        for tiktok_url in self.tiktok_test_urls:
            try:
                start = time.time()
                response = requests.get(
                    tiktok_url,
                    proxies=proxy_dict,
                    timeout=8,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    },
                )
                elapsed = time.time() - start

                if response.status_code == 200:
                    tiktok_scores.append(1)
                    result["tiktok_accessible"] = True

                    # Response time score for TikTok
                    if elapsed < 2:
                        tiktok_scores.append(10)
                    elif elapsed < 4:
                        tiktok_scores.append(7)
                    elif elapsed < 6:
                        tiktok_scores.append(5)
                    else:
                        tiktok_scores.append(2)

            except:
                tiktok_scores.append(0)

        # TikTok accessibility score (max 35 points)
        if tiktok_scores:
            tiktok_avg = sum(tiktok_scores) / len(tiktok_scores)
            result["score"] += int(tiktok_avg * 3.5)

        # Test 3: Speed test (download small file)
        try:
            start = time.time()
            response = requests.get(
                "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
                proxies=proxy_dict,
                timeout=5,
            )
            elapsed = time.time() - start

            if response.status_code == 200:
                # Estimate speed (very rough)
                file_size = len(response.content) / 1024  # KB
                speed_kbps = file_size / elapsed
                result["speed_mbps"] = round(speed_kbps / 1024, 2)

                # Speed score (max 25 points)
                if result["speed_mbps"] > 10:
                    result["score"] += 25
                elif result["speed_mbps"] > 5:
                    result["score"] += 20
                elif result["speed_mbps"] > 2:
                    result["score"] += 15
                elif result["speed_mbps"] > 1:
                    result["score"] += 10
                else:
                    result["score"] += 5

        except:
            pass

        # Test 4: Stability (multiple quick requests)
        success_count = 0
        for _ in range(5):
            try:
                response = requests.get(
                    "http://example.com", proxies=proxy_dict, timeout=3
                )
                if response.status_code == 200:
                    success_count += 1
            except:
                pass

        result["stability"] = (success_count / 5) * 100

        # Stability score (max 15 points)
        if result["stability"] >= 80:
            result["score"] += 15
        elif result["stability"] >= 60:
            result["score"] += 10
        elif result["stability"] >= 40:
            result["score"] += 5

        # Cache result
        self.cache["tested_ips"][proxy_str] = result
        self.save_cache()

        return result

    def test_proxies_parallel(
        self, proxies: List[Dict], max_workers: int = 10
    ) -> List[Dict]:
        """Test nhiều proxy song song"""
        print(f"\n🧪 Đang test {len(proxies)} IP với {max_workers} threads...")
        print("   Mỗi IP sẽ được đánh giá về:")
        print("   • Latency (độ trễ)")
        print("   • TikTok accessibility")
        print("   • Download speed")
        print("   • Connection stability")

        results = []
        tested = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_proxy = {
                executor.submit(self.test_proxy_quality, proxy): proxy
                for proxy in proxies
            }

            for future in as_completed(future_to_proxy):
                tested += 1
                try:
                    result = future.result()
                    results.append(result)

                    # Progress update
                    if tested % 5 == 0:
                        print(f"   📊 Đã test: {tested}/{len(proxies)} IPs...")

                except Exception as e:
                    proxy = future_to_proxy[future]
                    print(f"   ❌ Error testing {proxy['ip']}: {str(e)[:50]}")

        # Sort by score
        results.sort(key=lambda x: x.get("score", 0), reverse=True)

        return results

    def connect_to_proxy(self, proxy_info: Dict) -> bool:
        """
        Kết nối đến proxy được chọn
        Note: Đây là mock implementation - cần tool thực tế như OpenVPN, WireGuard, etc.
        """
        print(f"\n🔌 Đang kết nối đến {proxy_info['ip']}:{proxy_info['port']}...")

        # Windows: Cấu hình system proxy
        if sys.platform == "win32":
            try:
                # Set system proxy via netsh
                commands = [
                    f'netsh winhttp set proxy {proxy_info["ip"]}:{proxy_info["port"]}',
                    f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f',
                    f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyServer /d "{proxy_info["ip"]}:{proxy_info["port"]}" /f',
                ]

                for cmd in commands:
                    subprocess.run(cmd, shell=True, capture_output=True)

                print("✅ Đã cấu hình system proxy!")
                print(f"📍 IP: {proxy_info.get('ip')}")
                print(f"📍 Location: {proxy_info.get('location', 'US')}")
                print(f"📍 ISP: {proxy_info.get('isp', 'Unknown')}")

                # Verify connection
                try:
                    response = requests.get(
                        "http://ip-api.com/json",
                        proxies={
                            "http": f"http://{proxy_info['ip']}:{proxy_info['port']}",
                            "https": f"http://{proxy_info['ip']}:{proxy_info['port']}",
                        },
                        timeout=5,
                    )
                    if response.status_code == 200:
                        data = response.json()
                        print(
                            f"\n✅ Xác nhận: Đang dùng IP {data.get('query')} từ {data.get('country')}"
                        )
                        return True
                except:
                    pass

            except Exception as e:
                print(f"❌ Lỗi kết nối: {e}")
                return False

        else:
            # Linux/Mac: Export environment variables
            print("\n📝 Để sử dụng proxy này, chạy các lệnh sau:")
            print(f'export http_proxy="http://{proxy_info["ip"]}:{proxy_info["port"]}"')
            print(
                f'export https_proxy="http://{proxy_info["ip"]}:{proxy_info["port"]}"'
            )
            print(f'export HTTP_PROXY="http://{proxy_info["ip"]}:{proxy_info["port"]}"')
            print(
                f'export HTTPS_PROXY="http://{proxy_info["ip"]}:{proxy_info["port"]}"'
            )

        return True

    def disconnect_proxy(self):
        """Ngắt kết nối proxy"""
        print("\n🔌 Đang ngắt kết nối proxy...")

        if sys.platform == "win32":
            try:
                commands = [
                    "netsh winhttp reset proxy",
                    'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f',
                ]

                for cmd in commands:
                    subprocess.run(cmd, shell=True, capture_output=True)

                print("✅ Đã ngắt kết nối proxy!")

            except Exception as e:
                print(f"⚠️ Lỗi: {e}")

    def display_results(self, results: List[Dict]):
        """Hiển thị kết quả test"""
        print("\n" + "=" * 80)
        print("📊 KẾT QUẢ ĐÁNH GIÁ IP CHO TIKTOK")
        print("=" * 80)

        if not results:
            print("❌ Không tìm thấy IP nào khả dụng!")
            return

        # Find best IPs
        excellent_ips = [r for r in results if r.get("score", 0) >= 80]
        good_ips = [r for r in results if 60 <= r.get("score", 0) < 80]
        fair_ips = [r for r in results if 40 <= r.get("score", 0) < 60]

        if excellent_ips:
            print(f"\n🌟 IP XUẤT SẮC (Score >= 80) - {len(excellent_ips)} IPs:")
            print("-" * 80)
            for ip in excellent_ips[:5]:
                self._display_ip_info(ip)

        if good_ips:
            print(f"\n✅ IP TỐT (Score 60-79) - {len(good_ips)} IPs:")
            print("-" * 80)
            for ip in good_ips[:5]:
                self._display_ip_info(ip)

        if fair_ips:
            print(f"\n⚡ IP KHẢ DỤNG (Score 40-59) - {len(fair_ips)} IPs:")
            print("-" * 80)
            for ip in fair_ips[:3]:
                self._display_ip_info(ip)

        # Statistics
        print(f"\n📈 THỐNG KÊ:")
        print(f"   • Tổng IP đã test: {len(results)}")
        print(f"   • IP xuất sắc: {len(excellent_ips)}")
        print(f"   • IP tốt: {len(good_ips)}")
        print(f"   • IP khả dụng: {len(fair_ips)}")
        print(
            f"   • TikTok accessible: {len([r for r in results if r.get('tiktok_accessible')])}"
        )

    def _display_ip_info(self, ip_info: Dict):
        """Hiển thị thông tin 1 IP"""
        score = ip_info.get("score", 0)

        # Score bar
        bar_length = 20
        filled = int(bar_length * score / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        print(f"\n   🔹 {ip_info['ip']}:{ip_info['port']} [{bar}] {score}%")
        print(f"      📍 Location: {ip_info.get('location', 'Unknown')}")
        print(f"      🌐 ISP: {ip_info.get('isp', 'Unknown')}")
        print(f"      ⚡ Latency: {ip_info.get('latency', 999):.0f}ms")
        print(f"      📊 Speed: {ip_info.get('speed_mbps', 0):.1f} Mbps")
        print(
            f"      🎯 TikTok: {'✅ Accessible' if ip_info.get('tiktok_accessible') else '❌ Blocked'}"
        )
        print(f"      💪 Stability: {ip_info.get('stability', 0):.0f}%")

    def execute(self, input_folder=None, output_folder=None):
        """Main execution"""
        self.print_banner()

        print("🌐 AUTO VPN FAKER CHO TIKTOK")
        print("Tính năng:")
        print("  • Tự động tìm IP Mỹ free")
        print("  • Đánh giá chất lượng cho TikTok")
        print("  • Tự động kết nối IP tốt nhất")
        print("  • Hoặc cho phép chọn thủ công")

        # Menu
        print("\n📋 CHỌN CHẾ ĐỘ:")
        print("1. 🚀 Tự động (tìm và kết nối IP tốt nhất)")
        print("2. 🎯 Thủ công (xem danh sách và chọn)")
        print("3. 🔌 Ngắt kết nối proxy hiện tại")
        print("4. 🔙 Quay lại")

        choice = input("\n👉 Chọn chế độ: ").strip()

        if choice == "1":
            # Auto mode
            self._auto_mode()
        elif choice == "2":
            # Manual mode
            self._manual_mode()
        elif choice == "3":
            # Disconnect
            self.disconnect_proxy()
        elif choice == "4":
            return
        else:
            print("❌ Lựa chọn không hợp lệ!")

        input("\n✨ Nhấn Enter để tiếp tục...")

    def _auto_mode(self):
        """Chế độ tự động"""
        print("\n🚀 CHẾ ĐỘ TỰ ĐỘNG")

        # Fetch proxies
        proxies = self.fetch_us_proxies()
        if not proxies:
            print("❌ Không tìm thấy proxy nào!")
            return

        # Test proxies
        results = self.test_proxies_parallel(proxies[:30])  # Test top 30

        # Find best proxy
        best_proxy = None
        for result in results:
            if result.get("score", 0) >= 70 and result.get("tiktok_accessible"):
                best_proxy = result
                break

        if best_proxy:
            print(
                f"\n✅ Tìm thấy IP tốt nhất: {best_proxy['ip']} (Score: {best_proxy['score']}%)"
            )
            self._display_ip_info(best_proxy)

            confirm = input("\n👉 Kết nối đến IP này? (y/n): ").lower()
            if confirm == "y":
                self.connect_to_proxy(best_proxy)
        else:
            print("\n⚠️ Không tìm thấy IP đạt chuẩn (>70% và TikTok accessible)")
            print("🔄 Chuyển sang chế độ thủ công...")
            self.display_results(results)
            self._select_proxy_manual(results)

    def _manual_mode(self):
        """Chế độ thủ công"""
        print("\n🎯 CHẾ ĐỘ THỦ CÔNG")

        # Fetch proxies
        proxies = self.fetch_us_proxies()
        if not proxies:
            print("❌ Không tìm thấy proxy nào!")
            return

        # Ask how many to test
        print(f"\n📊 Tìm thấy {len(proxies)} IPs")
        num = input("👉 Số lượng IP muốn test (mặc định 20): ").strip()

        try:
            num = int(num) if num else 20
            num = min(num, len(proxies))
        except:
            num = 20

        # Test proxies
        results = self.test_proxies_parallel(proxies[:num])

        # Display results
        self.display_results(results)

        # Let user select
        self._select_proxy_manual(results)

    def _select_proxy_manual(self, results: List[Dict]):
        """Cho phép user chọn proxy thủ công"""
        if not results:
            return

        print("\n" + "=" * 80)
        print("📋 CHỌN IP ĐỂ KẾT NỐI")
        print("=" * 80)

        # Show top 10
        top_results = [r for r in results if r.get("score", 0) > 30][:10]

        for i, ip in enumerate(top_results, 1):
            score = ip.get("score", 0)
            status = "🌟" if score >= 80 else "✅" if score >= 60 else "⚡"
            tiktok = "✅" if ip.get("tiktok_accessible") else "❌"

            print(
                f"{i:2d}. {status} {ip['ip']}:{ip['port']} - Score: {score}% - TikTok: {tiktok}"
            )

        print("\n0. 🔙 Quay lại")

        try:
            choice = int(input("\n👉 Chọn IP (nhập số): "))
            if 1 <= choice <= len(top_results):
                selected = top_results[choice - 1]
                print(f"\n📌 Đã chọn: {selected['ip']}")
                self._display_ip_info(selected)

                confirm = input("\n👉 Xác nhận kết nối? (y/n): ").lower()
                if confirm == "y":
                    self.connect_to_proxy(selected)

        except ValueError:
            print("❌ Lựa chọn không hợp lệ!")

    def print_banner(self):
        """In banner"""
        print("\n" + "=" * 60)
        print("   🌐 VPN FAKER FOR TIKTOK   ")
        print("   Auto US Proxy Finder & Connector")
        print("=" * 60 + "\n")


# Test function
if __name__ == "__main__":
    vpn_faker = VPNFakerAction()
    vpn_faker.execute()
