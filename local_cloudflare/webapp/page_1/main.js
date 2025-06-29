// Проверяем прогресс пользователя при загрузке страницы
document.addEventListener('DOMContentLoaded', async function() {
    // Если это первая страница, проверяем, нужно ли перенаправить пользователя
    if (window.progressManager) {
        const lastPage = await window.progressManager.getProgress();
        if (lastPage > 1) {
            console.log('User has progress, redirecting to page:', lastPage);
            await window.progressManager.redirectToLastPage();
            return;
        }
    }
    
    // Инициализируем страницу как обычно
    initializePage();
});

function initializePage() {
    // Определяем базовый путь к картинкам
    let baseImgUrl = 'https://25a9-147-45-179-150.ngrok-free.app/local_ngrok/webapp/';

    // Пример: document.getElementById('main-img').src = baseImgUrl + '1_page_photo.jpeg';

    // Принудительная загрузка изображений для iPhone Safari
    function forceLoadImages() {
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            // Создаем новый Image объект для принудительной загрузки
            const newImg = new Image();
            newImg.onload = function() {
                img.src = this.src;
                img.style.opacity = '1';
            };
            newImg.onerror = function() {
                console.error('Failed to load image:', this.src);
                // Попробуем загрузить через fetch
                fetch(this.src)
                    .then(response => response.blob())
                    .then(blob => {
                        const url = URL.createObjectURL(blob);
                        img.src = url;
                        img.style.opacity = '1';
                    })
                    .catch(err => {
                        console.error('Fetch also failed:', err);
                    });
            };
            newImg.src = img.src;
        });
    }

    // Предзагрузка изображений для быстрой загрузки
    function preloadImages() {
        const images = ['../2_page_photo.jpeg'];
        images.forEach(src => {
            const img = new Image();
            img.src = src;
        });
    }

    // Запускаем принудительную загрузку и предзагрузку
    window.addEventListener('load', function() {
        preloadImages();
        setTimeout(forceLoadImages, 100); // Небольшая задержка для iPhone
    });

    // Обработчик кнопки "Lets go!"
    document.getElementById('letsGoBtn').addEventListener('click', async function() {
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
                const newUrl = baseUrl + '/../page_2/index.html';
                
                console.log('Navigating to:', newUrl);
                window.location.href = newUrl;
            }
        }, 500);
    });
} 