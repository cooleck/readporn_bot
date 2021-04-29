import os

TOKEN = 'TELEGRAM_BOT_TOKEN'

START_MESSAGE = 'Hello, {}!\nJust send me the name of the book and/or author and I will find the e-book you want!'

START_MESSAGE_RUS = 'Привет, {}!\nПросто отправь мне имя автора и/или название книги, и я найду тебе эту книгу!'

PORT = int(os.environ.get('PORT', '8443'))

HOME_LIB = 'https://zip.irt.host'

DB_NAME = 'databasename'
DB_USER = 'username'
DB_PASSWORD = 'password'
DB_HOST = 'hostname'
DB_PORT = 'port'
