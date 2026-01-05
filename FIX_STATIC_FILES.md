# Исправление проблемы с обновлением статических файлов

## Проблема
Изменения не отображаются на сервере, хотя на локальной машине всё работает.

## Причины и решения

### 1. WhiteNoise кэширует файлы с хэшами

WhiteNoise использует `CompressedManifestStaticFilesStorage`, который создает файлы с хэшами в именах (например, `style.abc123.css`). Если файлы не пересобраны, старые версии остаются.

**Решение:**
```bash
cd ~/burokv
source venv/bin/activate

# Удалить старые статические файлы
rm -rf staticfiles/*

# Пересобрать статические файлы
python manage.py collectstatic --noinput --clear

# Перезапустить Gunicorn
sudo systemctl restart burokv
```

### 2. Nginx кэширует статические файлы

Nginx может кэшировать статические файлы. Нужно проверить конфигурацию.

**Проверка конфигурации Nginx:**
```bash
cat /etc/nginx/sites-available/burokv | grep -A 5 "location /static"
```

**Временное отключение кэша (для тестирования):**
Добавь в конфигурацию Nginx:
```nginx
location /static/ {
    alias /root/burokv/staticfiles/;
    expires -1;  # Отключить кэш
    add_header Cache-Control "no-cache, no-store, must-revalidate";
    add_header Pragma "no-cache";
}
```

Затем:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

### 3. Файлы не обновились через Git

**Проверка:**
```bash
cd ~/burokv
git status
git log -1 --oneline
git pull origin main
```

### 4. Полная процедура обновления

```bash
cd ~/burokv

# 1. Получить изменения
git pull origin main

# 2. Активация venv
source venv/bin/activate

# 3. Удалить старые статические файлы
rm -rf staticfiles/*

# 4. Пересобрать статические файлы
python manage.py collectstatic --noinput --clear

# 5. Проверить, что файлы созданы
ls -lh staticfiles/css/

# 6. Перезапустить Gunicorn
sudo systemctl restart burokv

# 7. Перезагрузить Nginx (если нужно)
sudo systemctl reload nginx

# 8. Проверить логи
sudo journalctl -u burokv -n 20 --no-pager
```

### 5. Проверка версий файлов

```bash
# Проверь хэш CSS файла на сервере
md5sum static/css/style.css
md5sum staticfiles/css/style*.css

# Сравни с локальной версией (на локальной машине)
md5sum static/css/style.css
```

### 6. Если ничего не помогает

Временно отключи WhiteNoise и используй Nginx для статики:

В `config/settings.py` закомментируй:
```python
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

И убедись, что Nginx правильно настроен для статики.

