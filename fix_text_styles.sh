#!/bin/bash

echo "Добавляем CSS стили для текста на всех страницах, кроме page_3..."

# Добавляем стили для bio-text, bio-content и photo-caption
for page in 1 2 4 5 6 7 8 9 10 11 12 13 14 15; do
    echo "Добавляем стили на страницу $page..."
    
    # Добавляем стили в конец CSS файла
    cat >> webapp/page_${page}/style.css << 'EOF'

/* Стили для bio-text и bio-content */
.bio-text {
    color: #fff;
    margin-bottom: 32px;
    text-align: left;
    width: 100%;
    max-width: 320px;
}

.bio-content {
    font-size: 1.1rem;
    line-height: 1.6;
    text-align: justify;
}

.bio-content p {
    margin-bottom: 12px;
}

.photo-caption {
    font-size: 1.1rem;
    font-weight: bold;
    color: #ff4444;
    margin-bottom: 20px;
    text-align: center;
}

/* Mobile responsiveness для новых элементов */
@media (max-width: 768px) {
    .bio-content {
        font-size: 16px;
    }
    
    .bio-content p {
        margin-bottom: 12px;
    }
    
    .photo-caption {
        font-size: 18px;
        margin-bottom: 20px;
    }
}

@media (max-width: 480px) {
    .bio-content {
        font-size: 16px;
    }
    
    .photo-caption {
        font-size: 18px;
    }
}
EOF
done

echo "Стили для текста добавлены на все страницы, кроме page_3!" 