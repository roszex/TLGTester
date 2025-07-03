// Подключаем ProgressManager
// <script src="../progress.js"></script> должен быть в HTML

// Инициализация при загрузке страницы
window.addEventListener('load', function() {
    // Блокируем свайпы для закрытия приложения
    preventAppClose();
    // Инициализируем Telegram WebApp
    initTelegramWebApp();
    
    // Принудительно сохраняем текущую страницу
    if (window.progressManager) {
        window.progressManager.savePage(4);
    }
});

// Функция для предотвращения закрытия приложения свайпами
function preventAppClose() {
    let startY = 0;
    let startX = 0;
    let isDragging = false;
    
    // Блокируем touchstart
    document.addEventListener('touchstart', function(e) {
        startY = e.touches[0].clientY;
        startX = e.touches[0].clientX;
        isDragging = false;
    }, { passive: false });
    
    // Блокируем touchmove
    document.addEventListener('touchmove', function(e) {
        const currentY = e.touches[0].clientY;
        const currentX = e.touches[0].clientX;
        const deltaY = currentY - startY;
        const deltaX = Math.abs(currentX - startX);
        
        // Если пользователь находится в верхней части страницы и свайпает вниз
        // Теперь у нас есть scroll-buffer, поэтому проверяем только если мы выше него
        if (window.scrollY <= -200 && deltaY > 0) {
            // Блокируем свайп вниз для закрытия приложения
            e.preventDefault();
            e.stopPropagation();
            return false;
        }
        
        // Если свайп больше горизонтального, то это не закрытие приложения
        if (Math.abs(deltaY) > deltaX) {
            isDragging = true;
        }
    }, { passive: false });
    
    // Блокируем touchend
    document.addEventListener('touchend', function(e) {
        if (isDragging && window.scrollY <= 0) {
            e.preventDefault();
            e.stopPropagation();
        }
    }, { passive: false });
    
    // Дополнительная защита от overscroll
    document.addEventListener('gesturestart', function(e) {
        e.preventDefault();
    }, { passive: false });
    
    document.addEventListener('gesturechange', function(e) {
        e.preventDefault();
    }, { passive: false });
    
    document.addEventListener('gestureend', function(e) {
        e.preventDefault();
    }, { passive: false });
}

// Функция для отправки данных в бот
function sendDataToBot() {
    console.log('=== ОТПРАВКА ДАННЫХ В БОТ ===');
    console.log('Telegram WebApp доступен:', !!(window.Telegram && window.Telegram.WebApp));
    
    if (window.Telegram && window.Telegram.WebApp) {
        try {
            // Получаем данные формы из localStorage или sessionStorage
            let formData = null;
            try {
                const savedFormData = localStorage.getItem('formData') || sessionStorage.getItem('formData');
                if (savedFormData) {
                    formData = JSON.parse(savedFormData);
                    console.log('Найдены сохраненные данные формы:', formData);
                }
            } catch (e) {
                console.log('Ошибка при получении данных формы:', e);
            }
            
            const userData = {
                action: 'thank_you_response',
                user_id: window.progressManager ? window.progressManager.userId : 'unknown',
                timestamp: new Date().toISOString(),
                form_data: formData // Добавляем данные формы
            };
            
            console.log('Отправляем данные в бот:', userData);
            
            // Отправляем данные через Telegram WebApp
            window.Telegram.WebApp.sendData(JSON.stringify(userData));
            
            console.log('✅ Данные успешно отправлены в бот');
            
            // Дополнительная проверка
            setTimeout(() => {
                console.log('Проверяем статус отправки...');
                if (window.Telegram && window.Telegram.WebApp) {
                    console.log('WebApp все еще доступен');
                }
            }, 1000);
            
        } catch (error) {
            console.error('❌ Ошибка при отправке данных в бот:', error);
        }
    } else {
        console.log('❌ Telegram WebApp недоступен, данные не отправлены');
        console.log('window.Telegram:', window.Telegram);
        console.log('window.Telegram.WebApp:', window.Telegram?.WebApp);
    }
}

// Обработчик кнопки "Выход"
document.getElementById('exitBtn').addEventListener('click', function() {
    const container = document.querySelector('.container');
    
    // Добавляем анимацию "ветра"
    container.classList.add('wind-transition');
    
    // Ждём окончания анимации и закрываем приложение
    setTimeout(() => {
        // Отправляем данные в бот перед закрытием
        console.log('Начинаем отправку данных в бот...');
        sendDataToBot();
        
        // Ждем немного для отправки данных
        setTimeout(() => {
            console.log('Закрываем WebApp...');
            
            // Дополнительная попытка отправки данных
            if (window.Telegram && window.Telegram.WebApp) {
                try {
                    const userData = {
                        action: 'thank_you_response',
                        user_id: window.progressManager ? window.progressManager.userId : 'unknown',
                        timestamp: new Date().toISOString()
                    };
                    window.Telegram.WebApp.sendData(JSON.stringify(userData));
                    console.log('Дополнительная отправка данных выполнена');
                } catch (e) {
                    console.error('Ошибка при дополнительной отправке:', e);
                }
            }
            
            // Закрываем Telegram WebApp
            if (window.Telegram && window.Telegram.WebApp) {
                window.Telegram.WebApp.close();
            } else {
                // Fallback - просто закрываем окно
                window.close();
            }
        }, 1000); // Увеличиваем время ожидания
    }, 500);
}); 