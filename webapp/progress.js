// Простой ProgressManager для Telegram WebApp
class ProgressManager {
    constructor() {
        console.log('ProgressManager: Конструктор вызван');
        
        // Получаем user ID из URL или из Telegram WebApp
        const urlParams = new URLSearchParams(window.location.search);
        this.userId = urlParams.get('user_id');
        
        // Если нет user_id в URL, пробуем получить из Telegram WebApp
        if (!this.userId && window.Telegram && window.Telegram.WebApp) {
            const tgUser = window.Telegram.WebApp.initDataUnsafe?.user;
            if (tgUser && tgUser.username) {
                this.userId = '@' + tgUser.username;
            } else if (tgUser && tgUser.id) {
                this.userId = 'user_' + tgUser.id;
            }
        }
        
        // Определяем среду
        this.isTelegram = !!(window.Telegram && window.Telegram.WebApp);
        this.serverUrl = 'https://emelyanovtgbot-webapp-production.up.railway.app';
        
        console.log('ProgressManager: User ID =', this.userId);
        console.log('ProgressManager: Telegram =', this.isTelegram);
        console.log('ProgressManager: Server URL =', this.serverUrl);
        
        // Сохраняем текущую страницу
        this.saveCurrentPage();
    }
    
    getCurrentPage() {
        const path = window.location.pathname;
        const match = path.match(/page_(\d+)/);
        return match ? parseInt(match[1]) : 1;
    }
    
    async saveCurrentPage() {
        if (!this.userId) {
            console.log('ProgressManager: Нет user ID, пропускаем сохранение');
            return;
        }
        
        const page = this.getCurrentPage();
        console.log('ProgressManager: Сохраняем страницу', page);
        
        try {
            const response = await fetch(`${this.serverUrl}/api/save_progress`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: this.userId,
                    current_page: page
                })
            });
            
            if (response.ok) {
                console.log('ProgressManager: Страница сохранена');
            } else {
                console.error('ProgressManager: Ошибка сохранения', response.status);
            }
        } catch (error) {
            console.error('ProgressManager: Ошибка сети', error);
        }
    }
    
    async saveFormData(formData) {
        if (!this.userId) {
            console.log('ProgressManager: Нет user ID, пропускаем сохранение формы');
            return false;
        }
        
        console.log('ProgressManager: Сохраняем форму', formData);
        
        try {
            const response = await fetch(`${this.serverUrl}/api/save_progress`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: this.userId,
                    current_page: this.getCurrentPage(),
                    form_data: formData
                })
            });
            
            if (response.ok) {
                console.log('ProgressManager: Форма сохранена');
                return true;
            } else {
                console.error('ProgressManager: Ошибка сохранения формы', response.status);
                return false;
            }
        } catch (error) {
            console.error('ProgressManager: Ошибка сети при сохранении формы', error);
            return false;
        }
    }
    
    async goToNextPage() {
        const currentPage = this.getCurrentPage();
        const nextPage = currentPage + 1;
        
        console.log('ProgressManager: Переход на страницу', nextPage);
        
        // Сохраняем прогресс
        await this.saveCurrentPage();
        
        // Переходим на следующую страницу
        const currentUrl = window.location.href;
        const baseUrl = currentUrl.substring(0, currentUrl.lastIndexOf('/'));
        const newUrl = baseUrl + `/../page_${nextPage}/index.html?user_id=${this.userId}`;
        
        console.log('ProgressManager: Переходим на', newUrl);
        window.location.href = newUrl;
    }
}

// Создаем глобальный экземпляр
console.log('ProgressManager: Создаем экземпляр...');
window.progressManager = new ProgressManager();
console.log('ProgressManager: Экземпляр создан', window.progressManager); 