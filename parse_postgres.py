import psycopg2
from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

def find_book(name):
    conn_postgres = psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    cur_postgres = conn_postgres.cursor()
    cur_postgres.execute("SELECT title, translator, author, lang, rowid FROM lib " +
                         "WHERE textsearch_index_col @@ plainto_tsquery('{}') ORDER BY ".format(name) +
                         "ts_rank(textsearch_index_col, plainto_tsquery('{}')) DESC".format(name))

    books_list = cur_postgres.fetchall()

    cur_postgres.close()
    conn_postgres.close()

    books = []

    for i in books_list:
        book_name = i[0]
        if len(i[1]) != 0:
            book_name += ' (пер. {})'.format(i[1])

        author = i[2]
        if len(i[3]) != 0:
            author += ' ({})'.format(i[3])

        href = i[4]
        books.append((book_name, author, href))

    return books


# print(find_book(input()))