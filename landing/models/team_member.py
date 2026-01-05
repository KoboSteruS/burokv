"""
Модель члена команды компании.
"""
from django.db import models
from core.models import BaseModel


class TeamMember(BaseModel):
    """
    Модель члена команды компании Бюро Квартир.
    
    Содержит информацию о сотрудниках компании:
    - имя, должность, фото
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Имя'
    )
    position = models.CharField(
        max_length=200,
        verbose_name='Должность'
    )
    photo = models.ImageField(
        upload_to='team/',
        verbose_name='Фото'
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
        verbose_name = 'Член команды'
        verbose_name_plural = 'Члены команды'
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.name} - {self.position}"

