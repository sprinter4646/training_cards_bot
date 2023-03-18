# модуль с пользовательскими хэндлерами.
from copy import deepcopy

from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import CallbackQuery, Message
from database.database import user_dict_template, users_db
from keyboards.mode_kb import create_mode_kb
from keyboards.answers_kb import create_question_answers_keyboard
from keyboards.further_kb import create_further_kb
from lexicon.lexicon import LEXICON

router: Router = Router()
# для перемещения актуального значения ряда переменных между функциями объявим их глобальными
global ticket  # Билет с вариантами ответа и клавиатура для выбора номера ответа
global mode  # Режим тренировки Последовательный|Рандомный
global ticket_n  # Номер билета для Последовательного режима


# хэндлер на команду "/start" - добавляет пользователя в базу данных, если его там еще не было
# и отправляет ему приветственное сообщение, предлагает выбрать режим тренировки, обнуляем статистику пользователя
@router.message(CommandStart())
async def process_start_command(message: Message):
    # создаем клавиатуру выбора режима тренировки из mode_kb
    reply_markup = create_mode_kb()
    await message.answer(LEXICON[message.text], reply_markup=reply_markup)
    # Наполняем базу данных новым user.id
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)
    # Наполняем базу данных для нового user.id нулевыми значениями
    users_db[message.from_user.id]['correct_answers'] = 0
    users_db[message.from_user.id]['questions'] = 0
    users_db[message.from_user.id]['SCORE'] = 0.0


# Этот хэндлер на команду "/help" и отправляет пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


# хэндлер на команду в main_menu "/ticket_n" - Ввести номер вопроса
@router.message(Command(commands='ticket_n'))
async def process_ticket_n_command(message: Message):
    await message.answer(LEXICON[message.text])


# хэндлер на ввод/изменение номера вопроса ticket_n, после отправки корректного номера вопроса выводит этот вопрос,
# варианты ответа и Callback кнопки для выбора варианта
@router.message(Text(text=[str(i) for i in range(1, create_question_answers_keyboard(mode='random_mode')[3])]))
async def input_ticket_n(message: Message):
    global ticket
    global mode
    global ticket_n
    mode = 'sequential_mode'
    ticket_n = message.text
    ticket = create_question_answers_keyboard(mode, ticket_n=ticket_n)
    # создаем клавиатуру из вариантов ответов на вопрос из ticket
    reply_markup = ticket[1]
    # вопрос из random_ticket
    question = ticket[0]
    await message.answer(f"{question}", reply_markup=reply_markup)


# хэндлер на апдейт типа CallbackQuery с 'sequential_mode' или 'random_mode' и отправляет пользователю
# вопрос и клавиатуру с 3 вариантами ответа
@router.callback_query(Text(text=['sequential_mode', 'random_mode']))
async def choose_ticket_process(callback: CallbackQuery):
    # Случайным образом выбираем random_ticket
    global ticket
    global mode
    global ticket_n
    mode = callback.data
    ticket = create_question_answers_keyboard(mode)
    ticket_n = 1
    # создаем клавиатуру из вариантов ответов на вопрос из ticket
    reply_markup = ticket[1]
    # вопрос из random_ticket
    question = ticket[0]
    await callback.message.edit_text(f"{question}", reply_markup=reply_markup)


# хэндлер на апдейт типа CallbackQuery с data 'текст кнопки' с вариантом ответа и сверяет с
# правильным ответом, изменяя users_db и выводя из нее статистику пользователю
@router.callback_query(Text(text=['1', '2', '3']))
async def check_answer(callback: CallbackQuery):
    reply_markup = create_further_kb()
    answer = callback.data
    if answer == ticket[2]:
        result = 'Верно'
        users_db[callback.from_user.id]['correct_answers'] += 1
    else:
        result = 'Неверно'

    users_db[callback.from_user.id]['questions'] += 1
    users_db[callback.from_user.id]['SCORE'] = users_db[callback.from_user.id]['correct_answers'] / \
                                               users_db[callback.from_user.id]['questions']
    await callback.message.edit_text(
        text=f'{result}\n Ваш ответ: {answer} '
             f'\nВопрос: {ticket[0]}'
             f'\nВерный ответ: {ticket[2]}'
             f'\nСтатистика тренировки: {users_db[callback.from_user.id]["correct_answers"]} верных ответов '
             f'из {users_db[callback.from_user.id]["questions"]} вопросов = {users_db[callback.from_user.id]["SCORE"]}',
        reply_markup=reply_markup)


# Этот хэндлер на апдейт типа CallbackQuery с 'next_word' в зависимости от mode
@router.callback_query(Text(text=['next_word']))
async def next_ticket_press(callback: CallbackQuery):
    # выбираем ticket
    global ticket_n
    global ticket
    # ticket_n = 1
    if mode == 'sequential_mode':
        ticket_n = int(ticket_n) + 1
        ticket = create_question_answers_keyboard(mode, ticket_n=ticket_n)
    elif mode == 'random_mode':
        ticket = create_question_answers_keyboard(mode)
    # создаем клавиатуру из вариантов ответов на вопрос из random_ticket
    reply_markup = ticket[1]
    # вопрос из random_ticket
    question = ticket[0]
    await callback.message.edit_text(f"{question}", reply_markup=reply_markup)


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery с data 'stop'
# и выводит статистику тренировки пользователю
@router.callback_query(Text(text='stop'))
async def stop_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f'Тренировка завершена.'
             f'\nСтатистика тренировки: {users_db[callback.from_user.id]["correct_answers"]} верных ответов '
             f'из {users_db[callback.from_user.id]["questions"]} вопросов = {users_db[callback.from_user.id]["SCORE"]}')


# хэндлер на команду в меню '/score': 'Показать статистику' и отправляет пользователю статистику тренировки
@router.message(Command(commands='score'))
async def process_score_command(message: Message):
    await message.answer(text=f'\nСтатистика тренировки: {users_db[message.from_user.id]["correct_answers"]} '
                              f'верных ответов из {users_db[message.from_user.id]["questions"]} вопросов = '
                              f'{users_db[message.from_user.id]["SCORE"]}')
