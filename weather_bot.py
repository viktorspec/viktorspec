import logging
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Функция получения погоды
def get_weather(city: str, lang: str) -> str:
    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city}"
        f"&appid={API_KEY}"
        f"&units=metric"
        f"&lang={lang}"
    )
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or "main" not in data:
        return "⚠️ Не удалось получить данные о погоде. Проверьте название города."

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]

    return (
        f"🌤 Погода в {city.title()}:\n"
        f"Температура: {temp}°C\n"
        f"Описание: {desc}\n"
        f"Влажность: {humidity}%\n"
        f"Скорость ветра: {wind} м/с"
    )

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Отправь мне название города, чтобы узнать погоду 🌍")

# Обработчик команды /weather
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) == 0:
        await update.message.reply_text("Пожалуйста, укажи город после команды. Пример:\n`/weather Москва`", parse_mode="Markdown")
        return

    city = " ".join(context.args)
    user_lang = update.effective_user.language_code or "ru"

    report = get_weather(city, user_lang)
    await update.message.reply_text(report)

# Основной запуск
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weather", weather))

    app.run_polling()

if __name__ == "__main__":
    main()
