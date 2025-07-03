// Подключаем ProgressManager
// <script src="../progress.js"></script> должен быть в HTML

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

// Инициализация при загрузке страницы
window.addEventListener('load', async function() {
    console.log('=== ЗАГРУЗКА 3-Й СТРАНИЦЫ ===');
    
    // Инициализируем Telegram WebApp
    initTelegramWebApp();
    
    // Устанавливаем текущую дату
    const currentDate = new Date().toLocaleDateString('ru-RU');
    console.log('Устанавливаем дату:', currentDate);
    
    const dateElement = document.getElementById('currentDate');
    if (dateElement) {
        dateElement.textContent = currentDate;
        console.log('Дата установлена успешно');
    } else {
        console.error('Элемент currentDate не найден!');
    }
    
    // Блокируем свайпы для закрытия приложения
    preventAppClose();
    
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
        } else {
            // Пробуем восстановить из localStorage по user_id
            try {
                const userId = window.progressManager.userId;
                const formDataKey = `formData_${userId}`;
                
                let savedFormData = localStorage.getItem(formDataKey) || sessionStorage.getItem(formDataKey);
                
                // Если не найдено по user_id, пробуем общий ключ
                if (!savedFormData) {
                    savedFormData = localStorage.getItem('formData') || sessionStorage.getItem('formData');
                }
                
                if (savedFormData) {
                    const formData = JSON.parse(savedFormData);
                    console.log('Восстанавливаем данные формы из localStorage:', formData);
                    
                    // Заполняем поля формы
                    if (formData.age) {
                        document.getElementById('age').value = formData.age;
                    }
                    if (formData.occupation) {
                        document.getElementById('occupation').value = formData.occupation;
                    }
                    if (formData.income) {
                        document.getElementById('income').value = formData.income;
                    }
                    if (formData.motivation) {
                        document.getElementById('motivation').value = formData.motivation;
                    }
                    if (formData.teamwork) {
                        document.getElementById('teamwork').value = formData.teamwork;
                    }
                }
            } catch (e) {
                console.log('Ошибка при восстановлении данных из localStorage:', e);
            }
        }
    }
    
    // Очищаем форму при загрузке страницы
    console.log('Очищаем форму для нового заполнения');
    document.getElementById('contactForm').reset();
    
    // Очищаем старые данные формы из localStorage
    try {
        const userId = window.progressManager ? window.progressManager.userId : 'unknown';
        const formDataKey = `formData_${userId}`;
        
        // Удаляем данные по user_id
        localStorage.removeItem(formDataKey);
        sessionStorage.removeItem(formDataKey);
        
        // Также удаляем общие данные
        localStorage.removeItem('formData');
        sessionStorage.removeItem('formData');
        
        console.log('Старые данные формы очищены из localStorage');
    } catch (e) {
        console.log('Ошибка при очистке localStorage:', e);
    }
    
    // Принудительно сохраняем текущую страницу (3)
    if (window.progressManager) {
        window.progressManager.savePage(3);
    }
});

// Функция для показа попапа сохранения
function showSavePopup() {
    const popup = document.getElementById('savePopup');
    if (popup) {
        popup.classList.add('show');
    }
}

// Функция для скрытия попапа сохранения
function hideSavePopup() {
    const popup = document.getElementById('savePopup');
    if (popup) {
        popup.classList.remove('show');
    }
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
    
    console.log('=== ОТПРАВКА ФОРМЫ ===');
    console.log('Данные формы:', formData);
    console.log('ProgressManager доступен:', !!window.progressManager);
    console.log('User ID:', window.progressManager ? window.progressManager.userId : 'неизвестен');
    
    try {
        // Сохраняем данные формы в localStorage для отправки в бот
        try {
            // Получаем user_id для уникального ключа
            const userId = window.progressManager ? window.progressManager.userId : 'unknown';
            const formDataKey = `formData_${userId}`;
            
            localStorage.setItem(formDataKey, JSON.stringify(formData));
            sessionStorage.setItem(formDataKey, JSON.stringify(formData));
            
            // Также сохраняем под общим ключом для совместимости
            localStorage.setItem('formData', JSON.stringify(formData));
            sessionStorage.setItem('formData', JSON.stringify(formData));
            
            console.log('✅ Данные формы сохранены с ключом:', formDataKey);
            console.log('✅ Данные формы также сохранены под общим ключом');
        } catch (e) {
            console.error('❌ Ошибка при сохранении данных формы:', e);
        }
        
        // Сохраняем данные формы
        if (window.progressManager) {
            console.log('Начинаем сохранение через ProgressManager...');
            await window.progressManager.saveFormData(formData);
            console.log('✅ Данные отправлены на сервер');
        } else {
            console.log('❌ ProgressManager недоступен');
            throw new Error('ProgressManager недоступен');
        }
        
        // Ждем немного для показа попапа
        console.log('Ждем 2 секунды для показа попапа...');
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Скрываем попап
        hideSavePopup();
        
        // Переходим на следующую страницу
        console.log('Переходим на следующую страницу...');
        if (window.progressManager) {
            window.progressManager.goToNextPage();
        } else {
            // Fallback
            window.location.href = '../page_4/index.html';
        }
        
    } catch (error) {
        console.error('❌ ОШИБКА ПРИ СОХРАНЕНИИ:', error);
        
        // Скрываем попап
        hideSavePopup();
        
        // Показываем ошибку пользователю
        alert('Произошла ошибка при сохранении данных: ' + error.message);
        
        // Разблокируем кнопку
        submitBtn.disabled = false;
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