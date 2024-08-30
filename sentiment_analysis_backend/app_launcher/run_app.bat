@echo off
REM Check if Python is installed
python --version >nul 2>&1 || (
    echo Python is not installed. Please install Python first.
    exit /b
)

REM Run the Python script to create and activate the virtual environment and execute app.py
python run_app.py

pause
