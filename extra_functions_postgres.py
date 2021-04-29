import requests
from config import TOKEN, HOME_LIB, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
import psycopg2
import zlib

base = 'http://lib.it.cx'

url = 'https://api.telegram.org/bot' + TOKEN + '/sendDocument?chat_id={}'

def get_book_range(rowid):
    conn_postgres = psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    cur_postgres = conn_postgres.cursor()

    cur_postgres.execute("SELECT zip, \"offset\", compressed from zip WHERE rowid={}".format(str(rowid)))

    book_range = cur_postgres.fetchone()
    cur_postgres.close()
    conn_postgres.close()

    return book_range


def get_zip(rowid):
    zip_name, offset, compressed = map(str, get_book_range(rowid))
    compressed = str(int(offset) + int(compressed))

    headers = {
        "Range": 'bytes=' + offset + '-' + compressed
    }

    return requests.get(HOME_LIB + '/' + zip_name, headers=headers, auth=('lib', 'PsMx7dVPEXmiUkMD'))

def decompress_file(file: requests.Response):
    return zlib.decompressobj(-zlib.MAX_WBITS).decompress(file.content)


def send_file(rowid, id, name):

    global url


    files = {'document': (name + '.fb2', decompress_file(get_zip(rowid)))}

    response = requests.post(url.format(id), files=files)

    print(response.status_code)


# from parse_postgres import find_book
#
# with open('books/my_book_1.fb2', 'wb') as file:
#     file.write(decompress_file(get_zip(find_book(input())[0][2])))