import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiohttp import ClientSession

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "https://example.com")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message()
async def handle_message(message: types.Message):
    text = message.text.strip()

    async with ClientSession() as session:
        try:
            async with session.get(f"{BACKEND_URL}/search?q={text}") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    answer = data.get("answer", "Нет ответа")
                else:
                    answer = "Ошибка backend"
        except Exception:
            answer = "Backend недоступен"

    await message.answer(answer)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
