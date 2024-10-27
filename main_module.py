import sys

from db_module import add_records, get_records, update_records, delete_records
from db_module import input_add_record, input_update_record
from db_module import handle_db_error, open_connection, close_connection, get_connection, tables, is_number, got_yes
from test_data import insert_test_data

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
        print("7 - Просмотреть билеты")
        print("8 - В главное меню")
        
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
            view_tickets()
        elif choice == "8":
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
    while True:
        # 1. Запрашиваем ID удаляемого события и проверяем корректность ввода
        event_id_input = input("Введите ID удаляемого события (или 0 для выхода): ").strip()
        event_id = is_number(event_id_input, int, min_value=0)

        # Проверка корректности ID и завершение при вводе 0
        if not event_id:
            print("Ошибка: некорректный ID события.")
            continue
        event_id = event_id[0]
        if event_id == 0:
            break

        # 2. Проверка существования события в таблице events
        event_records = get_records("events", {"event_id": event_id})
        if not event_records:
            print(f"Событие с ID {event_id} не найдено.")
            continue
        event_title = event_records[0][1]  # Название события (например, event_title)

        # Установка соединения с базой данных
        connection = get_connection()
        if connection is None:
            print("Ошибка: соединение с базой данных не установлено.")
            return

        try:
            # 3. Устанавливаем точку восстановления
            connection.execute("SAVEPOINT delete_event_savepoint")

            # Удаляем событие из таблицы events
            deleted_count = delete_records("events", {"event_id": event_id})
            if deleted_count == 0:
                raise Exception(f"Не удалось удалить событие с ID {event_id} из таблицы events.")
            
            # Удаляем записи, связанные с событием, из таблиц tickets и events_employees
            delete_records("tickets", {"ticket_event_id": event_id})
            delete_records("events_employees", {"event_id": event_id}) 

            # Коммитим транзакцию
            connection.commit()
            print(f"Событие '{event_title}' (ID {event_id}) успешно удалено.")

        except Exception as e:
            # Откат к точке сохранения при ошибке
            connection.execute("ROLLBACK TO delete_event_savepoint")
            handle_db_error(e)
            print(f"Ошибка при удалении события с ID {event_id}. Все изменения отменены.")


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
    # Добавляет билеты на мероприятия, проверяя наличие мероприятия
    total_tickets_added = 0  # Общий счетчик добавленных билетов

    while True:
        # 1. Запрашиваем ID мероприятия
        event_id_input = input("Введите ID мероприятия, на которое будут добавлены билеты (или 0 для завершения): ").strip()
        event_id = is_number(event_id_input, int, min_value=0)
        if not event_id:
            print("Ошибка: некорректный ID мероприятия.")
            continue

        event_id = event_id[0]
        if event_id == 0:
            break  # Завершение функции, если введен 0

        # 2. Проверка наличия мероприятия в таблице events
        event_records = get_records("events", {"event_id": event_id})
        if not event_records:
            print(f"Мероприятие с ID {event_id} не найдено.")
            continue

        # 3. Если событие существует, вызываем add_tickets_for_event
        tickets_added_for_event = add_tickets_for_event(event_id)
        total_tickets_added += tickets_added_for_event

    # 5. Итоговое количество добавленных билетов
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
    while True:
        # 1. Запрашиваем ID удаляемого посетителя и проверяем корректность ввода
        visitor_id_input = input("Введите ID удаляемого посетителя (или 0 для выхода): ").strip()
        visitor_id = is_number(visitor_id_input, int, min_value=0)

        # Проверка корректности ID и завершение при вводе 0
        if not visitor_id:
            print("Ошибка: некорректный ID посетителя.")
            continue
        visitor_id = visitor_id[0]
        if visitor_id == 0:
            break

        # 2. Проверка существования посетителя в таблице visitors
        visitor_records = get_records("visitors", {"visitor_id": visitor_id})
        if not visitor_records:
            print(f"Посетитель с ID {visitor_id} не найден.")
            continue
        visitor_name = visitor_records[0][1]  # Имя посетителя

        # Установка соединения с базой данных
        connection = get_connection()
        if connection is None:
            print("Ошибка: соединение с базой данных не установлено.")
            return

        try:
            # 3. Устанавливаем точку восстановления
            connection.execute("SAVEPOINT delete_visitor_savepoint")

            # Удаляем посетителя из таблицы visitors
            deleted_count = delete_records("visitors", {"visitor_id": visitor_id})
            if deleted_count == 0:
                raise Exception(f"Не удалось удалить посетителя с ID {visitor_id} из таблицы visitors.")
            
            # Удаляем записи, связанные с посетителем, из таблицы tickets
            delete_records("tickets", {"ticket_visitor_id": visitor_id})

            # Коммитим транзакцию
            connection.commit()
            print(f"Посетитель '{visitor_name}' (ID {visitor_id}) успешно удален.")

        except Exception as e:
            # Откат к точке сохранения при ошибке
            connection.execute("ROLLBACK TO delete_visitor_savepoint")
            handle_db_error(e)
            print(f"Ошибка при удалении посетителя с ID {visitor_id}. Все изменения отменены.")

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

def add_employee():
    input_add_record("employees")

def view_employees():
    employees = get_records('employees')
    # Заголовки таблицы
    header = f"{'ID':<3} {'ФИО':<20} {'Должность':<15} {'Комментарий':<20}"
    print(header)
    print('-' * len(header))  # Разделительная линия
    # Вывод данных сотрудников
    for employee in employees:
        employee_id, full_name, position, comment = employee
        # Форматируем строки для выравнивания по столбцам
        row = f"{employee_id:<3} {full_name:<20} {position:<15} {comment:<20}"
        print(row)

def update_employee():
    print("Обновление данных сотрудника")
    input_update_record('employees')
def delete_employee():
    print("Удаление сотрудника")

    # Шаг 1: Запросить ID сотрудника и проверить формат
    employee_id_input = input("Введите ID сотрудника для удаления (0 для выхода): ").strip()
    employee_id = is_number(employee_id_input, int, min_value=0)
    if not employee_id:
        print("Ошибка: некорректный ID сотрудника.")
        return
    employee_id = employee_id[0]
    if employee_id  == 0:
        return

    # Проверка наличия сотрудника в таблице employees
    employee_record = get_records('employees', {"employee_id": employee_id})
    if not employee_record:
        print("Ошибка: сотрудник с таким ID не найден.")
        return
    full_name = employee_record[0][1]  # Извлекаем полное имя сотрудника
    print(f"{full_name}")

    # Шаг 2: Запросить подтверждение
    if not got_yes():
        return

    # Шаг 4: Удаление сотрудника с использованием транзакций
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SAVEPOINT delete_employee")  # Создаем точку возврата

        # Удаляем сотрудника из таблицы employees
        cursor.execute("DELETE FROM employees WHERE employee_id = ?", (employee_id,))
        if cursor.rowcount == 0:
            print(f"Ошибка: сотрудник с ID {employee_id} не был удален.")
            cursor.execute("ROLLBACK TO delete_employee")  # Откат к savepoint, если удаление не удалось
            return

        # Удаляем записи сотрудника из таблицы events_employees
        cursor.execute("DELETE FROM events_employees WHERE employee_id = ?", (employee_id,))
        
        # Подтверждаем транзакцию
        connection.commit()
        print(f"Сотрудник {full_name} удален из базы данных.")
    
    except Exception as e:
        # В случае ошибки откатываемся к savepoint и выводим сообщение об ошибке
        handle_db_error(e)
        connection.rollback()
        print("Удаление отменено из-за ошибки.")
    
    finally:
        cursor.close()
def assign_employee_to_event():
    print("Назначение менеджера ответственным за мероприятие")
    
    # Шаг 1: Запросить ID менеджера и проверить формат
    employee_id_input = input("Введите ID менеджера (0 для выхода): ").strip()
    employee_id = is_number(employee_id_input, int, min_value=0)
    if not employee_id:
        print("Ошибка: некорректный ID менеджера.")
        return
    employee_id = employee_id[0]
    if employee_id  == 0:
        return
    
    # Шаг 2: Проверить, есть ли такой менеджер в таблице employees
    employee_record = get_records('employees', {"employee_id": employee_id})
    if not employee_record:
        print("Ошибка: менеджер с таким ID не найден.")
        return
    employee_name = employee_record[0][1]  # Получаем полное имя менеджера
    print(f"{employee_name}")
    
    # Шаг 3: Запросить ID мероприятия и проверить формат
    event_id_input = input("Введите ID мероприятия: ").strip()
    event_id = is_number(event_id_input, int, min_value=1)
    if not event_id:
        print("Ошибка: некорректный ID мероприятия.")
        return
    event_id = event_id[0]
    
    # Шаг 4: Проверить, есть ли такое мероприятие в таблице events
    event_record = get_records('events', {"event_id": event_id})
    if not event_record:
        print("Ошибка: мероприятие с таким ID не найдено.")
        return
    event_title = event_record[0][1]  # Получаем название мероприятия
    print(f"{event_title}")
    
    # Шаг 5: Проверить, не назначен ли уже кто-то другой на это мероприятие
    existing_assignment = get_records('events_employees', {"event_id": event_id})
    if existing_assignment:
        # Получаем имя назначенного менеджера
        assigned_employee_id = existing_assignment[0][1]
        assigned_employee_record = get_records('employees', {"employee_id": assigned_employee_id})
        assigned_employee_name = assigned_employee_record[0][1] if assigned_employee_record else "неизвестно"
        print(f"За это мероприятие уже отвечает {assigned_employee_name}")
        return
    
    # Шаг 6: Если никто не назначен, назначить менеджера
    data = {
        "event_id": event_id,
        "employee_id": employee_id
    }
    add_records("events_employees", data)
    print(f"{employee_name} назначен ответственным за {event_title}")

# main program

open_connection()
# insert_test_data()
main_menu()
close_connection()
