// Функция для перехода на следующую страницу
function goToNextPage() {
    const currentUrl = window.location.href;
    const baseUrl = currentUrl.substring(0, currentUrl.lastIndexOf('/'));
    const newUrl = baseUrl + '/../page_13/index.html';
    // Используем ProgressManager если доступен
            if (window.progressManager) {
                console.log('Using ProgressManager for navigation');
                await window.progressManager.goToNextPage();
            } else {
                // Fallback на старый метод
                window.location.href = newUrl;
            }
}

// Добавляем обработчик для мобильных устройств
document.addEventListener('DOMContentLoaded', function() {
    // Предотвращаем масштабирование при двойном тапе на кнопку
    const nextButton = document.querySelector('.lets-go');
    if (nextButton) {
        nextButton.addEventListener('touchstart', function(e) {
            e.preventDefault();
        });
    }
    
    // Добавляем плавную анимацию появления контента
    const container = document.querySelector('.container');
    if (container) {
        container.style.opacity = '0';
        container.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            container.style.transition = 'all 0.5s ease';
            container.style.opacity = '1';
            container.style.transform = 'translateY(0)';
        }, 100);
    }
});

let baseImgUrl = "https://roszex.github.io/EmelyanovTGBot-webapp/";
