import sqlite3
from events import add_event, get_events, update_event, delete_event
from visitors import add_visitor, get_visitors, update_visitor, delete_visitor
from employees import add_employee, get_employees, update_employee, delete_employee
from globals import database_name

def create_database():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Таблица "events" (мероприятия)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        event_id INTEGER PRIMARY KEY,
        event_title TEXT NOT NULL,
        event_synopsis TEXT,
        event_start_dt TEXT NOT NULL,
        event_final_dt TEXT NOT NULL,
        event_location TEXT,
        event_age_restriction INTEGER,
        event_budget REAL,
        event_comment TEXT
    )
    ''')

    # Таблица "visitors" (посетители мероприятий)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS visitors (
        visitor_id INTEGER PRIMARY KEY,
        visitor_full_name TEXT NOT NULL,
        visitor_email TEXT NOT NULL,
        visitor_phone TEXT,
        visitor_age_category INTEGER,
        visitor_gender INTEGER
    )
    ''')

    # Таблица "employees" (сотрудники)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY,
        employee_full_name TEXT NOT NULL,
        employee_position TEXT NOT NULL,
        employee_login TEXT NOT NULL,
        employee_passwd TEXT NOT NULL,
        employee_access_level INTEGER,
        employee_comment TEXT
    )
    ''')

    # Таблица "tickets" (билеты)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        ticket_id INTEGER PRIMARY KEY,
        ticket_event_id INTEGER,
        ticket_visitor_id INTEGER DEFAULT NULL,
        ticket_price REAL,
        FOREIGN KEY (ticket_event_id) REFERENCES events(event_id),
        FOREIGN KEY (ticket_visitor_id) REFERENCES visitors(visitor_id)
    )
    ''')

    # Связывающая таблица "events_employees"
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events_employees (
        event_id INTEGER,
        employee_id INTEGER,
        FOREIGN KEY (event_id) REFERENCES events(event_id),
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
    )
    ''')

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

# Запускаем создание базы данных
create_database()



### CRUD для таблицы events_employees
def add_event_employee():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    event_id = input("Enter event ID: ")
    # Проверка существования event_id в таблице events
    cursor.execute('SELECT event_id FROM events WHERE event_id = ?', (event_id,))
    event = cursor.fetchone()
    if not event:
        print(f"Event with ID {event_id} does not exist.")
        conn.close()
        return

    employee_id = input("Enter employee ID: ")
    # Проверка существования employee_id в таблице employees
    cursor.execute('SELECT employee_id FROM employees WHERE employee_id = ?', (employee_id,))
    employee = cursor.fetchone()
    if not employee:
        print(f"Employee with ID {employee_id} does not exist.")
        conn.close()
        return

    # Если оба идентификатора существуют, добавляем запись
    cursor.execute('''
        INSERT INTO events_employees (event_id, employee_id)
        VALUES (?, ?)''', (event_id, employee_id))
    
    conn.commit()
    print("Event-Employee relation added successfully!")
    conn.close()
def get_event_employees():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events_employees')
    relations = cursor.fetchall()
    conn.close()
    return relations

def delete_event_employee():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    event_id = input("Enter event ID: ")
    # Проверка существования event_id в таблице events
    cursor.execute('SELECT event_id FROM events WHERE event_id = ?', (event_id,))
    event = cursor.fetchone()
    if not event:
        print(f"Event with ID {event_id} does not exist.")
        conn.close()
        return

    employee_id = input("Enter employee ID: ")
    # Проверка существования employee_id в таблице employees
    cursor.execute('SELECT employee_id FROM employees WHERE employee_id = ?', (employee_id,))
    employee = cursor.fetchone()
    if not employee:
        print(f"Employee with ID {employee_id} does not exist.")
        conn.close()
        return

    # Проверка существования связи между event_id и employee_id в таблице events_employees
    cursor.execute('SELECT * FROM events_employees WHERE event_id = ? AND employee_id = ?', (event_id, employee_id))
    relation = cursor.fetchone()
    if not relation:
        print(f"No relation found between event ID {event_id} and employee ID {employee_id}.")
        conn.close()
        return

    # Удаление связи
    cursor.execute('DELETE FROM events_employees WHERE event_id = ? AND employee_id = ?', (event_id, employee_id))
    conn.commit()

    print("Event-Employee relation deleted successfully!")
    conn.close()

# CLI для управления
def cli():
    while True:
        print("\nEvent Handler CLI")
        print("1 - Add event")
        print("2 - Show all events")
        print("3 - Update event")
        print("4 - Delete event")
        print("5 - Add visitor")
        print("6 - Show all visitors")
        print("7 - Update visitor")
        print("8 - Delete visitor")
        print("9 - Add employee")
        print("10 - Show all employees")
        print("11 - Update employee")
        print("12 - Delete employee")
        print("13 - Add event-employee relation")
        print("14 - Show all event-employee relations")
        print("15 - Delete event-employee relation")
        print("16 - Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            add_event()
        elif choice == '2':
            events = get_events()
            for event in events:
                print(event)
        elif choice == '3':
            update_event()
        elif choice == '4':
            delete_event()
        elif choice == '5':
            add_visitor()
        elif choice == '6':
            visitors = get_visitors()
            for visitor in visitors:
                print(visitor)
        elif choice == '7':
            update_visitor()
        elif choice == '8':
            delete_visitor()
        elif choice == '9':
            add_employee()
        elif choice == '10':
            employees = get_employees()
            for employee in employees:
                print(employee)
        elif choice == '11':
            update_employee()
        elif choice == '12':
            delete_employee()
        elif choice == '13':
            add_event_employee()
        elif choice == '14':
            relations = get_event_employees()
            for relation in relations:
                print(relation)
        elif choice == '15':
            delete_event_employee()
        elif choice == '16':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

# Запуск CLI
cli()
