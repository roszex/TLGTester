// Подключаем ProgressManager
// <script src="../progress.js"></script> должен быть в HTML

// Определяем базовый путь к картинкам (теперь относительно текущего домена)
let baseImgUrl = window.location.origin + "/";

// Пример: document.getElementById('main-img').src = baseImgUrl + '1_page_photo.jpeg';

// Инициализация Telegram WebApp для полноэкранного режима
function initTelegramWebApp() {
    if (window.Telegram && window.Telegram.WebApp) {
        const tg = window.Telegram.WebApp;
        
        try {
            // Расширяем WebApp на весь экран
            tg.expand();
            
            // Запрашиваем полноэкранный режим если доступен
            if (tg.requestFullscreen) {
                tg.requestFullscreen();
            }
            
            // Устанавливаем цвета темы для соответствия приложению
            tg.setHeaderColor('#000000');
            tg.setBackgroundColor('#000000');
            
            // Отключаем подтверждение закрытия для предотвращения сообщения "изменения могут не сохраниться"
            if (tg.enableClosingConfirmation) {
                // Не включаем подтверждение закрытия
            }
            
            // Устанавливаем основную кнопку если нужно
            if (tg.MainButton) {
                tg.MainButton.hide();
            }
            
            console.log('Telegram WebApp инициализирован успешно в полноэкранном режиме');
        } catch (error) {
            console.error('Ошибка инициализации Telegram WebApp:', error);
        }
    } else {
        console.log('Telegram WebApp недоступен - запуск в режиме браузера');
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
    const images = ['../2_page_photo.jpeg'];
    images.forEach(src => {
        const img = new Image();
        img.src = src;
    });
}

// Инициализация при загрузке страницы
window.addEventListener('load', function() {
    // Инициализируем Telegram WebApp (теперь через ProgressManager)
    if (window.progressManager) {
        // ProgressManager уже инициализировал WebApp
        console.log('WebApp инициализирован через ProgressManager');
    } else {
        // Fallback инициализация
        initTelegramWebApp();
    }
    
    // Загружаем изображения
    preloadImages();
    setTimeout(forceLoadImages, 100);
    
    // Принудительно сохраняем текущую страницу
    if (window.progressManager) {
        window.progressManager.savePage(1);
    }
});

// Обработчик кнопки "Поехали"
document.getElementById('letsGoBtn').addEventListener('click', function() {
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
            const newUrl = baseUrl + '/../page_2/index.html';
            
            console.log('Navigating to:', newUrl);
            window.location.href = newUrl;
        }
    }, 500);
}); 