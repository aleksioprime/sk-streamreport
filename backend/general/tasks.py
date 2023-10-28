from celery import shared_task
from .models import User
from django.core.cache import cache
from datetime import datetime

@shared_task
def update_user_activity():
     for user in User.objects.all():
        last_activity = cache.get(f'last_activity_{user.id}')
        print(f'Последняя активность пользователя {user.email}: {last_activity}')

        if last_activity:
            user.last_activity = last_activity
            user.save(update_fields=['last_activity'])
            
            # После сохранения, можно удалить значение из кеша (необязательно)
            cache.delete(f'last_activity_{user.id}')

# @shared_task
# def update_last_activity(user_id):
#     user = User.objects.get(id=user_id)
#     user.last_activity = datetime.now()
#     user.save()