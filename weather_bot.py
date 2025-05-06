from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import requests

from dotenv import load_dotenv
import os

# 🔑 Токен Telegram-бота
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
# 🔑 Токен OpenWeather API
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
# 🌍 Список стран и городов
countries = {
    "USA": [("New York", "New York"), ("Los Angeles", "Los Angeles")],
    "Russia": [("Москва", "Moscow"), ("Санкт-Петербург", "Saint Petersburg")],
    "Japan": [("Токио", "Tokyo"), ("Осака", "Osaka")],
}

# 📍 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(country, callback_data=f"country_{country}")]
        for country in countries
    ]
    await update.message.reply_text("Выберите страну:", reply_markup=InlineKeyboardMarkup(keyboard))

# 📍 Выбор страны
async def country_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    country = query.data.split("_")[1]
    context.user_data["country"] = country

    cities = countries[country]
    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"city_{city}")] for name, city in cities
    ]
    await query.edit_message_text("Выберите город:", reply_markup=InlineKeyboardMarkup(keyboard))

# 🏙️ Выбор города
async def city_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    city = query.data.split("_", 1)[1]
    context.user_data["city"] = city

    keyboard = [
        [InlineKeyboardButton("Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("English", callback_data="lang_en")],
    ]
    await query.edit_message_text(f"Вы выбрали город: {city}. Выберите язык:", reply_markup=InlineKeyboardMarkup(keyboard))

# 🌐 Выбор языка
async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("_")[1]
    context.user_data["lang"] = lang

    city = context.user_data.get("city")
    if not city:
        await query.edit_message_text("Ошибка: город не выбран.")
        return

    weather = get_weather(city, lang)
    await query.edit_message_text(weather)

# 🌤️ Получение погоды
def get_weather(city, lang):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=("7295c0329e9785c5635782bfaaf13991")&units=metric&lang={lang}"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        return "Ошибка при получении данных о погоде."

    name = data["name"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    desc = data["weather"][0]["description"]

    return (
        f"Город: {name}\n"
        f"Температура: {temp}°C\n"
        f"Погода: {desc.capitalize()}\n"
        f"Влажность: {humidity}%\n"
        f"Ветер: {wind} м/с"
    )

# 🚀 Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(country_callback, pattern="^country_"))
    app.add_handler(CallbackQueryHandler(city_callback, pattern="^city_"))
    app.add_handler(CallbackQueryHandler(language_callback, pattern="^lang_"))
    app.run_polling()
