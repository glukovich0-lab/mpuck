from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import aiohttp

from db import init_db, verify_user, is_verified
from config import BOT_TOKEN, BACKEND_URL

bot = Bot("8791998920:AAEveGDcaT7izBgfTHjdFQbaMYL2gOsq5S8")
dp = Dispatcher()

@dp.startup()
async def on_startup():
    init_db()


@dp.message(Command("start"))
async def start(message: types.Message):
    args = message.text.split()

    if len(args) == 2:
        code = args[1]

        if verify_user(message.from_user.id, code):
            await message.answer("Доступ открыт. Добро пожаловать в mpuck!")
        else:
            await message.answer("Неверный или использованный код.")
    else:
        await message.answer("Введите инвайт-код: /start OrangeLight1002-1111")


@dp.message(Command("search"))
async def search(message: types.Message):
    if not is_verified(message.from_user.id):
        await message.answer("У вас нет доступа. Введите инвайт-код.")
        return

    query = message.text.replace("/search", "").strip()

    if not query:
        await message.answer("Введите запрос: /search название")
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BACKEND_URL}/search?q={query}") as resp:
            data = await resp.json()

    if not data:
        await message.answer("Ничего не найдено.")
        return

    text = "Результаты поиска mpuck:\n\n"
    for item in data:
        text += f"• {item['title']} ({item['type']})\n"

    await message.answer(text)


if __name__ == "__main__":
    dp.run_polling(bot)
