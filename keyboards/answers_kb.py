# Модуль для формирования кнопок с ответами. В случайном порядке выбираем random_ticket из voprosy_otvety, из которого
# выбираем question_n,и CallbackButtons с 3 вариантами ответов, номер правильного ответа, общее число билетов
# Функция def create_question_answers_keyboard() возвращает question, kb_builder.as_markup(), answer_question, tickets_q
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.tickets_handling import voprosy_otvety
import random


def create_question_answers_keyboard(mode, ticket_n='1'):
    # формируем список билетов
    tickets = voprosy_otvety
    # Выбираем ticket, если mode == random_mode, выбираем случайный билет, иначе используем билет номер ticket_n
    if mode == 'random_mode':
        ticket = random.choice(tickets)
    else:
        ticket = tickets[int(ticket_n)-1]
    # Выбираем из ticket question
    question = f'{ticket[0]}\n{ticket[1]}\n{ticket[2]}\n{ticket[3]}'
    # Выбираем из ticket answers_question
    answers_question = [i[0] for i in ticket[1:4]]
    # Выбираем из ticket answer_question
    answer_question = ticket[4]
    # Создаем объект клавиатуры
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-ответами
    for button in answers_question:
        kb_builder.row(InlineKeyboardButton(text=f'{button}', callback_data=button))  # , callback_data=str(button)
    # общее число билетов
    tickets_q = len(voprosy_otvety)
    # возвращаем: вопрос, клавиатуру с вариантами ответов, правильный ответ, общее число билетов
    return question, kb_builder.as_markup(), answer_question, tickets_q

# print(create_question_answers_keyboard())
