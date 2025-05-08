import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Загрузка переменных из .env (локально) и среды (Render)
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Получение погоды по городу
def get_weather(city: str, lang: str = "ru") -> str:
    url = (
        "http://api.openweathermap.org/data/2.5/weather"
        f"?q={city}"
        f"&appid={WEATHER_API_KEY}"
        "&units=metric"
        f"&lang={lang}"
    )
    resp = requests.get(url)
    data = resp.json()

    if resp.status_code != 200 or "main" not in data:
        return "⚠️ Не удалось получить данные о погоде."

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]

    return (
        f"🌤 Погода в {city.title()}:\n"
        f"Температура: {temp}°C\n"
        f"Описание: {desc}\n"
        f"Влажность: {humidity}%\n"
        f"Ветер: {wind} м/с"
    )

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши /weather <город>, чтобы узнать погоду.")

# Команда /weather
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Пожалуйста, укажи город после команды. Пример:\n/weather Москва")
        return

    city = " ".join(context.args)
    lang = update.effective_user.language_code or "ru"
    weather_info = get_weather(city, lang)
    await update.message.reply_text(weather_info)

# Основная функция
def main():
    print("🔐 Загруженный токен:", BOT_TOKEN)
    if not BOT_TOKEN:
        raise RuntimeError("❌ Переменная TELEGRAM_TOKEN не найдена или пуста!")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weather", weather))
    app.run_polling()

if __name__ == "__main__":
    main()
