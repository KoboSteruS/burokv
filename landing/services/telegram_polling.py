"""
Фоновый polling для Telegram бота.
Запускается автоматически при старте Django приложения.
"""
import time
import threading
import requests
from django.conf import settings
from loguru import logger

from landing.models import TelegramSubscriber


class TelegramPolling:
    """
    Класс для фонового опроса Telegram бота.
    """
    _instance = None
    _thread = None
    _running = False
    
    def __init__(self):
        self.bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
        if not self.bot_token:
            logger.warning('TELEGRAM_BOT_TOKEN не установлен, polling не запущен')
            return
        
        self.api_url = f'https://api.telegram.org/bot{self.bot_token}'
        self.offset = 0
        self.interval = 5  # секунды
    
    @classmethod
    def get_instance(cls):
        """Получить единственный экземпляр."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def start(self):
        """Запустить polling в фоновом потоке."""
        if self._running:
            logger.warning('Telegram polling уже запущен')
            return
        
        if not self.bot_token:
            logger.warning('Не удалось запустить polling: нет токена')
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()
        logger.info('Telegram polling запущен')
    
    def stop(self):
        """Остановить polling."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info('Telegram polling остановлен')
    
    def _poll_loop(self):
        """Основной цикл опроса."""
        while self._running:
            try:
                self._process_updates()
                time.sleep(self.interval)
            except Exception as e:
                logger.error(f'Ошибка в polling цикле: {e}')
                time.sleep(self.interval)
    
    def _process_updates(self):
        """Обработать обновления от Telegram."""
        try:
            url = f'{self.api_url}/getUpdates'
            params = {
                'offset': self.offset,
                'timeout': 10,
                'allowed_updates': ['message', 'edited_message']
            }
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('ok'):
                logger.error(f'Ошибка получения обновлений: {data}')
                return
            
            updates = data.get('result', [])
            
            for update in updates:
                update_id = update.get('update_id', 0)
                self.offset = max(self.offset, update_id + 1)
                self._handle_update(update)
                
        except requests.RequestException as e:
            logger.error(f'Ошибка запроса к Telegram API: {e}')
        except Exception as e:
            logger.error(f'Ошибка обработки обновлений: {e}')
    
    def _handle_update(self, update: dict):
        """Обработать одно обновление."""
        message = update.get('message') or update.get('edited_message')
        if not message:
            return
        
        chat = message.get('chat', {})
        chat_id = str(chat.get('id'))
        text = message.get('text', '').strip()
        
        if text == '/start':
            user = message.get('from', {})
            username = user.get('username')
            first_name = user.get('first_name')
            last_name = user.get('last_name')
            
            subscriber, created = TelegramSubscriber.objects.update_or_create(
                chat_id=chat_id,
                defaults={
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                    'is_active': True,
                }
            )
            
            if created:
                logger.info(f'Новый подписчик: {subscriber}')
            else:
                logger.info(f'Подписчик обновлен: {subscriber}')
            
            # Отправляем приветствие
            self._send_welcome(chat_id)
    
    def _send_welcome(self, chat_id: str):
        """Отправить приветственное сообщение."""
        try:
            welcome_text = """<b>👋 Добро пожаловать!</b>

Вы подписаны на уведомления о новых заявках с сайта Бюро Квартир.

Теперь вы будете получать все новые заявки от клиентов."""
            
            url = f'{self.api_url}/sendMessage'
            payload = {
                'chat_id': chat_id,
                'text': welcome_text,
                'parse_mode': 'HTML'
            }
            
            requests.post(url, json=payload, timeout=10)
            logger.info(f'Приветствие отправлено в чат {chat_id}')
        except Exception as e:
            logger.error(f'Ошибка отправки приветствия: {e}')

