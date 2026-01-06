"""
Модель подписчика Telegram бота.
"""
from django.db import models
from core.models import BaseModel


class TelegramSubscriber(BaseModel):
    """
    Модель подписчика Telegram бота.
    
    Сохраняет chat_id пользователей, которые написали /start боту.
    """
    chat_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Chat ID',
        help_text='Уникальный идентификатор чата в Telegram'
    )
    username = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Username',
        help_text='Username пользователя в Telegram (если указан)'
    )
    first_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Имя',
        help_text='Имя пользователя в Telegram'
    )
    last_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Фамилия',
        help_text='Фамилия пользователя в Telegram'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен',
        help_text='Получает ли пользователь уведомления'
    )

    class Meta:
        verbose_name = 'Подписчик Telegram'
        verbose_name_plural = 'Подписчики Telegram'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['chat_id']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        name = self.username or f"{self.first_name or ''} {self.last_name or ''}".strip() or 'Без имени'
        return f"{name} ({self.chat_id})"
    
    def get_full_name(self):
        """Получить полное имя пользователя."""
        parts = [self.first_name, self.last_name]
        return ' '.join(filter(None, parts)) or self.username or 'Без имени'

