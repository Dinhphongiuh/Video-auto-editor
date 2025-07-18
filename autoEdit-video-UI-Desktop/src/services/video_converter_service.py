"""
Video Converter Service
Handles video format conversion using FFmpeg
"""

from PyQt6.QtCore import QThread, pyqtSignal
import os
import subprocess
import re
from typing import List, Dict, Tuple


class VideoConverterThread(QThread):
    """Thread for video conversion processing"""
    progress = pyqtSignal(int)  # Overall progress 0-100
    status = pyqtSignal(str)  # Status messages
    file_progress = pyqtSignal(int, int)  # current file, total files
    current_file = pyqtSignal(str)  # Current file being processed
    conversion_finished = pyqtSignal(bool, str)  # Success, message
    
    # Format configurations for FFmpeg
    FORMAT_CONFIGS = {
        "mp4": {
            "container": "mp4",
            "video_codec": "libx264",
            "audio_codec": "aac",
            "extra_params": ["-preset", "medium", "-crf", "23"]
        },
        "avi": {
            "container": "avi", 
            "video_codec": "libx264",
            "audio_codec": "mp3",
            "extra_params": []
        },
        "mov": {
            "container": "mov",
            "video_codec": "libx264", 
            "audio_codec": "aac",
            "extra_params": ["-preset", "medium"]
        },
        "mkv": {
            "container": "matroska",
            "video_codec": "libx264",
            "audio_codec": "aac",
            "extra_params": ["-preset", "medium", "-crf", "23"]
        },
        "wmv": {
            "container": "asf",
            "video_codec": "wmv2",
            "audio_codec": "wmav2",
            "extra_params": []
        },
        "webm": {
            "container": "webm",
            "video_codec": "libvpx-vp9",
            "audio_codec": "libopus",
            "extra_params": ["-b:v", "1M", "-threads", "4"]
        }
    }
    
    def __init__(self):
        super().__init__()
        self.input_folder = ""
        self.output_folder = ""
        self.output_format = "mp4"
        self.custom_params = ""
        self.is_running = True
        self.total_duration = 0
        
    def setup(self, input_folder: str, output_folder: str, output_format: str, custom_params: str = ""):
        """Setup conversion parameters"""
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.output_format = output_format.lower()
        self.custom_params = custom_params
        self.is_running = True
        
    def get_video_files(self, folder: str) -> List[str]:
        """Get list of video files in folder"""
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg']
        video_files = []
        
        try:
            for file in os.listdir(folder):
                if any(file.lower().endswith(ext) for ext in video_extensions):
                    video_files.append(os.path.join(folder, file))
        except Exception as e:
            self.status.emit(f"Error reading folder: {str(e)}")
            
        return video_files
        
    def get_video_duration(self, video_path: str) -> float:
        """Get video duration in seconds using FFprobe"""
        try:
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return float(result.stdout.strip())
        except:
            pass
        return 0
        
    def parse_ffmpeg_progress(self, line: str, total_duration: float) -> int:
        """Parse FFmpeg output to get progress percentage"""
        # Look for time progress
        time_match = re.search(r'time=(\d+):(\d+):(\d+\.\d+)', line)
        if time_match and total_duration > 0:
            hours = int(time_match.group(1))
            minutes = int(time_match.group(2))
            seconds = float(time_match.group(3))
            current_time = hours * 3600 + minutes * 60 + seconds
            progress = int((current_time / total_duration) * 100)
            return min(progress, 100)
        return -1
        
    def check_ffmpeg_available(self) -> bool:
        """Check if FFmpeg is available"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True)
            return True
        except:
            return False
            
    def run(self):
        """Run video conversion process"""
        if not self.check_ffmpeg_available():
            self.conversion_finished.emit(False, "FFmpeg not found! Please install FFmpeg first.")
            return
            
        # Get video files
        video_files = self.get_video_files(self.input_folder)
        
        if not video_files:
            self.conversion_finished.emit(False, "No video files found in input folder!")
            return
            
        total_files = len(video_files)
        self.status.emit(f"Found {total_files} video file(s)")
        
        success_count = 0
        failed_count = 0
        
        # Process each video
        for i, video_file in enumerate(video_files):
            if not self.is_running:
                self.status.emit("Conversion cancelled by user")
                break
                
            filename = os.path.basename(video_file)
            name, _ = os.path.splitext(filename)
            output_file = os.path.join(self.output_folder, f"{name}.{self.output_format}")
            
            self.current_file.emit(filename)
            self.file_progress.emit(i + 1, total_files)
            
            # Get video duration for progress tracking
            duration = self.get_video_duration(video_file)
            
            # Convert the file
            if self.convert_file(video_file, output_file, duration):
                success_count += 1
                self.status.emit(f"✅ Converted: {filename}")
            else:
                failed_count += 1
                self.status.emit(f"❌ Failed: {filename}")
                
        # Final status
        if self.is_running:
            message = f"Conversion completed! Success: {success_count}, Failed: {failed_count}"
            self.conversion_finished.emit(success_count > 0, message)
        else:
            message = f"Conversion cancelled. Processed: {success_count} file(s)"
            self.conversion_finished.emit(False, message)
            
    def convert_file(self, input_file: str, output_file: str, duration: float) -> bool:
        """Convert a single video file"""
        try:
            # Get format config
            config = self.FORMAT_CONFIGS.get(self.output_format, self.FORMAT_CONFIGS["mp4"])
            
            # Build FFmpeg command
            cmd = [
                'ffmpeg',
                '-i', input_file,
                '-c:v', config['video_codec'],
                '-c:a', config['audio_codec']
            ]
            
            # Add extra parameters from config
            cmd.extend(config['extra_params'])
            
            # Add custom parameters if provided
            if self.custom_params:
                custom_args = self.custom_params.split()
                cmd.extend(custom_args)
            
            # Add output format and file
            cmd.extend([
                '-f', config['container'],
                '-y',  # Overwrite output
                output_file
            ])
            
            # Run FFmpeg with real-time progress
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1
            )
            
            # Monitor progress
            while True:
                if not self.is_running:
                    process.terminate()
                    return False
                    
                line = process.stderr.readline()
                if not line:
                    break
                    
                # Parse progress
                progress = self.parse_ffmpeg_progress(line, duration)
                if progress >= 0:
                    self.progress.emit(progress)
                    
            process.wait()
            return process.returncode == 0
            
        except Exception as e:
            self.status.emit(f"Error: {str(e)}")
            return False
            
    def stop(self):
        """Stop the conversion process"""
        self.is_running = False


class VideoConverterService:
    """Service class for video conversion"""
    
    @staticmethod
    def get_supported_formats() -> List[str]:
        """Get list of supported output formats"""
        return ["MP4", "AVI", "MOV", "MKV", "WMV", "WEBM"]
        
    @staticmethod
    def validate_folders(input_folder: str, output_folder: str) -> Tuple[bool, str]:
        """Validate input and output folders"""
        if not input_folder:
            return False, "Please select input folder"
            
        if not output_folder:
            return False, "Please select output folder"
            
        if not os.path.exists(input_folder):
            return False, "Input folder does not exist"
            
        if not os.path.exists(output_folder):
            try:
                os.makedirs(output_folder)
            except:
                return False, "Cannot create output folder"
                
        return True, "OK"