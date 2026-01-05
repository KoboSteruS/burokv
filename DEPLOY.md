# Инструкция по деплою проекта Бюро Квартир

## Подготовка к production

### 1. Настройка переменных окружения

Создайте файл `.env` на основе `.env.production`:

```bash
cp .env.production .env
```

Отредактируйте `.env` и укажите:

```env
# ОБЯЗАТЕЛЬНО измените секретный ключ!
SECRET_KEY=ваш-уникальный-секретный-ключ-минимум-50-символов

# Отключите debug в production
DEBUG=False

# Укажите ваш домен
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Для PostgreSQL (рекомендуется)
DATABASE_URL=postgresql://user:password@localhost:5432/burokv_db
```

### 2. Генерация SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Скопируйте результат в `.env` файл.

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка базы данных

#### Для SQLite (только для разработки):
```bash
python manage.py migrate
```

#### Для PostgreSQL (рекомендуется для production):

1. Установите PostgreSQL
2. Создайте базу данных:
```sql
CREATE DATABASE burokv_db;
CREATE USER burokv_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE burokv_db TO burokv_user;
```

3. Обновите `.env`:
```env
DATABASE_URL=postgresql://burokv_user:your_password@localhost:5432/burokv_db
```

4. Примените миграции:
```bash
python manage.py migrate
```

### 5. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 6. Сбор статических файлов

```bash
python manage.py collectstatic --noinput
```

### 7. Загрузка медиа файлов

Убедитесь, что папка `media/` существует и доступна для записи:
```bash
mkdir -p media/properties media/articles media/services/icons media/team
chmod -R 755 media/
```

## Деплой на сервер

### Вариант 1: Деплой на Linux сервер (Ubuntu/Debian)

#### 1. Подготовка сервера

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и зависимостей
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib nginx -y

# Установка Git
sudo apt install git -y
```

#### 2. Клонирование проекта

```bash
cd /var/www
sudo git clone <your-repo-url> burokv
sudo chown -R $USER:$USER burokv
cd burokv
```

#### 3. Настройка виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. Настройка .env

```bash
cp .env.production .env
nano .env  # Отредактируйте файл
```

#### 5. Настройка базы данных

```bash
# Создайте базу данных PostgreSQL
sudo -u postgres psql
CREATE DATABASE burokv_db;
CREATE USER burokv_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE burokv_db TO burokv_user;
\q
```

#### 6. Применение миграций

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

#### 7. Настройка Gunicorn

Создайте файл `/etc/systemd/system/burokv.service`:

```ini
[Unit]
Description=BuroKV Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/burokv
Environment="PATH=/var/www/burokv/venv/bin"
ExecStart=/var/www/burokv/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/burokv/burokv.sock \
    config.wsgi:application

[Install]
WantedBy=multi-user.target
```

Запустите сервис:
```bash
sudo systemctl start burokv
sudo systemctl enable burokv
```

#### 8. Настройка Nginx

Создайте файл `/etc/nginx/sites-available/burokv`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location /static/ {
        alias /var/www/burokv/staticfiles/;
    }

    location /media/ {
        alias /var/www/burokv/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/burokv/burokv.sock;
    }
}
```

Активируйте конфигурацию:
```bash
sudo ln -s /etc/nginx/sites-available/burokv /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 9. Настройка SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Вариант 2: Деплой на Heroku

#### 1. Установка Heroku CLI

```bash
# Windows
# Скачайте с https://devcenter.heroku.com/articles/heroku-cli

# Linux/Mac
curl https://cli-assets.heroku.com/install.sh | sh
```

#### 2. Создание файлов для Heroku

Создайте `Procfile`:
```
web: gunicorn config.wsgi --log-file -
```

Создайте `runtime.txt`:
```
python-3.11.0
```

#### 3. Деплой

```bash
heroku login
heroku create burokv-app
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
heroku config:set ALLOWED_HOSTS=burokv-app.herokuapp.com

git push heroku main

heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Вариант 3: Деплой на PythonAnywhere

1. Загрузите код через Git или файловый менеджер
2. Настройте виртуальное окружение
3. Установите зависимости
4. Настройте базу данных
5. Настройте статические файлы
6. Настройте WSGI файл

## Проверка после деплоя

1. Проверьте доступность сайта
2. Проверьте админ-панель: `https://yourdomain.com/admin/`
3. Проверьте статические файлы
4. Проверьте загрузку медиа файлов
5. Проверьте работу форм

## Безопасность

- ✅ DEBUG=False в production
- ✅ SECRET_KEY должен быть уникальным и сложным
- ✅ SSL сертификат (HTTPS)
- ✅ Защита от XSS и CSRF
- ✅ Безопасные cookies
- ✅ HSTS заголовки

## Мониторинг и логи

Проверка логов Gunicorn:
```bash
sudo journalctl -u burokv -f
```

Проверка логов Nginx:
```bash
sudo tail -f /var/log/nginx/error.log
```

## Резервное копирование

Настройте автоматическое резервное копирование базы данных:
```bash
# Добавьте в crontab
0 2 * * * pg_dump -U burokv_user burokv_db > /backup/burokv_$(date +\%Y\%m\%d).sql
```

## Обновление проекта

```bash
cd /var/www/burokv
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart burokv
```

