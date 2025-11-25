@echo off
cd /d "C:\Users\isaias.ns\AGENDAMENTOS_SALAS\"
call venv\Scripts\activate.bat
python manage.py runserver 0.0.0.0:8000
pause
