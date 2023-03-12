from copy import deepcopy

from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import CallbackQuery, Message
from database.database import user_dict_template, users_db
from keyboards.direction_kb import create_direction_keyboard
from keyboards.answers_kb import create_question_answers_keyboard
from keyboards.further_kb import create_further_kb
from lexicon.lexicon import LEXICON

# from services.tikets_handling import voprosy_otvety

router: Router = Router()
# для перемещения между хэндлерами объявим random_ticket глобальной
global random_ticket


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)
    # Наполняем базу данных для нового user.id нулевыми значениями
    users_db[message.from_user.id]['correct_answers'] = 0
    users_db[message.from_user.id]['questions'] = 0
    users_db[message.from_user.id]['SCORE'] = 0.0


# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


# Этот хэндлер будет срабатывать на команду "/begin"
# и отправлять пользователю случайный вопрос и клавиатуру с 3 вариантами ответа
@router.message(Command(commands='begin'))
async def process_begin_command(message: Message):
    # Случайным образом выбираем random_ticket
    global random_ticket
    random_ticket = create_question_answers_keyboard()
    # создаем клавиатуру из вариантов ответов на вопрос из random_ticket
    reply_markup = random_ticket[1]
    # вопрос из random_ticket
    question = random_ticket[0]
    await message.answer(f"{question}", reply_markup=reply_markup)


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery с data 'текст кнопки' с вариантом ответа и сверять с
# правильным ответом, изменяя users_db и выводя из нее статистику пользователю
@router.callback_query(Text(text=['1', '2', '3']))
async def check_answer(callback: CallbackQuery):
    reply_markup = create_further_kb()
    answer = callback.data
    if answer == random_ticket[2]:
        result = 'Верно'
        users_db[callback.from_user.id]['correct_answers'] += 1
    else:
        result = 'Неверно'

    users_db[callback.from_user.id]['questions'] += 1
    users_db[callback.from_user.id]['SCORE'] = users_db[callback.from_user.id]['correct_answers'] / \
                                               users_db[callback.from_user.id]['questions']
    await callback.message.edit_text(
        text=f'{result}\n Ваш ответ: {answer} '
             f'\nВопрос: {random_ticket[0]}'
             f'\nВерный ответ: {random_ticket[2]}'
             f'\nСтатистика тренировки: {users_db[callback.from_user.id]["correct_answers"]} верных ответов '
             f'из {users_db[callback.from_user.id]["questions"]} вопросов = {users_db[callback.from_user.id]["SCORE"]}',
        reply_markup=reply_markup)


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery с 'next_word'
@router.callback_query(Text(text='next_word'))
async def next_ticket_press(callback: CallbackQuery):
    # Случайным образом выбираем random_ticket
    global random_ticket
    random_ticket = create_question_answers_keyboard()
    # создаем клавиатуру из вариантов ответов на вопрос из random_ticket
    reply_markup = random_ticket[1]
    # вопрос из random_ticket
    question = random_ticket[0]
    await callback.message.edit_text(f"{question}", reply_markup=reply_markup)


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery с data 'stop'
# и выводит статистику тренировки пользователю
@router.callback_query(Text(text='stop'))
async def stop_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f'Тренировка завершена.'
             f'\nСтатистика тренировки: {users_db[callback.from_user.id]["correct_answers"]} верных ответов '
             f'из {users_db[callback.from_user.id]["questions"]} вопросов = {users_db[callback.from_user.id]["SCORE"]}')


# хэндлер на команду в меню '/score': 'Показать статистику' и отправлять пользователю статистику тренировки
@router.message(Command(commands='score'))
async def process_score_command(message: Message):
    await message.answer(text=f'\nСтатистика тренировки: {users_db[message.from_user.id]["correct_answers"]} '
                              f'верных ответов из {users_db[message.from_user.id]["questions"]} вопросов = '
                              f'{users_db[message.from_user.id]["SCORE"]}')
