# 💰 Financial Telegram Bot

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Aiogram](https://img.shields.io/badge/aiogram-3.x-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

Финансовый бот-помощник для управления личными расходами и отслеживания курсов валют

## ✨ Возможности

| Функция | Описание |
|---------|----------|
| 📊 Учет расходов | Ведение бюджета по 3 категориям |
| 💱 Курсы валют | Актуальные курсы USD/RUB и EUR/RUB |
| 💡 Советы | Персонализированные советы по экономии |
| 👤 Профиль | Система регистрации пользователей |

## 🚀 Быстрый старт

### Предварительные требования
- Python 3.9+
- Аккаунт Telegram
- API ключ от [exchangerate-api.com](https://www.exchangerate-api.com/)

### Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/financial-telegram-bot.git
cd financial-telegram-bot
Установите зависимости:

bash
pip install -r requirements.txt
Настройте окружение:

bash
cp .env.example .env
nano .env  # заполните вашими данными
🛠 Конфигурация
Файл .env должен содержать:

ini
BOT_TOKEN=your_telegram_bot_token
EXCHANGE_RATE_API_KEY=your_exchangerate_api_key
🖥 Запуск
bash
python financial_bot.py
📚 Команды бота
/start - Начать работу с ботом

Регистрация - Зарегистрироваться в системе

Курс валют - Показать текущие курсы

Советы - Получить случайный совет

Финансы - Начать ввод расходов

🗃 Структура базы данных
sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    telegram_id INTEGER UNIQUE,
    name TEXT,
    category1 TEXT,
    category2 TEXT,
    category3 TEXT,
    expenses1 REAL,
    expenses2 REAL,
    expenses3 REAL
)
🌟 Примеры использования
<img width="537" height="1021" alt="Выделение_896" src="https://github.com/user-attachments/assets/112d003c-afac-484b-9085-614f007386d6" />

🤝 Как внести вклад
Форкните репозиторий

Создайте ветку (git checkout -b feature/AmazingFeature)

Сделайте коммит (git commit -m 'Add some AmazingFeature')

Запушьте изменения (git push origin feature/AmazingFeature)

Откройте Pull Request

📜 Лицензия
Распространяется под лицензией MIT. См. LICENSE для подробностей.
