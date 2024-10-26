import sys

from db_module import add_records, get_records, update_records, delete_records
from db_module import input_add_record, input_update_record
from db_module import handle_db_error, open_connection, close_connection, get_connection, tables, is_number

def main_menu():
    while True:
        print("\n=== Управление событиями ===")
        print("1 - События")
        print("2 - Посетители")
        print("3 - Сотрудники")
        print("4 - Отчеты")
        print("5 - Тест для демонстрации")
        print("6 - Выход")
        
        choice = input("Выберите действие: ")
        if choice == "1":
            events_menu()
        elif choice == "2":
            visitors_menu()
        elif choice == "3":
            employees_menu()
        elif choice == "4":
            print("Раздел 'Отчеты' пока не реализован.")
        elif choice == "5":
            print("Тестовая демонстрация пока не реализована.")
        elif choice == "6":
            print("Выход из программы.")
            close_connection()
            sys.exit()
        else:
            print("Неверный выбор. Попробуйте снова.")

def events_menu():
    while True:
        print("\n=== Меню 'События' ===")
        print("1 - Добавить событие")
        print("2 - Просмотреть события")
        print("3 - Обновить событие")
        print("4 - Удалить событие")
        print("5 - Добавить билеты")
        print("6 - Просмотреть билеты")
        print("7 - В главное меню")
        
        choice = input("Выберите действие: ")
        if choice == "1":
            add_event()
        elif choice == "2":
            view_events()
        elif choice == "3":
            update_event()
        elif choice == "4":
            delete_event()
        elif choice == "5":
            add_tickets()
        elif choice == "6":
            view_tickets()
        elif choice == "7":
            return
        else:
            print("Неверный выбор. Попробуйте снова.")

def visitors_menu():
    while True:
        print("\n=== Меню 'Посетители' ===")
        print("1 - Добавить посетителя")
        print("2 - Просмотреть посетителей")
        print("3 - Обновить данные посетителя")
        print("4 - Удалить посетителя")
        print("5 - Продать билет")
        print("6 - Вернуть билет")
        print("7 - В главное меню")
        
        choice = input("Выберите действие: ")
        if choice == "1":
            add_visitor()
        elif choice == "2":
            view_visitors()
        elif choice == "3":
            update_visitor()
        elif choice == "4":
            delete_visitor()
        elif choice == "5":
            sell_ticket()
        elif choice == "6":
            refund_ticket()
        elif choice == "7":
            return
        else:
            print("Неверный выбор. Попробуйте снова.")

def employees_menu():
    while True:
        print("\n=== Меню 'Сотрудники' ===")
        print("1 - Добавить сотрудника")
        print("2 - Просмотреть сотрудников")
        print("3 - Обновить данные сотрудника")
        print("4 - Удалить сотрудника")
        print("5 - Назначить сотрудника на событие")
        print("6 - В главное меню")
        
        choice = input("Выберите действие: ")
        if choice == "1":
            add_employee()
        elif choice == "2":
            view_employees()
        elif choice == "3":
            update_employee()
        elif choice == "4":
            delete_employee()
        elif choice == "5":
            assign_employee_to_event()
        elif choice == "6":
            return
        else:
            print("Неверный выбор. Попробуйте снова.")

# меню tickets закомментировано
'''
def tickets_menu():
    while True:
        print("\n=== Меню 'Билеты' ===")
        print("1 - Добавить билеты")
        print("2 - Просмотреть билеты")
        print("3 - В главное меню")
        
        choice = input("Выберите действие: ")
        if choice == "1":
            add_tickets()
        elif choice == "2":
            view_tickets()
        elif choice == "3":
            return
        else:
            print("Неверный выбор. Попробуйте снова.")
'''
# конец закомментированного меню tickets

# функции, вызываемые по выбору пользователя в меню

def add_event():
    input_add_record("events")
    event_id = last_event_id()
    if event_id:
        add_tickets_for_event(event_id)

def last_event_id():
    # возвращает id последнего события в таблице или 0
    events = get_records("events")
    if events:
        return events[-1][0]  # Возвращаем ID последнего события
    else:
        return 0  # Если таблица пустая

def view_events():
    print("Просмотр событий")
    events = get_records('events')
    [print(event) for event in events]

def update_event():
    print("Обновление события")
    input_update_record('events')
def delete_event():
    print("Удаление события")
    id = input('Введите номер записи: ')
    if not id.isdigit():
        print("Ошибка: ID должен быть целым числом.")
        return
    delete_records('events', {'event_id': id})

def add_visitor():
    input_add_record("visitors")

def view_visitors():
    print("Просмотр посетителей")
    visitors = get_records('visitors')
    [print(visitor) for visitor in visitors]

def update_visitor():
    print("Обновление данных посетителя")
    input_update_record('visitors')
def delete_visitor():
    print("Удаление посетителя")
    id = input('Введите номер записи: ')
    if not id.isdigit():
        print("Ошибка: ID должен быть целым числом.")
        return
    delete_records('visitors', {'visitor_id': id})

def sell_ticket():
    while True:
        # 1. Запрашиваем и проверяем ID посетителя
        visitor_id_input = input("Введите ID посетителя (или 0 для завершения): ").strip()
        visitor_id = is_number(visitor_id_input, int, min_value=0)
        if not visitor_id:
            print("Ошибка: некорректный ID посетителя.")
            continue
        visitor_id = visitor_id[0]

        # Проверка на завершение
        if visitor_id == 0:
            print("Завершение продажи билетов.")
            break

        # 2. Проверка наличия ID посетителя в базе данных
        visitor_records = get_records("visitors", {"visitor_id": visitor_id})
        if not visitor_records:
            print(f"Посетитель с ID {visitor_id} не найден.")
            continue

        visitor = visitor_records[0]
        visitor_name = visitor[1]  # Имя посетителя

        # 3. Запрашиваем и проверяем ID мероприятия
        event_id_input = input("Введите ID мероприятия: ").strip()
        event_id = is_number(event_id_input, int, min_value=1)
        if not event_id:
            print("Ошибка: некорректный ID мероприятия.")
            continue
        event_id = event_id[0]

        # 4. Проверка наличия мероприятия
        event_records = get_records("events", {"event_id": event_id})
        if not event_records:
            print(f"Мероприятие с ID {event_id} не найдено.")
            continue

        event = event_records[0]
        event_title = event[1]      # Название мероприятия
        event_start_dt = event[3]   # Дата начала мероприятия

        # 5. Поиск первого непроданного билета для данного мероприятия
        connection = get_connection()
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM tickets WHERE ticket_event_id = ? AND ticket_visitor_id IS NULL LIMIT 1", (event_id,))
            ticket = cursor.fetchone()  # Получаем первый непроданный билет

            if ticket is None:
                print("Свободные билеты на это мероприятие отсутствуют.")
                continue

            ticket_id = ticket[0]        # ID билета
            ticket_price = ticket[3]     # Цена билета

            # 6. Обновляем запись билета, чтобы установить его как проданный
            cursor.execute("UPDATE tickets SET ticket_visitor_id = ? WHERE ticket_id = ?", (visitor_id, ticket_id))
            connection.commit()

            # Уведомление об успешной продаже
            print(f"Успешно продан билет: посетитель {visitor_name} (ID {visitor_id}) на мероприятие '{event_title}' "
                  f"(ID {event_id}) с датой начала {event_start_dt}, цена билета: {ticket_price}.")

        except Exception as e:
            print(f"Ошибка при продаже билета: {e}")
            if cursor:
                connection.rollback()  # Откатываем транзакцию в случае ошибки

        finally:
            if cursor:
                cursor.close()  # Закрываем курсор

def refund_ticket():
    while True:
        # запрашиваем ID посетителя
        visitor_id_input = input("Введите ID посетителя (или 0 для завершения): ").strip()
        visitor_id = is_number(visitor_id_input, int, min_value=0)
        if not visitor_id:
            print("Ошибка: Некорректный ID посетителя.")
            continue
        visitor_id = visitor_id[0]

        # Проверка на завершение
        if visitor_id == 0:
            print("Завершение возврата билетов.")
            break

        # проверка наличия ID посетителя в базе данных
        visitor_records = get_records("visitors", {"visitor_id": visitor_id})
        if not visitor_records:
            print(f"Ошибка: Посетитель с ID {visitor_id} не найден.")
            continue

        visitor = visitor_records[0]
        visitor_name = visitor[1]  # Имя посетителя

        # запрашиваем ID мероприятия
        event_id_input = input("Введите ID мероприятия: ").strip()
        event_id = is_number(event_id_input, int, min_value=1)
        if not event_id:
            print("Ошибка: Некорректный ID мероприятия.")
            continue
        event_id = event_id[0]

        # проверка наличия билета у пользователя на это мероприятие
        ticket_records = get_records("tickets", {"ticket_event_id": event_id, "ticket_visitor_id": visitor_id})
        if not ticket_records:
            print(f"Ошибка: У посетителя с ID {visitor_id} нет билета на мероприятие с ID {event_id}.")
            continue

        # Данные о мероприятии и билете для вывода
        ticket_price = ticket_records[0][3]

        event_records = get_records("events", {"event_id": event_id})
        if not event_records:
            print(f"Ошибка: Мероприятие с ID {event_id} не найдено.")
            continue

        event_title = event_records[0][1]

        # возврат билета - обнуление поля ticket_visitor_id
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE tickets SET ticket_visitor_id = NULL WHERE ticket_event_id = ? AND ticket_visitor_id = ?",
                (event_id, visitor_id)
            )
            connection.commit()
            cursor.close()
            print(f"Посетитель {visitor_name} (ID {visitor_id}) возвратил билет на мероприятие '{event_title}' (ID {event_id}), цена билета {ticket_price}.")
        except Exception as e:
            print(f"Ошибка при возврате билета: {e}")

def add_tickets_for_event(event_id):
    # добавляет билеты на мероприятие event_id 
    # вызывается из функций add_event и add_tickets
    # возвращает количество добавленных билетов
    total_tickets_added = 0
    while True:
        # Запрашиваем количество билетов для добавления на мероприятие event_id
        ticket_count_input = input("Введите количество добавляемых билетов (введите 0 для завершения): ").strip()
        ticket_count = is_number(ticket_count_input, int, min_value=0)
        if not ticket_count:
            print("Ошибка: некорректное количество билетов.")
            continue
        ticket_count = ticket_count[0]

        if ticket_count == 0:
            # print("Завершение добавления билетов.")
            break

        # Запрашиваем цену билетов
        ticket_price_input = input("Введите цену билетов: ").strip()
        ticket_price = is_number(ticket_price_input, float, min_value=0.0)
        if not ticket_price:
            print("Ошибка: некорректная цена билета.")
            continue
        ticket_price = ticket_price[0]

        # Подготовка данных для вставки в таблицу tickets
        data = [
            {
                "ticket_event_id": event_id,
                "ticket_visitor_id": None,  # Устанавливаем как свободный билет
                "ticket_price": ticket_price
            }
            for _ in range(ticket_count)
        ]

        # Используем функцию add_records для вставки каждой записи
        added_count = add_records("tickets", data)
        total_tickets_added += added_count

        # Отображение количества добавленных билетов в текущей итерации
        print(f"Добавлено {added_count} билетов для мероприятия с ID {event_id}.")

    # Возвращаем общее количество добавленных записей
    return total_tickets_added
def add_tickets():
    # добавляет билеты на мероприятия
    # запрашивает id мероприятия и вызывает add_tickets_for_event
    total_tickets_added = 0  # Общий счетчик добавленных билетов

    # Запрашиваем ID мероприятия
    event_id_input = input("Введите ID мероприятия, на которое будут добавлены билеты: ").strip()
    event_id = is_number(event_id_input, int, min_value=1)
    if not event_id:
        print("Ошибка: некорректный ID мероприятия.")
        return 0
    event_id = event_id[0]  # Извлекаем ID мероприятия
    total_tickets_added += add_tickets_for_event(event_id)

    print(f"Всего добавлено {total_tickets_added} билетов.")
    return total_tickets_added
def view_tickets():
    # Запрашиваем ID события
    event_id_input = input("Введите ID события (или 0 для всех событий): ").strip()
    event_id = is_number(event_id_input, int, min_value=0)
    if not event_id:
        print("Ошибка: некорректный ID события.")
        return
    event_id = event_id[0]  # Извлекаем ID события или 0 для всех

    # Формируем критерии поиска
    criteria = {}
    if event_id != 0:
        criteria["ticket_event_id"] = event_id

    # Получаем записи билетов, соответствующих критериям
    tickets = get_records("tickets", criteria)
    if not tickets:
        print("Билеты не найдены.")
        return

    # Словарь для накопления информации по каждому событию
    event_summary = {}
    for ticket in tickets:
        event_id = ticket[1]  # ticket_event_id
        is_sold = ticket[2] is not None  # ticket_visitor_id

        # Инициализация записи для события
        if event_id not in event_summary:
            # Получаем название события из таблицы events
            event_records = get_records("events", {"event_id": event_id})
            event_title = event_records[0][1] if event_records else "Неизвестно"

            event_summary[event_id] = {
                "event_title": event_title,
                "total_tickets": 0,
                "sold_tickets": 0,
                "unsold_tickets": 0
            }

        # Увеличиваем общее количество билетов для события
        event_summary[event_id]["total_tickets"] += 1

        # Увеличиваем количество проданных/непроданных билетов
        if is_sold:
            event_summary[event_id]["sold_tickets"] += 1
        else:
            event_summary[event_id]["unsold_tickets"] += 1

    # Вывод отчета с заголовком
    print("\nID | Событие                 | Всего | Продано | Осталось")
    print("-" * 50)
    for event_id, summary in event_summary.items():
        print(f"{event_id:<2} | {summary['event_title']:<22} | {summary['total_tickets']:<5} | "
              f"{summary['sold_tickets']:<7} | {summary['unsold_tickets']:<8}")

def add_employee():
    input_add_record("employees")

def view_employees():
    print("Просмотр сотрудников")
    employees = get_records('employees')
    [print(employee) for employee in employees]

def update_employee():
    print("Обновление данных сотрудника")
    input_update_record('employees')
def delete_employee():
    print("Удаление сотрудника")
    id = input('Введите номер записи: ')
    if not id.isdigit():
        print("Ошибка: ID должен быть целым числом.")
        return
    delete_records('employees', {'employee_id': id})

def assign_employee_to_event():
    print("Назначение сотрудника на событие")

open_connection()
main_menu()
close_connection()
