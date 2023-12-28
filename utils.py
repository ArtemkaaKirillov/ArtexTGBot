from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_keyboard(keyboard_data):  # Преобразование json в кнопки
    row_width = 2 if keyboard_data[0]['callback_data'][-1] == '2' else 1
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    keyboard.add(
        *[InlineKeyboardButton(text=data['text'], callback_data=data['callback_data']) for data in keyboard_data])
    return keyboard
