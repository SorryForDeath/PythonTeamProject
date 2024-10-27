import sqlite3
from db_module import *

# Константы
# Сообщения и приглашения
MAIN_PROMPT = '''
    Выберите вид отчета:
1 - По событиям
2 - По гостям
3 - Вернуться в предыдущее меню
'''
INPUT_PROMPT = "Выберите действие: "
SELECT_EVENT_PROMPT = "Выберите событие (0 - выход): "
UNEXPECTED_INPUT = "Неверный выбор. Попробуйте снова."
EVENT_VALUE_ERROR = "Ошибка: событие должно быть целым числом."
EVENT_RANGE_ERROR = "События под таким номером не существует."
EVENT_TABLE_ERROR = "События отсутствуют."
EVENT_TITLE = 1
EVENT_BUDGET = 7
TICKET_VISITOR_ID = 2
TICKET_PRICE = 3

# Меню отчетов
def reports_menu():
    while True:
        print(MAIN_PROMPT)
        choice = input(INPUT_PROMPT)
        match choice:
            case "1":
                report_events()
            case "3":
                return
            case _:
                print(UNEXPECTED_INPUT)

def report_events():
    events = get_records('events')
    if len(events) == 0: # Нет событий
        print(EVENT_TABLE_ERROR)
        return
    while True:
        # Выводим список событий
        [print(event) for event in events]
        user_input = input(SELECT_EVENT_PROMPT)
        if user_input == "0": # Выбрали выход
            return
        try:
            user_event_id = int(user_input)
            # Проверяем диапазон
            if not (0 < user_event_id <= len(events)):
                print(EVENT_RANGE_ERROR)
                continue
            # Индекс события в списке событий
            index = user_event_id - 1
            # Берем билеты, связанные с событием
            db_cursor.execute(f"SELECT * FROM tickets WHERE ticket_event_id={user_event_id}")
            tickets = db_cursor.fetchall()
            # Проданные билеты, то есть связанные с каким-то посетителем
            sold_tickets = [ticket for ticket in tickets if ticket[TICKET_VISITOR_ID] is not None]
            # Суммируем проданные билеты
            revenue = sum(ticket[TICKET_PRICE] for ticket in sold_tickets)
            # Печатаем
            print(F'''
        Отчет по событию {events[index][EVENT_TITLE]}
----------------------------------------
Расходы: {events[index][EVENT_BUDGET]}
Всего билетов: {len(tickets)}
Продано: {len(sold_tickets)}
Доход: {revenue}
            ''')
        except ValueError:
            print(EVENT_VALUE_ERROR)

open_connection()
conn = sqlite3.connect(db_name)
db_cursor = conn.cursor()
# db_cursor.execute("PRAGMA table_info('tickets')")
# tickets_fields = db_cursor.fetchall()
# print(*tickets_fields)

reports_menu()
conn.close()
close_connection()
