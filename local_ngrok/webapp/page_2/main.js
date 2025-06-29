// Ждем загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    const listenBtn = document.getElementById('listenBtn');
    
    if (!listenBtn) {
        console.error('Button with id "listenBtn" not found!');
        return;
    }
    
    console.log('Button found, adding event listener');
    
    listenBtn.addEventListener('click', async function() {
        console.log('Button clicked!');
        const container = document.querySelector('.container');
        
        // Добавляем анимацию "ветра"
        container.classList.add('wind-transition');
        
        // Ждём окончания анимации и переходим
        setTimeout(async () => {
            // Используем новую систему прогресса
            if (window.progressManager) {
                await window.progressManager.goToNextPage();
            } else {
                // Fallback на старый метод
                const currentUrl = window.location.href;
                const baseUrl = currentUrl.substring(0, currentUrl.lastIndexOf('/'));
                const newUrl = baseUrl + '/../page_3/index.html';
                
                console.log('Navigating to:', newUrl);
                window.location.href = newUrl;
            }
        }, 500);
    });
});
