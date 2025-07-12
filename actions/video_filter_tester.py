#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Filter Tester - Test bộ lọc video
"""

import os
import subprocess
from .base_action import BaseAction


class VideoFilterTester(BaseAction):
    """Test chức năng filter của VideoForge"""
    
    def test_single_video(self, video_file, output_folder):
        """Test filter trên 1 video"""
        
        filename = os.path.basename(video_file)
        name, ext = os.path.splitext(filename)
        
        # Test brightness
        print("🔆 Testing Brightness...")
        brightness_output = os.path.join(output_folder, f"{name}_brightness_test{ext}")
        self.run_videoforge_command([
            "process",
            "-i", video_file,
            "-o", brightness_output,
            "--brightness", "20"
        ])
        
        # Test contrast
        print("🔳 Testing Contrast...")
        contrast_output = os.path.join(output_folder, f"{name}_contrast_test{ext}")
        self.run_videoforge_command([
            "process", 
            "-i", video_file,
            "-o", contrast_output,
            "--contrast", "30"
        ])
        
        # Test saturation
        print("🌈 Testing Saturation...")
        saturation_output = os.path.join(output_folder, f"{name}_saturation_test{ext}")
        self.run_videoforge_command([
            "process",
            "-i", video_file, 
            "-o", saturation_output,
            "--saturation", "50"
        ])
        
        # Test combined
        print("✨ Testing Combined...")
        combined_output = os.path.join(output_folder, f"{name}_combined_test{ext}")
        self.run_videoforge_command([
            "process",
            "-i", video_file,
            "-o", combined_output,
            "--brightness", "10",
            "--contrast", "20", 
            "--saturation", "15"
        ])
        
        print("✅ Filter testing completed!")