import asyncio
import logging
import os
import secrets
import string

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiohttp import ClientSession

logging.basicConfig(level=logging.INFO)

# === Настройки ===
BOT_TOKEN = os.getenv("8791998920:AAEveGDcaT7izBgfTHjdFQbaMYL2gOsq5S8")
BACKEND_URL = os.getenv("BACKEND_URL", "https://example.com")
ADMIN_ID = 6248909662  # ← ВПИШИ СВОЙ TELEGRAM ID

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# === Хранилище кодов ===
invite_codes = {}   # {код: кто выдал}
used_codes = set()  # использованные коды


# === Генерация кода ===
def generate_invite_code(length=8):
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


# === Команда для админа: создать код ===
@dp.message(commands=["getcode"])
async def get_code(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("У вас нет прав.")

    code = generate_invite_code()
    invite_codes[code] = message.from_user.id

    await message.answer(
        f"Ваш пригласительный код:\n\n<code>{code}</code>\n\n"
        f"Отправьте его пользователю, чтобы он мог войти."
    )


# === Проверка кода при входе ===
@dp.message(commands=["start"])
async def start(message: types.Message):
    args = message.text.split()

    # Если пользователь ввёл код
    if len(args) == 2:
        code = args[1].strip().upper()

        if code in used_codes:
            return await message.answer("Этот код уже использован.")

        if code not in invite_codes:
            return await message.answer("Неверный или просроченный код.")

        used_codes.add(code)
        return await message.answer("Добро пожаловать! Код принят.")

    # Если код не указан
    await message.answer(
        "Чтобы войти, используйте:\n"
        "/start <пригласительный_код>"
    )


# === Основная логика бота ===
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


# === Запуск ===
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
