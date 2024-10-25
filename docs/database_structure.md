# Event Concentrator

## Структура таблиц базы данных

### Таблица "events" (мероприятия)

Основная таблица, содержащая сведения о мероприятиях.

  **Поле**               **Комментарий**              **Тип*
event_id               Идентификатор                INTEGER PRIMARY KEY
event_title            Заголовок                    TEXT
event_synopsis         Описание                     TEXT
event_start_dt         Дата время начала            TEXT
event_final_dt         Дата время окончания         TEXT
event_location         Место проведения             TEXT
event_age_restriction  возрастная категория         INTEGER
event_budget           Расходы организатора         REAL
event_comment          Любой дополнительный текст   TEXT

### Таблица "visitors" (посетители мероприятий)

Содержит доступную (не всегда полную) информацию о посетителях мероприятий.

  **Поле**               **Комментарий*               **Тип**
visitor_id             Идентификатор                INTEGER PRIMARY KEY
visitor_full_name      ФИО                          TEXT
visitor_email          Электронный адрес            TEXT
visitor_phone          Номер телефона               TEXT
visitor_age_category   Возрастная категория         INTEGER
visitor_gender         Пол гостя                    INTEGER

### Таблица employees (сотрудники)

Содержит сведения о сотрудниках, организующих и координирующих мероприятия, и сведения о допуске к инструментам приложения "Event Concentrator".

  **Поле**               **Комментарий                **Тип**
employee_id            Идентификатор                INTEGER PRIMARY KEY
employee_full_name     ФИО                          TEXT
employee_position      Должность, роль              TEXT
employee_login         Имя пользователя в системе   TEXT
employee_passwd        Хеш пароля                   TEXT
employee_access_level  Уровень доступа              INTEGER
employee_comment       Любой дополнительный текст   TEXT

### Таблица "tickets" (билеты)

  **Поле**               **Комментарий**              **Тип**
ticket_id              Идентификатор                INTEGER PRIMARY KEY
ticket_event_id        Идентификатор мероприятия    INTEGER
                                                    FOREIGN KEY (ticket_event_id) REFERENCES events(event_id)
ticket_visitor_id      Идентификатор гостя          INTEGER DEFAULT NULL
                                                    FOREIGN KEY (ticket_visitor_id) REFERENCES Visitors(visitor_id)
ticket_price           Цена                         REAL

### Связывающая таблица events_employees

  **Поле**               **Комментарий**              **Тип**
event_id               Идентификатор мероприятия    INTEGER
                                                    FOREIGN KEY (event_id) REFERENCES events(event_id)
employee_id      Идентификатор сотрудника           INTEGER
                                                    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)

### В развитие

* Таблица артистов.
* Blacklist посетителей.
* Поле event_docs - Доп. материалы: пресс-релизы, афиша, логотипы...
* Возможность резервирования билета без выкупа.
* Разбивку билетов на категории.

