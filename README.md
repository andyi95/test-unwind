# test-unwind
Тестовое задание для Каналсервис и Unwind Digital

## Настройка окружения и запуск

Склонируйте репозиторий в рабочий каталог
`git clone git@github.com:andyi95/test-unwind.git`
Скопируйте файл .env.dist в .env. Для локального запуска используйте конфигурацию docker-compose.override.yaml, для этого достаточно оставить параметр `COMPOSE_FILE` пустым. Остальные параметры можно оставить или изменить на своё усмотрение.
Сборка и запуск проекта `docker-compose up -d --build`
Swagger API документация будет доступна по адресу `localhost:8000/api/doc/`
