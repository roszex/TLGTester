# Ограничения для мобильных устройств

## Примененные изменения

### HTML Meta теги
Во всех страницах webapp добавлены следующие meta теги для предотвращения поворота экрана и зума:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<meta name="screen-orientation" content="portrait">
<meta name="x5-orientation" content="portrait">
<meta name="full-screen" content="yes">
<meta name="x5-fullscreen" content="true">
```

### CSS стили
В CSS файлах добавлены стили для предотвращения зума и поворота:

#### В селекторе `html`:
```css
/* Prevent zoom and rotation */
touch-action: manipulation;
-webkit-touch-action: manipulation;
```

#### В селекторе `body`:
```css
/* Prevent zoom and rotation */
touch-action: manipulation;
-webkit-touch-action: manipulation;
/* Prevent text selection and zoom */
-webkit-text-size-adjust: none;
-moz-text-size-adjust: none;
-ms-text-size-adjust: none;
text-size-adjust: none;
```

## Что это дает

1. **Запрет зума**: `maximum-scale=1.0, user-scalable=no` и `touch-action: manipulation` предотвращают масштабирование страницы
2. **Фиксация ориентации**: `screen-orientation: portrait` и `x5-orientation: portrait` фиксируют портретную ориентацию
3. **Предотвращение изменения размера текста**: `text-size-adjust: none` отключает автоматическое изменение размера текста
4. **Полноэкранный режим**: `full-screen: yes` и `x5-fullscreen: true` для лучшего отображения

## Обработанные файлы

Обновлено **25 страниц** в папке `webapp/`:
- page_1 до page_25
- Каждая страница содержит обновленный HTML и CSS

## Совместимость

Примененные ограничения работают на:
- iOS Safari
- Android Chrome
- Telegram WebApp
- Другие мобильные браузеры 