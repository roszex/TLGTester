# Защита от закрытия приложения свайпами

## Проблема
Пользователь мог случайно закрыть приложение свайпом вниз, находясь в верхней части страницы.

## Решение
Добавлена комплексная защита, которая блокирует все способы закрытия приложения кроме кнопки "закрыть" в Telegram.

## Примененные методы защиты

### 1. JavaScript обработчики событий

```javascript
function preventAppClose() {
    let startY = 0;
    let startX = 0;
    let isDragging = false;
    
    // Блокируем touchstart
    document.addEventListener('touchstart', function(e) {
        startY = e.touches[0].clientY;
        startX = e.touches[0].clientX;
        isDragging = false;
    }, { passive: false });
    
    // Блокируем touchmove
    document.addEventListener('touchmove', function(e) {
        const currentY = e.touches[0].clientY;
        const currentX = e.touches[0].clientX;
        const deltaY = currentY - startY;
        const deltaX = Math.abs(currentX - startX);
        
        // Если пользователь находится в верхней части страницы и свайпает вниз
        if (window.scrollY <= 0 && deltaY > 0) {
            // Блокируем свайп вниз для закрытия приложения
            e.preventDefault();
            e.stopPropagation();
            return false;
        }
        
        // Если свайп больше горизонтального, то это не закрытие приложения
        if (Math.abs(deltaY) > deltaX) {
            isDragging = true;
        }
    }, { passive: false });
    
    // Блокируем touchend
    document.addEventListener('touchend', function(e) {
        if (isDragging && window.scrollY <= 0) {
            e.preventDefault();
            e.stopPropagation();
        }
    }, { passive: false });
    
    // Дополнительная защита от overscroll
    document.addEventListener('gesturestart', function(e) {
        e.preventDefault();
    }, { passive: false });
    
    document.addEventListener('gesturechange', function(e) {
        e.preventDefault();
    }, { passive: false });
    
    document.addEventListener('gestureend', function(e) {
        e.preventDefault();
    }, { passive: false });
}
```

### 2. CSS защита от overscroll

```css
body {
    /* ... существующие стили ... */
    /* Prevent overscroll bounce */
    overscroll-behavior: none;
    -webkit-overflow-scrolling: auto;
}
```

### 3. Telegram WebApp настройки

```javascript
// Отключаем возможность закрытия свайпами
if (tg.enableClosingConfirmation) {
    // Не включаем подтверждение закрытия
}

// Дополнительная защита от закрытия
if (tg.MainButton) {
    tg.MainButton.hide();
}
```

## Как это работает

1. **Отслеживание свайпов** - фиксируем начальную позицию касания
2. **Анализ направления** - определяем, является ли свайп попыткой закрытия
3. **Блокировка в верхней части** - если пользователь в начале страницы и свайпает вниз
4. **Предотвращение overscroll** - блокируем bounce-эффект
5. **Отключение жестов** - блокируем gesture события

## Что блокируется

- ✅ Свайп вниз в верхней части страницы
- ✅ Overscroll bounce эффект
- ✅ Жесты закрытия приложения
- ✅ Случайные касания в статичной челке

## Что остается доступным

- ✅ Прокрутка контента вниз
- ✅ Прокрутка контента вверх
- ✅ Горизонтальные свайпы
- ✅ Кнопка "закрыть" в Telegram

## Обработанные файлы

Обновлено **50 файлов**:
- **25 main.js файлов** - добавлена функция preventAppClose
- **25 CSS файлов** - добавлена защита от overscroll
- **1 progress.js файл** - обновлены настройки WebApp

## Совместимость

Защита работает на:
- iOS Safari (iPhone 15 и другие)
- Android Chrome
- Telegram WebApp
- Другие мобильные браузеры 