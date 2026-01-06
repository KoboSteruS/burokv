from django.apps import AppConfig


class LandingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'landing'
    verbose_name = 'Лендинг'
    
    def ready(self):
        """Запуск при инициализации приложения."""
        # Запускаем Telegram polling в фоновом потоке
        try:
            from landing.services.telegram_polling import TelegramPolling
            polling = TelegramPolling.get_instance()
            polling.start()
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f'Не удалось запустить Telegram polling: {e}')

