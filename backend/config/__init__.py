from .celery import app as celery_app

# Это гарантирует, что Celery приложение всегда будет импортировано, когда запущен Django
__all__ = ("celery_app",)