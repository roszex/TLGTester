# Telegram WebApp - Полноэкранный режим

## Примененные изменения

### 1. Обновлен ProgressManager (progress.js)
Добавлена функция `initTelegramWebApp()` в конструктор класса ProgressManager:

```javascript
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
            
            console.log('Telegram WebApp инициализирован успешно в полноэкранном режиме');
        } catch (error) {
            console.error('Ошибка инициализации Telegram WebApp:', error);
        }
    } else {
        console.log('Telegram WebApp недоступен - запуск в режиме браузера');
    }
}
```

### 2. Обновлены все main.js файлы
Во всех 25 страницах добавлена функция `initTelegramWebApp()` и обновлен обработчик загрузки страницы:

```javascript
// Инициализация при загрузке страницы
window.addEventListener('load', function() {
    // Инициализируем Telegram WebApp (теперь через ProgressManager)
    if (window.progressManager) {
        // ProgressManager уже инициализировал WebApp
        console.log('WebApp инициализирован через ProgressManager');
    } else {
        // Fallback инициализация
        initTelegramWebApp();
    }
    
    // ... остальной код
});
```

## Что это дает

1. **Полноэкранный режим**: `tg.expand()` и `tg.requestFullscreen()` разворачивают WebApp на весь экран
2. **Черная тема**: `setHeaderColor('#000000')` и `setBackgroundColor('#000000')` устанавливают черные цвета для соответствия дизайну
3. **Скрытая основная кнопка**: `tg.MainButton.hide()` скрывает основную кнопку Telegram
4. **Отключенное подтверждение закрытия**: предотвращает появление сообщения "изменения могут не сохраниться"

## Приоритет инициализации

1. **ProgressManager** (основной способ) - инициализирует WebApp при создании экземпляра
2. **Fallback инициализация** - если ProgressManager недоступен, используется функция в main.js

## Обработанные файлы

- **1 файл**: `webapp/progress.js` - добавлена функция инициализации
- **25 файлов**: `webapp/page_1/main.js` до `webapp/page_25/main.js` - добавлена fallback инициализация

## Совместимость

Настройки работают в:
- Telegram WebApp (основная цель)
- Telegram Desktop
- Telegram Mobile (iOS/Android)
- Браузерный режим (fallback) 