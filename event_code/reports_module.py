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
BUDGET = 7

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
    if len(events) == 0:
        print(EVENT_TABLE_ERROR)
        return
    while True:
        [print(event) for event in events]
        user_input = input(SELECT_EVENT_PROMPT)
        if user_input == "0":
            return
        try:
            user_event_id = int(user_input)
            # Проверяем диапазон
            if not (0 < user_event_id <= len(events)):
                print(EVENT_RANGE_ERROR)
                continue
            index = user_event_id - 1
            print("Бюджет: ", events[index][BUDGET])
        except ValueError:
            print(EVENT_VALUE_ERROR)

open_connection()
print(db_name)
# reports_menu()
close_connection()
