#!/bin/bash

# Убираем onclick из всех страниц 7-13
for page in {7..13}; do
    echo "Исправляем страницу $page"
    sed -i '' 's/onclick="goToNextPage()"//g' webapp/page_${page}/index.html
done

echo "Все onclick удалены!" 