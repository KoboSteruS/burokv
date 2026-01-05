# Быстрый старт - Решение проблем установки

## Проблема с Pillow и Python 3.13

Если у вас Python 3.13 и возникают проблемы с установкой Pillow, выполните следующие шаги:

### Вариант 1: Установка минимальных зависимостей (рекомендуется)

```bash
# Сначала установите только Django и Pillow
pip install Django>=4.2.7 Pillow>=10.3.0

# Затем установите остальные зависимости
pip install -r requirements.txt
```

### Вариант 2: Установка без виртуального окружения (если проблемы с правами)

```bash
# Установка с флагом --user
pip install --user -r requirements.txt
```

### Вариант 3: Использование виртуального окружения (рекомендуется)

```bash
# Создайте виртуальное окружение
python -m venv venv

# Активация (Windows)
venv\Scripts\activate

# Активация (Linux/Mac)
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

## Проблема с модулем decouple

Проект настроен так, что он будет работать **БЕЗ** python-decouple. Если модуль не установится, Django будет использовать переменные окружения напрямую.

### После установки зависимостей:

1. **Примените миграции:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Создайте суперпользователя:**
   ```bash
   python manage.py createsuperuser
   ```

3. **Запустите сервер:**
   ```bash
   python manage.py runserver
   ```

## Если проблемы продолжаются

### Установка Pillow вручную (для Python 3.13)

```bash
# Обновите pip
python -m pip install --upgrade pip

# Установите Pillow последней версии
pip install --upgrade Pillow

# Или установите из wheel файла
pip install Pillow --only-binary :all:
```

### Альтернатива: использование Python 3.11 или 3.12

Если проблемы с Python 3.13 продолжаются, рекомендуется использовать Python 3.11 или 3.12:

```bash
# Создайте виртуальное окружение с Python 3.11/3.12
py -3.11 -m venv venv
# или
py -3.12 -m venv venv
```

## Проверка установки

После установки проверьте:

```bash
python manage.py check
```

Если команда выполнилась без ошибок - всё готово!

