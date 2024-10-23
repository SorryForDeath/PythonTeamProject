import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE events (
    event_id INTEGER PRIMARY KEY,
    event_title TEXT,
    event_synopsis TEXT,
    event_docx TEXT,
    event_start_dt TEXT,
    event_final_dt TEXT,
    event_location TEXT,
    event_comment TEXT,
    event_age_category TEXT,
    event_budget REAL
)
''')

cursor.execute('''
CREATE TABLE visitors (
    visitor_id INTEGER PRIMARY KEY,
    visitor_full_name TEXT,
    visitor_email TEXT,
    visitor_phone TEXT,
    visitor_age_category TEXT,
    visitor_gender TEXT
)
''')

cursor.execute('''
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    employee_full_name TEXT,
    employee_position TEXT,
    employee_login TEXT,
    employee_passwd INTEGER,
    employee_access_level TEXT,
    employee_comment TEXT
)
''')

cursor.execute('''
CREATE TABLE tickets (
    ticket_id INTEGER PRIMARY KEY,
    ticket_event_id INTEGER,
    ticket_type TEXT,
    ticket_visitor_id INTEGER,
    ticket_price REAL,
    ticket_status TEXT,
    FOREIGN KEY(ticket_event_id) REFERENCES events(event_id),
    FOREIGN KEY(ticket_visitor_id) REFERENCES visitors(visitor_id)
)
''')

cursor.execute('''
CREATE TABLE event_employee (
    ee_event_id INTEGER,
    ee_employee_id INTEGER,
    role TEXT,
    FOREIGN KEY(ee_event_id) REFERENCES events(event_id),
    FOREIGN KEY(ee_employee_id) REFERENCES visitors(employee_id)
)    
''')

events_data = [
    (1, 'Cinema', 'New triller directed by Tarantino', 'any information', '2020-10-05', '2020-11-05', 'Skolkovo', 'Must see', '+18', '1000000$'),
    (2, 'Theatre', 'Classic of russian culture', 'any information', '2024-01-05', '2024-02-05', 'Theatre "Masterskaya"', 'Love it', '+18', '123123rub')
]

visitors_data = [
    (1, 'Alice Popovich', 'alice@bk.ru', '+79021234912', 'under 16', 'female'),
    (2, 'Segrei Barencev', 'Serg@gmal.com', '+79003451234', '+18', 'male')
]

employees_data = [
    (1, 'Eve', 'Security', 'Eve123', '*', '1', 'any comment'),
    (2, 'Frank', 'Manager', 'Frank123', '**', '2', 'any comment')
]

tickets_data = [
    (1, 1,  'Cinema ticket',1, 50.00, 'bought'), #Alice bought a ticket to cinema
    (2, 2,  'Theatre ticket', 2, 50.00, 'free') #Sergei bought(?) a ticket to theatre
]

event_employee_data = [
    (1, 1, 'All'),
    (2, 2, 'All')
]

cursor.executemany('INSERT INTO Events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', events_data)
cursor.executemany('INSERT INTO Visitors VALUES (?, ?, ?, ?, ?, ?)', visitors_data)
cursor.executemany('INSERT INTO Employees VALUES (?, ?, ?, ?, ?, ?, ?)', employees_data)
cursor.executemany('INSERT INTO Tickets VALUES (?, ?, ?, ?, ?, ?)', tickets_data)
cursor.executemany('INSERT INTO Event_Employee VALUES (?, ?, ?)', event_employee_data)

conn.commit()

cursor.execute('SELECT * FROM Events')
events_result = cursor.fetchall()

cursor.execute('SELECT * FROM Visitors')
visitors_result = cursor.fetchall()

cursor.execute('SELECT * FROM Employees')
employees_result = cursor.fetchall()

cursor.execute('SELECT * FROM Tickets')
tickets_result = cursor.fetchall()

cursor.execute('SELECT * FROM Event_Employee')
event_employee_result = cursor.fetchall()

for i in (events_result, visitors_result, employees_result, tickets_result, event_employee_result):
    print(i)
