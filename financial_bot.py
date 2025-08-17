import logging
import random
import sqlite3
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import requests

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
EXCHANGE_RATE_API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')

# Настройка бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Подключение к базе данных
conn = sqlite3.connect('user.db')
cursor = conn.cursor()

# Создание таблицы пользователей
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
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
''')
conn.commit()

# Клавиатура
button_registr = KeyboardButton(text="Регистрация в телеграм боте")
button_exchange_rates = KeyboardButton(text="Курс валют")
button_tips = KeyboardButton(text="Советы по экономии")
button_finances = KeyboardButton(text="Личные финансы")

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [button_registr, button_exchange_rates],
        [button_tips, button_finances]
    ],
    resize_keyboard=True
)


# Состояния для учёта финансов
class FinancesForm(StatesGroup):
    category1 = State()
    expenses1 = State()
    category2 = State()
    expenses2 = State()
    category3 = State()
    expenses3 = State()


# Обработчик команды /start
@dp.message(Command('start'))
async def send_start(message: Message):
    await message.answer(
        "Привет! Я ваш личный финансовый помощник. Выберите одну из опций в меню:",
        reply_markup=keyboard
    )


# Обработчик регистрации
@dp.message(F.text == "Регистрация в телеграм боте")
async def registration(message: Message):
    telegram_id = message.from_user.id
    name = message.from_user.full_name
    cursor.execute('''SELECT * FROM users WHERE telegram_id = ?''', (telegram_id,))
    user = cursor.fetchone()
    if user:
        await message.answer("Вы уже зарегистрированы!")
    else:
        cursor.execute('''INSERT INTO users (telegram_id, name) VALUES (?, ?)''', (telegram_id, name))
        conn.commit()
        await message.answer("Вы успешно зарегистрированы!")


# Обработчик курса валют
@dp.message(F.text == "Курс валют")
async def exchange_rates(message: Message):
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/USD"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            await message.answer("Не удалось получить данные о курсе валют!")
            return

        usd_to_rub = data['conversion_rates']['RUB']
        eur_to_usd = data['conversion_rates']['EUR']
        euro_to_rub = eur_to_usd * usd_to_rub

        await message.answer(
            f"1 USD - {usd_to_rub:.2f} RUB\n"
            f"1 EUR - {euro_to_rub:.2f} RUB"
        )
    except Exception as e:
        logging.error(f"Ошибка при получении курса валют: {e}")
        await message.answer("Произошла ошибка при получении курса валют")


# Остальные обработчики остаются без изменений...
# [Здесь должен быть тот же код, что и в предыдущем примере, для советов и личных финансов]
# Обработчик советов по экономии
@dp.message(F.text == "Советы по экономии")
async def send_tips(message: Message):
    tips = [
        "Совет 1: Ведите бюджет и следите за своими расходами.",
        "Совет 2: Откладывайте часть доходов на сбережения.",
        "Совет 3: Покупайте товары по скидкам и распродажам.",
        "Совет 4: Используйте кэшбэк и бонусные программы.",
        "Совет 5: Планируйте крупные покупки заранее."
    ]
    tip = random.choice(tips)
    await message.answer(tip)


# Обработчик личных финансов
@dp.message(F.text == "Личные финансы")
async def finances(message: Message, state: FSMContext):
    await state.set_state(FinancesForm.category1)
    await message.reply("Введите первую категорию расходов:")


@dp.message(FinancesForm.category1)
async def process_category1(message: Message, state: FSMContext):
    await state.update_data(category1=message.text)
    await state.set_state(FinancesForm.expenses1)
    await message.reply("Введите расходы для категории 1:")


@dp.message(FinancesForm.expenses1)
async def process_expenses1(message: Message, state: FSMContext):
    try:
        await state.update_data(expenses1=float(message.text))
        await state.set_state(FinancesForm.category2)
        await message.reply("Введите вторую категорию расходов:")
    except ValueError:
        await message.reply("Пожалуйста, введите число для расходов:")


@dp.message(FinancesForm.category2)
async def process_category2(message: Message, state: FSMContext):
    await state.update_data(category2=message.text)
    await state.set_state(FinancesForm.expenses2)
    await message.reply("Введите расходы для категории 2:")


@dp.message(FinancesForm.expenses2)
async def process_expenses2(message: Message, state: FSMContext):
    try:
        await state.update_data(expenses2=float(message.text))
        await state.set_state(FinancesForm.category3)
        await message.reply("Введите третью категорию расходов:")
    except ValueError:
        await message.reply("Пожалуйста, введите число для расходов:")


@dp.message(FinancesForm.category3)
async def process_category3(message: Message, state: FSMContext):
    await state.update_data(category3=message.text)
    await state.set_state(FinancesForm.expenses3)
    await message.reply("Введите расходы для категории 3:")


@dp.message(FinancesForm.expenses3)
async def process_expenses3(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        telegram_id = message.from_user.id

        cursor.execute('''
            UPDATE users 
            SET category1 = ?, expenses1 = ?, 
                category2 = ?, expenses2 = ?, 
                category3 = ?, expenses3 = ? 
            WHERE telegram_id = ?
        ''', (
            data['category1'], data['expenses1'],
            data['category2'], data['expenses2'],
            data['category3'], float(message.text),
            telegram_id
        ))
        conn.commit()
        await state.clear()
        await message.answer("Категории и расходы сохранены!")
    except ValueError:
        await message.reply("Пожалуйста, введите число для расходов:")

# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import asyncio

    asyncio.run(main())