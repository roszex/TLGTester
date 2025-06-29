// Простой ProgressManager для GitHub Pages
class ProgressManager {
    constructor() {
        console.log('ProgressManager: Конструктор вызван');
        
        // Получаем user ID из URL
        const urlParams = new URLSearchParams(window.location.search);
        this.userId = urlParams.get('user_id');
        
        // Для GitHub Pages используем простой подход
        this.serverUrl = 'https://your-github-pages-domain.com'; // Замените на ваш домен
        
        console.log('ProgressManager: User ID =', this.userId);
        console.log('ProgressManager: Server URL =', this.serverUrl);
        
        // Сохраняем текущую страницу в localStorage
        this.saveCurrentPage();
    }
    
    getCurrentPage() {
        const path = window.location.pathname;
        const match = path.match(/page_(\d+)/);
        return match ? parseInt(match[1]) : 1;
    }
    
    saveCurrentPage() {
        if (!this.userId) {
            console.log('ProgressManager: Нет user ID, пропускаем сохранение');
            return;
        }
        
        const page = this.getCurrentPage();
        console.log('ProgressManager: Сохраняем страницу', page);
        
        // Сохраняем в localStorage для GitHub Pages
        const progressData = {
            user_id: this.userId,
            current_page: page,
            timestamp: new Date().toISOString()
        };
        
        localStorage.setItem(`progress_${this.userId}`, JSON.stringify(progressData));
        console.log('ProgressManager: Страница сохранена в localStorage');
    }
    
    async saveFormData(formData) {
        if (!this.userId) {
            console.log('ProgressManager: Нет user ID, пропускаем сохранение формы');
            return false;
        }
        
        console.log('ProgressManager: Сохраняем форму', formData);
        
        // Сохраняем в localStorage для GitHub Pages
        const formDataKey = `form_${this.userId}`;
        localStorage.setItem(formDataKey, JSON.stringify(formData));
        
        // Также сохраняем прогресс
        this.saveCurrentPage();
        
        console.log('ProgressManager: Форма сохранена в localStorage');
        return true;
    }
    
    getFormData() {
        if (!this.userId) {
            return null;
        }
        
        const formDataKey = `form_${this.userId}`;
        const saved = localStorage.getItem(formDataKey);
        return saved ? JSON.parse(saved) : null;
    }
    
    getProgress() {
        if (!this.userId) {
            return null;
        }
        
        const progressKey = `progress_${this.userId}`;
        const saved = localStorage.getItem(progressKey);
        return saved ? JSON.parse(saved) : null;
    }
    
    async goToNextPage() {
        const currentPage = this.getCurrentPage();
        const nextPage = currentPage + 1;
        
        console.log('ProgressManager: Переход на страницу', nextPage);
        
        // Сохраняем прогресс
        this.saveCurrentPage();
        
        // Переходим на следующую страницу
        const currentUrl = window.location.href;
        const baseUrl = currentUrl.substring(0, currentUrl.lastIndexOf('/'));
        const newUrl = baseUrl + `/../page_${nextPage}/index.html?user_id=${this.userId}`;
        
        console.log('ProgressManager: Переходим на', newUrl);
        window.location.href = newUrl;
    }
    
    async goToPrevPage() {
        const currentPage = this.getCurrentPage();
        const prevPage = Math.max(1, currentPage - 1);
        
        console.log('ProgressManager: Переход на страницу', prevPage);
        
        // Сохраняем прогресс
        this.saveCurrentPage();
        
        // Переходим на предыдущую страницу
        const currentUrl = window.location.href;
        const baseUrl = currentUrl.substring(0, currentUrl.lastIndexOf('/'));
        const newUrl = baseUrl + `/../page_${prevPage}/index.html?user_id=${this.userId}`;
        
        console.log('ProgressManager: Переходим на', newUrl);
        window.location.href = newUrl;
    }
}

// Создаем глобальный экземпляр
console.log('ProgressManager: Создаем экземпляр...');
window.progressManager = new ProgressManager();
console.log('ProgressManager: Экземпляр создан', window.progressManager); 