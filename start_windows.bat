@echo off
if not exist .venv\Scripts\python.exe (echo Run run_windows.bat first.& pause & exit /b 1)
.venv\Scripts\python.exe app.py
pause
