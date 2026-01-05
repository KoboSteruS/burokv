"""
Импорт всех views из landing приложения.
"""
from .landing_view import LandingView
from .articles_view import ArticlesListView, ArticleDetailView

__all__ = ['LandingView', 'ArticlesListView', 'ArticleDetailView']

