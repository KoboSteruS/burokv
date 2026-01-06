"""
Импорт всех админ-классов.
"""
from .service_admin import ServiceAdmin
from .property_admin import PropertyAdmin
from .article_admin import ArticleAdmin
from .team_member_admin import TeamMemberAdmin
from .application_admin import ApplicationAdmin
from .telegram_subscriber_admin import TelegramSubscriberAdmin

__all__ = ['ServiceAdmin', 'PropertyAdmin', 'ArticleAdmin', 'TeamMemberAdmin', 'ApplicationAdmin', 'TelegramSubscriberAdmin']

