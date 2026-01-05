"""
Views для страниц статей.
"""
from django.views.generic import ListView, DetailView
from landing.models import Article


class ArticlesListView(ListView):
    """
    Страница со списком всех статей.
    """
    model = Article
    template_name = 'landing/articles_list.html'
    context_object_name = 'articles'
    paginate_by = 10
    
    def get_queryset(self):
        """
        Получение опубликованных статей, отсортированных по дате публикации.
        
        Returns:
            QuerySet: Опубликованные статьи
        """
        return Article.objects.filter(is_published=True).order_by('-published_at')


class ArticleDetailView(DetailView):
    """
    Детальная страница статьи.
    """
    model = Article
    template_name = 'landing/article_detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        """
        Получение только опубликованных статей.
        
        Returns:
            QuerySet: Опубликованные статьи
        """
        return Article.objects.filter(is_published=True)

