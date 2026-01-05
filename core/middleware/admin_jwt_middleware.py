"""
Middleware для защиты админ-панели через JWT токен в URL.
Доступ к админке возможен только по пути: /admin/<jwt_token>/
"""
import jwt
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import re


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
        has_token_in_url = len(path_parts) >= 2 and path_parts[0] == 'admin'
        
        # Проверяем, есть ли валидный токен в сессии (для внутренних запросов админки)
        # Это нужно для POST-запросов формы логина и других внутренних запросов
        if hasattr(request, 'session') and not has_token_in_url:
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
                        # Для POST-запросов (форма логина) не нужно менять путь
                        return None
                except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                    # Токен в сессии невалиден, очищаем сессию
                    request.session.pop('admin_jwt_token', None)
                    request.session.pop('admin_jwt_valid', None)
        
        if not has_token_in_url:
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
        Обрабатывает ответы, добавляя токен во все редиректы и ссылки админки.
        """
        # Проверяем, есть ли токен в сессии (для всех запросов, не только к админке)
        if hasattr(request, 'session'):
            session_token = request.session.get('admin_jwt_token')
            
            if session_token:
                # Обрабатываем редиректы (включая редиректы после логина, сохранения и т.д.)
                if isinstance(response, HttpResponseRedirect):
                    redirect_url = response.url
                    
                    # Если редирект на /admin/ или начинается с /admin/
                    if redirect_url.startswith('/admin/'):
                        # Убираем /admin/ и добавляем токен
                        admin_path = redirect_url[7:].lstrip('/')  # Убираем '/admin/'
                        # Обрабатываем query параметры
                        if '?' in admin_path:
                            path_part, query_part = admin_path.split('?', 1)
                            new_url = f'/admin/{session_token}/{path_part}?{query_part}'
                        else:
                            new_url = f'/admin/{session_token}/{admin_path}'
                        # Создаем новый HttpResponseRedirect с обновленным URL
                        response = HttpResponseRedirect(new_url)
                    # Если редирект на /admin (без слэша) - тоже обрабатываем
                    elif redirect_url == '/admin':
                        response = HttpResponseRedirect(f'/admin/{session_token}/')
                
                # Обрабатываем HTML ответы (только для запросов к админке)
                elif (request.path.startswith('/admin') and 
                      hasattr(response, 'content')):
                    content_type = response.get('Content-Type', '')
                    if isinstance(content_type, str) and content_type.startswith('text/html'):
                        try:
                            content = response.content.decode('utf-8')
                            
                            # Функция для замены URL
                            def replace_admin_url(match):
                                attr = match.group(1)  # href, action, src, data-url и т.д.
                                path = match.group(2).lstrip('/')  # путь после /admin/
                                return f'{attr}="/admin/{session_token}/{path}"'
                            
                            # Заменяем все ссылки на админку:
                            # 1. href="/admin/... и action="/admin/...
                            content = re.sub(
                                r'(href|action)=["\']/admin/([^"\']*)["\']',
                                replace_admin_url,
                                content
                            )
                            
                            # 2. data-url="/admin/... (для AJAX запросов)
                            content = re.sub(
                                r'(data-url|data-href|data-action)=["\']/admin/([^"\']*)["\']',
                                replace_admin_url,
                                content
                            )
                            
                            # 3. В JavaScript коде: "/admin/...
                            content = re.sub(
                                r'["\'](/admin/[^"\']*)["\']',
                                lambda m: f'"/admin/{session_token}/{m.group(1)[7:].lstrip("/")}"',
                                content
                            )
                            
                            # 4. Пустые action="" в формах заменяем на текущий URL с токеном
                            if '<form' in content:
                                current_path = request.path
                                if current_path.startswith('/admin/'):
                                    # Убираем /admin/ и добавляем токен
                                    path_after_admin = current_path[7:].lstrip('/')
                                    # Заменяем action="" на полный путь с токеном
                                    content = re.sub(
                                        r'action=["\']{2}',
                                        f'action="/admin/{session_token}/{path_after_admin}"',
                                        content
                                    )
                            
                            # 5. Обрабатываем CSRF токен в формах (может содержать ссылки)
                            # Django admin использует {% url %} теги, которые уже обработаны,
                            # но на всякий случай проверяем все относительные пути
                            
                            response.content = content.encode('utf-8')
                        except (UnicodeDecodeError, AttributeError, KeyError, Exception):
                            # Если не удалось обработать контент, просто пропускаем
                            pass
        
        return response
