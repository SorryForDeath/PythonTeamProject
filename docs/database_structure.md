# Event Concentrator

## Структура таблиц базы данных

### Таблица "events" (мероприятия)

Основная таблица, содержащая сведения о мероприятиях.

  **Поле**               **Комментарий**
event_id               Идентификатор
event_title            Заголовок
event_synopsis         Описание
event_docs             Доп. материалы: пресс-релизы, афиша, логотипы...
event_start_dt         Дата время начала
event_final_dt         Дата время окончания
event_location         Место проведения
event_comment          Любой дополнительный текст

### Таблица "visitors" (посетители мероприятий)

Содержит доступную (не всегда полную) информацию о посетителях мероприятий.

  **Поле**               **Комментарий**
visitor_id             Идентификатор
visitor_full_name      ФИО
visitor_email          Электронный адрес
visitor_phone          Номер телефона

### Таблица employees (сотрудники)

Содержит сведения о сотрудниках, организующих и координирующих мероприятия, и сведения о допуске к инструментам приложения "Event Concentrator".

  **Поле**               **Комментарий**
employee_id            Идентификатор
employee_full_name     ФИО
employee_position      Должность, роль в организации
employee_login         Имя пользователя в системе
employee_passwd        Хеш пароля
employee_access_level  Уровень доступа к информации
employee_comment       Любой дополнительный текст

### Таблица "tickets" (билеты)

  **Поле**               **Комментарий**
ticket_id              Идентификатор
ticket_type            Тип
ticket_price           Цена
ticket_status          Свободен, зарезервирован, выкуплен

### Доделать

* Таблицы связей:
1. events -> visitors,
2. events -> tickets,
3. events -> employees,
4. tickets -> visitors.

### На перспективу

* Таблица артистов.
* Blacklist посетителей.

