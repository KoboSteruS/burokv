"""
Модель заявки от клиента.
"""
from django.db import models
from core.models import BaseModel


class Application(BaseModel):
    """
    Модель заявки от клиента.
    
    Содержит информацию о заявке:
    - имя, телефон, сообщение
    - статус обработки
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Имя клиента'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон'
    )
    message = models.TextField(
        blank=True,
        null=True,
        verbose_name='Сообщение'
    )
    
    class Status(models.TextChoices):
        NEW = 'new', 'Новая'
        PROCESSED = 'processed', 'Обработана'
        REJECTED = 'rejected', 'Отклонена'
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name='Статус'
    )
    
    is_sent_to_telegram = models.BooleanField(
        default=False,
        verbose_name='Отправлено в Telegram'
    )
    
    telegram_error = models.TextField(
        blank=True,
        null=True,
        verbose_name='Ошибка отправки в Telegram'
    )

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.phone} ({self.get_status_display()})'

