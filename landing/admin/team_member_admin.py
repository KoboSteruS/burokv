"""
Админ-панель для управления членами команды.
"""
from django.contrib import admin
from landing.models import TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    """
    Админ-класс для управления членами команды.
    """
    list_display = ['name', 'position', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'position']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'position', 'photo')
        }),
        ('Настройки отображения', {
            'fields': ('order', 'is_active')
        }),
        ('Системная информация', {
            'fields': ('uuid', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['uuid', 'created_at', 'updated_at']

