# Инструкция по обновлению на сервере через Git

## Быстрое обновление

Выполни на сервере:

```bash
cd ~/burokv

# 1. Получить последние изменения
git pull origin main

# 2. Активация виртуального окружения
source venv/bin/activate

# 3. Обновление зависимостей (если requirements.txt изменился)
pip install -r requirements.txt

# 4. Применение миграций (если есть новые)
python manage.py migrate

# 5. Сбор статических файлов (ОБЯЗАТЕЛЬНО для CSS/JS изменений!)
python manage.py collectstatic --noinput --clear

# 6. Перезапуск Gunicorn
sudo systemctl restart burokv

# 7. Проверка статуса
sudo systemctl status burokv --no-pager -l
```

## Важные моменты

1. **Статические файлы** - всегда выполняй `collectstatic` после обновления CSS/JS
2. **Перезапуск Gunicorn** - обязателен после изменений в Python коде
3. **Кэш браузера** - очисти кэш браузера (Ctrl+F5) после обновления

## Проверка обновления

```bash
# Проверь, что файлы обновились
ls -la core/middleware/admin_jwt_middleware.py
ls -la static/css/style.css

# Проверь логи
sudo journalctl -u burokv -n 50 --no-pager

# Проверь статические файлы
ls -la staticfiles/css/
```

## Если что-то не работает

1. Проверь логи: `sudo journalctl -u burokv -f`
2. Проверь, что файлы загружены: `git status`
3. Проверь права доступа: `ls -la`
4. Перезапусти Nginx: `sudo systemctl restart nginx`

