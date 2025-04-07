from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties

import asyncio
from aiohttp import web 
import os

# 🔐 Впиши сюда свой секретный токен
TOKEN = "7613268698:AAGLKzPJMPmv9sZQvTv-Stf9CmXRh2ZdUmg"

# 🧠 Инициализация бота и диспетчера
default_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)  # Настройка parse_mode
bot = Bot(token=TOKEN, default=default_properties)  # Передаем default_properties
dp = Dispatcher(storage=MemoryStorage())

# Простой HTTP-сервер для Render.com
async def on_startup(app):
    asyncio.create_task(dp.start_polling(bot))

app = web.Application()
app.on_startup.append(on_startup)

# Маршрут для проверки работоспособности
async def healthcheck(request):
    return web.Response(text="OK")

app.router.add_get("/", healthcheck)

START_TEXT = """
➤ ТАКСИ-БОТ | НӨКИС - ШЫМБАЙ

Хош келдиңиз!
Бул бот Нөкис ҳәм Шымбай арасында такси буйыртпа етиўдиң ең әпиўайы усылы.

🔹 ЕКИ ЖӨНЕЛИС АРТИҚША ЕМЕС.
🔹 ҲӘММЕ НӘРСЕ ТЕЗ ҲӘМ КҮТИЛМЕГЕН ҲАЛДА ИСЛЕЙДИ.
🔹 АЙДАЎШИЛАР ТЕКСЕРИЛДИ, БУЙЫРТПАЛАР БАҚЛАЎ АЛДИНДА.
🔹 СИЗ ТАНЛАЙСИЗ - БИР НЕШЕ СЕКУНДТА

✅ Маршрут таңласаңыз болды, қалғаны менен биз шуғылланамыз.

✅ 24/7 ислейди.
✅ Әпиўайы. Тез. Исенимли.

☎️ +998976547788

☎️ +998976547788

☎️ +998976547788
"""

TEXT_NOKIS_SHYMBAY = """
🚕 <b>Нокистен → Шымбайга</b>  
   - Жол узынлығы: <i>59,3 км</i>  
   - Уақыт: <i>1 сагат</i>

📞 <b>Телефон</b>: +998770149797
✅ <b>Қосымша хызметлер</b>: АМАНАТ БОЛСА АЛЫП КЕТЕМИЗ  
"""

TEXT_SHYMBAY_NOKIS = """
🚗 <b>Шымбайдан → Нокиске</b>
   - Жол узынлығы: <i>59,3 км</i>   
   - Уақыт: <i>1 сагат</i> 

📞 <b>Телефон</b>: +998770149797
✅ <b>Қосымша хызметлер</b>: АМАНАТ БОЛСА АЛЫП КЕТЕМИЗ  
"""

# Словарь для хранения статистики
user_stats = {}

# 🪑 Обычные кнопки маршрутов
def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Нокис-Шымбай")],
            [KeyboardButton(text="Шымбай-Нукус")]
        ],
        resize_keyboard=True,  # подгоняет размер
        one_time_keyboard=False  # клавиатура остаётся
    )

# 🌀 Команда /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id

    # Если пользователь новый, добавляем его в статистику
    if user_id not in user_stats:
        user_stats[user_id] = 1
    else:
        user_stats[user_id] += 1

    await message.answer(
        START_TEXT,
        reply_markup=get_main_keyboard()
    )

# 🚖 Обработка выбора маршрута
@dp.message(F.text == "Нокис-Шымбай")
async def handle_nukus_shymbay(message: Message):
    user_id = message.from_user.id

    # Увеличиваем счетчик взаимодействий пользователя
    if user_id not in user_stats:
        user_stats[user_id] = 1
    else:
        user_stats[user_id] += 1

    await message.answer(TEXT_NOKIS_SHYMBAY)

@dp.message(F.text == "Шымбай-Нукус")
async def handle_shymbay_nukus(message: Message):
    user_id = message.from_user.id

    # Увеличиваем счетчик взаимодействий пользователя
    if user_id not in user_stats:
        user_stats[user_id] = 1
    else:
        user_stats[user_id] += 1

    await message.answer(TEXT_SHYMBAY_NOKIS)

# 📊 Команда /stats для вывода статистики
@dp.message(F.text == "/stats")
async def show_stats(message: Message):
    total_users = len(user_stats)  # Количество уникальных пользователей
    total_interactions = sum(user_stats.values())  # Общее количество взаимодействий

    await message.answer(
        f"📊 <b>Статистика использования бота:</b>\n"
        f"• Всего пользователей: <b>{total_users}</b>\n"
        f"• Всего взаимодействий: <b>{total_interactions}</b>",
        parse_mode=ParseMode.HTML
    )

# Запуск HTTP-сервера
if __name__ == "__main__":
    web.run_app(app, port=int(os.getenv("PORT", 8080)))
