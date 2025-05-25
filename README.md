# 🌤️ Weather Telegram Bot with Buttons

A user-friendly and multilingual Telegram bot that shows current weather based on the selected country, city, and language — with interactive buttons and OpenWeather API integration.

---

## 🚀 Features

- Country → City → Language selection via buttons
- Weather info includes:
  - Temperature
  - Description
  - Humidity
  - Wind speed
  - Last update time
- Supports multiple countries (🇺🇦 🇷🇺 🇺🇸 🇯🇵 🇩🇪 🇫🇷)
- Includes **Merefa**, hometown of the creator ❤️
- Built with `python-telegram-bot` and `requests`
- Secure token handling with `.env`
- Fully compatible with **Render** deployment

---

## 🌍 Example Countries and Cities

- **🇺🇦 Ukraine**: Kyiv, Lviv, Merefa
- **🇷🇺 Russia**: Moscow, Saint Petersburg
- **🇺🇸 USA**: New York, Los Angeles
- **🇯🇵 Japan**: Tokyo, Osaka
- **🇩🇪 Germany**: Berlin, Munich
- **🇫🇷 France**: Paris, Lyon

---

## 🛠️ Technologies

- Python 3.11+
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- requests
- dotenv

---

## 📦 Project Structure

```
weather_bot/
├── weather_bot.py          # Main bot code
├── .env                    # Environment variables (not uploaded)
├── requirements.txt        # Dependencies
└── README.md               # Project description
```

---

## 📥 Installation

1. **Clone the repository**

```bash
git clone https://github.com/viktorspec/viktorspec.git
cd viktorspec
```

2. **Create `.env` file** with your tokens:

```env
TELEGRAM_TOKEN=your_botfather_token
WEATHER_API_KEY=your_openweather_token
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the bot locally**

```bash
python weather_bot.py
```

---

## ☁️ Deploy to Render

- Set environment variables in Render dashboard:
  - `TELEGRAM_TOKEN`
  - `WEATHER_API_KEY`
- Use `web service` with **start command**:

```bash
python weather_bot.py
```

---

## 👤 Author

Created with ❤️ by **Viktor Yevtushenko** (aka @viktormatrix)

📫 Contact: [t.me/viktormatrixweatherhelperbot](https://t.me/viktormatrixweatherhelperbot)

---

## 🌟 License

MIT — free to use, modify, and distribute.
