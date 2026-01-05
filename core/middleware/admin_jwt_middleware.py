"""
Middleware для защиты админ-панели через JWT токен в URL.
Доступ к админке возможен только по пути: /admin/<jwt_token>/
"""
import jwt
from django.http import HttpResponseForbidden
from django.conf import settings
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
        # Ожидаемый формат: /admin/<token>/ или /admin/<token>
        path_parts = [p for p in request.path.strip('/').split('/') if p]
        
        if len(path_parts) < 2 or path_parts[0] != 'admin':
            # Если нет токена, возвращаем 404 (Not Found) вместо кастомного сообщения
            from django.http import Http404
            raise Http404('Страница не найдена')
        
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
                from django.http import Http404
                raise Http404('Страница не найдена')
            
            # Токен валиден, сохраняем в сессии для последующих запросов
            if hasattr(request, 'session'):
                request.session['admin_jwt_token'] = token
                request.session['admin_jwt_valid'] = True
            
            # Убираем токен из пути для Django admin
            # Оставляем только путь после /admin/<token>/
            remaining_path = '/'.join(path_parts[2:]) if len(path_parts) > 2 else ''
            new_path = '/admin/' + (remaining_path + '/' if remaining_path else '')
            
            # Обновляем путь запроса для Django admin
            request.path = new_path
            request.path_info = new_path
            request.META['PATH_INFO'] = new_path
            # Также обновляем SCRIPT_NAME если нужно
            if 'SCRIPT_NAME' in request.META:
                request.META['SCRIPT_NAME'] = ''
            
            return None
            
        except jwt.ExpiredSignatureError:
            from django.http import Http404
            raise Http404('Страница не найдена')
        except jwt.InvalidTokenError:
            from django.http import Http404
            raise Http404('Страница не найдена')
        except Exception:
            from django.http import Http404
            raise Http404('Страница не найдена')
