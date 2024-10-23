# Event Concentrator

## Структура таблиц базы данных

### Таблица "events" (мероприятия)

Основная таблица, содержащая сведения о мероприятиях.

  **Поле**               **Комментарий****type*
event_id               Идентификатор   int 
event_title            Заголово  strк
event_synopsis         Описание   str
event_docs             Доп. материалы: пресс-релизы, афиша, логотипы    files...
event_start_dt         Дата время начала    datetime.datetime
event_final_dt         Дата время окончания     datetime.datetime
event_location         Место проведения   str
event_comment          Любой дополнительный текст str
event_age_category      возрастная категория     str
event_budget    Расходы организатора    float

### Таблица "visitors" (посетители мероприятий)

Содержит доступную (не всегда полную) информацию о посетителях мероприятий.

  **Поле**               **Комментарий***type**
visitor_id             Идентификато  intр
visitor_full_name      ФИ   strО
visitor_email          Электронный адрес  str
visitor_phone          Номер телефона    str
visitor_age_category    возрастная категория  str
visitor_gender   Пол гостя     str

### Таблица employees (сотрудники)

Содержит сведения о сотрудниках, организующих и координирующих мероприятия, и сведения о допуске к инструментам приложения "Event Concentrator".

  **Поле**               **Комментарий **type**
employee_id            Идентификатор   int
employee_full_name     ФИО   str
employee_position      Должность, роль в организации   str
employee_login         Имя пользователя в системе  str
employee_passwd        Хеш пароля   int
employee_access_level  Уровень доступа к информации   str
employee_comment       Любой дополнительный текс   strт

### Таблица "tickets" (билеты)

  **Поле**               **Комментарий****type**
ticket_id              Идентификатор     int
ticket_event_id   Идентификатор мероприятия   int
ticket_type            Тип, класс билета люкс/эконом    str
ticket_guest_id     Идентификатор гостя, по умолчанию None     int
ticket_price           Цена    float
ticket_status          Свободен, зарезервирован, выкуплен     str

### Доделать

* Таблицы связей:
1. events -> visitors,
2. events -> tickets,
3. events -> employees,
4. tickets -> visitors.

### На перспективу

* Таблица артистов.
* Blacklist посетителей.

