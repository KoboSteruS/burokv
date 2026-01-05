"""
URL конфигурация для landing приложения.
"""
from django.urls import path
from landing.views import LandingView, ArticlesListView, ArticleDetailView

app_name = 'landing'

urlpatterns = [
    path('', LandingView.as_view(), name='index'),
    path('articles/', ArticlesListView.as_view(), name='articles_list'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
]

