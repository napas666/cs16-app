@echo off
cd /d "%~dp0"
echo Installing...
pip install --no-index --find-links=wheels pymem customtkinter pygame pywin32
echo.
echo Starting...
python app.py
pause
