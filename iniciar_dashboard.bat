@echo off
echo Iniciando Servidor de Infobyte...
start http://localhost:8000
python -m http.server 8000
