"""
Админ-панель для модели TelegramSubscriber.
"""
from django.contrib import admin
from landing.models import TelegramSubscriber


@admin.register(TelegramSubscriber)
class TelegramSubscriberAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления подписчиками Telegram бота.
    """
    list_display = (
        'get_full_name',
        'username',
        'chat_id',
        'is_active',
        'created_at',
    )
    list_filter = (
        'is_active',
        'created_at',
    )
    search_fields = (
        'chat_id',
        'username',
        'first_name',
        'last_name',
    )
    readonly_fields = (
        'uuid',
        'created_at',
        'updated_at',
    )
    fieldsets = (
        ('Информация о пользователе', {
            'fields': ('chat_id', 'username', 'first_name', 'last_name')
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
        ('Системная информация', {
            'fields': ('uuid', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    def get_full_name(self, obj):
        """Отображение полного имени в списке."""
        return obj.get_full_name()
    get_full_name.short_description = 'Имя'

