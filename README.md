Инструкции по установке и запуску проекта
Локальная установка (без Docker)
Клонировать репозиторий: git clone https://github.com/MyachinRoma/DRF-Prj.git
Перейти в папку проекта: DRF-Prj
Установить зависимости: из requirements.txt
Создайте файл .env в корневой папке проекта и заполните его по шаблону .env.sample переменными:
SECRET_KEY: секретный ключ проекта (например, случайная строка из 50 символов)
NAME: имя базы данных
DBUSER: имя пользователя базы данных
PASSWORD: пароль пользователя базы данных
HOST: адрес хоста базы данных (например, localhost)
PORT: порт базы данных (например, 5432)
Создать базу данных: python manage.py migrate
Запустить сервер: python manage.py runserver
Запуск через Docker Compose
Клонировать репозиторий: git clone https://github.com/MyachinRoma/DRF-Prj.git
Перейти в папку проекта: DRF-Prj
Создать файл .env на основе .env.sample
Запустить проект: docker-compose up -d --build
Проект будет доступен по адресу: http://localhost:8000
Проверка работоспособности сервисов
Django-приложение (web):

Откройте в браузере: http://localhost:8000
Проверка логов: docker-compose logs web
PostgreSQL (db):

Проверить подключение: docker-compose exec db psql -U postgres -d drf
Проверка логов: docker-compose logs db
Redis:

Проверить работу: docker-compose exec redis redis-cli ping (должен ответить "PONG")
Проверка логов: docker-compose logs redis
Celery (worker):

Проверка логов: docker-compose logs Celery
Celery Beat (scheduler):

Проверка логов: docker-compose logs celery_beat
Остановка проекта
Для остановки всех сервисов выполните: docker-compose down

Для полной очистки (с удалением volumes): docker-compose down -v
