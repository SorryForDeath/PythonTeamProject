import sqlite3
import csv
from db_module import *

# Константы
# Сообщения и приглашения
MAIN_PROMPT = '''
=== Меню "Отчеты" ===
1 - Отчет по событиям
2 - Отчет по гостям
0 - Вернуться в Главное меню
'''
INPUT_PROMPT = "Выберите действие: "
SELECT_EVENTS_PROMPT = "Введите команду (1 - сохранить, 0 - выход): "
UNEXPECTED_INPUT = "Неверный выбор. Попробуйте снова."
EVENT_VALUE_ERROR = "Ошибка: событие должно быть целым числом."
EVENT_RANGE_ERROR = "События под таким номером не существует."
EVENT_TABLE_ERROR = "События отсутствуют."
EVENT_ID = 0
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
            case "0":
                return
            case _:
                print(UNEXPECTED_INPUT)

def get_event_finance_info(event):
    '''
    Аргумент: информация о событии,
    Возвращаем список с финансовыми данными.
    '''
    # Берем билеты, связанные с событием
    db_cursor.execute(f"SELECT * FROM tickets WHERE ticket_event_id={event[EVENT_ID]}")
    tickets = db_cursor.fetchall()
    # Проданные билеты, то есть связанные с каким-то посетителем, visitor_id не None
    sold_tickets = [ticket for ticket in tickets if ticket[TICKET_VISITOR_ID] is not None]
    title = event[EVENT_TITLE]
    budget = event[EVENT_BUDGET]
    quantity = len(tickets)
    sold = len(sold_tickets)
    # Суммируем проданные билеты
    revenue = sum(ticket[TICKET_PRICE] for ticket in sold_tickets)
    return (title, budget, quantity, sold, revenue)

def save_to_csv(events):
    '''
    Запрашиваем имя CSV-файла и записываем данные.
    '''

    the_report = [["НАЗВАНИЕ", "РАСХОДЫ", "БИЛЕТОВ", "ПРОДАНО", "ДОХОД"]]

    for event in events:
        the_report.append(get_event_finance_info(event))

    while True:
        user_input = input("Введите имя CSV-файла (0 - для выхода): ")
        if user_input == "0":
            return
        try:
            with open(user_input, 'w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerows(the_report)
            print("Отчет сохранен в файл ", user_input)
            print("-" * 30)
            return
        except FileNotFoundError:
            print("Ошибка: файл не найден. Проверьте путь и попробуйте снова.")
        except Exception as err:
            print("Ошибка записи в файл: ", err)
    return

def report_events():
    events = get_records('events')
    if len(events) == 0: # Нет событий
        print(EVENT_TABLE_ERROR)
        return
    max_title_length = max(len(event[EVENT_TITLE]) for event in events)
    while True:
        print("ОТЧЕТ ПО СОБЫТИЯМ")
        headers = f"{'НАЗВАНИЕ':<{max_title_length}} {'РАСХОДЫ':<10} {'БИЛЕТОВ':<7} {'ПРОДАНО':<7} {'ДОХОД':<10}"
        print("-" * len(headers))
        print(headers)
        print("-" * len(headers))
        # Выводим отчет по всем событиям
        for event in events:
            title, budget, quantity, sold, revenue = get_event_finance_info(event)
            # Печатаем
            row = f"{title:<{max_title_length}} {budget:<10} {quantity:<7} {sold:<7} {revenue:<10}"
            print(row)
        user_input = input(SELECT_EVENTS_PROMPT)
        if user_input == "0": # Выбрали выход
            return
        if user_input == "1": # Вывод в файл
            save_to_csv(events)
            continue
    return

open_connection()
# conn = sqlite3.connect(db_name)
conn = get_connection()
db_cursor = conn.cursor()
if __name__ == "__main__":
    # db_cursor.execute("PRAGMA table_info('tickets')")
    # tickets_fields = db_cursor.fetchall()
    # print(*tickets_fields)
    reports_menu()
db_cursor.close()
conn.close()
close_connection()
