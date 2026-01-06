"""
Админ-панель для модели Application.
"""
from django.contrib import admin
from landing.models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления заявками от клиентов.
    """
    list_display = (
        'name',
        'phone',
        'status',
        'is_sent_to_telegram',
        'created_at',
    )
    list_filter = (
        'status',
        'is_sent_to_telegram',
        'created_at',
    )
    search_fields = (
        'name',
        'phone',
        'message',
    )
    readonly_fields = (
        'uuid',
        'created_at',
        'updated_at',
        'is_sent_to_telegram',
        'telegram_error',
    )
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'phone', 'message')
        }),
        ('Статус', {
            'fields': ('status', 'is_sent_to_telegram', 'telegram_error')
        }),
        ('Системная информация', {
            'fields': ('uuid', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    def get_readonly_fields(self, request, obj=None):
        """
        Все поля только для чтения при создании, кроме статуса при редактировании.
        """
        if obj is None:
            return self.readonly_fields
        return self.readonly_fields

