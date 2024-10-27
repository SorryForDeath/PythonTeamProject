import sqlite3
from datetime import datetime


# имя базы данных
db_name = 'event_database.db'
# переменная для соединения
connection = None

# Описание структуры таблиц в словаре
tables = {
    "events": {
        "event_id": {
            "type": "INTEGER PRIMARY KEY"
        },
        "event_title": {
            "type": "TEXT"
        },
        "event_synopsis": {
            "type": "TEXT"
        },
        "event_start_dt": {
            "type": "TEXT",
            "format": "yyyy-mm-dd hh:mm"  # Ожидаемый формат для даты и времени
        },
        "event_final_dt": {
            "type": "TEXT",
            "format": "yyyy-mm-dd hh:mm"
        },
        "event_location": {
            "type": "TEXT"
        },
        "event_age_restriction": {
            "type": "INTEGER",
            "min": 0,
            "max": 21  # Диапазон для возрастных ограничений
        },
        "event_budget": {
            "type": "REAL",
            "min": 0.0,
            "max": 1_000_000.0  # Диапазон для бюджета
        },
        "event_comment": {
            "type": "TEXT"
        }
    },
    "visitors": {
        "visitor_id": {
            "type": "INTEGER PRIMARY KEY"
        },
        "visitor_full_name": {
            "type": "TEXT"
        },
        "visitor_email": {
            "type": "TEXT"
        },
        "visitor_phone": {
            "type": "TEXT"
        }
    },
    "employees": {
        "employee_id": {
            "type": "INTEGER PRIMARY KEY"
        },
        "employee_full_name": {
            "type": "TEXT"
        },
        "employee_position": {
            "type": "TEXT"
        },
        "employee_comment": {
            "type": "TEXT"
        }
    },
    "tickets": {
        "ticket_id": {
            "type": "INTEGER PRIMARY KEY"
        },
        "ticket_event_id": {
            "type": "INTEGER"
        },
        "ticket_visitor_id": {
            "type": "INTEGER DEFAULT NULL"
        },
        "ticket_price": {
            "type": "REAL"
        }
    },
    "events_employees": {
        "event_id": {
            "type": "INTEGER"
        },
        "employee_id": {
            "type": "INTEGER"
        }
    }
}


# Создание таблиц на основе структуры данных
def create_tables():
    global connection
    cursor = connection.cursor()
    for table_name, columns in tables.items():
        # Формируем строку определения столбцов
        columns_definition = ", ".join([f"{col} {properties['type']}" for col, properties in columns.items()])
        
        # Добавляем внешние ключи отдельно, если они есть
        foreign_keys = []
        for col, properties in columns.items():
            if 'FOREIGN KEY' in properties:
                foreign_keys.append(properties['FOREIGN KEY'])
        
        if foreign_keys:
            columns_definition += ", " + ", ".join(foreign_keys)

        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition})")
    
    cursor.close()

# Функция для инициализации базы данных
def open_connection():
    global connection
    connection = sqlite3.connect(db_name)
    create_tables()  # Создаем таблицы

# Закрытие соединения с базой данных
def close_connection():
    if connection:
        connection.close()

# для передачи connection в другие модули
def get_connection():
    return connection

# Функция для обработки ошибок работы с БД
def handle_db_error(error):
    if isinstance(error, sqlite3.OperationalError):
        print(f"OperationalError: {error}")
    elif isinstance(error, sqlite3.IntegrityError):
        print(f"IntegrityError: {error}")
    else:
        print(f"Unexpected database error: {error}")

# Добавление записей в таблицу
def add_records(table, data):
    if not data:
        print("No data provided for insertion.")
        return 0  # Возвращаем 0, если нет данных
    
    # Преобразуем одиночный словарь в список словарей для единообразия
    if isinstance(data, dict):
        data = [data]

    columns = ', '.join(data[0].keys())
    placeholders = ', '.join(['?' for _ in data[0]])
    values = [tuple(item.values()) for item in data]

    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    
    try:
        cursor = connection.cursor()
        cursor.executemany(query, values)
        connection.commit()  # Выполняем коммит
        count = cursor.rowcount  # Сохраняем количество добавленных строк
        cursor.close()  # Закрываем курсор
        return count
    except Exception as e:
        handle_db_error(e)
        return 0

# Получение записей из таблицы
def get_records(table, criteria=None):
    query = f"SELECT * FROM {table}"
    values = ()
    if criteria:
        conditions = ' AND '.join([f"{key} = ?" for key in criteria.keys()])
        query += f" WHERE {conditions}"
        values = tuple(criteria.values())
    
    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        records = cursor.fetchall()  # Возвращаем все выбранные записи
        cursor.close()  # Закрываем курсор
        return records
    except Exception as e:
        handle_db_error(e)
        return []

# Обновление записей в таблице
def update_records(table, data, criteria):
    if not data:
        print("No data provided for update.")
        return 0

    updates = ', '.join([f"{key} = ?" for key in data.keys()])
    conditions = ' AND '.join([f"{key} = ?" for key in criteria.keys()])
    values = tuple(data.values()) + tuple(criteria.values())

    query = f"UPDATE {table} SET {updates} WHERE {conditions}"
    
    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()  # Выполняем коммит
        count = cursor.rowcount  # Сохраняем количество обновленных строк
        cursor.close()  # Закрываем курсор
        return count
    except Exception as e:
        handle_db_error(e)
        return 0

# Удаление записей из таблицы
def delete_records(table, criteria):
    if not criteria:
        print("No criteria provided for deletion.")
        return 0

    # Обработка оператора IN
    conditions = []
    values = []
    for key, value in criteria.items():
        if isinstance(value, tuple):
            placeholders = ', '.join(['?' for _ in value])
            conditions.append(f"{key} IN ({placeholders})")
            values.extend(value)
        else:
            conditions.append(f"{key} = ?")
            values.append(value)

    query = f"DELETE FROM {table} WHERE {' AND '.join(conditions)}"

    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, values)
            return cursor.rowcount  # Возвращаем количество удаленных строк
    except Exception as e:
        handle_db_error(e)
        return 0

def input_add_record(table_name):
    # принимает от пользователя ввод новых данных в любую таблицу
    # проверяет каждую вводимую строку на корректность согласно описанию таблиц tables
    # добавляет введенные данные в бд, вызывая add_records
    # email и phone пока не проверяет
    print(f"Добавление новой записи в таблицу '{table_name}'")

    # Получаем структуру полей для указанной таблицы, исключая автоинкрементные поля (например, id)
    new_record = {field: None for field in tables[table_name] if "PRIMARY KEY" not in tables[table_name][field]["type"]}

    for field, properties in tables[table_name].items():
        # Пропускаем автоинкрементное поле
        if "PRIMARY KEY" in properties["type"]:
            continue

        field_type = properties["type"]
        allows_null = "DEFAULT NULL" in field_type  # Проверка на возможность значения NULL

        while True:
            value = input(f"{field.replace('_', ' ').capitalize()}: ").strip()

            # Если поле допускает NULL и ввод пустой, присваиваем None
            if allows_null and not value:
                new_record[field] = None
                break

            # Проверка для полей с форматом даты и времени
            if "format" in properties:
                date_format = "%Y-%m-%d %H:%M"  # Исправленный формат
                try:
                    value = datetime.strptime(value, date_format)
                    new_record[field] = value.strftime(date_format)
                    break
                except ValueError:
                    print(f"Ошибка: неверный формат для {field}. Ожидается {properties['format']}.")
                    continue

            # Проверка диапазонов для целых чисел
            elif field_type == "INTEGER":
                try:
                    value = int(value)
                    min_value = properties.get("min")
                    max_value = properties.get("max")
                    # Проверяем наличие ограничений
                    if min_value is not None and max_value is not None:
                        if min_value <= value <= max_value:
                            new_record[field] = value
                            break
                        else:
                            print(f"Ошибка: значение должно быть между {min_value} и {max_value}.")
                    else:
                        # Если ограничений нет, просто принимаем целое значение
                        new_record[field] = value
                        break
                except ValueError:
                    print(f"Ошибка: {field} должно быть целым числом.")

            # Проверка диапазонов для вещественных чисел
            elif field_type == "REAL":
                try:
                    value = float(value)
                    min_value = properties.get("min")
                    max_value = properties.get("max")
                    if min_value is not None and max_value is not None:
                        if min_value <= value <= max_value:
                            new_record[field] = value
                            break
                        else:
                            print(f"Ошибка: значение должно быть между {min_value} и {max_value}.")
                    else:
                        new_record[field] = value
                        break
                except ValueError:
                    print(f"Ошибка: {field} должно быть числом.")

            # Поля типа TEXT
            elif field_type == "TEXT":
                new_record[field] = value
                break

    # Добавляем запись в таблицу
    row_count = add_records(table_name, new_record)
    if row_count:
        print(f"Запись успешно добавлена в таблицу '{table_name}' ({row_count} запись(ей)).")
    else:
        print("Ошибка при добавлении записи.")

def input_update_record(table_name):
    # принимает от пользователя данные для изменения существующей записи в любой таблице
    # проверяет каждую введенную строку на корректность согласно описанию бд в tables
    # обновляет запись, вызывая update_records
    # Запрашиваем ID записи, которую необходимо обновить
    record_id = input(f"Введите ID записи, которую хотите обновить в таблице '{table_name}': ").strip()
    if not record_id.isdigit():
        print("Ошибка: ID должен быть целым числом.")
        return
    record_id = int(record_id)

    # Словарь для хранения обновлённых значений
    updated_record = {}

    # Проходим по полям таблицы
    for field, properties in tables[table_name].items():
        # Пропускаем автоинкрементное поле ID
        if "PRIMARY KEY" in properties["type"]:
            continue

        field_type = properties["type"]
        allows_null = "DEFAULT NULL" in field_type  # Поля, допускающие NULL

        # Запрашиваем новое значение для поля
        value = input(f"{field.replace('_', ' ').capitalize()} (оставьте пустым для сохранения текущего значения): ").strip()

        # Если пользователь оставил поле пустым, мы его пропускаем
        if not value:
            continue

        # Проверка для полей с форматом даты и времени
        if "format" in properties:
            date_format = "%Y-%m-%d %H:%M"  # Используем указанный формат
            try:
                value = datetime.strptime(value, date_format)
                updated_record[field] = value.strftime(date_format)
            except ValueError:
                print(f"Ошибка: неверный формат для {field}. Ожидается {properties['format']}.")
                continue

        # Проверка диапазонов для целых чисел
        elif field_type == "INTEGER":
            try:
                value = int(value)
                min_value = properties.get("min")
                max_value = properties.get("max")
                if min_value is not None and max_value is not None:
                    if min_value <= value <= max_value:
                        updated_record[field] = value
                    else:
                        print(f"Ошибка: значение должно быть между {min_value} и {max_value}.")
                        continue
                else:
                    updated_record[field] = value
            except ValueError:
                print(f"Ошибка: {field} должно быть целым числом.")
                continue

        # Проверка диапазонов для вещественных чисел
        elif field_type == "REAL":
            try:
                value = float(value)
                min_value = properties.get("min")
                max_value = properties.get("max")
                if min_value is not None and max_value is not None:
                    if min_value <= value <= max_value:
                        updated_record[field] = value
                    else:
                        print(f"Ошибка: значение должно быть между {min_value} и {max_value}.")
                        continue
                else:
                    updated_record[field] = value
            except ValueError:
                print(f"Ошибка: {field} должно быть числом.")
                continue

        # Поля типа TEXT
        elif field_type == "TEXT":
            updated_record[field] = value

    # Если есть изменения, обновляем запись, используя update_records
    if updated_record:
        criteria = {f"{table_name[:-1]}_id": record_id}  # Критерий для поиска записи по ID
        row_count = update_records(table_name, updated_record, criteria)
        
        if row_count:
            print(f"Запись с ID {record_id} успешно обновлена в таблице '{table_name}' ({row_count} запись(ей)).")
        else:
            print("Ошибка при обновлении записи.")
    else:
        print("Изменения не были внесены.")

def is_number(data, num_type, min_value=None, max_value=None):
    # проверяет строку или список строк на число заданного типа в заданном диапазоне
    # возвращает список в виде чисел, прошедших проверку
    if isinstance(data, str):
        data = [data]  # Преобразуем строку в список для унифицированной обработки

    result = []
    for item in data:
        try:
            # Приводим данные к указанному типу (int или float)
            number = num_type(item)
            
            # Проверяем диапазон значений, если он указан
            if min_value is not None and number < min_value:
                # print(f"Ошибка: значение {number} меньше минимально допустимого ({min_value}).")
                continue
            if max_value is not None and number > max_value:
                # print(f"Ошибка: значение {number} больше максимально допустимого ({max_value}).")
                continue

            # Если проверка прошла, добавляем число в результат
            result.append(number)
        
        except ValueError:
            # print(f"Ошибка: '{item}' не является допустимым числом типа {num_type.__name__}.")
            continue

    return result

def got_yes():
    # выводит сообщение на подтверждение удаления записи и возвращает 1, если нажата "д" или "Д"
    confirmation = input("Подтвердите удаление (д/н): ").strip().lower()
    return confirmation == 'д'
