@echo off
cd /d D:\VideoForge\videoforge-core

echo Removing old virtual environment...
if exist venv (
    rmdir /s /q venv
    echo Virtual environment removed.
) else (
    echo No virtual environment found.
)

echo Creating new virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Failed to create virtual environment.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo Installing VideoForge Core...
pip install -e .
if %errorlevel% neq 0 (
    echo Failed to install VideoForge Core.
    pause
    exit /b 1
)

echo Setup completed successfully!
echo You can now run: cd D:\VideoForge\scripts && ./build
pause
