from aiogram import executor
from handlers import handle_start, handle_show_choices, handle_clear_choices, handle_help, handle_callback
from handlers import START_COMMAND, HISTORY_COMMAND, CLEAR_COMMAND, HELP_COMMAND
from database import dp

dp.register_message_handler(handle_start, commands=[START_COMMAND])  # Команда начала общения с ботом
dp.register_message_handler(handle_show_choices, commands=[HISTORY_COMMAND])  # Команда показа выборов пользователя
dp.register_message_handler(handle_clear_choices, commands=[CLEAR_COMMAND])  # Команда отчистки выборов пользователя
dp.register_message_handler(handle_help, commands=[HELP_COMMAND])  # Команда списка доступных команд
dp.register_callback_query_handler(handle_callback)  # Главная функция программы

if __name__ == '__main__':
    from asyncio import run

    run(executor.start_polling(dp, skip_updates=True))




