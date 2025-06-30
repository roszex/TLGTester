#!/bin/bash

# Добавляем обработчики на страницы 8-13
for page in {8..13}; do
    echo "Добавляем обработчик на страницу $page"
    
    # Добавляем обработчик в конец файла
    cat >> webapp/page_${page}/main.js << 'EOF'

// Обработчик кнопки
document.addEventListener('DOMContentLoaded', function() {
    const nextBtn = document.querySelector('.lets-go');
    if (nextBtn) {
        nextBtn.addEventListener('click', goToNextPage);
    }
});
EOF
done

echo "Все обработчики добавлены!" 