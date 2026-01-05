"""
Модель статьи/новости.
"""
from django.db import models
from core.models import BaseModel


class Article(BaseModel):
    """
    Модель статьи или новости для блога компании.
    
    Содержит информацию о статьях, публикуемых на сайте.
    """
    title = models.CharField(
        max_length=300,
        verbose_name='Заголовок'
    )
    slug = models.SlugField(
        max_length=300,
        unique=True,
        verbose_name='URL-адрес'
    )
    short_description = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Краткое описание'
    )
    content = models.TextField(
        verbose_name='Содержание статьи'
    )
    image = models.ImageField(
        upload_to='articles/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    published_at = models.DateTimeField(
        verbose_name='Дата публикации'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок отображения'
    )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['order', '-published_at']

    def __str__(self):
        return self.title

