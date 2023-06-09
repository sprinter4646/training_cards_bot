# модуль с текстами для реакции на различные события в работе бота
from services.tickets_handling import voprosy_otvety

LEXICON: dict[str, str] = {
    'next_word': 'Еще билет',
    'begin': 'Вопрос и 3 кнопки выбора варианта ответа:',
    '/start':  '<b>Привет!</b>\nЭто бот, в котором Вы можете потренировать свои знания '
               '\n\nЧтобы приступить к тренировке выберите режим тренировки вопросов',
    '/help': '<b>Это бот, в котором Вы можете потренировать свои знания</b>'
             '\n\nДоступные команды:\n\n/start - Начать тренировку, обновить статистику тренировки'
             '\n\n /score - Показать статистику\n\n/help - справка по работе бота\n\n'
             '<b>Приятной тренировки!</b>',
    'sequential_mode': 'Вопросы по порядку',
    'random_mode': 'Случайный выбор',
    'cancel': 'Завершить',
    'sequential_mode_press': f'Введите номер вопроса в диапазоне: 1 - {len(voprosy_otvety)}"',
    '/ticket_n': 'Напишите номер вопроса'
}
# еще в этом модуле хранится словарь соответствий команд и их описаний для кнопки Menu бота
LEXICON_COMMANDS: dict[str, str] = {
    '/start': 'Начать тренировку заново, обновить статистику тренировки',
    '/ticket_n': 'Ввести номер вопроса',
    '/score': 'Показать статистику',
    '/help': 'Справка по работе бота'
}
