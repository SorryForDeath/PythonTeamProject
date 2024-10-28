import sqlite3
from datetime import datetime, timedelta
import re

# имя базы данных
db_name = 'event_database.db'
# переменная для соединения
connection = None

# регулярные выражения для мейла и телефона
email_pattern = r"\b[a-zA-Z0-9#\$%&'*+/=?^_`{|}~]+(?:\.[a-zA-Z0-9#\$%&'*+/=?^_`{|}~]+)*@(?:(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,}\b"
phone_pattern = r"^(?:\+?([78])[-\s]?)?(?:\(?\d{3}\)?[-\s]?)\d{3}[-\s]?\d{2}[-\s]?\d{2}$"

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
                continue
            if max_value is not None and number > max_value:
                continue

            # Если проверка прошла, добавляем число в результат
            result.append(number)
        
        except ValueError:
            continue

    return result


# Подсказки пользователю для ввода полей таблиц
field_prompts = {
    "events": {
        "event_title": "Название события",
        "event_synopsis": "Описание события",
        "event_start_dt": "Дата начала события (формат: ГГГГ-ММ-ДД ЧЧ:ММ)",
        "event_final_dt": "Дата окончания события (формат: ГГГГ-ММ-ДД ЧЧ:ММ)",
        "event_location": "Место проведения",
        "event_age_restriction": "Возрастное ограничение (целое число от 0 до 21)",
        "event_budget": "Бюджет события (вещественное число от 0 до 1 000 000)",
        "event_comment": "Комментарий"
    },
    "visitors": {
        "visitor_full_name": "ФИО посетителя",
        "visitor_email": "Email посетителя",
        "visitor_phone": "Телефон посетителя"
    },
    "employees": {
        "employee_full_name": "ФИО сотрудника",
        "employee_position": "Должность сотрудника",
        "employee_comment": "Комментарий о сотруднике"
    }
}

# Вспомогательные функции для проверки данных

def validate_number(value, num_type, min_value=None, max_value=None):
    try:
        num = num_type(value)
        if (min_value is not None and num < min_value) or (max_value is not None and num > max_value):
            return None
        return num
    except ValueError:
        return None

def validate_date_time(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M")
    except ValueError:
        return None

def validate_required(value):
    return bool(value.strip())

def validate_event_dates(start_date, final_date=None):
    now = datetime.now()
    max_date = now + timedelta(days=2*365)
    if start_date < now or start_date > max_date:
        print("Ошибка: дата начала события должна быть не раньше текущей и не больше чем через 2 года.")
        return False
    if final_date:
        if final_date < start_date:
            print("Ошибка: дата окончания события не может быть раньше даты начала.")
            return False
        if final_date > start_date + timedelta(days=1):
            print("Ошибка: дата окончания события не может быть позже чем через 24 часа от даты начала.")
            return False
    return True

def format_phone(phone):
    """Форматирование телефона в формат +7 (XXX) XXX-XX-XX."""
    digits = re.sub(r'\D', '', phone)
    if len(digits) == 10:
        return f"+7 ({digits[:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:]}"
    elif len(digits) == 11 and digits[0] == '8':
        return f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:]}"
    return phone  # Возвращаем исходный номер, если не соответствует формату

# Универсальная функция для ручного добавления одной записи в любую таблицу
def add_new_record(table_name):
    record_data = {}
    fields = tables[table_name]
    prompts = field_prompts[table_name]
    start_date = None

    for field, prompt in prompts.items():
        field_type = fields[field]["type"]
        is_required = "PRIMARY KEY" not in field_type and field not in ["event_synopsis", "event_comment", "visitor_email", "visitor_phone", "employee_comment"]

        while True:
            user_input = input(f"{prompt}{' (обязательно)' if is_required else ''}: ").strip()

            # Пустые значения для необязательных полей
            if not user_input and not is_required:
                record_data[field] = ""
                break

            # Проверка обязательного поля
            if is_required and not validate_required(user_input):
                print("Ошибка: это поле обязательно для заполнения.")
                continue

            # Проверка на email
            if field == "visitor_email":
                if not re.match(email_pattern, user_input):
                    print("Ошибка: введён некорректный email.")
                    continue
                record_data[field] = user_input
                break

            # Проверка и форматирование телефона
            elif field == "visitor_phone":
                if not re.match(phone_pattern, user_input):
                    print("Ошибка: введён некорректный телефон.")
                    continue
                record_data[field] = format_phone(user_input)  # Приводим телефон к нужному формату
                break

            # Проверка числовых полей с диапазоном
            if field_type == "INTEGER" or field_type == "REAL":
                num_type = int if field_type == "INTEGER" else float
                result = validate_number(user_input, num_type, fields[field].get("min"), fields[field].get("max"))
                if result is not None:
                    record_data[field] = result
                    break
                print("Ошибка: неверный формат числа или выход за диапазон.")

            # Проверка дат для событий
            elif field in ["event_start_dt", "event_final_dt"]:
                date_value = validate_date_time(user_input)
                if date_value:
                    if field == "event_start_dt" and not validate_event_dates(date_value):
                        continue
                    elif field == "event_final_dt" and not validate_event_dates(start_date, date_value):
                        continue
                    record_data[field] = date_value.strftime("%Y-%m-%d %H:%M")
                    if field == "event_start_dt":
                        start_date = date_value
                    break
                print("Ошибка: неверный формат даты. Используйте формат ГГГГ-ММ-ДД ЧЧ:ММ.")

            # Текстовые поля
            else:
                record_data[field] = user_input
                break

    # Добавление записи в БД
    if add_records(table_name, record_data):
        print(f"Запись в таблицу {table_name} успешно добавлена.")
    else:
        print("Ошибка: не удалось добавить запись.")

def build_dict_from_tuple(table_name, record_tuple):
    # Проверяем, есть ли в структуре таблиц описание полей для указанной таблицы
    if table_name not in tables:
        raise ValueError(f"Таблица '{table_name}' не найдена в структуре таблиц.")
    
    # Получаем список полей для указанной таблицы
    field_names = list(tables[table_name].keys())
    
    # Проверка, что длины кортежа и полей совпадают
    if len(record_tuple) != len(field_names):
        raise ValueError("Количество значений в кортеже не совпадает с количеством полей таблицы.")
    
    # Создаём словарь, сопоставляя каждое поле с элементом кортежа
    record_dict = {field: value for field, value in zip(field_names, record_tuple)}
    
    return record_dict

# универсальная функция для ручного обновления данных в любой таблице
def update_one_record(table_name):
    # 1. Запрос id записи для обновления
    record_id = input("Введите id записи для обновления: ").strip()

    # 2. Проверка валидности id
    record_id = is_number(record_id, int, 1)
    if not record_id:
        print("Ошибка: id должен быть положительным числом.")
        return

    record_id = record_id[0]

    # 3. Проверка существования записи с данным id
    id_field = table_name[:-1] + '_id'
    existing_record = get_records(table_name, {id_field: record_id})
    if not existing_record:
        print("Ошибка: запись с указанным id не найдена.")
        return
    existing_record = build_dict_from_tuple(table_name, existing_record[0])
    print(f"Обновление данных для таблицы {table_name.capitalize()}")
    print("Введите новые данные или нажмите Enter для сохранения текущих значений.")

    # 4. Подготовка полей и запросов
    fields = tables[table_name]
    prompts = field_prompts[table_name]
    updated_data = {}
    start_date = None  # Для проверки дат событий

    # 5. Перебор полей для обновления
    for field, prompt in prompts.items():
        field_type = fields[field]["type"]
        current_value = existing_record[field]
        print(f"{prompt} (текущее значение: {current_value})")

        while True:  # Начинаем цикл для ввода данных, продолжаем, пока не будет введено корректное значение.
            # Ввод нового значения
            user_input = input("Новое значение: ").strip()

            # Если поле не изменяется, переходим к следующему полю
            if not user_input:
                break

            # Обработка каждого типа данных

            # Проверка числовых полей
            if field_type == "INTEGER" or field_type == "REAL":
                num_type = int if field_type == "INTEGER" else float
                result = validate_number(user_input, num_type, fields[field].get("min"), fields[field].get("max"))
                if result is not None:
                    # Только добавляем в `updated_data`, если значение изменилось
                    if result != current_value:
                        updated_data[field] = result
                    break
                else:
                    print("Ошибка: неверный формат числа или выход за диапазон.")
                    continue

            # Проверка email
            elif field == "visitor_email":
                if re.match(email_pattern, user_input):
                    if user_input != current_value:
                        updated_data[field] = user_input
                    break
                else:
                    print("Ошибка: введён некорректный email.")
                    continue

            # Проверка и форматирование телефона
            elif field == "visitor_phone":
                if re.match(phone_pattern, user_input):
                    formatted_phone = format_phone(user_input)
                    if formatted_phone != current_value:
                        updated_data[field] = formatted_phone
                    break
                else:
                    print("Ошибка: введён некорректный телефон.")
                    continue

            # Проверка дат для событий
            elif field in ["event_start_dt", "event_final_dt"]:
                date_value = validate_date_time(user_input)
                if date_value:
                    if field == "event_start_dt":
                        if not validate_event_dates(date_value):
                            continue
                        start_date = date_value
                    elif field == "event_final_dt":
                        if not validate_event_dates(start_date, date_value):
                            continue
                    # Только добавляем в `updated_data`, если значение изменилось
                    formatted_date = date_value.strftime("%Y-%m-%d %H:%M")
                    if formatted_date != current_value:
                        updated_data[field] = formatted_date
                    break
                else:
                    print("Ошибка: неверный формат даты. Используйте формат ГГГГ-ММ-ДД ЧЧ:ММ.")
                    continue

            # Текстовые поля
            else:
                if user_input != current_value:
                    updated_data[field] = user_input
                break

    # 6. Обновление записи, если есть изменения
    if updated_data:
        if update_records(table_name, updated_data, {id_field: record_id}):
            print(f"Запись с id {record_id} успешно обновлена.")
        else:
            print("Ошибка: не удалось обновить запись.")
    else:
        print("Изменений не было внесено.")
