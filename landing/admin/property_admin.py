"""
Админ-панель для управления объектами недвижимости.
"""
from django.contrib import admin
from landing.models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    """
    Админ-класс для управления объектами недвижимости.
    """
    list_display = ['title', 'location', 'price', 'property_type', 'is_sold', 'is_active', 'order']
    list_filter = ['property_type', 'is_sold', 'is_active', 'created_at']
    search_fields = ['title', 'location', 'description']
    list_editable = ['order', 'is_active', 'is_sold']
    ordering = ['order', '-created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'location', 'property_type')
        }),
        ('Финансовая информация', {
            'fields': ('price', 'is_sold')
        }),
        ('Медиа', {
            'fields': ('image',)
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

