"""
Views для лендинга компании Бюро Квартир.
"""
from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.db.utils import OperationalError, ProgrammingError
from loguru import logger

from landing.models import Service, Property, Article, TeamMember, Application
from landing.services import TelegramService


class LandingView(TemplateView):
    """
    Главная страница лендинга.
    
    Отображает все основные разделы:
    - Услуги компании
    - Примеры проданных объектов
    - Последние статьи
    
    Обрабатывает POST запросы от формы заявки и отправляет их в Telegram.
    """
    template_name = 'landing/index.html'

    def get_context_data(self, **kwargs):
        """
        Получение контекста для шаблона.
        
        Returns:
            dict: Контекст с данными для отображения на главной странице
        """
        context = super().get_context_data(**kwargs)

        # Важно: при первом запуске на новом ПК БД может быть пустой/без миграций.
        # Вместо падения страницы отдаём пустые списки и пишем понятный лог.
        try:
            # Получаем активные услуги, отсортированные по порядку
            context['services'] = Service.objects.filter(is_active=True).order_by('order', 'created_at')

            # Получаем активных членов команды, отсортированных по порядку
            context['team_members'] = TeamMember.objects.filter(is_active=True).order_by('order', 'created_at')

            # Получаем активные объекты недвижимости, отсортированные по порядку
            context['properties'] = Property.objects.filter(is_active=True).order_by('order', '-created_at')[:3]

            # Получаем опубликованные статьи, отсортированные по дате публикации
            context['articles'] = Article.objects.filter(is_published=True).order_by('-published_at')[:3]
        except (OperationalError, ProgrammingError) as e:
            logger.warning(
                "База данных не инициализирована или миграции не применены. "
                "Откройте терминал и выполните: python manage.py migrate. "
                "Техническая причина: {error}",
                error=str(e),
            )
            context['services'] = Service.objects.none()
            context['team_members'] = TeamMember.objects.none()
            context['properties'] = Property.objects.none()
            context['articles'] = Article.objects.none()
        
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Обработка POST запроса от формы заявки.
        
        Получает данные формы, сохраняет заявку в БД и отправляет в Telegram.
        
        Returns:
            HttpResponseRedirect: Редирект на главную страницу с сообщением
        """
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Валидация обязательных полей
        if not name or not phone:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля.')
            return redirect(reverse('landing:index') + '#contact-form')
        
        # Создаем заявку в БД
        try:
            application = Application.objects.create(
                name=name,
                phone=phone,
                message=message if message else None
            )
            logger.info(f'Создана новая заявка: {application}')
        except (OperationalError, ProgrammingError) as e:
            logger.error(
                "Заявка не сохранена: база данных не инициализирована (нет таблиц). "
                "Выполните миграции: python manage.py migrate. Причина: {error}",
                error=str(e),
            )
            messages.error(request, 'Сервер не готов: база данных не инициализирована. Обратитесь к администратору.')
            return redirect(reverse('landing:index') + '#contact-form')
        except Exception as e:
            logger.error(f'Ошибка создания заявки: {e}')
            messages.error(request, 'Произошла ошибка при отправке заявки. Попробуйте позже.')
            return redirect(reverse('landing:index') + '#contact-form')
        
        # Отправляем в Telegram
        try:
            telegram_service = TelegramService()
            result = telegram_service.send_application(name, phone, message)
            
            if result.get('ok') or result.get('sent_count', 0) > 0:
                application.is_sent_to_telegram = True
                application.save(update_fields=['is_sent_to_telegram'])
                messages.success(request, 'Спасибо! Ваша заявка успешно отправлена. Мы свяжемся с вами в ближайшее время.')
                logger.info(f'Заявка {application} успешно отправлена в Telegram. Отправлено: {result.get("sent_count", 0)}')
            else:
                error_msg = result.get('error', 'Неизвестная ошибка')
                application.telegram_error = error_msg
                application.save(update_fields=['telegram_error'])
                messages.warning(request, 'Заявка сохранена, но произошла ошибка при отправке уведомления. Мы обработаем вашу заявку вручную.')
                logger.warning(f'Ошибка отправки заявки {application} в Telegram: {error_msg}')
        except Exception as e:
            error_msg = str(e)
            application.telegram_error = error_msg
            application.save(update_fields=['telegram_error'])
            messages.warning(request, 'Заявка сохранена, но произошла ошибка при отправке уведомления. Мы обработаем вашу заявку вручную.')
            logger.error(f'Критическая ошибка отправки заявки {application} в Telegram: {error_msg}')
        
        return redirect(reverse('landing:index') + '#contact-form')

