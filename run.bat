@echo off
echo ========================================
echo Запуск проекта Бюро Квартир
echo ========================================
echo.

echo Проверка виртуального окружения...
if not exist venv (
    echo Создание виртуального окружения...
    python -m venv venv
)

echo Активация виртуального окружения...
call venv\Scripts\activate.bat

echo Установка зависимостей...
pip install -r requirements.txt

echo Применение миграций...
python manage.py migrate

echo Сбор статических файлов...
python manage.py collectstatic --noinput

echo.
echo ========================================
echo Проект готов к запуску!
echo ========================================
echo.
echo Запуск сервера разработки...
python manage.py runserver

