# readporn_bot
Telegram-бот для подбора электронных книжек в формате FB2

Оригинальный инстанс бота развернут на Heroku. Бот написан на Python с помощью библиотеки [`python-telegram-bot`](https://python-telegram-bot.readthedocs.io/en/stable/index.html).
Удаленное хранилище книг расположено по адресу [`https://zip.irt.host`](https://zip.irt.host). В реализации бота использована БД `PostgreSQL`.

# Настройка
Для настройки бота редактируйте файл [`config.py`](./config.py). Поля `DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT` используются для
конфигурации имени БД, имени юзера, пароля БД, хоста БД и порта. Поле `TOKEN` используется для конфигурации токена бота.