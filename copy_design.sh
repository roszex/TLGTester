#!/bin/bash

echo "Копируем дизайн с page_1 ко всем страницам, кроме page_3..."

# Копируем CSS с page_1 на все остальные страницы (кроме page_3)
for page in 2 4 5 6 7 8 9 10 11 12 13 14 15; do
    echo "Копируем CSS на страницу $page..."
    cp webapp/page_1/style.css webapp/page_${page}/style.css
done

echo "Дизайн скопирован на все страницы, кроме page_3!" 