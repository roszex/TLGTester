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
    const formData = {
        age: document.getElementById('age').value,
        occupation: document.getElementById('occupation').value.trim(),
        income: document.getElementById('income').value.trim(),
        motivation: document.getElementById('motivation').value.trim(),
        teamwork: document.getElementById('teamwork').value.trim(),
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent
    };
    
    // Сохраняем данные в localStorage для возможного использования
    localStorage.setItem('formData', JSON.stringify(formData));
    
    // Здесь можно добавить отправку данных на сервер
    console.log('Собранные данные:', formData);
    
    return formData;
}

// Обработчик клика по кнопке
document.getElementById('submitBtn').addEventListener('click', function() {
    // Скрываем клавиатуру только при нажатии на кнопку отправки
    hideKeyboard();
    
    if (validateForm()) {
        // Собираем данные формы
        const formData = collectFormData();
        
        // Переходим на следующую страницу
        const currentUrl = window.location.href;
        const baseUrl = currentUrl.substring(0, currentUrl.lastIndexOf('/'));
        const newUrl = baseUrl + '/../page_4/index.html';
        
        console.log('Navigating to:', newUrl);
        window.location.href = newUrl;
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
