"""
Главный URL конфигуратор проекта.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Админ-панель защищена JWT токеном в URL: /admin/<token>/
    # Токен генерируется командой: python manage.py generate_admin_token
    # Middleware проверяет токен и преобразует путь из /admin/<token>/ в /admin/
    # Поэтому здесь используем стандартный паттерн
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

