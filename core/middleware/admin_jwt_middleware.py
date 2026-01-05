"""
Middleware для защиты админ-панели через JWT токен в URL.
Доступ к админке возможен только по пути: /admin/<jwt_token>/
"""
import jwt
from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse


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
        
        # Проверяем, есть ли валидный токен в сессии (для внутренних запросов админки)
        if hasattr(request, 'session'):
            session_token = request.session.get('admin_jwt_token')
            session_valid = request.session.get('admin_jwt_valid', False)
            
            if session_token and session_valid:
                # Проверяем токен из сессии
                try:
                    decoded = jwt.decode(
                        session_token,
                        jwt_secret,
                        algorithms=['HS256']
                    )
                    
                    if decoded.get('type') == 'admin_access':
                        # Токен из сессии валиден, разрешаем доступ
                        return None
                except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                    # Токен в сессии невалиден, очищаем сессию
                    request.session.pop('admin_jwt_token', None)
                    request.session.pop('admin_jwt_valid', None)
        
        # Извлекаем токен из URL
        # Ожидаемый формат: /admin/<token>/ или /admin/<token>
        path_parts = [p for p in request.path.strip('/').split('/') if p]
        
        if len(path_parts) < 2 or path_parts[0] != 'admin':
            # Если нет токена в URL и нет валидного токена в сессии - 404
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
                raise Http404('Страница не найдена')
            
            # Токен валиден, сохраняем в сессии для последующих запросов
            if hasattr(request, 'session'):
                request.session['admin_jwt_token'] = token
                request.session['admin_jwt_valid'] = True
                request.session.set_expiry(86400 * 365)  # 1 год
            
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
            raise Http404('Страница не найдена')
        except jwt.InvalidTokenError:
            raise Http404('Страница не найдена')
        except Exception:
            raise Http404('Страница не найдена')
    
    def process_response(self, request, response):
        """
        Обрабатывает ответы, добавляя токен в редиректы и ссылки админки.
        """
        # Если это запрос к админке и есть токен в сессии
        if (hasattr(request, 'session') and 
            request.path.startswith('/admin')):
            
            session_token = request.session.get('admin_jwt_token')
            
            if session_token:
                # Обрабатываем редиректы
                if isinstance(response, HttpResponseRedirect):
                    if response.url.startswith('/admin/'):
                        # Убираем /admin/ и добавляем токен
                        admin_path = response.url[7:].lstrip('/')  # Убираем '/admin/'
                        # Обрабатываем query параметры
                        if '?' in admin_path:
                            path_part, query_part = admin_path.split('?', 1)
                            response.url = f'/admin/{session_token}/{path_part}?{query_part}'
                        else:
                            response.url = f'/admin/{session_token}/{admin_path}'
                
                # Обрабатываем HTML ответы (заменяем ссылки в HTML)
                elif hasattr(response, 'content'):
                    content_type = response.get('Content-Type', '')
                    if isinstance(content_type, str) and content_type.startswith('text/html'):
                        try:
                            content = response.content.decode('utf-8')
                            
                            # Заменяем все ссылки /admin/ на /admin/<token>/
                            import re
                            
                            # Функция для замены URL
                            def replace_admin_url(match):
                                attr = match.group(1)  # href или action
                                path = match.group(2).lstrip('/')  # путь после /admin/
                                return f'{attr}="/admin/{session_token}/{path}"'
                            
                            # Заменяем href="/admin/... и action="/admin/...
                            content = re.sub(
                                r'(href|action)=["\']/admin/([^"\']*)["\']',
                                replace_admin_url,
                                content
                            )
                            
                            response.content = content.encode('utf-8')
                        except (UnicodeDecodeError, AttributeError, KeyError):
                            # Если не удалось обработать контент, просто пропускаем
                            pass
        
        return response
