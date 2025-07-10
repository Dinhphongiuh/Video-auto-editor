# VideoForge Core - Professional Video Processing Engine

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/videoforge/videoforge-core)

VideoForge Core is a powerful, AI-enhanced video processing engine that runs both as a CLI tool and background service. It provides professional-grade video editing capabilities including automatic subtitle generation, intelligent logo removal, and batch processing.

## 🚀 Features

### Core Video Processing
- **Resolution & Aspect Ratio**: Convert between any resolution and aspect ratio
- **Speed Control**: Adjust video speed from 0.25x to 4x
- **Duration Management**: Trim, split, and merge videos
- **Batch Processing**: Process entire folders automatically

### AI-Powered Features
- **Auto Subtitle Generation**: AI-powered Vietnamese subtitle generation
- **Logo Detection & Removal**: Intelligent logo detection and removal
- **Scene Detection**: Automatic scene change detection
- **Color Correction**: AI-enhanced color grading

### Advanced Image Processing
- **Color Grading**: Professional color correction tools
- **Overlay Management**: Add watermarks, logos, and text overlays
- **Noise Reduction**: Automatic audio and video noise reduction
- **Smart Cropping**: Intelligent content-aware cropping

## 📦 Installation

### Quick Install
```bash
pip install videoforge-core
```

### Development Install
```bash
git clone https://github.com/videoforge/videoforge-core.git
cd videoforge-core
pip install -e .[dev]
```

### GPU Support (Optional)
```bash
pip install videoforge-core[gpu]
```

## 🎯 Quick Start

### CLI Usage
```bash
# Basic processing
videoforge process --input ./videos --output ./processed

# With AI features
videoforge process \
  --input ./videos \
  --output ./processed \
  --resolution 1920x1080 \
  --aspect-ratio 16:9 \
  --auto-subtitle \
  --remove-logo \
  --profile youtube_shorts

# Background service
videoforge serve --port 8080
```

### Python API
```python
from videoforge.core import VideoProcessor

processor = VideoProcessor()
result = processor.process_video(
    input_path="input.mp4",
    output_path="output.mp4",
    resolution="1920x1080",
    aspect_ratio="16:9",
    auto_subtitle=True
)
```

## 🔧 Configuration

### Default Config Location
- Windows: `%APPDATA%/VideoForge/config.json`
- macOS: `~/Library/Application Support/VideoForge/config.json`
- Linux: `~/.config/VideoForge/config.json`

### Sample Configuration
```json
{
  "processing": {
    "max_concurrent_jobs": 4,
    "temp_directory": "./temp",
    "output_quality": "high"
  },
  "ai": {
    "subtitle_language": "vi",
    "whisper_model": "base",
    "translation_service": "google"
  },
  "profiles": {
    "youtube_shorts": {
      "resolution": "1080x1920",
      "aspect_ratio": "9:16",
      "max_duration": 60,
      "auto_subtitle": true
    }
  }
}
```

## 📚 Documentation

- [CLI Usage Guide](docs/CLI_USAGE.md)
- [API Reference](docs/API_REFERENCE.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)

## 🛠️ System Requirements

### Minimum Requirements
- Python 3.9+
- 4GB RAM
- 2GB free disk space
- FFmpeg (installed system-wide)

### Recommended
- Python 3.11+
- 16GB RAM
- SSD storage
- NVIDIA GPU with CUDA support
- 8GB free disk space

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- 📧 Email: support@videoforge.com
- 💬 Discord: [VideoForge Community](https://discord.gg/videoforge)
- 🐛 Issues: [GitHub Issues](https://github.com/videoforge/videoforge-core/issues)
- 📖 Documentation: [docs.videoforge.com](https://docs.videoforge.com)

## 🙏 Acknowledgments

- [FFmpeg](https://ffmpeg.org/) - The backbone of video processing
- [OpenAI Whisper](https://github.com/openai/whisper) - AI speech recognition
- [OpenCV](https://opencv.org/) - Computer vision library
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework

---

**VideoForge** - *Forge Your Videos to Perfection* 🎬
