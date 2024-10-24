import sqlite3
from globals import database_name

### CRUD для таблицы employees
# functions: add_employee(), get_employees(), update_employee(), delete_employee()

def add_employee():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    full_name = input("Enter employee full name: ")
    position = input("Enter employee position: ")
    login = input("Enter employee login: ")
    passwd = input("Enter employee password: ")
    access_level = input("Enter employee access level: ")
    comment = input("Enter employee comment (optional): ")

    cursor.execute('''
        INSERT INTO employees (employee_full_name, employee_position, employee_login, employee_passwd, employee_access_level, employee_comment)
        VALUES (?, ?, ?, ?, ?, ?)''', 
        (full_name, position, login, passwd, access_level, comment))
    
    conn.commit()
    print("Employee added successfully!")
    conn.close()

def get_employees():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    employees = cursor.fetchall()
    conn.close()
    return employees

def update_employee():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    employee_id = input("Enter employee ID to update: ")

    cursor.execute('SELECT employee_id FROM employees WHERE employee_id = ?', (employee_id,))
    employee = cursor.fetchone()

    if not employee:
        print(f"Employee with ID {employee_id} does not exist.")
        conn.close()
        return

    full_name = input("Enter new employee full name (leave blank to skip): ")
    position = input("Enter new employee position (leave blank to skip): ")
    login = input("Enter new employee login (leave blank to skip): ")
    passwd = input("Enter new employee password (leave blank to skip): ")
    access_level = input("Enter new employee access level (leave blank to skip): ")
    comment = input("Enter new employee comment (leave blank to skip): ")

    updates = []
    params = []

    if full_name:
        updates.append('employee_full_name = ?')
        params.append(full_name)
    if position:
        updates.append('employee_position = ?')
        params.append(position)
    if login:
        updates.append('employee_login = ?')
        params.append(login)
    if passwd:
        updates.append('employee_passwd = ?')
        params.append(passwd)
    if access_level:
        updates.append('employee_access_level = ?')
        params.append(access_level)
    if comment:
        updates.append('employee_comment = ?')
        params.append(comment)

    if updates:
        sql = 'UPDATE employees SET ' + ', '.join(updates) + ' WHERE employee_id = ?'
        params.append(employee_id)
        cursor.execute(sql, params)
        conn.commit()
        print("Employee updated successfully!")
    else:
        print("No fields provided for update.")
    
    conn.close()

def delete_employee():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    employee_id = input("Enter employee ID to delete: ")

    cursor.execute('SELECT employee_id FROM employees WHERE employee_id = ?', (employee_id,))
    employee = cursor.fetchone()

    if not employee:
        print(f"Employee with ID {employee_id} does not exist.")
        conn.close()
        return

    cursor.execute('DELETE FROM employees WHERE employee_id = ?', (employee_id,))
    conn.commit()
    print("Employee deleted successfully!")

    conn.close()

