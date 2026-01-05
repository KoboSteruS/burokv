"""
Админ-панель для landing приложения.
Модели регистрируются через декораторы в отдельных файлах.
"""
# Импортируем админ-классы для их регистрации через декораторы
from landing.admin.service_admin import ServiceAdmin  # noqa
from landing.admin.property_admin import PropertyAdmin  # noqa
from landing.admin.article_admin import ArticleAdmin  # noqa
from landing.admin.team_member_admin import TeamMemberAdmin  # noqa

