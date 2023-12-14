import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from datetime import timedelta

# Устанавливаем дефолтные настройки Django для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Используем настройки из settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'update-user-activity-every-minute': {
        'task': 'general.tasks.update_user_activity',
        'schedule': crontab(minute='*/1'),
    },
}

# Автоматически обнаруживаем задачи из всех установленных приложений
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

