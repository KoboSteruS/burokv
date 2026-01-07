# Инструкция по установке и запуску

## Быстрый старт

### Windows

1. Запустите `run.bat` - скрипт автоматически:
   - Создаст виртуальное окружение (если его нет)
   - Установит зависимости
   - Применит миграции
   - Запустит сервер

2. Или выполните вручную:

```bash
# Создание виртуального окружения
python -m venv venv

# Активация
venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt

# Создание .env файла
copy .env.example .env

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Запуск сервера
python manage.py runserver
```

### Linux/Mac

```bash
# Создание виртуального окружения
python3 -m venv venv

# Активация
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Создание .env файла
cp .env.example .env

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Запуск сервера
python manage.py runserver
```

## Первоначальная настройка

1. **Создайте файл `.env`** на основе `.env.example`:
   ```env
   SECRET_KEY=ваш-секретный-ключ
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   TELEGRAM_BOT_TOKEN=   # опционально, если нужен Telegram
   TELEGRAM_POLLING_ENABLED=False
   ```

2. **Создайте суперпользователя** для доступа к админ-панели:
   ```bash
   python manage.py createsuperuser
   ```

3. **Откройте админ-панель**: http://127.0.0.1:8000/admin/

4. **Добавьте контент**:
   - Услуги компании
   - Примеры проданных объектов
   - Статьи и новости

## Структура данных

### Услуги
- Название
- Описание
- Иконка (CSS класс)
- Порядок отображения
- Активна/неактивна

### Объекты недвижимости
- Название
- Описание
- Местоположение
- Цена
- Тип недвижимости
- Изображение
- Статус продажи
- Порядок отображения

### Статьи
- Заголовок
- URL (slug)
- Краткое описание
- Содержание
- Изображение
- Дата публикации
- Опубликовано/не опубликовано
- Порядок отображения

## Решение проблем

### Ошибка импорта модулей
Убедитесь, что все приложения правильно установлены в `INSTALLED_APPS` в `config/settings.py`

### Ошибка `ModuleNotFoundError: No module named 'pkg_resources'`
На Python 3.12 в виртуальном окружении может отсутствовать `setuptools` (а `pkg_resources` находится именно там).

Решение:
```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

### Ошибка статических файлов
Выполните:
```bash
python manage.py collectstatic --noinput
```

### Ошибка `OperationalError: no such table ...`
Это означает, что миграции не применены (обычно на новом ПК или если удалили `db.sqlite3`).

Решение:
```bash
python manage.py migrate
```

Если миграции “не видятся” (редко), выполните:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Ошибка миграций
```bash
python manage.py makemigrations
python manage.py migrate
```

### Проблемы с изображениями
Убедитесь, что папки `media/properties` и `media/articles` существуют и доступны для записи.

