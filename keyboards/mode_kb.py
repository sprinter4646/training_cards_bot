# модуль с функцией, которая отвечает за создание кнопок 'Случайный выбор' и 'Вопросы по порядку'
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


def create_mode_kb() -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Создаем кнопки
    kb_builder.row(InlineKeyboardButton(text=f'{LEXICON["random_mode"]}', callback_data="random_mode"))
    kb_builder.row(InlineKeyboardButton(text=f'{LEXICON["sequential_mode"]}', callback_data="sequential_mode"))
    return kb_builder.as_markup()
