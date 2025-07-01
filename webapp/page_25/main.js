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
    const images = ['../25_page_photo.jpeg'];
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
        window.progressManager.savePage(25);
    }
});

// Функция закрытия WebApp и отправки сообщения
function closeWebAppAndSendMessage() {
    const container = document.querySelector('.container');
    
    // Добавляем анимацию "ветра"
    container.classList.add('wind-transition');
    
    // Ждём окончания анимации и закрываем WebApp
    setTimeout(() => {
        if (window.Telegram && window.Telegram.WebApp) {
            const tg = window.Telegram.WebApp;
            
            // Отправляем данные обратно в бота
            tg.sendData(JSON.stringify({
                action: 'thank_you_response',
                user_id: window.progressManager ? window.progressManager.userId : null,
                message: 'пока'
            }));
            
            // Закрываем WebApp
            tg.close();
        } else {
            // Fallback если Telegram WebApp не доступен
            console.log('Telegram WebApp not available, redirecting to bot');
            // Можно добавить редирект на бота или показать сообщение
            alert('Спасибо! Возвращайтесь к боту.');
        }
    }, 500);
}

// Обработчик кнопки
document.addEventListener('DOMContentLoaded', function() {
    const nextBtn = document.querySelector('.next-button');
    if (nextBtn) {
        nextBtn.addEventListener('click', closeWebAppAndSendMessage);
    }
}); 