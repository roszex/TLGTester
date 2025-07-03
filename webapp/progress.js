// Простой ProgressManager для Telegram WebApp - ТЕСТИРОВАНИЕ
// ВСЕ ОТПРАВКИ ДАННЫХ ОТКЛЮЧЕНЫ

class ProgressManager {
    constructor() {
        console.log('=== ТЕСТИРОВАНИЕ - ProgressManager ===');
        console.log('ProgressManager: ВСЕ ОТПРАВКИ ДАННЫХ ОТКЛЮЧЕНЫ');
        console.log('ProgressManager: Конструктор вызван');
        console.log('ProgressManager: Telegram WebApp доступен:', !!(window.Telegram && window.Telegram.WebApp));
        
        // Инициализируем Telegram WebApp
        this.initTelegramWebApp();
        
        // Сначала пробуем получить из URL (приоритет от бота)
        const urlParams = new URLSearchParams(window.location.search);
        this.userId = urlParams.get('user_id');
        console.log('ProgressManager: user_id из URL:', this.userId);
        console.log('ProgressManager: Полный URL:', window.location.href);
        console.log('ProgressManager: Все параметры URL:', Array.from(urlParams.entries()));
        
        // Если нет из URL, пробуем из Telegram WebApp (fallback)
        if (!this.userId && window.Telegram && window.Telegram.WebApp) {
            const tgUser = window.Telegram.WebApp.initDataUnsafe?.user;
            console.log('ProgressManager: Telegram user:', tgUser);
            console.log('ProgressManager: Telegram user.username:', tgUser?.username);
            console.log('ProgressManager: Telegram user.id:', tgUser?.id);
            console.log('ProgressManager: Telegram user.first_name:', tgUser?.first_name);
            console.log('ProgressManager: Telegram user.last_name:', tgUser?.last_name);
            
            if (tgUser && tgUser.username) {
                this.userId = '@' + tgUser.username;
                console.log('ProgressManager: user_id из Telegram username:', this.userId);
            } else if (tgUser && tgUser.id) {
                this.userId = 'user_' + tgUser.id;
                console.log('ProgressManager: user_id из Telegram ID:', this.userId);
            }
        }
        
        // Если все еще нет user_id, создаем временный
        if (!this.userId) {
            this.userId = 'temp_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            console.log('ProgressManager: Создан временный user ID:', this.userId);
        }
        
        // Определяем среду
        this.isTelegram = !!(window.Telegram && window.Telegram.WebApp);
        this.serverUrl = 'https://emelyanovtgbot-webapp-production.up.railway.app';
        
        console.log('ProgressManager: User ID =', this.userId);
        console.log('ProgressManager: Telegram =', this.isTelegram);
        console.log('ProgressManager: Server URL =', this.serverUrl);
        console.log('ProgressManager: ⚠️ ТЕСТИРОВАНИЕ - ВСЕ ОТПРАВКИ ДАННЫХ ОТКЛЮЧЕНЫ ⚠️');
        console.log('ProgressManager: Данные НЕ будут отправляться на сервер');
        
        // НЕ восстанавливаем прогресс при загрузке автоматически
        // Это будет делаться только при явном вызове
    }
    
    initTelegramWebApp() {
        if (window.Telegram && window.Telegram.WebApp) {
            try {
                window.Telegram.WebApp.ready();
                console.log('ProgressManager: Telegram WebApp готов');
                
                // Устанавливаем тему
                window.Telegram.WebApp.setHeaderColor('#000000');
                window.Telegram.WebApp.setBackgroundColor('#000000');
                
                console.log('ProgressManager: Тема установлена');
            } catch (error) {
                console.error('ProgressManager: Ошибка инициализации Telegram WebApp:', error);
            }
        } else {
            console.log('ProgressManager: Telegram WebApp недоступен');
        }
    }
    
    getCurrentPage() {
        const currentUrl = window.location.href;
        const pageMatch = currentUrl.match(/page_(\d+)/);
        if (pageMatch) {
            return parseInt(pageMatch[1]);
        }
        return 1;
    }
    
    async saveCurrentPage() {
        console.log('⚠️ ProgressManager: ТЕСТИРОВАНИЕ - сохранение страницы ОТКЛЮЧЕНО');
        console.log('⚠️ Данные НЕ отправляются на сервер');
        return;
    }
    
    async saveFormData(formData) {
        console.log('⚠️ ProgressManager: ТЕСТИРОВАНИЕ - сохранение формы ОТКЛЮЧЕНО');
        console.log('⚠️ Данные формы (НЕ отправляются):', formData);
        console.log('⚠️ В реальном приложении эти данные были бы отправлены на сервер');
        return true; // Возвращаем true для продолжения работы
    }
    
    async goToNextPage() {
        const currentPage = this.getCurrentPage();
        const nextPage = currentPage + 1;
        
        console.log('ProgressManager: Переход на страницу', nextPage);
        
        // Если это последняя страница (4), возвращаемся к первой
        if (currentPage >= 4) {
            console.log('ProgressManager: Это последняя страница, возвращаемся к началу');
            const currentUrl = window.location.href;
            const baseUrl = currentUrl.substring(0, currentUrl.lastIndexOf('/'));
            const newUrl = baseUrl + `/../page_1/index.html?user_id=${this.userId}`;
            
            console.log('ProgressManager: Переходим на первую страницу', newUrl);
            window.location.href = newUrl;
            return;
        }
        
        // Переходим на следующую страницу
        const currentUrl = window.location.href;
        const baseUrl = currentUrl.substring(0, currentUrl.lastIndexOf('/'));
        const newUrl = baseUrl + `/../page_${nextPage}/index.html?user_id=${this.userId}`;
        
        console.log('ProgressManager: Переходим на', newUrl);
        window.location.href = newUrl;
    }
    
    async savePage(pageNumber) {
        console.log('⚠️ ProgressManager: ТЕСТИРОВАНИЕ - сохранение страницы', pageNumber, 'ОТКЛЮЧЕНО');
        console.log('⚠️ Данные НЕ отправляются на сервер');
        return;
    }
    
    async getSavedProgress() {
        console.log('⚠️ ProgressManager: ТЕСТИРОВАНИЕ - получение прогресса ОТКЛЮЧЕНО');
        console.log('⚠️ Данные НЕ загружаются с сервера');
        return null;
    }
    
    async restoreProgressOnLoad() {
        console.log('⚠️ ProgressManager: ТЕСТИРОВАНИЕ - восстановление прогресса ОТКЛЮЧЕНО');
        console.log('⚠️ Данные НЕ загружаются с сервера');
        return;
    }
    
    async restoreProgress() {
        console.log('⚠️ ProgressManager: ТЕСТИРОВАНИЕ - восстановление прогресса ОТКЛЮЧЕНО');
        console.log('⚠️ Данные НЕ загружаются с сервера');
        return false;
    }
}

// Создаем глобальный экземпляр
console.log('=== ТЕСТИРОВАНИЕ - Создание ProgressManager ===');
console.log('⚠️ ВСЕ ОТПРАВКИ ДАННЫХ ОТКЛЮЧЕНЫ ⚠️');
window.progressManager = new ProgressManager();
console.log('ProgressManager: Экземпляр создан', window.progressManager); 