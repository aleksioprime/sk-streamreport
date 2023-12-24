import subprocess
import datetime
import os

# Параметры подключения к базе данных
db_name = os.environ.get("SQL_DATABASE")
db_user = os.environ.get("SQL_USER")
db_host = os.environ.get("SQL_HOST")
backup_file = f"backup_{db_name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.backup"

backup_dir = 'backup'
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

# Команда для создания бэкапа
backup_command = f"pg_dump -h {db_host} -U {db_user} {db_name} > {os.path.join(backup_dir, backup_file)}"

# Выполнение команды
subprocess.run(backup_command, shell=True, check=True)