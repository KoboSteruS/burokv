"""
Сервис для отправки сообщений в Telegram бота.
"""
import requests
from typing import Optional
from django.conf import settings
from loguru import logger


class TelegramService:
    """
    Сервис для отправки сообщений в Telegram бота.
    
    Использует Telegram Bot API для отправки сообщений всем подписчикам бота.
    """
    
    BASE_URL = 'https://api.telegram.org/bot'
    
    def __init__(self, bot_token: Optional[str] = None):
        """
        Инициализация сервиса.
        
        Args:
            bot_token: Токен Telegram бота. Если не указан, берется из settings.
        """
        self.bot_token = bot_token or getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
        if not self.bot_token:
            raise ValueError('TELEGRAM_BOT_TOKEN не установлен в settings или не передан в конструктор')
        
        self.api_url = f"{self.BASE_URL}{self.bot_token}"
    
    def send_message(self, text: str, chat_id: Optional[str] = None) -> dict:
        """
        Отправка сообщения в Telegram.
        
        Args:
            text: Текст сообщения для отправки
            chat_id: ID чата для отправки. Если не указан, отправляется всем подписчикам.
        
        Returns:
            dict: Ответ от Telegram API
        
        Raises:
            requests.RequestException: При ошибке отправки запроса
        """
        if chat_id:
            # Отправка в конкретный чат
            return self._send_to_chat(chat_id, text)
        else:
            # Отправка всем активным подписчикам из БД
            return self._broadcast_message(text)
    
    def _send_to_chat(self, chat_id: str, text: str) -> dict:
        """
        Отправка сообщения в конкретный чат.
        
        Args:
            chat_id: ID чата
            text: Текст сообщения
        
        Returns:
            dict: Ответ от Telegram API
        """
        url = f"{self.api_url}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f'Ошибка отправки сообщения в Telegram: {e}')
            raise
    
    def _broadcast_message(self, text: str) -> dict:
        """
        Отправка сообщения всем подписчикам бота.
        
        Получает список всех активных подписчиков из БД и отправляет сообщение каждому.
        
        Args:
            text: Текст сообщения
        
        Returns:
            dict: Результат отправки с количеством успешных и неуспешных отправок
        """
        try:
            from landing.models import TelegramSubscriber
            
            # Получаем всех активных подписчиков из БД
            subscribers = TelegramSubscriber.objects.filter(is_active=True)
            chat_ids = [subscriber.chat_id for subscriber in subscribers]
            
            if not chat_ids:
                logger.warning('Не найдено ни одного активного подписчика для отправки сообщения')
                return {
                    'ok': False,
                    'error': 'Не найдено ни одного активного подписчика',
                    'sent_count': 0,
                    'failed_count': 0
                }
            
            logger.info(f'Найдено {len(chat_ids)} активных подписчиков для отправки')
            
            sent_count = 0
            failed_count = 0
            errors = []
            
            # Отправляем сообщение каждому подписчику
            for chat_id in chat_ids:
                try:
                    self._send_to_chat(chat_id, text)
                    sent_count += 1
                    logger.info(f'Сообщение успешно отправлено в чат {chat_id}')
                except Exception as e:
                    failed_count += 1
                    error_msg = f'Ошибка отправки в чат {chat_id}: {str(e)}'
                    errors.append(error_msg)
                    logger.error(error_msg)
            
            return {
                'ok': True,
                'sent_count': sent_count,
                'failed_count': failed_count,
                'errors': errors if errors else None
            }
        except ImportError:
            logger.error('Не удалось импортировать TelegramSubscriber')
            return {
                'ok': False,
                'error': 'Ошибка импорта модели TelegramSubscriber',
                'sent_count': 0,
                'failed_count': 0
            }
    
    
    def send_application(self, name: str, phone: str, message: str = '') -> dict:
        """
        Отправка заявки от клиента в Telegram.
        
        Форматирует заявку в читаемый вид и отправляет всем подписчикам.
        
        Args:
            name: Имя клиента
            phone: Телефон клиента
            message: Сообщение от клиента (опционально)
        
        Returns:
            dict: Результат отправки
        """
        text = f"""
<b>📋 Новая заявка с сайта</b>

<b>Имя:</b> {name}
<b>Телефон:</b> {phone}
"""
        
        if message:
            text += f"\n<b>Сообщение:</b>\n{message}"
        
        text += f"\n\n<i>Время:</i> {self._get_current_time()}"
        
        # Проверяем, есть ли указанный chat_id в настройках
        from django.conf import settings
        chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', None)
        
        if chat_id:
            # Отправляем в указанный чат/группу/канал
            return self.send_message(text, chat_id=chat_id)
        else:
            # Отправляем всем подписчикам
            return self.send_message(text)
    
    @staticmethod
    def _get_current_time() -> str:
        """
        Получение текущего времени в читаемом формате.
        
        Returns:
            str: Текущее время
        """
        from django.utils import timezone
        from django.utils.dateformat import format
        
        return format(timezone.now(), 'd.m.Y H:i')

