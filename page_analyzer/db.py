import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL)


def get_url_by_name(name):

    with conn.cursor() as curs:
        select = 'SELECT * FROM URLS WHERE name=(%s)'
        curs.execute(select, [name])
        url = curs.fetchone()
    conn.close()

    return url
