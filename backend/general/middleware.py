from django.utils import timezone
from django.core.cache import cache
from django.db import connection
import logging

logger = logging.getLogger('main')

class LastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Проверяем, что пользователь аутентифицирован
        if request.user.is_authenticated:
            # Устанавливаем или обновляем время последней активности пользователя в кеше
            cache.set(f'last_activity_{request.user.id}', timezone.now(), 3600) # срок жизни в 1 час, например
            # print('Записан cache: ', cache.get(f'last_activity_{request.user.id}'))
            logger.info(f'Записан cache: { cache.get(f"last_activity_{request.user.id}")}')
        return response
    
class DBCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Сброс подсчета перед обработкой запроса
        connection.queries_log.clear()

        # Получение ответа от следующего слоя middleware
        response = self.get_response(request)

        # Логирование подробностей каждого запроса
        for query in connection.queries:
            logger.info(f"Query: {query['sql']} Time: {query['time']}")

        # Подсчет количества запросов к базе данных
        total_queries = len(connection.queries)
        logger.info(f"Total DB Queries: {total_queries}")

        return response