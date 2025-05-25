import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("WEATHER_API_KEY")

# Настройка логов
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Структура стран и городов
countries = {
    "Россия 🇷🇺": ["Москва", "Санкт-Петербург"],
    "Украина 🇺🇦": ["Киев", "Львов", "Мерефа"],
    "США 🇺🇸": ["Нью-Йорк", "Лос-Анджелес"],
    "Япония 🇯🇵": ["Токио", "Осака"],
    "Германия 🇩🇪": ["Берлин", "Мюнхен"],
    "Франция 🇫🇷": ["Париж", "Лион"]
}

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(country, callback_data=f"country|{country}")]
                for country in countries.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите страну:", reply_markup=reply_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split("|")
    step = data[0]
    value = data[1]

    user_id = query.from_user.id

    if step == "country":
        user_data[user_id] = {"country": value}
        keyboard = [[InlineKeyboardButton(city, callback_data=f"city|{city}")]
                    for city in countries[value]]
        await query.edit_message_text("Выберите город:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif step == "city":
        user_data[user_id]["city"] = value
        keyboard = [
            [InlineKeyboardButton("Русский", callback_data="lang|ru"),
             InlineKeyboardButton("English", callback_data="lang|en")]
        ]
        await query.edit_message_text(f"Вы выбрали город: {value}. Выберите язык:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif step == "lang":
        user_data[user_id]["lang"] = value
        city = user_data[user_id]["city"]
        lang = user_data[user_id]["lang"]
        await send_weather(query, city, lang)

async def send_weather(query, city, lang):
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang={lang}"
    )
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            msg = data.get("message", "Ошибка API")
            await query.edit_message_text(f"⚠️ Ошибка: {msg.capitalize()}")
            return

        if "main" not in data or "weather" not in data:
            await query.edit_message_text("⚠️ Не удалось найти данные о погоде.")
            return

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"].capitalize()
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        dt = datetime.fromtimestamp(data["dt"]).strftime("%d.%m.%Y %H:%M")

        weather_report = (
            f"📍 Город: {city}\n"
            f"🌡 Температура: {temp}°C\n"
            f"🌤 Описание: {desc}\n"
            f"💧 Влажность: {humidity}%\n"
            f"💨 Ветер: {wind} м/с\n"
            f"🕒 Обновлено: {dt}"
        )

        await query.edit_message_text(weather_report)

    except Exception as e:
        await query.edit_message_text(f"❌ Ошибка получения погоды: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.run_polling()
