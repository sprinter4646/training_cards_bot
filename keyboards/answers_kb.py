# Модуль для формирования кнопок с ответами. В случайном порядке выбираем random_ticket из voprosy_otvety, из которого
# выбираем question_n,и CallbackButtons с 3 вариантами ответов и номер правильного ответа
# Функция def create_question_answers_keyboard() возвращает question, kb_builder.as_markup(), answer_question
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from services.tikets_handling import voprosy_otvety
import random


def create_question_answers_keyboard():
    # формируем список билетов
    tickets = voprosy_otvety
    # Выбираем случайный ticket
    random_ticket = random.choice(tickets)
    # print(random_ticket)
    # Выбираем из ticket question
    question = f'{random_ticket[0]}\n{random_ticket[1]}\n{random_ticket[2]}\n{random_ticket[3]}'
    # Выбираем из ticket answers_question
    answers_question = [i[0] for i in random_ticket[1:4]]
    # print('answers_question', answers_question)
    # Выбираем из ticket answer_question
    answer_question = random_ticket[4]
    # Создаем объект клавиатуры
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-ответами
    for button in answers_question:
        kb_builder.row(InlineKeyboardButton(text=f'{button}', callback_data=button))  # , callback_data=str(button)
        # kb_builder.row(InlineKeyboardButton(text=f'{button}', callback_data=f'{button}'))
    # возвращаем: вопрос, клавиатуру с вариантами ответов, правильный ответ
    return question, kb_builder.as_markup(), answer_question


# print(create_question_answers_keyboard())
