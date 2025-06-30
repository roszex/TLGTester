// Подключаем ProgressManager
// <script src="../progress.js"></script> должен быть в HTML

// Инициализация при загрузке страницы
window.addEventListener('load', async function() {
    // Инициализируем Telegram WebApp
    initTelegramWebApp();
    
    // Устанавливаем текущую дату
    const currentDate = new Date().toLocaleDateString('ru-RU');
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

// Обработчик отправки формы
document.getElementById('submitBtn').addEventListener('click', async function() {
    const form = document.getElementById('contactForm');
    
    // Проверяем валидность формы
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
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
                alert('Ошибка при сохранении данных. Попробуйте еще раз.');
            }
        } catch (error) {
            console.error('Ошибка при сохранении формы:', error);
            alert('Ошибка при сохранении данных: ' + error.message);
        }
    } else {
        alert('Ошибка: ProgressManager не загружен');
    }
}); 