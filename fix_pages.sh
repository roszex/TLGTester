#!/bin/bash

# Исправляем страницы 8-13
for page in {8..13}; do
    next_page=$((page + 1))
    echo "Исправляем страницу $page -> $next_page"
    
    # Создаем временный файл с исправленным содержимым
    sed 's|const urlParams = new URLSearchParams(window.location.search); const userId = urlParams.get('\''user_id'\''); const newUrl = baseUrl + '\''\/..\/page_'$next_page'\/index.html'\'' + (userId ? `?user_id=${userId}` : '\''\'');|const urlParams = new URLSearchParams(window.location.search);\n            const userId = urlParams.get('\''user_id'\'');\n            const newUrl = baseUrl + '\''\/..\/page_'$next_page'\/index.html'\'' + (userId ? `?user_id=${userId}` : '\''\'');|g' webapp/page_${page}/main.js > temp_fix.js
    
    # Заменяем оригинальный файл
    mv temp_fix.js webapp/page_${page}/main.js
done

echo "Все страницы исправлены!" 