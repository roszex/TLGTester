// Подключаем ProgressManager
// <script src="../progress.js"></script> должен быть в HTML

// Инициализация при загрузке страницы
window.addEventListener('load', function() {
    // Инициализируем Telegram WebApp
    initTelegramWebApp();
    
    // Устанавливаем текущую дату
    const currentDate = new Date().toLocaleDateString('ru-RU');
    document.getElementById('currentDate').textContent = currentDate;
    
    // Прогресс сохраняется автоматически в ProgressManager
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
    
    // Сохраняем данные через ProgressManager
    if (window.progressManager) {
        const success = await window.progressManager.saveFormData(formData);
        if (success) {
            // Переходим на следующую страницу
            const currentUrl = window.location.href;
            const baseUrl = currentUrl.substring(0, currentUrl.lastIndexOf('/'));
            const newUrl = baseUrl + '/../page_4/index.html';
            
            console.log('Navigating to:', newUrl);
            window.location.href = newUrl;
        } else {
            alert('Ошибка при сохранении данных. Попробуйте еще раз.');
        }
    } else {
        alert('Ошибка: ProgressManager не загружен');
    }
}); 