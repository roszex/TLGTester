// Ждем загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    const nextBtn = document.getElementById('nextBtn');
    
    if (!nextBtn) {
        console.error('Button with id "nextBtn" not found!');
        return;
    }
    
    console.log('Button found, adding event listener');
    
    let baseImgUrl = 'https://roszex.github.io/EmelyanovTGBot-webapp/';
    
    nextBtn.addEventListener('click', function() {
        console.log('Button clicked!');
        const container = document.querySelector('.container');
        
        // Добавляем анимацию "ветра"
        container.classList.add('wind-transition');
        
        // Ждём окончания анимации и переходим
        setTimeout(() => {
            // Используем более надежный метод для избежания ngrok предупреждений
            const currentUrl = window.location.href;
            const baseUrl = currentUrl.substring(0, currentUrl.lastIndexOf('/'));
            const newUrl = baseUrl + '/../page_5/index.html';
            
            console.log('Navigating to:', newUrl);
            
            // Простое перенаправление без создания элементов
            window.location.href = newUrl;
        }, 500);
    });
}); 