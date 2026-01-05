"""
Админ-панель для управления услугами.
"""
from django.contrib import admin
from landing.models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    Админ-класс для управления услугами компании.
    """
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'icon')
        }),
        ('Настройки отображения', {
            'fields': ('order', 'is_active')
        }),
        ('Системная информация', {
            'fields': ('uuid', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        """Переопределение формы для улучшения отображения загрузки изображений."""
        form = super().get_form(request, obj, **kwargs)
        return form
    
    readonly_fields = ['uuid', 'created_at', 'updated_at']

