# Быстрый старт для деплоя

## 🚀 Быстрая настройка для production

### 1. Создайте .env файл

```bash
# Скопируйте пример
cp .env.production .env

# Или создайте вручную
nano .env
```

**ОБЯЗАТЕЛЬНО заполните:**
```env
SECRET_KEY=сгенерируйте-новый-ключ-минимум-50-символов
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

**Генерация SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Установите зависимости

```bash
pip install -r requirements.txt
```

### 3. Настройте базу данных

**Для SQLite (только разработка):**
```bash
python manage.py migrate
```

**Для PostgreSQL (production):**
```env
# В .env добавьте:
DATABASE_URL=postgresql://user:password@localhost:5432/burokv_db
```

```bash
python manage.py migrate
```

### 4. Создайте суперпользователя

```bash
python manage.py createsuperuser
```

### 5. Соберите статические файлы

```bash
python manage.py collectstatic --noinput
```

### 6. Запустите сервер

**Для разработки:**
```bash
python manage.py runserver
```

**Для production (с Gunicorn):**
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## 📋 Чеклист перед деплоем

- [ ] `.env` файл создан и заполнен
- [ ] `SECRET_KEY` изменен на уникальный
- [ ] `DEBUG=False` в production
- [ ] `ALLOWED_HOSTS` содержит ваш домен
- [ ] База данных настроена (PostgreSQL для production)
- [ ] Миграции применены
- [ ] Суперпользователь создан
- [ ] Статические файлы собраны
- [ ] Медиа папки созданы и доступны для записи
- [ ] SSL сертификат настроен (HTTPS)
- [ ] Gunicorn настроен
- [ ] Nginx настроен (если используется)

## 🔧 Полезные команды

```bash
# Проверка настроек Django
python manage.py check --deploy

# Создание резервной копии БД
python manage.py dumpdata > backup.json

# Загрузка резервной копии
python manage.py loaddata backup.json

# Обновление проекта
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

## 📚 Подробная документация

См. `DEPLOY.md` для детальных инструкций по деплою на различные платформы.
