@echo off
winget install python3
pip install Flask --upgrade
start /B cmd /k ".\venv\Scripts\activate & python main.py"
timeout /t 1 /nobreak >nul
start http:/localhost:5000