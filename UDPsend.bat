@echo off
start /B python main.py
timeout /t 1 /nobreak >nul
start http:/localhost:5000