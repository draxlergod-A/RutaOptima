@echo off
REM Doble clic: instala lo necesario y abre la pagina del proyecto.
python --version >nul 2>&1 || (echo Instala Python desde https://www.python.org/downloads/ y marca "Add Python to PATH" & pause & exit /b)
python -m pip install -r requirements.txt
python app.py
pause
