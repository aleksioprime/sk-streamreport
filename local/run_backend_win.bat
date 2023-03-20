@echo on
call "C:\venv\freshstream\Scripts\activate.bat"
set POSTGRES_PORT=5432
set POSTGRES_HOST=localhost
set POSTGRES_DB=igskolkovo
set POSTGRES_USER=igadmin
set POSTGRES_PASSWORD=Pox{@K
cd "D:\development\freshstream\backend"
python manage.py runserver
pause
