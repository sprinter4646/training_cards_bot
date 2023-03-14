# Формирует список билетов voprosy_otvety, состоящий из билетов в виде списка списков вида
# [['question_n ', 'answer1', 'answer2', 'answer3', 'right_answer']]
# [[билет_вопрос, ответ1, ответ2, ответ3, 'правильный_ответ]]
TICKETS_PATH = '/home/oleg/REPOS/TrainingCardsBot/tickets/2023 ВОПРОСЫ БОО.txt'
with open(TICKETS_PATH, 'r', encoding='utf-8') as file:
    voprosy_otvety: list[[]] = []
    ticket_row = 0
    ticket = []
    for row in file:
        row = row.replace('\ufeff', '')
        row = row.rstrip('\n')
        ticket_row += 1
        if ticket_row % 5 == 1:
            question_n = row
            ticket.append(question_n)
            # print(ticket_row, row)
        elif ticket_row % 5 == 2:
            answer1 = row
            ticket.append(answer1)
            # print(ticket_row, row)
        elif ticket_row % 5 == 3:
            answer2 = row
            ticket.append(answer2)
            # print(ticket_row, row)
        elif ticket_row % 5 == 4:
            answer3 = row
            ticket.append(answer3)
            # print(ticket_row, row)
        elif ticket_row % 5 == 0:
            right_answer = row.strip('Ответ- ')
            ticket.append(right_answer)
            # print(ticket_row, row)
            voprosy_otvety.append(ticket)
            ticket = []
# print(len(voprosy_otvety))
'''for ticket in voprosy_otvety:
    print(ticket, end='\n')'''

