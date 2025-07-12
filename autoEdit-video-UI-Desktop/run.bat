@echo off
echo ========================================
echo AutoEdit Video UI Desktop - Starting...
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ERROR: Virtual environment not found!
    echo Please run install.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if main.py exists
if not exist "main.py" (
    echo ERROR: main.py not found!
    pause
    exit /b 1
)

REM Run the application
echo Starting AutoEdit Video UI Desktop...
echo.
python main.py

REM Pause if there's an error
if %errorlevel% neq 0 (
    echo.
    echo Application exited with error code: %errorlevel%
    pause
)
