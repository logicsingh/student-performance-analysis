@echo off
title Student Performance Analysis Setup
where py >nul 2>nul
if errorlevel 1 (echo Install Python 3.10+ from python.org and enable Add Python to PATH.& pause & exit /b 1)
py -m venv .venv
call .venv\Scripts\activate
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
if errorlevel 1 (echo Dependency installation failed. Check Python and internet connection.& pause & exit /b 1)
echo Setup complete. Now run start_windows.bat.
pause
