import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv(".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
# Используем Git-Pages сервер для WebApp
WEBAPP_URL = str(os.getenv("WEBAPP_URL"))

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN должен быть задан в .env файле")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    # Логируем данные пользователя
    print(f"Bot: Получен /start от пользователя:")
    if message.from_user:
        print(f"Bot: username = {message.from_user.username}")
        print(f"Bot: id = {message.from_user.id}")
        print(f"Bot: first_name = {message.from_user.first_name}")
        print(f"Bot: last_name = {message.from_user.last_name}")
    else:
        print(f"Bot: message.from_user is None")
    
    # Формируем user_id - ВСЕГДА используем username или ID
    user_id = None
    if message.from_user and message.from_user.username:
        user_id = '@' + message.from_user.username
    elif message.from_user and message.from_user.id:
        user_id = 'user_' + str(message.from_user.id)
    else:
        user_id = 'unknown_user'
    
    print(f"Bot: Создан user_id = {user_id}")
    
    # Добавляем user_id к URL
    webapp_url = f"{WEBAPP_URL}?user_id={user_id}"
    print(f"Bot: WebApp URL = {webapp_url}")
    
    # Формируем приветствие
    if message.from_user and message.from_user.username:
        greeting = f"Привет, @{message.from_user.username}! Это демонстрационный вариант Telegram Lead Generator:\n\n📱 Интерактивное веб-приложение\n📊 Сбор данных через форму\n🎯 Автоматические уведомления\n\nНажми 'Смотреть' чтобы протестировать:"
    elif message.from_user and message.from_user.first_name:
        greeting = f"Привет, {message.from_user.first_name}! Это демонстрационный вариант Telegram Lead Generator:\n\n📱 Интерактивное веб-приложение\n📊 Сбор данных через форму\n🎯 Автоматические уведомления\n\nНажми 'Смотреть' чтобы протестировать:"
    else:
        greeting = "Привет! Это демонстрационный вариант Telegram Lead Generator:\n\n📱 Интерактивное веб-приложение\n📊 Сбор данных через форму\n🎯 Автоматические уведомления\n\nНажми 'Смотреть' чтобы протестировать:"
    
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(
        text="Смотреть",
        web_app=WebAppInfo(url=webapp_url)
    ))
    await message.answer(
        greeting,
        reply_markup=builder.as_markup(resize_keyboard=True),
        parse_mode=ParseMode.HTML
    )

@dp.message()
async def handle_webapp_data(message: types.Message):
    # Проверяем, есть ли данные от WebApp
    if message.web_app_data:
        try:
            import json
            data = json.loads(message.web_app_data.data)
            print(f"Bot: Получены данные от WebApp: {data}")
            
            # Обрабатываем разные типы действий
            if data.get('action') == 'thank_you_response':
                # Пользователь завершил приложение
                user_id = data.get('user_id', 'unknown')
                form_data = data.get('form_data', {})
                print(f"Bot: Пользователь {user_id} завершил приложение")
                print(f"Bot: Данные формы: {form_data}")
                
                # Формируем сообщение с данными формы
                form_message = ""
                if form_data:
                    form_message = "\n\n📋 Введенные данные:\n"
                    if form_data.get('age'):
                        form_message += f"• Возраст: {form_data['age']} лет\n"
                    if form_data.get('occupation'):
                        form_message += f"• Деятельность: {form_data['occupation']}\n"
                    if form_data.get('income'):
                        form_message += f"• Доход: {form_data['income']}\n"
                    if form_data.get('motivation'):
                        form_message += f"• Мотивация: {form_data['motivation']}\n"
                    if form_data.get('teamwork'):
                        form_message += f"• Командная работа: {form_data['teamwork']}\n"
                else:
                    form_message = "\n\n📋 Данные формы не найдены"
                
                # Создаем клавиатуру с кнопкой рестарта
                builder = ReplyKeyboardBuilder()
                builder.add(KeyboardButton(
                    text="🔄 Запустить заново",
                    web_app=WebAppInfo(url=f"{WEBAPP_URL}?user_id={user_id}")
                ))
                
                # Отправляем фото с описанием, данными формы и кнопкой рестарта
                caption = f"Если тебе интересно рассчитать стоимость под твой проект или сделать подобный -{form_message}\n\nСвязь со мной: @desperatecoder\n\nТелеграм канал: https://t.me/desperateecoder"
                
                try:
                    await message.answer_photo(
                        photo=types.FSInputFile("outro_image.JPG"),
                        caption=caption,
                        reply_markup=builder.as_markup(resize_keyboard=True)
                    )
                    print(f"Bot: Сообщение с данными формы и кнопкой рестарта отправлено пользователю {user_id}")
                except Exception as photo_error:
                    print(f"Bot: Ошибка при отправке фото: {photo_error}")
                    # Отправляем только текст, если фото не удалось отправить
                    await message.answer(
                        caption,
                        reply_markup=builder.as_markup(resize_keyboard=True)
                    )
                    print(f"Bot: Отправлено текстовое сообщение с данными формы пользователю {user_id}")
                
            else:
                print(f"Bot: Неизвестное действие: {data.get('action')}")
                
        except json.JSONDecodeError as e:
            print(f"Bot: Ошибка парсинга JSON: {e}")
        except Exception as e:
            print(f"Bot: Ошибка обработки данных WebApp: {e}")
    else:
        # Обычное сообщение, игнорируем
        pass

async def main():
    # Удаляем webhook перед запуском polling
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        print("Webhook удален, запускаем polling...")
    except Exception as e:
        print(f"Ошибка при удалении webhook: {e}")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 