#!/bin/bash
# Build and install script for VideoForge Core

set -e

echo "🔨 Building VideoForge Core..."

# Navigate to core directory
cd "$(dirname "$0")/../videoforge-core"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.9+ required. Found: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg not found in PATH. Please install FFmpeg:"
    echo "   Ubuntu/Debian: sudo apt install ffmpeg"
    echo "   macOS: brew install ffmpeg"
    echo "   Windows: Download from https://ffmpeg.org/"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ FFmpeg found: $(ffmpeg -version | head -n1)"
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Install in development mode
echo "🔧 Installing VideoForge Core..."
pip install -e .

# Verify installation
echo "🧪 Verifying installation..."
if videoforge --version; then
    echo "✅ VideoForge Core installed successfully!"
    echo ""
    echo "🚀 Quick start:"
    echo "   videoforge process -i ./input -o ./output"
    echo "   videoforge serve --port 8080"
    echo "   videoforge info --system-info"
    echo ""
    echo "📚 Documentation: https://docs.videoforge.com"
else
    echo "❌ Installation verification failed"
    exit 1
fi

echo "🎉 Build completed successfully!"
