import asyncio
import sqlite3
from aiogram import Bot, Dispatcher
from bot_token import BOT_TOKEN
from bot_token import ADMIN_CHAT_ID

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

conn = sqlite3.connect('user_choices.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS user_choices
                  (chat_id INTEGER, choices TEXT, user_name TEXT)''')
conn.commit()


async def save_choices(chat_id, choices):  # Сохранение выборов пользователя
    try:
        cursor.execute('SELECT choices FROM user_choices WHERE chat_id = ?',
                       (chat_id,))  # Пытаемся получить выборы(все) от конкретного пользователя
        result = cursor.fetchone()
        if result:
            current_choices = list(result)
            merge_choices = current_choices[0] + choices + '\n'
            cursor.execute('''UPDATE user_choices SET choices = ? WHERE chat_id = ?''', (merge_choices, chat_id))
        else:
            cursor.execute('''INSERT INTO user_choices VALUES (?, ?, ?)''', (chat_id, 'расчет\n', ''))
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"Ошибка при выполнении запроса к базе данных: {e}")
        # Обработка ошибки, если это необходимо


async def get_user_choices(chat_id):  # Получить все выборы пользователей
    try:
        cursor.execute('SELECT choices FROM user_choices WHERE chat_id = ?', (chat_id,))
        result = cursor.fetchone()
        if result:
            choices = result[0].split('\n') if result[0] else []  # Разделяем строку выборов на список
            return choices
        else:
            return []
    except sqlite3.OperationalError as e:
        print(f"Ошибка при выполнении запроса к базе данных: {e}")
        return []


async def send_notification(user_name, chat_id):  # Отправка уведомлений
    await asyncio.sleep(10)  # Подождать 10 секунд
    choices = await get_user_choices(chat_id)
    # Отправить уведомление администратору с выборами пользователя
    [await bot.send_message(admin, f"Пользователь {user_name} сделал выборы: {choices}") for admin in ADMIN_CHAT_ID]
