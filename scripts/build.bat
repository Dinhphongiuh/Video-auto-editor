@echo off
REM Build and install script for VideoForge Core on Windows

echo 🔨 Building VideoForge Core...

REM Navigate to core directory
cd /d "%~dp0\..\videoforge-core"

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✅ Python version: %python_version%

REM Check if FFmpeg is installed
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  FFmpeg not found in PATH. Please install FFmpeg:
    echo    Download from https://ffmpeg.org/
    echo    Add to system PATH
    echo.
    set /p continue="Continue anyway? (y/N): "
    if /i not "%continue%"=="y" exit /b 1
) else (
    echo ✅ FFmpeg found
)

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Install in development mode
echo 🔧 Installing VideoForge Core...
pip install -e .

REM Verify installation
echo 🧪 Verifying installation...
videoforge --version
if errorlevel 1 (
    echo ❌ Installation verification failed
    exit /b 1
)

echo ✅ VideoForge Core installed successfully!
echo.
echo 🚀 Quick start:
echo    videoforge process -i .\input -o .\output
echo    videoforge serve --port 8080
echo    videoforge info --system-info
echo.
echo 📚 Documentation: https://docs.videoforge.com

echo 🎉 Build completed successfully!
pause
