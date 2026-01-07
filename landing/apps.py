from django.apps import AppConfig
import os
import sys


class LandingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'landing'
    verbose_name = 'Лендинг'
    
    def ready(self):
        """Запуск при инициализации приложения."""
        # Запускаем Telegram polling в фоновом потоке (только при явном включении).
        #
        # Важно:
        # - Django autoreload в dev запускает приложение дважды -> 409 Conflict в Telegram getUpdates
        # - manage.py migrate/check/collectstatic не должны стартовать фоновые потоки
        from django.conf import settings

        if not getattr(settings, 'TELEGRAM_POLLING_ENABLED', False):
            return

        # Только runserver
        if len(sys.argv) < 2 or sys.argv[1] != 'runserver':
            return

        # Только основной процесс (защита от двойного старта при autoreload)
        if os.environ.get('RUN_MAIN') != 'true':
            return

        try:
            from landing.services.telegram_polling import TelegramPolling
            polling = TelegramPolling.get_instance()
            polling.start()
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f'Не удалось запустить Telegram polling: {e}')

