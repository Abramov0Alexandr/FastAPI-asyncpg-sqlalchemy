# FastAPI-asyncpg-sqlalchemy
### ❗ Проект находится на стадии написания и не отображает итогового результата❗

## О проекте
Проект представляет собой пример интеграции и взаимодействия Pydantic 2.0 в связке с SQLAlchemy ORM и PostgreSQL,
подключенной через асинхронную библиотеку взаимодействия с базами данных asyncpg.

Основные цели, которые ставились перед проектом:
- максимальная скорость работы
- использование асинхронных операций
- организация структуры проекта согласно лучшим практикам
- аутентификацию пользователей (JWT + cookie)
- написание асинхронных тестов (httpx + pytest-asyncio)

## Стек технологий:
- python
- fastapi
- sqlalchemy
- asyncpg
- alembic
- pydantic
- ipython
- passlib
- python-slugify
- httpx
- pytest-asyncio

## Установка
Прежде чем начать использовать Marketplace API, убедитесь, что у вас установлен
интерпретатор Python c версией не ниже 3.9:

Клонируйте репозиторий с помощью следующей команды:
   ```bash
   git git@github.com:Abramov0Alexandr/FastAPI-asyncpg-sqlalchemy.git
   ```

Перейдите в директорию проекта:
   ```bash
   cd FastAPI-asyncpg-sqlalchemy
   ```

Активируйте виртуальное окружение Poetry и установите зависимости:

   ```bash
   poetry init
   poetry shell
   poetry install
   ```

Создайте .env файл в основной директории проекта, который будет содержать основные настройки
для взаимодействия с базой данных.

   ```bash
   touch .env
   ```

Структура проекта:

<pre>
<code>
.
|-- app
|-- migrations
|-- .env  ## NEW FILE!
|-- .env.sample
|-- .gitignore
|-- alembic.ini
|-- LICENSE
|-- poetry.lock
|-- pyproject.toml
|-- README.md
</code>
</pre>

Создайте базу данных, которая будет использоваться в проекте:

   ```bash
   psql -U <database username>
   create database <your database title>;
   ```

Заполните .env файл. Необходимые переменные можно увидеть в .env.sample:
   ```bash
   vim .env
   ```

<pre>
<code>
DB_USER="your database username"
DB_PASSWORD="your database password"
DB_HOST="default is localhost"
DB_PORT="default is 5432"
DB_NAME="your database title"
</code>
</pre>

Примените миграции для базы данных:

   ```bash
   alembic upgrade head
   ```

Запустите сервер:
   ```bash
   uvicorn app.main:app
   ```

## Тестирование
Для запуска тестов воспользуйтесь следующей командой:
   ```bash
   pytest -vv app/tests/
   ```

## Документация
Для тестирования API, вы можете использовать автогенерируемую документацию, которая отображает весь функционал и
содержит все зарегистрированные в приложении маршруты.
Документацию к API вы можете найти перейдя по ссылке:<br>
http://127.0.0.1:8000/docs/


## Лицензия
FastAPI-asyncpg-sqlalchemy распространяется по [MIT License](https://opensource.org/licenses/MIT).

## Контакты

Спасибо за использование FastAPI-asyncpg-sqlalchemy! Если у вас есть какие-либо вопросы или предложения, не стесняйтесь обращаться к нам.

Автор: [Alexandr Abramov <https://github.com/Abramov0Alexandr>]

Email: [alexandr.abramovv@gmail.com <https://github.com/Abramov0Alexandr>]

GitHub: [https://github.com/Abramov0Alexandr]
