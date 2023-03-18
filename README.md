# TrainingCardsBot
## Идея программы 
Программа, взаимодействующая с API Telegram, которая предназначена для подготовки пользователя к сдаче билетов по 
определенной тематике. Тренировка осуществляется через отправку пользователю сообщения с текстом вопроса и 3-х вариантов
ответа в виде кнопок с цифрами 1 - 3. После выбора пользователем варианта ответа он проверяется и выводится результат, 
заданный вопрос, 3 варианта ответа и номер правильного ответа, изменяется статистика тренировки.
В  проекте использованы вопросы пна тему ТЕОРЕТИЧЕСКИЕ ВОПРОСЫ С ОТВЕТАМИ ДЛЯ ПРОВЕДЕНИЯ ТЕОРЕТИЧЕСКОЙ ЧАСТИ ИТОГОВОЙ 
АТТЕСТАЦИИ И ПРОВЕРКИ ЗНАНИЯ ПРАВИЛ БЕЗОПАСНОГО ОБРАЩЕНИЯ С ОРУЖИЕМ, можно использовать другую тематику тренировки.
## Описание программы
Программа написана на языке python3.11 с использованием библиотеки aiogram 3.x - асинхронный python фреймворк 
для создания telegram-ботов
## Порядок использования программы
Блок-схема функционирования бота нарисована в файле TrainingCardsBot.drawio.pdf
1. В Телеграм пользователь отправляет команду /start боту (или стартует его, найдя в поиске)
2. Бот приветствует пользователя, сообщает: 
«Привет! Это бот, в котором Вы можете потренировать свои знания. Чтобы приступить к тренировке выберите режим 
тренировки вопросов»: Выводятся 2 инлайн-кнопоки:
'Случайный выбор' и 'Вопросы по порядку' 
3. После выбора режима тренировки (нажатия инлайн-кнопки) пользователю предлагается вопрос и 3 варианта ответа,
включая верный, в виде инлайн-кнопок с соответствующими цифрами.
4. После нажатия кнопки с ответом, он проверяется,  выводится результат, заданный вопрос, варианты ответа и номер 
правильного ответа, изменяется и выводится статистика (Статистика тренировки=верных ответов/вопросов) пользователя и 
2 инлайн кнопки: «Еще билет» и «Завершить»
5. После кнопки «Еще билет» повторяется п. 3 - предлагается вопроса (вопрос, в зависимости от выбранного режима 
тренировки) и 3 варианта ответа, включая верный, в виде инлайн-кнопок с соответствующими записями.
6. После кнопки «Завершить» выводится: «Тренировка окончена. Ваш результат» — статистика
7. Имеется меню вызвав которое можно отправить боту команды: 
'/start': 'Начать тренировку заново, обновить статистику тренировки',
'/ticket_n': 'Ввести номер вопроса',
'/score': 'Показать статистику',
'/help': 'Справка по работе бота'
8. Если пользователь отправляет в чат любое текстовое сообщение, кроме определенных командЫ или кнопки:
Бот реагирует эхом
  