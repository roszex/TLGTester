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
    # Формируем user_id
    user_id = None
    if message.from_user and message.from_user.username:
        user_id = '@' + message.from_user.username
    elif message.from_user and message.from_user.id:
        user_id = 'user_' + str(message.from_user.id)
    else:
        user_id = 'unknown_user'
    
    # Добавляем user_id к URL
    webapp_url = f"{WEBAPP_URL}?user_id={user_id}"
    
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(
        text="Открыть WebApp",
        web_app=WebAppInfo(url=webapp_url)
    ))
    await message.answer(
        "Нажми кнопку для запуска WebApp:",
        reply_markup=builder.as_markup(resize_keyboard=True),
        parse_mode=ParseMode.HTML
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 