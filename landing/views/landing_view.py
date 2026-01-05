"""
Views для лендинга компании Бюро Квартир.
"""
from django.views.generic import TemplateView
from landing.models import Service, Property, Article, TeamMember


class LandingView(TemplateView):
    """
    Главная страница лендинга.
    
    Отображает все основные разделы:
    - Услуги компании
    - Примеры проданных объектов
    - Последние статьи
    """
    template_name = 'landing/index.html'

    def get_context_data(self, **kwargs):
        """
        Получение контекста для шаблона.
        
        Returns:
            dict: Контекст с данными для отображения на главной странице
        """
        context = super().get_context_data(**kwargs)
        
        # Получаем активные услуги, отсортированные по порядку
        context['services'] = Service.objects.filter(is_active=True).order_by('order', 'created_at')
        
        # Получаем активных членов команды, отсортированных по порядку
        context['team_members'] = TeamMember.objects.filter(is_active=True).order_by('order', 'created_at')
        
        # Получаем активные объекты недвижимости, отсортированные по порядку
        context['properties'] = Property.objects.filter(is_active=True).order_by('order', '-created_at')[:3]
        
        # Получаем опубликованные статьи, отсортированные по дате публикации
        context['articles'] = Article.objects.filter(is_published=True).order_by('-published_at')[:3]
        
        return context

