from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import json
import logging

API_TOKEN = "7573925049:AAE8rY1dNCO9anir_lJ7XN56e228jDqXsbc"
OWNER_ID = 454453304

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton(
            text="📝 Записаться",
            web_app=WebAppInfo(url="https://telegram-booking-app.vercel.app")
        )
    )
    await message.answer("Нажмите кнопку ниже, чтобы заполнить анкету:", reply_markup=keyboard)

@dp.message_handler(content_types=['web_app_data'])
async def webapp_data_handler(message: types.Message):
    data = json.loads(message.web_app_data.data)

    text = (
        "🆕 <b>Новая заявка</b>\n\n"
        f"👪 <b>Родитель:</b> {data.get('parent')}\n"
        f"📞 <b>Телефон:</b> {data.get('phone')}\n"
        f"🎂 <b>Возраст ребёнка:</b> {data.get('age')}\n"
        f"📋 <b>Противопоказания:</b> {data.get('contraindications') or '—'}\n"
        f"🥋 <b>Опыт спорта:</b> {data.get('sport_experience') or '—'}\n"
        f"🎯 <b>Цели:</b> {', '.join(data.get('goals', [])) or '—'}\n"
        f"📅 <b>Дни:</b> {', '.join(data.get('days', [])) or '—'}\n"
        f"🔍 <b>Источник:</b> {', '.join(data.get('source', [])) or '—'}\n"
        f"📝 <b>Комментарий:</b> {data.get('comment') or '—'}"
    )

    await bot.send_message(chat_id=OWNER_ID, text=text, parse_mode="HTML")
    await message.answer("✅ Заявка отправлена! Спасибо!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)