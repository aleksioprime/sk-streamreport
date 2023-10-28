from .models import User
from django.utils import timezone
from django.core.cache import cache

class LastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Проверяем, что пользователь аутентифицирован
        if request.user.is_authenticated:
            # Устанавливаем или обновляем время последней активности пользователя в кеше
            cache.set(f'last_activity_{request.user.id}', timezone.now(), 3600) # срок жизни в 1 час, например
            print('Записан cache: ', cache.get(f'last_activity_{request.user.id}'))
        return response

# class LastActivityMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             update_last_activity.delay(request.user.id)
#         response = self.get_response(request)
#         return response