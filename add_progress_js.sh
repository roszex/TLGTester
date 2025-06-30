#!/bin/bash

# Добавляем progress.js на все страницы 6-14
for page in {6..14}; do
    echo "Добавляем progress.js на страницу $page"
    
    # Добавляем progress.js перед main.js
    sed -i '' 's|<script src="main.js"></script>|<script src="../progress.js"></script>\n    <script src="main.js"></script>|g' webapp/page_${page}/index.html
done

echo "Все progress.js добавлены!" 