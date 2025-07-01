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
# Используем Railway сервер для WebApp
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
        greeting = f"Привет, @{message.from_user.username}! Я Emelyanov и это моя история:"
    elif message.from_user and message.from_user.first_name:
        greeting = f"Привет, {message.from_user.first_name}! Я Emelyanov и это моя история:"
    else:
        greeting = "Привет! Я Emelyanov и это моя история:"
    
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(
        text="Читать историю",
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
                # Пользователь нажал кнопку "Как я могу тебя отблагодарить?"
                user_id = data.get('user_id', 'unknown')
                print(f"Bot: Пользователь {user_id} завершил историю")
                
                # Отправляем фото с описанием
                await message.answer_photo(
                    photo=types.FSInputFile("outro_photo.jpeg"),
                    caption="Потом сочтемся)\n\nПиши мне на аккаунт @MakerssAsis, мой ассистент назначит время созвона.\n\nДо встречи братец! Я полетел",
                    reply_markup=types.ReplyKeyboardRemove()
                )
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