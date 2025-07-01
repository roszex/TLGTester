#!/bin/bash

echo "Добавляем CSS стили для класса red-text на все страницы, кроме page_3..."

# Добавляем стили для red-text
for page in 1 2 4 5 6 7 8 9 10 11 12 13 14 15; do
    echo "Добавляем стили red-text на страницу $page..."
    
    # Добавляем стили в конец CSS файла
    cat >> webapp/page_${page}/style.css << 'EOF'

/* Стили для красного текста */
.red-text {
    font-size: 1.3rem;
    font-weight: bold;
    color: #ff0000;
    margin: 20px 0;
    text-align: center;
}
EOF
done

echo "Стили для red-text добавлены на все страницы, кроме page_3!" 