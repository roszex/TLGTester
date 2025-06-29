#!/usr/bin/env python3
"""
Скрипт для обновления всех страниц в GitHub Pages версии
Добавляет progress.js и Telegram WebApp скрипт во все HTML файлы
"""

import os
import re

def update_html_file(file_path):
    """Обновляет HTML файл, добавляя необходимые скрипты"""
    print(f"Обновляю {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем, есть ли уже progress.js
    if 'progress.js' in content:
        print(f"  {file_path} уже обновлен")
        return
    
    # Ищем место для вставки скриптов (перед закрывающим </body>)
    if '</body>' in content:
        # Подготавливаем скрипты для вставки
        scripts = '''
    <!-- Telegram WebApp Script -->
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    
    <!-- Progress Manager -->
    <script src="../progress.js"></script>
    
    <!-- Main Script -->
    <script src="main.js"></script>
'''
        
        # Вставляем скрипты перед </body>
        new_content = content.replace('</body>', f'{scripts}</body>')
        
        # Записываем обновленный файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  {file_path} обновлен")
    else:
        print(f"  Ошибка: не найден </body> в {file_path}")

def update_main_js(file_path):
    """Обновляет main.js файл для использования ProgressManager"""
    print(f"Обновляю {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем, есть ли уже ProgressManager
    if 'progressManager' in content:
        print(f"  {file_path} уже обновлен")
        return
    
    # Ищем навигацию и обновляем её
    if 'window.location.href' in content:
        # Простой паттерн для обновления навигации
        old_pattern = r'window\.location\.href\s*=\s*([^;]+);'
        new_pattern = r'''// Используем ProgressManager если доступен
            if (window.progressManager) {
                console.log('Using ProgressManager for navigation');
                await window.progressManager.goToNextPage();
            } else {
                // Fallback на старый метод
                window.location.href = \1;
            }'''
        
        # Обновляем навигацию
        new_content = re.sub(old_pattern, new_pattern, content)
        
        # Добавляем async к функциям с навигацией
        if 'addEventListener' in new_content and 'async' not in new_content:
            new_content = new_content.replace(
                'addEventListener(\'click\', function() {',
                'addEventListener(\'click\', async function() {'
            )
        
        # Записываем обновленный файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  {file_path} обновлен")
    else:
        print(f"  {file_path} не содержит навигацию")

def main():
    """Основная функция"""
    webapp_dir = 'webapp'
    
    if not os.path.exists(webapp_dir):
        print(f"Ошибка: папка {webapp_dir} не найдена")
        return
    
    print("Начинаю обновление всех страниц...")
    
    # Проходим по всем папкам page_*
    for item in os.listdir(webapp_dir):
        page_dir = os.path.join(webapp_dir, item)
        
        if os.path.isdir(page_dir) and item.startswith('page_'):
            print(f"\nОбрабатываю {item}...")
            
            # Обновляем index.html
            index_path = os.path.join(page_dir, 'index.html')
            if os.path.exists(index_path):
                update_html_file(index_path)
            
            # Обновляем main.js
            main_js_path = os.path.join(page_dir, 'main.js')
            if os.path.exists(main_js_path):
                update_main_js(main_js_path)
    
    print("\nОбновление завершено!")
    print("\nТеперь все страницы используют ProgressManager для навигации и сохранения прогресса.")

if __name__ == '__main__':
    main() 