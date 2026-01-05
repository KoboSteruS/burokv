"""
Middleware для защиты админ-панели через JWT токен в URL.
Доступ к админке возможен только по пути: /admin/<jwt_token>/
"""
import jwt
from django.http import HttpResponseForbidden
from django.conf import settings
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin


class AdminJWTMiddleware(MiddlewareMixin):
    """
    Middleware проверяет наличие валидного JWT токена в URL для доступа к админ-панели.
    
    Если токен отсутствует или невалиден, доступ запрещается.
    """
    
    def process_request(self, request):
        """
        Проверяет JWT токен в URL перед доступом к админ-панели.
        """
        # Проверяем, что запрос идет к админ-панели
        if not request.path.startswith('/admin'):
            return None
        
        # Получаем секретный ключ для JWT из настроек
        jwt_secret = getattr(settings, 'ADMIN_JWT_SECRET', None)
        
        if not jwt_secret:
            # Если секрет не настроен, разрешаем доступ (для разработки)
            # В production это должно быть обязательно настроено!
            return None
        
        # Извлекаем токен из URL
        # Ожидаемый формат: /admin/<token>/
        path_parts = request.path.strip('/').split('/')
        
        if len(path_parts) < 2 or path_parts[0] != 'admin':
            return HttpResponseForbidden('Доступ запрещен. Требуется JWT токен в URL.')
        
        # Второй элемент должен быть токеном
        token = path_parts[1]
        
        # Проверяем токен
        try:
            decoded = jwt.decode(
                token,
                jwt_secret,
                algorithms=['HS256']
            )
            
            # Проверяем тип токена
            if decoded.get('type') != 'admin_access':
                return HttpResponseForbidden('Неверный тип токена')
            
            # Токен валиден, разрешаем доступ
            # Убираем токен из пути для Django admin
            request.path = '/admin/' + ('/'.join(path_parts[2:]) if len(path_parts) > 2 else '')
            if not request.path.endswith('/') and len(path_parts) == 2:
                request.path += '/'
            request.path_info = request.path
            
            return None
            
        except jwt.ExpiredSignatureError:
            return HttpResponseForbidden('Токен истек. Сгенерируйте новый токен.')
        except jwt.InvalidTokenError as e:
            return HttpResponseForbidden(f'Невалидный токен: {str(e)}')
        except Exception as e:
            return HttpResponseForbidden(f'Ошибка проверки токена: {str(e)}')

