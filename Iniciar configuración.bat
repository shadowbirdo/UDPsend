@echo off
start http:/localhost:5000
cmd /k ".\venv\Scripts\activate & python main.py"

