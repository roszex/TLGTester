// Устанавливаем текущую дату
function setCurrentDate() {
    const today = new Date();
    const day = String(today.getDate()).padStart(2, '0');
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const year = today.getFullYear();
    const formattedDate = `${day}.${month}.${year}`;
    
    document.getElementById('currentDate').textContent = formattedDate;
}

// Функция для скрытия клавиатуры только при необходимости
function hideKeyboard() {
    // Скрываем фокус со всех полей ввода
    if (document.activeElement && document.activeElement.tagName === 'INPUT') {
        document.activeElement.blur();
    }
}

// Функция для валидации формы
function validateForm() {
    const form = document.getElementById('contactForm');
    const age = document.getElementById('age').value;
    const occupation = document.getElementById('occupation').value.trim();
    const income = document.getElementById('income').value.trim();
    const motivation = document.getElementById('motivation').value.trim();
    const teamwork = document.getElementById('teamwork').value.trim();
    
    // Проверяем, что все поля заполнены
    if (!age || !occupation || !income || !motivation || !teamwork) {
        alert('Пожалуйста, заполните все поля формы!');
        return false;
    }
    
    // Проверяем возраст
    const ageNum = parseInt(age);
    if (ageNum < 16 || ageNum > 100) {
        alert('Возраст должен быть от 16 до 100 лет!');
        return false;
    }
    
    // Проверяем, что текстовые поля не слишком короткие
    if (income.length < 3) {
        alert('Пожалуйста, укажите ваш доход!');
        return false;
    }
    
    if (motivation.length < 5) {
        alert('Пожалуйста, расскажите о вашей мотивации!');
        return false;
    }
    
    if (teamwork.length < 5) {
        alert('Пожалуйста, расскажите о желании работать в команде!');
        return false;
    }
    
    return true;
}

// Функция для сбора данных формы
function collectFormData() {
    console.log('=== collectFormData: Начинаем сбор данных ===');
    
    const age = document.getElementById('age').value;
    const occupation = document.getElementById('occupation').value.trim();
    const income = document.getElementById('income').value.trim();
    const motivation = document.getElementById('motivation').value.trim();
    const teamwork = document.getElementById('teamwork').value.trim();
    
    console.log('=== collectFormData: Собранные значения ===');
    console.log('age:', age);
    console.log('occupation:', occupation);
    console.log('income:', income);
    console.log('motivation:', motivation);
    console.log('teamwork:', teamwork);
    
    const formData = {
        age: age,
        occupation: occupation,
        income: income,
        motivation: motivation,
        teamwork: teamwork
    };
    
    console.log('=== collectFormData: Финальный объект ===', formData);
    
    return formData;
}

// Обработчик клика по кнопке
document.getElementById('submitBtn').addEventListener('click', async function() {
    console.log('=== ФОРМА: Кнопка отправки нажата ===');
    
    // Скрываем клавиатуру только при нажатии на кнопку отправки
    hideKeyboard();
    
    if (validateForm()) {
        console.log('=== ФОРМА: Валидация прошла успешно ===');
        
        // Собираем данные формы
        const formData = collectFormData();
        console.log('=== ФОРМА: Собранные данные ===', formData);
        
        // Проверяем, доступен ли ProgressManager
        if (window.progressManager) {
            console.log('=== ФОРМА: ProgressManager доступен ===');
            console.log('ProgressManager userId:', window.progressManager.userId);
            console.log('ProgressManager serverUrl:', window.progressManager.serverUrl);
            console.log('ProgressManager isTelegram:', window.progressManager.isTelegram);
            
            try {
                console.log('=== ФОРМА: Начинаем сохранение данных ===');
                const result = await window.progressManager.saveFormData(formData);
                console.log('=== ФОРМА: Результат сохранения ===', result);
                
                if (result) {
                    console.log('=== ФОРМА: Данные успешно сохранены ===');
                    // Переходим на следующую страницу
                    await window.progressManager.goToNextPage();
                } else {
                    console.error('=== ФОРМА: Ошибка сохранения данных ===');
                    alert('Ошибка сохранения данных');
                }
            } catch (error) {
                console.error('=== ФОРМА: Ошибка сохранения данных ===', error);
                alert('Ошибка сохранения данных: ' + error.message);
            }
        } else {
            console.error('=== ФОРМА: ProgressManager недоступен ===');
            alert('Ошибка: ProgressManager недоступен');
        }
    } else {
        console.log('=== ФОРМА: Валидация не прошла ===');
    }
});

// Добавляем обработчик Enter для полей формы
document.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {
        e.preventDefault();
        hideKeyboard();
        document.getElementById('submitBtn').click();
    }
});

// Скрываем клавиатуру только при изменении ориентации экрана
window.addEventListener('orientationchange', function() {
    setTimeout(hideKeyboard, 100);
});

// Запускаем при загрузке страницы
window.addEventListener('load', setCurrentDate);

let baseImgUrl = "https://roszex.github.io/EmelyanovTGBot-webapp/";
