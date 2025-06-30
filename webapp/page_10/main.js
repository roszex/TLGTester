
// Обработчик кнопки
document.addEventListener('DOMContentLoaded', function() {
    const nextBtn = document.querySelector('.lets-go');
    if (nextBtn) {
        nextBtn.addEventListener('click', goToNextPage);
    }
});
