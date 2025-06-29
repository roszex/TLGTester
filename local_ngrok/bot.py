import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv
import asyncio

# Load environment variables from env.local
load_dotenv('env.local')

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBAPP_URL = str(os.getenv('WEBAPP_URL'))
SERVER_URL = os.getenv('SERVER_URL', 'http://localhost:8001')

if not BOT_TOKEN or BOT_TOKEN == 'YOUR_BOT_TOKEN':
    raise RuntimeError("BOT_TOKEN должен быть задан в env.local (не placeholder)")
if not WEBAPP_URL:
    raise RuntimeError("WEBAPP_URL должен быть задан в env.local")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def save_user_to_server(user_id, username):
    """Сохраняет пользователя на сервере"""
    try:
        response = requests.post(
            f"{SERVER_URL}/api/user/{user_id}",
            json={"username": username},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print(f"User {username} saved to server")
        else:
            print(f"Failed to save user: {response.status_code}")
    except Exception as e:
        print(f"Error saving user to server: {e}")

@dp.message(Command("start"))
async def start(message: types.Message):
    # Получаем username пользователя
    user = message.from_user
    if user and user.username:
        username = f"@{user.username}"
    elif user and user.id:
        username = f"user_{user.id}"
    else:
        username = "unknown_user"
    
    # Сохраняем пользователя на сервере
    if user and user.id:
        await save_user_to_server(str(user.id), username)
    
    # Создаем URL с Telegram ID
    webapp_url_with_id = f"{WEBAPP_URL}?user_id={user.id}" if user and user.id else WEBAPP_URL
    
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(
        text="Открыть WebApp",
        web_app=WebAppInfo(url=webapp_url_with_id)
    ))
    await message.answer(
        f"Привет, {username}! Нажми кнопку для запуска WebApp:",
        reply_markup=builder.as_markup(resize_keyboard=True),
        parse_mode=ParseMode.HTML
    )

async def main():
    print(f"Bot starting with token: {BOT_TOKEN[:10] if BOT_TOKEN else 'None'}...")
    print(f"WebApp URL: {WEBAPP_URL}")
    print(f"Server URL: {SERVER_URL}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 