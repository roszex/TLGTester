// Простой ProgressManager для Telegram WebApp
class ProgressManager {
    constructor() {
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
        
        // НЕ восстанавливаем прогресс при загрузке автоматически
        // Это будет делаться только при явном вызове
    }
    
    // Инициализация Telegram WebApp для полноэкранного режима
    initTelegramWebApp() {
        if (window.Telegram && window.Telegram.WebApp) {
            const tg = window.Telegram.WebApp;
            
            try {
                // Расширяем WebApp на весь экран
                tg.expand();
                
                // Запрашиваем полноэкранный режим если доступен
                if (tg.requestFullscreen) {
                    tg.requestFullscreen();
                }
                
                // Устанавливаем цвета темы для соответствия приложению
                tg.setHeaderColor('#000000');
                tg.setBackgroundColor('#000000');
                
                // Отключаем подтверждение закрытия для предотвращения сообщения "изменения могут не сохраниться"
                if (tg.enableClosingConfirmation) {
                    // Не включаем подтверждение закрытия
                }
                
                // Устанавливаем основную кнопку если нужно
                if (tg.MainButton) {
                    tg.MainButton.hide();
                }
                
                // Устанавливаем безопасную зону для контента
                if (tg.setViewportSettings) {
                    tg.setViewportSettings({
                        can_minimize: false,
                        can_expand: true
                    });
                }
                
                // Отключаем возможность закрытия свайпами
                if (tg.enableClosingConfirmation) {
                    // Не включаем подтверждение закрытия
                }
                
                // Дополнительная защита от закрытия
                if (tg.MainButton) {
                    tg.MainButton.hide();
                }
                
                console.log('Telegram WebApp инициализирован успешно в полноэкранном режиме с безопасной зоной');
            } catch (error) {
                console.error('Ошибка инициализации Telegram WebApp:', error);
            }
        } else {
            console.log('Telegram WebApp недоступен - запуск в режиме браузера');
        }
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
            console.log('ProgressManager: ❌ Нет user ID, пропускаем сохранение формы');
            return false;
        }
        
        console.log('ProgressManager: 🔄 Сохраняем форму для пользователя', this.userId);
        console.log('ProgressManager: 📝 Данные формы:', formData);
        
        try {
            const requestBody = {
                user_id: this.userId,
                form_data: formData
            };
            console.log('ProgressManager: 📤 Отправляем запрос на сервер:', requestBody);
            console.log('ProgressManager: 🌐 URL:', `${this.serverUrl}/api/save_form_data`);
            
            const response = await fetch(`${this.serverUrl}/api/save_form_data`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            });
            
            console.log('ProgressManager: 📥 Получен ответ от сервера:', response.status, response.statusText);
            console.log('ProgressManager: 📋 Headers ответа:', Object.fromEntries(response.headers.entries()));
            
            if (response.ok) {
                const responseData = await response.json();
                console.log('ProgressManager: ✅ Форма успешно сохранена!');
                console.log('ProgressManager: 📄 Ответ сервера:', responseData);
                return true;
            } else {
                const errorText = await response.text();
                console.error('ProgressManager: ❌ Ошибка сохранения формы');
                console.error('ProgressManager: 📊 Статус:', response.status);
                console.error('ProgressManager: 📝 Текст ошибки:', errorText);
                return false;
            }
        } catch (error) {
            console.error('ProgressManager: ❌ Ошибка сети при сохранении формы');
            console.error('ProgressManager: 🐛 Детали ошибки:', error);
            return false;
        }
    }
    
    async goToNextPage() {
        const currentPage = this.getCurrentPage();
        const nextPage = currentPage + 1;
        
        console.log('ProgressManager: Переход на страницу', nextPage);
        
        // Если это последняя страница (25), возвращаемся к первой
        if (currentPage >= 25) {
            console.log('ProgressManager: Это последняя страница, возвращаемся к началу');
            const currentUrl = window.location.href;
            const baseUrl = currentUrl.substring(0, currentUrl.lastIndexOf('/'));
            const newUrl = baseUrl + `/../page_1/index.html?user_id=${this.userId}`;
            
            console.log('ProgressManager: Переходим на первую страницу', newUrl);
            window.location.href = newUrl;
            return;
        }
        
        // Сохраняем прогресс на следующую страницу
        await this.savePage(nextPage);
        
        // Переходим на следующую страницу
        const currentUrl = window.location.href;
        const baseUrl = currentUrl.substring(0, currentUrl.lastIndexOf('/'));
        const newUrl = baseUrl + `/../page_${nextPage}/index.html?user_id=${this.userId}`;
        
        console.log('ProgressManager: Переходим на', newUrl);
        window.location.href = newUrl;
    }
    
    async savePage(pageNumber) {
        if (!this.userId) {
            console.log('ProgressManager: Нет user ID, пропускаем сохранение страницы', pageNumber);
            return;
        }
        
        console.log('ProgressManager: Сохраняем страницу', pageNumber, 'для пользователя', this.userId);
        
        try {
            const requestBody = {
                user_id: this.userId,
                current_page: pageNumber
            };
            console.log('ProgressManager: Отправляем запрос:', requestBody);
            
            const response = await fetch(`${this.serverUrl}/api/save_progress`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            });
            
            console.log('ProgressManager: Получен ответ:', response.status, response.statusText);
            
            if (response.ok) {
                const responseData = await response.json();
                console.log('ProgressManager: Страница', pageNumber, 'сохранена, ответ:', responseData);
            } else {
                const errorText = await response.text();
                console.error('ProgressManager: Ошибка сохранения страницы', pageNumber, response.status, errorText);
            }
        } catch (error) {
            console.error('ProgressManager: Ошибка сети при сохранении страницы', pageNumber, error);
        }
    }
    
    async getSavedProgress() {
        if (!this.userId) {
            console.log('ProgressManager: Нет user ID, пропускаем получение прогресса');
            return null;
        }
        
        try {
            const response = await fetch(`${this.serverUrl}/api/get_progress/${encodeURIComponent(this.userId)}`);
            
            if (response.ok) {
                const data = await response.json();
                console.log('ProgressManager: Получен прогресс', data);
                return data;
            } else {
                console.error('ProgressManager: Ошибка получения прогресса', response.status);
                return null;
            }
        } catch (error) {
            console.error('ProgressManager: Ошибка сети при получении прогресса', error);
            return null;
        }
    }
    
    async restoreProgressOnLoad() {
        console.log('ProgressManager: Восстанавливаем прогресс при загрузке...');
        
        // Получаем текущую страницу
        const currentPage = this.getCurrentPage();
        console.log('ProgressManager: Текущая страница:', currentPage);
        
        // Если мы на первой странице, проверяем есть ли сохраненный прогресс
        if (currentPage === 1) {
            const savedProgress = await this.getSavedProgress();
            
            if (savedProgress && savedProgress.current_page && savedProgress.current_page > 1) {
                console.log(`ProgressManager: Найден сохраненный прогресс - страница ${savedProgress.current_page}`);
                
                // Переходим на сохраненную страницу
                const currentUrl = window.location.href;
                const baseUrl = currentUrl.substring(0, currentUrl.lastIndexOf('/'));
                const newUrl = baseUrl + `/../page_${savedProgress.current_page}/index.html?user_id=${this.userId}`;
                
                console.log('ProgressManager: Переходим на сохраненную страницу', newUrl);
                window.location.href = newUrl;
                return;
            }
        }
        
        // Если мы не на первой странице или нет сохраненного прогресса, просто сохраняем текущую
        console.log('ProgressManager: Сохраняем текущую страницу', currentPage);
        this.saveCurrentPage();
    }
    
    async restoreProgress() {
        const savedProgress = await this.getSavedProgress();
        
        if (savedProgress && savedProgress.current_page) {
            const currentPage = this.getCurrentPage();
            const savedPage = savedProgress.current_page;
            
            // Если мы не на той странице, куда нужно вернуться
            if (currentPage !== savedPage) {
                console.log(`ProgressManager: Восстанавливаем прогресс с страницы ${savedPage}`);
                
                // Переходим на сохраненную страницу
                const currentUrl = window.location.href;
                const baseUrl = currentUrl.substring(0, currentUrl.lastIndexOf('/'));
                const newUrl = baseUrl + `/../page_${savedPage}/index.html?user_id=${this.userId}`;
                
                console.log('ProgressManager: Переходим на сохраненную страницу', newUrl);
                window.location.href = newUrl;
                return true;
            }
        }
        
        return false;
    }
}

// Создаем глобальный экземпляр
console.log('ProgressManager: Создаем экземпляр...');
window.progressManager = new ProgressManager();
console.log('ProgressManager: Экземпляр создан', window.progressManager); 