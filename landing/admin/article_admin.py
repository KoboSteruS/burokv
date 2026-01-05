"""
Админ-панель для управления статьями.
"""
from django.contrib import admin
from landing.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Админ-класс для управления статьями и новостями.
    """
    list_display = ['title', 'published_at', 'is_published', 'order', 'created_at']
    list_filter = ['is_published', 'published_at', 'created_at']
    search_fields = ['title', 'short_description', 'content']
    list_editable = ['order', 'is_published']
    ordering = ['order', '-published_at']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'short_description')
        }),
        ('Содержание', {
            'fields': ('content',)
        }),
        ('Медиа', {
            'fields': ('image',)
        }),
        ('Публикация', {
            'fields': ('published_at', 'is_published', 'order')
        }),
        ('Системная информация', {
            'fields': ('uuid', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['uuid', 'created_at', 'updated_at']

