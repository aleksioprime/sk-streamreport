@echo on
call "C:\venv\freshstream\Scripts\activate.bat"
set POSTGRES_PORT=32768
set POSTGRES_HOST=localhost
set POSTGRES_DB=igskolkovo
set POSTGRES_USER=igadmin
set POSTGRES_PASSWORD=Pox{@K
python manage.py runserver
pause
