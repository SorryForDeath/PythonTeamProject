### CRUD для таблицы visitors
# functions: add_visitor(), get_visitors(), update_visitor(), delete_visitor()
import sqlite3
from globals import database_name

def add_visitor():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    full_name = input("Enter visitor full name: ")
    email = input("Enter visitor email: ")
    phone = input("Enter visitor phone: ")
    age_category = input("Enter visitor age category: ")
    gender = input("Enter visitor gender (0 - Male, 1 - Female): ")

    cursor.execute('''
        INSERT INTO visitors (visitor_full_name, visitor_email, visitor_phone, visitor_age_category, visitor_gender)
        VALUES (?, ?, ?, ?, ?)''', (full_name, email, phone, age_category, gender))
    
    conn.commit()
    print("Visitor added successfully!")
    conn.close()

def get_visitors():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM visitors')
    visitors = cursor.fetchall()
    conn.close()
    return visitors

def update_visitor():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    visitor_id = input("Enter visitor ID to update: ")

    cursor.execute('SELECT visitor_id FROM visitors WHERE visitor_id = ?', (visitor_id,))
    visitor = cursor.fetchone()

    if not visitor:
        print(f"Visitor with ID {visitor_id} does not exist.")
        conn.close()
        return

    full_name = input("Enter new visitor full name (leave blank to skip): ")
    email = input("Enter new visitor email (leave blank to skip): ")
    phone = input("Enter new visitor phone (leave blank to skip): ")
    age_category = input("Enter new visitor age category (leave blank to skip): ")
    gender = input("Enter new visitor gender (leave blank to skip): ")

    updates = []
    params = []

    if full_name:
        updates.append('visitor_full_name = ?')
        params.append(full_name)
    if email:
        updates.append('visitor_email = ?')
        params.append(email)
    if phone:
        updates.append('visitor_phone = ?')
        params.append(phone)
    if age_category:
        updates.append('visitor_age_category = ?')
        params.append(age_category)
    if gender:
        updates.append('visitor_gender = ?')
        params.append(gender)

    if updates:
        sql = 'UPDATE visitors SET ' + ', '.join(updates) + ' WHERE visitor_id = ?'
        params.append(visitor_id)
        cursor.execute(sql, params)
        conn.commit()
        print("Visitor updated successfully!")
    else:
        print("No fields provided for update.")
    
    conn.close()

def delete_visitor():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    visitor_id = input("Enter visitor ID to delete: ")

    cursor.execute('SELECT visitor_id FROM visitors WHERE visitor_id = ?', (visitor_id,))
    visitor = cursor.fetchone()

    if not visitor:
        print(f"Visitor with ID {visitor_id} does not exist.")
        conn.close()
        return

    cursor.execute('DELETE FROM visitors WHERE visitor_id = ?', (visitor_id,))
    conn.commit()
    print("Visitor deleted successfully!")

    conn.close()

