// Подключаем ProgressManager
// <script src="../progress.js"></script> должен быть в HTML

// Определяем базовый путь к картинкам (теперь относительно текущего домена)
let baseImgUrl = window.location.origin + "/";

// Пример: document.getElementById('main-img').src = baseImgUrl + '1_page_photo.jpeg';

// Инициализация Telegram WebApp
function initTelegramWebApp() {
    if (window.Telegram && window.Telegram.WebApp) {
        const tg = window.Telegram.WebApp;
        tg.ready();
        tg.expand();
        
        // Настройка темы
        if (tg.colorScheme === 'dark') {
            document.body.style.backgroundColor = '#000';
        }
        
        console.log('Telegram WebApp initialized');
    } else {
        console.log('Telegram WebApp not available');
    }
}

// Принудительная загрузка изображений для iPhone Safari
function forceLoadImages() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        // Создаем новый Image объект для принудительной загрузки
        const newImg = new Image();
        newImg.onload = function() {
            img.src = this.src;
            img.style.opacity = '1';
        };
        newImg.onerror = function() {
            console.error('Failed to load image:', this.src);
            // Попробуем загрузить через fetch
            fetch(this.src)
                .then(response => response.blob())
                .then(blob => {
                    const url = URL.createObjectURL(blob);
                    img.src = url;
                    img.style.opacity = '1';
                })
                .catch(err => {
                    console.error('Fetch also failed:', err);
                });
        };
        newImg.src = img.src;
    });
}

// Предзагрузка изображений для быстрой загрузки
function preloadImages() {
    const images = ['../23_page_photo.jpeg'];
    images.forEach(src => {
        const img = new Image();
        img.src = src;
    });
}

// Инициализация при загрузке страницы
window.addEventListener('load', function() {
    // Инициализируем Telegram WebApp
    initTelegramWebApp();
    
    // Загружаем изображения
    preloadImages();
    setTimeout(forceLoadImages, 100);
    
    // Принудительно сохраняем текущую страницу
    if (window.progressManager) {
        window.progressManager.savePage(23);
    }
});

// Функция перехода на следующую страницу
function goToNextPage() {
    const container = document.querySelector('.container');
    
    // Добавляем анимацию "ветра"
    container.classList.add('wind-transition');
    
    // Ждём окончания анимации и переходим
    setTimeout(() => {
        // Переходим на следующую страницу через ProgressManager
        if (window.progressManager) {
            window.progressManager.goToNextPage();
        } else {
            // Fallback если ProgressManager не загружен
            const currentUrl = window.location.href;
            const baseUrl = currentUrl.substring(0, currentUrl.lastIndexOf('/'));
            const urlParams = new URLSearchParams(window.location.search);
            const userId = urlParams.get('user_id');
            // Переходим на 24-ю страницу
            const newUrl = baseUrl + '/../page_24/index.html' + (userId ? `?user_id=${userId}` : '');
            
            console.log('Navigating to:', newUrl);
            window.location.href = newUrl;
        }
    }, 500);
}

// Обработчик кнопки
document.addEventListener('DOMContentLoaded', function() {
    const nextBtn = document.querySelector('.next-button');
    if (nextBtn) {
        nextBtn.addEventListener('click', goToNextPage);
    }
}); 