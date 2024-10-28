import sys
from db_module import add_records, get_records, update_records, delete_records
from db_module import add_new_record, update_one_record
from db_module import handle_db_error, open_connection, close_connection, get_connection, tables, is_number
from reports_module import *
# вспомогательные функции для обработки пользовательского ввода
def id_input(hint, hint2 = 'Ошибка: ожидается положительное число или 0'):
    # запрашивает у пользователя id записи бд
    # проверяет ввод при помощи is_number, которая возвращает список чисел
    # если список пуст, т.е. введено не целое число большее или равное нулю, выводит сообщение об ошибке и возвращает пустой список
    # если ввод корректный, возвращает непустой список с введенным числом
    # hint - строка-подсказка пользователю в операторе input
    # hint2 - строка в сообщении об ошибке
    id_str = input(hint).strip()
    id_list = is_number(id_str, int, min_value=0)
    if not id_list:
        print(hint2)
    return id_list

def got_yes():
    # выводит сообщение на подтверждение удаления записи и возвращает 1, если нажата "д" или "Д"
    confirmation = input("Подтвердите удаление (д/н): ").strip().lower()
    return confirmation == 'д'

# меню программы
def main_menu():
    while True:
        print("\n=== Event Manager ===")
        print("1 - События")
        print("2 - Посетители")
        print("3 - Сотрудники")
        print("4 - Отчеты")
        # print("5 - Тест для демонстрации")
        print("0 - Выход")
        
        choice = input("Выберите действие: ")
        if choice == "1":
            events_menu()
        elif choice == "2":
            visitors_menu()
        elif choice == "3":
            employees_menu()
        elif choice == "4":
            reports_menu()
        # elif choice == "5":
            # print("Тестовая демонстрация пока не реализована.")
        elif choice == "0":
            print("Выход из программы.")
            break
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
        print("0 - В главное меню")
        
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
        elif choice == "0":
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
        print("0 - В главное меню")
        
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
        elif choice == "0":
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
        print("0 - В главное меню")
        
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
        elif choice == "0":
            return
        else:
            print("Неверный выбор. Попробуйте снова.")

# функции, вызываемые по выбору пользователя в меню

def add_event():
    add_new_record('events')
    event_id = last_id_in('events')
    if event_id:
        add_tickets_for_event(event_id)

def last_id_in(table):
    # возвращает id последней записи в таблице table или 0
    # считаем, что id хранится в нулевом поле записи и id автоинкрементируется
    records = get_records(table)
    if records:
        return records[-1][0]  # Возвращаем ID последней записи
    else:
        return 0  # Если таблица пустая

def view_events():
    events = get_records('events')
    
    # Заголовки таблицы
    header = f"{'ID':<3} {'Название':<30} {'Дата начала':<16} {'Дата окончания':<16} {'Место проведения':<25}"
    print(header)
    print('-' * len(header))  # Разделительная линия
    
    # Вывод данных о событиях
    for event in events:
        event_id, title, synopsis, start_dt, final_dt, location, age_restriction, budget, comment = event
        # Форматируем строки для выравнивания по столбцам
        row = (
            f"{event_id:<3} {title[:28]:<30} {start_dt:<16} {final_dt:<16} {location[:23]:<25}"
        )
        print(row)

    # Запуск цикла для просмотра подробной информации по ID
    while True:
        # Запрос ID события для подробного просмотра
        event_id_input = input("Введите id события для подробного просмотра или 0 для возврата: ").strip()
        
        # Проверка ввода на числовое значение
        valid_id = is_number(event_id_input, int, min_value=0)
        if not valid_id:
            print("Ошибка: некорректный ID. Введите целое число 0 или больше.")
            continue

        event_id = valid_id[0]

        # Завершение функции при вводе 0
        if event_id == 0:
            break

        # Поиск события с введенным ID в списке events
        event = next((e for e in events if e[0] == event_id), None)
        if event is None:
            print(f"Событие с ID {event_id} не найдено.")
            continue

        # Печать подробной информации о найденном событии
        event_details = [
            ("ID", event[0]),
            ("Название", event[1]),
            ("Описание", event[2]),
            ("Дата начала", event[3]),
            ("Дата окончания", event[4]),
            ("Место проведения", event[5]),
            ("Возрастное ограничение", event[6]),
            ("Бюджет", f"{event[7]:.2f}"),
            ("Комментарий", event[8])
        ]
        
        print("\nПодробная информация о событии:")
        for field_name, field_value in event_details:
            print(f"{field_name:<20}: {field_value}")
        print()  # Пустая строка для визуального разделения

def update_event():
    print("Обновление события")
    update_one_record('events')

def delete_event():
    while True:
        # 1. Запрашиваем ID удаляемого события и проверяем корректность ввода
        event_id = id_input("Введите ID удаляемого события (0 для выхода): ")
        if not event_id:
            continue
        event_id = event_id[0]
        if event_id == 0:
            break

        # 2. Проверка существования события в таблице events
        event_records = get_records("events", {"event_id": event_id})
        if not event_records:
            print(f"Событие с ID {event_id} не найдено.")
            continue
        event_title = event_records[0][1]  
        print(event_title)
        if not got_yes():
            continue

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
        ticket_count = id_input("Введите количество добавляемых билетов (0 для завершения): ", "Ошибка: неверное количество билетов")
        if not ticket_count:
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
        event_id = id_input("Введите ID мероприятия, на которое будут добавлены билеты (0 для завершения): ")
        if not event_id:
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
        event_title = event_records[0][1]
        print(event_title)
        tickets_added_for_event = add_tickets_for_event(event_id)
        total_tickets_added += tickets_added_for_event

    # 5. Итоговое количество добавленных билетов
    print(f"Всего добавлено {total_tickets_added} билетов.")
    return total_tickets_added

def view_tickets():
    # Запрашиваем ID события
    event_id = id_input("Введите ID события (или 0 для всех событий): ")
    if not event_id:
        return
    event_id = event_id[0]  # Извлекаем ID события или 0 для всех

    # Формируем критерии поиска и получаем записи билетов
    criteria = {"ticket_event_id": event_id} if event_id != 0 else {}
    tickets = get_records("tickets", criteria)
    if not tickets:
        print("Билеты не найдены.")
        return

    # Словарь для суммарной информации по каждому событию
    event_summary = {}
    for ticket in tickets:
        event_id = ticket[1]  # ticket_event_id
        is_sold = ticket[2] is not None  # ticket_visitor_id

        # Инициализация записи для события при первом появлении
        if event_id not in event_summary:
            event_title = get_records("events", {"event_id": event_id})
            event_title = event_title[0][1] if event_title else "Неизвестно"
            event_summary[event_id] = {"event_title": event_title, "total": 0, "sold": 0, "unsold": 0}

        # Подсчет общего числа и количества проданных/непроданных билетов
        event_summary[event_id]["total"] += 1
        if is_sold:
            event_summary[event_id]["sold"] += 1
        else:
            event_summary[event_id]["unsold"] += 1

    # Заголовок таблицы
    header = f"{'ID':<3} {'Событие':<30} {'Всего':<8} {'Продано':<8} {'Осталось':<8}"
    print(header)
    print('-' * len(header))

    # Форматированный вывод для каждого события
    for event_id, summary in event_summary.items():
        row = (
            f"{event_id:<3} {summary['event_title'][:28]:<30} "
            f"{summary['total']:<8} {summary['sold']:<8} {summary['unsold']:<8}"
        )
        print(row)

def add_visitor():
    add_new_record('visitors')
    # visitor_id = last_id_in('visitors')

def view_visitors():
    visitors = get_records('visitors')
    
    # Заголовки таблицы
    header = f"{'ID':<5} {'ФИО':<20} {'Email':<25} {'Телефон':<18}"
    print(header)
    print('-' * len(header))  # Разделительная линия
    
    # Вывод данных посетителей
    for visitor in visitors:
        visitor_id, full_name, email, phone = visitor
        # Форматируем строки для выравнивания по столбцам
        row = f"{visitor_id:<5} {full_name[:18]:<20} {email[:23]:<25} {phone:<18}"
        print(row)

def update_visitor():
    print("Обновление данных посетителя")
    update_one_record('visitors')

def delete_visitor():
    while True:
        # 1. Запрашиваем ID удаляемого посетителя и проверяем корректность ввода
        visitor_id = id_input("Введите ID удаляемого посетителя (0 для выхода): ")
        if not visitor_id:
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
        print(visitor_name )
        if not got_yes():
            continue

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
        visitor_id = id_input("Введите ID посетителя (0 для завершения): ")
        if not visitor_id:
            continue
        visitor_id = visitor_id[0]

        # Проверка на завершение
        if visitor_id == 0:
            break

        # 2. Проверка наличия ID посетителя в базе данных
        visitor_records = get_records("visitors", {"visitor_id": visitor_id})
        if not visitor_records:
            print(f"Посетитель с ID {visitor_id} не найден.")
            continue

        visitor = visitor_records[0]
        visitor_name = visitor[1]  # Имя посетителя
        print(visitor_name)

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
        print(event_title)

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
        visitor_id = id_input("Введите ID посетителя (0 для завершения): ")
        if not visitor_id:
            continue
        visitor_id = visitor_id[0]

        # Проверка на завершение
        if visitor_id == 0:
            break

        # проверка наличия ID посетителя в базе данных
        visitor_records = get_records("visitors", {"visitor_id": visitor_id})
        if not visitor_records:
            print(f"Ошибка: Посетитель с ID {visitor_id} не найден.")
            continue

        visitor = visitor_records[0]
        visitor_name = visitor[1]  # Имя посетителя
        print(visitor_name)

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
            print(f"Ошибка: У посетителя {visitor_name} (ID {visitor_id}) нет билета на мероприятие с ID {event_id}.")
            continue

        # Данные о мероприятии и билете для вывода
        ticket_price = ticket_records[0][3]

        event_records = get_records("events", {"event_id": event_id})
        if not event_records:
            print(f"Ошибка: Мероприятие с ID {event_id} не найдено.")
            continue

        event_title = event_records[0][1]
        print(event_title)
        if not got_yes():
            continue

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
    add_new_record('employees')
    # employee_id = last_id_in('employees')

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
    update_one_record('employees')

def delete_employee():
    print("Удаление сотрудника")

    # Шаг 1: Запросить ID сотрудника и проверить формат
    employee_id = id_input("Введите ID сотрудника для удаления (0 для выхода): ")
    if not employee_id:
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
    employee_id = id_input("Введите ID менеджера (0 для выхода): ")
    if not employee_id:
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
main_menu()
close_connection()
