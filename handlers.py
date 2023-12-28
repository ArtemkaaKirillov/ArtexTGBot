import asyncio
from aiogram import types
from utils import get_keyboard
from database import save_choices, send_notification
from database import conn, cursor
from database import bot

# Константы
START_COMMAND = 'start'
HISTORY_COMMAND = 'history'
CLEAR_COMMAND = 'clear'
HELP_COMMAND = 'help'

handlers = {
    'start': {
        'message': "Здравствуйте {name} 🖐 \n"
                   "Я чат-бот компании ARTEX\n"
                   "Помогу вам расчёитать стоимость создания сайта 📝\n"
                   "Для этого выберите кнопку ⬇️",
        'keyboard': [
            {'text': 'Рассчитать проект 🧾', 'callback_data': '-----'}
        ]
    },
    '-----': {
        'message': "Выберите нужный тип сайта 📝",
        'keyboard': [
            {'text': 'Многостраничник 🗒', 'callback_data': 'сайт_многостраничник2'},
            {'text': 'Интернет магазин 🛒', 'callback_data': 'интернет_магазин'},
            {'text': 'Лендинг 📃', 'callback_data': 'лендинг2'},
            {'text': 'Сайт-визитка 📄', 'callback_data': 'сайт-визитка'},
            {'text': 'Пока не опредилися(-ась) 🤔', 'callback_data': 'пока_не_опредилися(-ась)'}
        ]
    },
    'сайт_многостраничник2': {
        'message': "Выберите вид вашей деятельности : ⬇️",
        'keyboard': [
            {'text': 'Юридические услуги ⚖️', 'callback_data': 'юридические_услуги'},
            {'text': 'Строительные услуги 🧱', 'callback_data': 'строительные_услуги'},
            {'text': 'Спецтехника ⚙️', 'callback_data': 'спецтехника'},
            {'text': 'Туризм и отдых ✈️', 'callback_data': 'туризм_и_отдых'},
            {'text': 'Изготовление мебели 🛠', 'callback_data': 'изготовление_мебели'},
            {'text': 'Другое... 📦', 'callback_data': 'другое'}
        ]
    },
    'пока_не_опредилися(-ась)': {
        'message': "Выберите вид вашей деятельности : ⬇️",
        'keyboard': [
            {'text': 'Юридические услуги ⚖️', 'callback_data': 'юридические_услуги'},
            {'text': 'Строительные услуги 🧱', 'callback_data': 'строительные_услуги'},
            {'text': 'Спецтехника ⚙️', 'callback_data': 'спецтехника'},
            {'text': 'Туризм и отдых ✈️', 'callback_data': 'туризм_и_отдых'},
            {'text': 'Изготовление мебели 🛠', 'callback_data': 'изготовление_мебели'},
            {'text': 'Другое... 📦', 'callback_data': 'другое'}
        ]
    },

    'юридические_услуги': {
        'message': "У вас есть наполнение для для вашего сайта ? 📃",
        'keyboard': [
            {'text': 'Да ✅', 'callback_data': 'да2'},
            {'text': 'Нет ❌', 'callback_data': 'нет'}
        ]
    },
    'строительные_услуги': {
        'message': "У вас есть наполнение для для вашего сайта ? 📃",
        'keyboard': [
            {'text': 'Да ✅', 'callback_data': 'да2'},
            {'text': 'Нет ❌', 'callback_data': 'нет'}

        ]
    },
    'спецтехника': {
        'message': "У вас есть наполнение для для вашего сайта ? 📃",
        'keyboard': [
            {'text': 'Да ✅', 'callback_data': 'да2'},
            {'text': 'Нет ❌', 'callback_data': 'нет'}
        ]
    },
    'туризм_и_отдых': {
        'message': "У вас есть наполнение для для вашего сайта ? 📃",
        'keyboard': [
            {'text': 'Да ✅', 'callback_data': 'да2'},
            {'text': 'Нет ❌', 'callback_data': 'нет'}
        ]
    },
    'изготовление_мебели': {
        'message': "У вас есть наполнение для для вашего сайта ? 📃",
        'keyboard': [
            {'text': 'Да ✅', 'callback_data': 'да2'},
            {'text': 'Нет ❌', 'callback_data': 'нет'}
        ]
    },
    'другое': {
        'message': "У вас есть наполнение для для вашего сайта ? 📃",
        'keyboard': [
            {'text': 'Да ✅', 'callback_data': 'да2'},
            {'text': 'Нет ❌', 'callback_data': 'нет'}
        ]
    },
    "да2": {
        "message": "Размещение информации на вашем сайте: ℹ️",
        "keyboard": [
            {"text": "Требуется услуга по размещению 👥", "callback_data": "требуется_услуга_по_размещению"},
            {"text": "Самостоятельно 👤", "callback_data": "самостоятельно"}
        ]
    },
    "нет": {
        "message": "Размещение информации на вашем сайте: ℹ️",
        "keyboard": [
            {"text": "Требуется услуга по размещению 👥", "callback_data": "требуется_услуга_по_размещению"},
            {"text": "Самостоятельно 👤", "callback_data": "самостоятельно"}
        ]
    },
    "требуется_услуга_по_размещению": {
        "message": "Хорошо, мы учли все ваши пожелания 👍\nВ скором времени с вами свяжутся, ожидайте ! 💬",
        "keyboard": [
            {"text": "Буду ждать ! ⏳", "callback_data": "ожидает"}
        ]
    },
    "самостоятельно": {
        "message": "Хорошо, мы учли все ваши пожелания 👍\nВ скором времени с вами свяжутся, ожидайте ! 💬",
        "keyboard": [
            {"text": "Буду ждать ! ⏳", "callback_data": "ожидает"}
        ]

    },
    'лендинг2': {
        'message': "Выберите вид вашей деятельности : ⬇️",
        'keyboard': [
            {'text': 'Юридические услуги ⚖️', 'callback_data': 'юридические_услуги'},
            {'text': 'Строительные услуги 🧱', 'callback_data': 'строительные_услуги'},
            {'text': 'Спецтехника ⚙️', 'callback_data': 'спецтехника'},
            {'text': 'Туризм и отдых ✈️', 'callback_data': 'туризм_и_отдых'},
            {'text': 'Изготовление мебели 🛠', 'callback_data': 'изготовление_мебели'},
            {'text': 'Другое... 📦', 'callback_data': 'другое'}
        ]
    },

    "интернет_магазин": {
        "message": "Вы продаете : 🏷",
        "keyboard": [
            {"text": "Готовую еду 🍴", "callback_data": "готовую_еду2"},
            {"text": "Электротехнику 💡", "callback_data": "электротехнику"},
            {"text": "Одежду и обувь 👕", "callback_data": "одежду_и_обувь"},
            {"text": "Мебель 🛏", "callback_data": "мебель"},
            {"text": "Другое... 📦", "callback_data": "другое_3"}
        ]
    },

    "сайт-визитка": {
        "message": "Вы продаете : 🏷",
        "keyboard": [
            {"text": "Готовую еду 🍴", "callback_data": "готовую_еду2"},
            {"text": "Электротехнику 💡", "callback_data": "электротехнику"},
            {"text": "Одежду и обувь 👕", "callback_data": "одежду_и_обувь"},
            {"text": "Мебель 🛏", "callback_data": "мебель"},
            {"text": "Другое... 📦", "callback_data": "другое_3"}
        ]
    },

    "готовую_еду2": {
        "message": "Количество ваших товаров : 📄",
        "keyboard": [
            {"text": "менее 100", "callback_data": "менее100_2"},
            {"text": "до 5000", "callback_data": "до5000"},
            {"text": "до 45000", "callback_data": "до45000"},
            {"text": "Другое... ", "callback_data": "другое_4"}
        ]
    },

    "электротехнику": {
        "message": "Количество ваших товаров : 📄",
        "keyboard": [
            {"text": "менее 100", "callback_data": "менее100_2"},
            {"text": "до 5000", "callback_data": "до5000"},
            {"text": "до 45000", "callback_data": "до45000"},
            {"text": "Другое... ", "callback_data": "другое_4"}
        ]
    },

    "одежду_и_обувь": {
        "message": "Количество ваших товаров : 📄",
        "keyboard": [
            {"text": "менее 100", "callback_data": "менее100_2"},
            {"text": "до 5000", "callback_data": "до5000"},
            {"text": "до 45000", "callback_data": "до45000"},
            {"text": "Другое... ", "callback_data": "другое_4"}
        ]
    },

    "мебель": {
        "message": "Количество ваших товаров : 📄",
        "keyboard": [
            {"text": "менее 100", "callback_data": "менее100_2"},
            {"text": "до 5000", "callback_data": "до5000"},
            {"text": "до 45000", "callback_data": "до45000"},
            {"text": "Другое... ", "callback_data": "другое_4"}
        ]
    },

    "другое_3": {
        "message": "Количество ваших товаров : 📄",
        "keyboard": [
            {"text": "менее 100", "callback_data": "менее100_2"},
            {"text": "до 5000", "callback_data": "до5000"},
            {"text": "до 45000", "callback_data": "до45000"},
            {"text": "Другое... ", "callback_data": "другое_4"}
        ]
    },

    "менее100_2": {
        "message": "Для вас настроено и нужно подключить:",
        "keyboard": [
            {"text": "Интеграция в маркетплейсы 🛒", "callback_data": "Интеграция_в_маркетплейсы"},
            {"text": "1С и «Мой склад» 📦", "callback_data": "1С_и_«Мой склад»"},
            {"text": "Настроен приём любых видов платежей через сайт 💳",
             "callback_data": "Прием_платежей_сайт"}
        ]
    },

    "до5000": {
        "message": "Для вас настроено и нужно подключить:",
        "keyboard": [
            {"text": "Интеграция в маркетплейсы 🛒", "callback_data": "Интеграция_в_маркетплейсы"},
            {"text": "1С и «Мой склад» 📦", "callback_data": "1С_и_«Мой склад»"},
            {"text": "Настроен приём любых видов платежей через сайт 💳",
             "callback_data": "Прием_платежей_сайт"}
        ]
    },

    "до45000": {
        "message": "Для вас настроено и нужно подключить:",
        "keyboard": [
            {"text": "Интеграция в маркетплейсы 🛒", "callback_data": "Интеграция_в_маркетплейсы"},
            {"text": "1С и «Мой склад» 📦", "callback_data": "1С_и_«Мой склад»"},
            {"text": "Настроен приём любых видов платежей через сайт 💳",
             "callback_data": "Прием_платежей_сайт"}
        ]
    },

    "Интеграция_в_маркетплейсы": {
        "message": "Хорошо, мы учли все ваши пожелания 👍\nВ скором времени с вами свяжутся, ожидайте ! 💬",
        "keyboard": [
            {"text": "Буду ждать ! ⏳", "callback_data": "ожидает"}
        ]

    },

    "1С_и_«Мой склад»": {
        "message": "Хорошо, мы учли все ваши пожелания 👍\nВ скором времени с вами свяжутся, ожидайте ! 💬",
        "keyboard": [
            {"text": "Буду ждать ! ⏳", "callback_data": "ожидает"}
        ]

    },

    "Прием_платежей_сайт": {
        "message": "Хорошо, мы учли все ваши пожелания 👍\nВ скором времени с вами свяжутся, ожидайте ! 💬",
        "keyboard": [
            {"text": "Буду ждать ! ⏳", "callback_data": "ожидает"}
        ]

    },

    "другое_4": {
        "message": "Для вас настроено и нужно подключить:",
        "keyboard": [
            {"text": "Интеграция в маркетплейсы 🛒", "callback_data": "Интеграция_в_маркетплейсы"},
            {"text": "1С и «Мой склад» 📦", "callback_data": "1С_и_«Мой склад»"},
            {"text": "Настроен приём любых видов платежей через сайт 💳",
             "callback_data": "Прием_платежей_сайт"}
        ]
    },
}


async def handle_callback(callback_query: types.CallbackQuery):  # Главная функция
    chat_id = callback_query.message.chat.id
    button_data = callback_query.data

    await save_choices(chat_id, button_data)

    handler = handlers.get(button_data)
    if handler:
        await bot.send_message(chat_id, handler['message'], reply_markup=await get_keyboard(handler['keyboard']))
    else:
        # Запись выбора в БД и отправка уведомлений
        user = await bot.get_chat(chat_id)
        user = user.username
        cursor.execute('''UPDATE user_choices SET user_name = ? WHERE chat_id = ?''', (user, chat_id))
        conn.commit()
        asyncio.create_task(send_notification(user, chat_id))  # Вызов функции отправки уведомления

    await bot.delete_message(chat_id, callback_query.message.message_id)


async def handle_start(message: types.Message):  # Команда начала общения с ботом
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    handler = handlers['start']
    await bot.send_message(chat_id, handler['message'].format(name=user_name),
                           reply_markup=await get_keyboard(handler['keyboard']))


async def handle_show_choices(message: types.Message):  # Команда показа выборов пользователя
    chat_id = message.chat.id

    # Получить choices из базы данных
    cursor.execute('''SELECT choices FROM user_choices WHERE chat_id = ?''',
                   (chat_id,))  # Получаем полный choice От конкретного пользователя
    result = cursor.fetchone()

    if result:
        choices = result[0]
        await bot.send_message(chat_id, f"Ваши выборы: {choices}")
    else:
        await bot.send_message(chat_id, "Вы еще не сделали никаких выборов.")


async def handle_clear_choices(message: types.Message):  # Команда отчистки выборов пользователя
    chat_id = message.chat.id

    # Удалить запись из базы данных для данного chat_id
    cursor.execute('''DELETE FROM user_choices WHERE chat_id = ?''', (chat_id,))
    conn.commit()

    await bot.send_message(chat_id, "Ваши выборы были успешно очищены.")


async def handle_help(message: types.Message):  # Команда списка доступных команд
    chat_id = message.chat.id

    # Список доступных команд
    commands_list = [
        f"/{START_COMMAND} - Начать общение с ботом",
        f"/{HISTORY_COMMAND} - Показать ваши выборы",
        f"/{CLEAR_COMMAND} - Очистить ваши выборы",
        f"/{HELP_COMMAND} - Показать список доступных команд"
        # Добавьте другие команды, если необходимо
    ]

    # Отправить список команд пользователю
    response = "\n".join(commands_list)
    await bot.send_message(chat_id, response)
