import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.filters import CommandStart
from dotenv import load_dotenv
import asyncio

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    raise ValueError('BOT_TOKEN is not set in .env file')

WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://roszex.github.io/EmelyanovTGBot-webapp/page_1/index.html')

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def send_webapp_link(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Lets go!', web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await message.answer('Открой WebApp для продолжения:', reply_markup=keyboard)

if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot)) 