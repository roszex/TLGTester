// Подключаем ProgressManager
// <script src="../progress.js"></script> должен быть в HTML

// Инициализация при загрузке страницы
window.addEventListener('load', async function() {
    // Инициализируем Telegram WebApp
    initTelegramWebApp();
    
    // Устанавливаем текущую дату
    const currentDate = new Date().toLocaleDateString('ru-RU');

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

    document.getElementById('currentDate').textContent = currentDate;
    
    // Восстанавливаем данные формы если есть
    if (window.progressManager) {
        const savedProgress = await window.progressManager.getSavedProgress();
        if (savedProgress && savedProgress.form_data) {
            console.log('Восстанавливаем данные формы:', savedProgress.form_data);
            
            // Заполняем поля формы
            if (savedProgress.form_data.age) {
                document.getElementById('age').value = savedProgress.form_data.age;
            }
            if (savedProgress.form_data.occupation) {
                document.getElementById('occupation').value = savedProgress.form_data.occupation;
            }
            if (savedProgress.form_data.income) {
                document.getElementById('income').value = savedProgress.form_data.income;
            }
            if (savedProgress.form_data.motivation) {
                document.getElementById('motivation').value = savedProgress.form_data.motivation;
            }
            if (savedProgress.form_data.teamwork) {
                document.getElementById('teamwork').value = savedProgress.form_data.teamwork;
            }
        }
    }
    
    // Принудительно сохраняем текущую страницу (3)
    if (window.progressManager) {
        window.progressManager.savePage(3);
    }
});

// Функция для показа попапа сохранения
function showSavePopup() {
    const popup = document.getElementById('savePopup');
    popup.classList.add('show');
}

// Функция для скрытия попапа сохранения
function hideSavePopup() {
    const popup = document.getElementById('savePopup');
    popup.classList.remove('show');
}

// Функция для проверки сохранения данных в базе
async function checkDataSaved(userId, maxAttempts = 30) {
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        try {
            const response = await fetch(`https://emelyanovtgbot-webapp-production.up.railway.app/api/get_progress/${encodeURIComponent(userId)}`);
            
            if (response.ok) {
                const data = await response.json();
                // Проверяем, что данные формы сохранены (current_page = 4 означает, что форма сохранена)
                if (data.current_page === 4 && data.question_1 && data.question_2) {
                    console.log('Данные успешно сохранены в базе данных');
                    return true;
                }
            }
            
            console.log(`Попытка ${attempt}/${maxAttempts}: данные еще не сохранены, ждем...`);
            await new Promise(resolve => setTimeout(resolve, 1000)); // Ждем 1 секунду
        } catch (error) {
            console.error(`Ошибка при проверке сохранения (попытка ${attempt}):`, error);
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
    }
    
    console.log('Превышено время ожидания сохранения данных');
    return false;
}

// Обработчик отправки формы
document.getElementById('submitBtn').addEventListener('click', async function() {
    const submitBtn = document.getElementById('submitBtn');
    const form = document.getElementById('contactForm');
    
    // Проверяем валидность формы
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    // Блокируем кнопку и показываем попап
    submitBtn.disabled = true;
    showSavePopup();
    
    // Собираем данные формы
    const formData = {
        age: document.getElementById('age').value,
        occupation: document.getElementById('occupation').value,
        income: document.getElementById('income').value,
        motivation: document.getElementById('motivation').value,
        teamwork: document.getElementById('teamwork').value
    };
    
    console.log('Отправляем данные формы:', formData);
    console.log('ProgressManager доступен:', !!window.progressManager);
    console.log('User ID:', window.progressManager ? window.progressManager.userId : 'неизвестен');
    
    // Сохраняем данные через ProgressManager
    if (window.progressManager) {
        try {
            const success = await window.progressManager.saveFormData(formData);
            console.log('Результат сохранения формы:', success);
            
            if (success) {
                // Ждем подтверждения сохранения в базе данных
                const dataSaved = await checkDataSaved(window.progressManager.userId);
                
                if (dataSaved) {
                    // Скрываем попап
                    hideSavePopup();
                    
                    // Анимация перехода
                    const container = document.querySelector('.container');
                    container.classList.add('wind-transition');
                    
                    // Переходим на следующую страницу
                    setTimeout(() => {
                        const currentUrl = window.location.href;
                        const baseUrl = currentUrl.substring(0, currentUrl.lastIndexOf('/'));
                        const newUrl = baseUrl + '/../page_4/index.html?user_id=' + window.progressManager.userId;
                        console.log('Navigating to:', newUrl);
                        window.location.href = newUrl;
                    }, 500);
                } else {
                    // Если данные не сохранились, показываем ошибку
                    hideSavePopup();
                    submitBtn.disabled = false;
                    alert('Ошибка при сохранении данных. Попробуйте еще раз.');
                }
            } else {
                hideSavePopup();
                submitBtn.disabled = false;
                alert('Ошибка при сохранении данных. Попробуйте еще раз.');
            }
        } catch (error) {
            console.error('Ошибка при сохранении формы:', error);
            hideSavePopup();
            submitBtn.disabled = false;
            alert('Ошибка при сохранении данных: ' + error.message);
        }
    } else {
        hideSavePopup();
        submitBtn.disabled = false;
        alert('Ошибка: ProgressManager не загружен');
    }
}); 