import sys

from db_module import add_records, get_records, update_records, delete_records
from db_module import open_connection, close_connection, tables 
from db_module import input_add_record, input_update_record


def main_menu():
    while True:
        print("\n=== Управление событиями ===")
        print("1 - События")
        print("2 - Посетители")
        print("3 - Сотрудники")
        print("4 - Билеты")
        print("5 - Отчеты")
        print("6 - Тест для демонстрации")
        print("7 - Выход")
        
        choice = input("Выберите действие: ")
        if choice == "1":
            events_menu()
        elif choice == "2":
            visitors_menu()
        elif choice == "3":
            employees_menu()
        elif choice == "4":
            tickets_menu()
        elif choice == "5":
            print("Раздел 'Отчеты' пока не реализован.")
        elif choice == "6":
            print("Тестовая демонстрация пока не реализована.")
        elif choice == "7":
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
        print("5 - В главное меню")
        
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
        print("6 - В главное меню")
        
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

def tickets_menu():
    while True:
        print("\n=== Меню 'Билеты' ===")
        print("1 - Добавить билет (при вводе visitor event id нажмите enter)")
        print("2 - Просмотреть билеты")
        print("3 - В главное меню")
        
        choice = input("Выберите действие: ")
        if choice == "1":
            add_ticket()
        elif choice == "2":
            view_tickets()
        elif choice == "3":
            return
        else:
            print("Неверный выбор. Попробуйте снова.")

# функции, вызываемые по выбору пользователя в меню

def add_event():
    input_add_record("events")

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
    print("Продажа билета")

def add_ticket():
    input_add_record("tickets")

def view_tickets():
    print("Просмотр билетов")
    tickets = get_records('tickets')
    [print(ticket) for ticket in tickets]

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
