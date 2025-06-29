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
WEBAPP_URL = "https://emelyanovtgbot-webapp-production.up.railway.app/"

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN должен быть задан в .env файле")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(
        text="Открыть WebApp",
        web_app=WebAppInfo(url=WEBAPP_URL)
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