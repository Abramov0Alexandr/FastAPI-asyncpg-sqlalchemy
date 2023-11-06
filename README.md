# FastAPI-asyncpg-sqlalchemy
### ❗ Проект находится на стадии написания и не отображает итогового результата❗ 

## О проекте
Проект представляет собой пример интеграции и взаимодействия Pydantic 2.0 в связке с SQLAlchemy ORM и PostgreSQL, 
подключенной через асинхронную библиотеку взаимодействия с базами данных asyncpg.

Основные цели, которые ставилась перед проектом:
- максимальная скорость работы
- использование асинхронных операций
- организация структуры проекта согласно лучшим практикам
- аутентификацию пользователей, основанную на связке JWT + cookie

## Стек технологий:
- python
- fastapi
- sqlalchemy
- asyncpg
- alembic
- pydantic
- ipython
- passlib

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

Примените миграции для базы данных:

   ```bash
   alembic revision upgrade head
   ```

Запустите сервер:
   ```bash
   uvicorn app.main:app
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