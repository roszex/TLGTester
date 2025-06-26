# Emelyanov Telegram Bot - GitHub Pages Version

Это версия Telegram бота, настроенная для развертывания на GitHub Pages.

## Структура проекта

```
github-pages/
├── bot.py              # Основной файл бота
├── env.github          # Переменные окружения для GitHub Pages
├── requirements.txt    # Зависимости Python
└── README.md          # Этот файл
```

## Настройка

1. **Клонируйте репозиторий:**
   ```bash
   git clone <your-repo-url>
   cd EmelyanovTGBot/github-pages
   ```

2. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Настройте переменные окружения:**
   - Откройте файл `env.github`
   - Замените `YOUR_BOT_TOKEN` на токен вашего бота
   - Замените `YOUR_GITHUB_PAGES_URL` на URL вашего GitHub Pages сайта

## Развертывание на GitHub Pages

1. **Создайте репозиторий на GitHub**

2. **Загрузите файлы веб-приложения:**
   - Скопируйте все файлы из папки `webapp/` в корень репозитория
   - Убедитесь, что `index.html` находится в корне

3. **Настройте GitHub Pages:**
   - Перейдите в Settings → Pages
   - Выберите Source: "Deploy from a branch"
   - Выберите Branch: "main" (или "master")
   - Нажмите Save

4. **Получите URL вашего сайта:**
   - GitHub Pages URL будет: `https://your-username.github.io/your-repo-name`
   - Обновите `YOUR_GITHUB_PAGES_URL` в файле `env.github`

## Запуск бота

```bash
python bot.py
```

## Особенности GitHub Pages версии

- **Статическое размещение:** Веб-приложение размещается на GitHub Pages
- **Публичный доступ:** Сайт доступен всем пользователям
- **Автоматическое обновление:** При пуше в main ветку сайт автоматически обновляется
- **HTTPS:** Автоматическое SSL-шифрование

## Структура веб-приложения

Веб-приложение состоит из 14 страниц:
- `page_1/` - `page_14/` - HTML страницы с контентом
- `index.html` - Главная страница с редиректом на page_1
- Изображения: `1_page_photo.jpeg` - `14_page_photo.jpeg`

## Поддержка

При возникновении проблем:
1. Проверьте правильность токена бота
2. Убедитесь, что GitHub Pages URL корректный
3. Проверьте, что все файлы веб-приложения загружены в репозиторий 