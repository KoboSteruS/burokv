"""
Конфигурация Gunicorn для production.
"""
import multiprocessing
import os

# Количество воркеров (рекомендуется: количество CPU * 2 + 1)
workers = multiprocessing.cpu_count() * 2 + 1

# Путь к сокету
bind = "unix:/var/www/burokv/burokv.sock"

# Пользователь и группа
user = "www-data"
group = "www-data"

# Логирование
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

# Таймауты
timeout = 120
keepalive = 5

# Перезагрузка при изменении кода (только для разработки)
reload = False

# Предзагрузка приложения
preload_app = True

# Максимальное количество запросов на воркер перед перезапуском
max_requests = 1000
max_requests_jitter = 50

