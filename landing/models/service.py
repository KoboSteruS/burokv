"""
Модель услуги компании.
"""
from django.db import models
from core.models import BaseModel


class Service(BaseModel):
    """
    Модель услуги компании Бюро Квартир.
    
    Содержит информацию об услугах, предоставляемых компанией:
    - название, описание, иконка
    """
    title = models.CharField(
        max_length=200,
        verbose_name='Название услуги'
    )
    description = models.TextField(
        verbose_name='Описание услуги'
    )
    icon = models.ImageField(
        upload_to='services/icons/',
        blank=True,
        null=True,
        verbose_name='Иконка'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок отображения'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна'
    )

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.title

