# API backend : Информация об организациях, видах деятельностях, лоцирования, телефонных номеров.

### Запуск: 
1. Заполняем все необходимые поля в `.env.template`
2. Переименовываем в `.env`
3. Поднимаем локально базу данных:
```bash
docker compose -f docker-compose.yaml up db -d
```
4. Устанавливаем локально зависимости.
```shell
poetry shell
```
```shell
poetry install
```
5. Генерируем тестовые данные для БД.
```bash
poetry run coverage run -m pytest -v -s && coverage report --show-missing
```

6. Запускаем Docker compose:
```shell
docker compose up -d
```