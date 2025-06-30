#!/bin/bash

# Добавляем анимацию в CSS файлы страниц 6-14
for page in {6..14}; do
    echo "Добавляем анимацию в страницу $page"
    
    # Добавляем анимацию перед закрывающей скобкой
    cat >> webapp/page_${page}/style.css << 'EOF'

/* Анимация "ветра" при переходе */
@keyframes windTransition {
    0% {
        transform: translateX(0) scale(1);
        opacity: 1;
    }
    25% {
        transform: translateX(-10px) scale(0.95);
        opacity: 0.8;
    }
    50% {
        transform: translateX(-30px) scale(0.9);
        opacity: 0.6;
    }
    75% {
        transform: translateX(-50px) scale(0.85);
        opacity: 0.4;
    }
    100% {
        transform: translateX(-100vw) scale(0.8);
        opacity: 0;
    }
}

.wind-transition {
    animation: windTransition 0.5s ease-out forwards;
}
EOF
done

echo "Анимация добавлена на все страницы!" 