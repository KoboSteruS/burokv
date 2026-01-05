"""
Модель объекта недвижимости (наши работы).
"""
from django.db import models
from core.models import BaseModel


class PropertyType(models.TextChoices):
    """Типы недвижимости."""
    APARTMENT = 'apartment', 'Квартира'
    HOUSE = 'house', 'Дом'
    COTTAGE = 'cottage', 'Коттедж'
    COMMERCIAL = 'commercial', 'Коммерческая недвижимость'
    LAND = 'land', 'Земельный участок'


class Property(BaseModel):
    """
    Модель объекта недвижимости (примеры проданных объектов).
    
    Содержит информацию о проданных объектах для демонстрации на сайте.
    """
    title = models.CharField(
        max_length=200,
        verbose_name='Название объекта'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    location = models.CharField(
        max_length=300,
        verbose_name='Местоположение'
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Цена продажи'
    )
    property_type = models.CharField(
        max_length=50,
        choices=PropertyType.choices,
        default=PropertyType.APARTMENT,
        verbose_name='Тип недвижимости'
    )
    image = models.ImageField(
        upload_to='properties/',
        verbose_name='Изображение'
    )
    is_sold = models.BooleanField(
        default=True,
        verbose_name='Продано'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок отображения'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Отображать на сайте'
    )

    class Meta:
        verbose_name = 'Объект недвижимости'
        verbose_name_plural = 'Объекты недвижимости'
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.location}"

