### CRUD для таблицы events
# functions: add_event(), get_events(), update_event(), delete_event()
import sqlite3
from globals import database_name

# Функция для добавления события (CREATE)
def add_event():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    title = input("Enter event title: ")
    synopsis = input("Enter event synopsis: ")
    start_dt = input("Enter event start date and time: ")
    final_dt = input("Enter event end date and time: ")
    location = input("Enter event location: ")
    age_restriction = input("Enter event age restriction: ")
    budget = input("Enter event budget: ")
    comment = input("Enter event comment (optional): ")

    cursor.execute('''
        INSERT INTO events (event_title, event_synopsis, event_start_dt, event_final_dt, event_location, event_age_restriction, event_budget, event_comment)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
        (title, synopsis, start_dt, final_dt, location, age_restriction, budget, comment))
    
    conn.commit()
    print("Event added successfully!")
    conn.close()

# Функция для получения всех событий (READ)
def get_events():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()
    conn.close()
    return events

# Функция для обновления события (UPDATE)
def update_event():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    event_id = input("Enter event ID to update: ")

    # Проверка существования события
    cursor.execute('SELECT event_id FROM events WHERE event_id = ?', (event_id,))
    event = cursor.fetchone()

    if not event:
        print(f"Event with ID {event_id} does not exist.")
        conn.close()
        return

    # Запрос данных для обновления
    title = input("Enter new event title (leave blank to skip): ")
    synopsis = input("Enter new event synopsis (leave blank to skip): ")
    start_dt = input("Enter new event start date and time (leave blank to skip): ")
    final_dt = input("Enter new event end date and time (leave blank to skip): ")
    location = input("Enter new event location (leave blank to skip): ")
    age_restriction = input("Enter new event age restriction (leave blank to skip): ")
    budget = input("Enter new event budget (leave blank to skip): ")
    comment = input("Enter new event comment (leave blank to skip): ")

    updates = []
    params = []

    if title:
        updates.append('event_title = ?')
        params.append(title)
    if synopsis:
        updates.append('event_synopsis = ?')
        params.append(synopsis)
    if start_dt:
        updates.append('event_start_dt = ?')
        params.append(start_dt)
    if final_dt:
        updates.append('event_final_dt = ?')
        params.append(final_dt)
    if location:
        updates.append('event_location = ?')
        params.append(location)
    if age_restriction:
        updates.append('event_age_restriction = ?')
        params.append(age_restriction)
    if budget:
        updates.append('event_budget = ?')
        params.append(budget)
    if comment:
        updates.append('event_comment = ?')
        params.append(comment)

    if updates:
        sql = 'UPDATE events SET ' + ', '.join(updates) + ' WHERE event_id = ?'
        params.append(event_id)
        cursor.execute(sql, params)
        if cursor.rowcount > 0:
            conn.commit()
            print("Event updated successfully!")
        else:
            print("No changes were made.")
    else:
        print("No fields provided for update.")

    conn.close()
    
# Функция для удаления события (DELETE)
def delete_event():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    event_id = input("Enter event ID to delete: ")

    # Проверка существования события
    cursor.execute('SELECT event_id FROM events WHERE event_id = ?', (event_id,))
    event = cursor.fetchone()

    if not event:
        print(f"Event with ID {event_id} does not exist.")
        conn.close()
        return

    # Удаление события
    cursor.execute('DELETE FROM events WHERE event_id = ?', (event_id,))
    conn.commit()

    print("Event deleted successfully!")

    conn.close()
