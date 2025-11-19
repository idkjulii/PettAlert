@echo off
cd /d "%~dp0"
echo ================================================
echo REINICIANDO BACKEND CON FIX
echo ================================================
echo.
echo Presiona Ctrl+C si hay otro backend corriendo
timeout /t 3
echo.
echo Iniciando backend...
python -m uvicorn main:app --host 0.0.0.0 --port 8003 --reload


