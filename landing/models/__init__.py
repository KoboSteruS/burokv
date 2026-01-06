"""
Импорт всех моделей из landing приложения.
"""
from .service import Service
from .property import Property
from .article import Article
from .team_member import TeamMember
from .application import Application
from .telegram_subscriber import TelegramSubscriber

__all__ = ['Service', 'Property', 'Article', 'TeamMember', 'Application', 'TelegramSubscriber']

