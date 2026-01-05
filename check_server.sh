#!/bin/bash
# Скрипт для проверки состояния сервера

echo "🔍 Проверка состояния сервера..."
echo ""

# Проверка Git статуса
echo "📦 Git статус:"
cd ~/burokv
git status --short
echo ""

# Проверка последнего коммита
echo "📝 Последний коммит:"
git log -1 --oneline
echo ""

# Проверка версии файлов
echo "📄 Проверка версий файлов:"
echo "Middleware:"
ls -lh core/middleware/admin_jwt_middleware.py
echo ""
echo "CSS:"
ls -lh static/css/style.css
echo ""

# Проверка статических файлов
echo "📦 Статические файлы:"
if [ -d "staticfiles/css" ]; then
    ls -lh staticfiles/css/ | head -5
    echo ""
    echo "Размер CSS файла:"
    du -h staticfiles/css/style*.css 2>/dev/null | head -1
else
    echo "❌ Директория staticfiles/css не найдена!"
fi
echo ""

# Проверка Gunicorn
echo "🔄 Статус Gunicorn:"
sudo systemctl status burokv --no-pager -l | head -10
echo ""

# Проверка времени последнего изменения
echo "⏰ Время последнего изменения файлов:"
stat -c "%y %n" core/middleware/admin_jwt_middleware.py 2>/dev/null || stat -f "%Sm %N" core/middleware/admin_jwt_middleware.py
stat -c "%y %n" static/css/style.css 2>/dev/null || stat -f "%Sm %N" static/css/style.css
echo ""

# Проверка хэшей файлов
echo "🔐 Хэши файлов (первые 32 символа):"
md5sum core/middleware/admin_jwt_middleware.py 2>/dev/null | cut -d' ' -f1 || md5 core/middleware/admin_jwt_middleware.py | cut -d' ' -f4
md5sum static/css/style.css 2>/dev/null | cut -d' ' -f1 || md5 static/css/style.css | cut -d' ' -f4
echo ""

echo "✅ Проверка завершена"

