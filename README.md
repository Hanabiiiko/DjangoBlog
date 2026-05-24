# Simple Django Blog

Учебный проект блога на Django с системой ролей пользователей.

## Стек

- Python 3.11+
- Django 5.2 LTS
- SQLite

## Установка и запуск

1. Клонировать репозиторий:
   git clone <url>
   cd <project-folder>

2. Создать и активировать виртуальное окружение:
   python -m venv venv
   source venv/bin/activate
   На Windows: venv\Scripts\activate

3. Установить зависимости:
   pip install -r requirements.txt

4. Создать файл .env в корне проекта:
   SECRET_KEY=your-secret-key-here
   DEBUG=True

5. Применить миграции:
   python manage.py migrate

6. Заполнить тестовыми данными:
   python manage.py seed

7. Запустить сервер:
   python manage.py runserver

8. Открыть в браузере: http://127.0.0.1:8000/

## Роли пользователей

| Роль   | Просмотр | Создание постов | Управление своими постами | Управление всем |
|--------|----------|-----------------|---------------------------|-----------------|
| User   | да       | нет             | нет                       | нет             |
| Poster | да       | да              | да                        | нет             |
| Admin  | да       | да              | да                        | да              |

## Тестовые аккаунты

| Логин       | Пароль    | Роль   |
|-------------|-----------|--------|
| admin       | admin123  | Admin  |
| poster_user | poster123 | Poster |
| reader_user | reader123 | User   |

## Django Admin

Доступен по адресу http://127.0.0.1:8000/admin/
Логин: admin / Пароль: admin123
```
