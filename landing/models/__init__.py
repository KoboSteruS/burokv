"""
Импорт всех моделей из landing приложения.
"""
from .service import Service
from .property import Property
from .article import Article
from .team_member import TeamMember

__all__ = ['Service', 'Property', 'Article', 'TeamMember']

