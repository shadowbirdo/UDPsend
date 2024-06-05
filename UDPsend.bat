@echo off
start /B cmd /k ".\venv\Scripts\activate & python main.py"
timeout /t 1 /nobreak >nul
start http:/localhost:5000