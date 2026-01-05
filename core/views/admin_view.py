"""
Кастомный view для админ-панели с проверкой JWT токена.
"""
from django.contrib import admin
from django.http import HttpResponseForbidden
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
import jwt


class AdminSiteWithJWT(admin.AdminSite):
    """
    Кастомный AdminSite с проверкой JWT токена.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.site_header = 'Бюро Квартир - Админ-панель'
        self.site_title = 'Бюро Квартир'
        self.index_title = 'Администрирование'
    
    def check_jwt_token(self, request, token):
        """
        Проверяет JWT токен.
        """
        jwt_secret = getattr(settings, 'ADMIN_JWT_SECRET', None)
        
        if not jwt_secret:
            # Если секрет не настроен, разрешаем доступ (для разработки)
            return True
        
        try:
            decoded = jwt.decode(
                token,
                jwt_secret,
                algorithms=['HS256']
            )
            
            # Проверяем тип токена
            if decoded.get('type') != 'admin_access':
                return False
            
            return True
            
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return False
        except Exception:
            return False


# Создаем кастомный экземпляр AdminSite
admin_site = AdminSiteWithJWT(name='admin')


def admin_view_with_jwt(request, jwt_token, extra_context=None):
    """
    View для админ-панели с проверкой JWT токена.
    """
    jwt_secret = getattr(settings, 'ADMIN_JWT_SECRET', None)
    
    if not jwt_secret:
        # Если секрет не настроен, используем стандартную админку
        return admin.site.index(request)
    
    # Проверяем токен
    try:
        decoded = jwt.decode(
            jwt_token,
            jwt_secret,
            algorithms=['HS256']
        )
        
        # Проверяем тип токена
        if decoded.get('type') != 'admin_access':
            return HttpResponseForbidden('Неверный тип токена')
        
        # Токен валиден, отображаем админку
        # Используем стандартный admin.site, но с проверенным токеном
        return admin.site.index(request)
        
    except jwt.ExpiredSignatureError:
        return HttpResponseForbidden('Токен истек. Сгенерируйте новый токен.')
    except jwt.InvalidTokenError as e:
        return HttpResponseForbidden(f'Невалидный токен: {str(e)}')
    except Exception as e:
        return HttpResponseForbidden(f'Ошибка проверки токена: {str(e)}')

