import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_url_by_name(name):
    conn = psycopg2.connect(DATABASE_URL)

    with conn.cursor() as curs:
        select = 'SELECT * FROM urls WHERE name=(%s)'
        curs.execute(select, [name])
        url = curs.fetchone()
    conn.close()

    return url


def get_url_by_id(id):
    conn = psycopg2.connect(DATABASE_URL)

    with conn.cursor() as curs:
        select = 'SELECT * FROM urls WHERE id=(%s);'
        curs.execute(select, [id])
        url = curs.fetchone()
    conn.close()

    return url


def add_url_to_db(address):
    conn = psycopg2.connect(DATABASE_URL)

    with conn.cursor() as curs:
        insert = 'INSERT INTO urls (name) VALUES (%s);'
        curs.execute(insert, [address])
        conn.commit()
    conn.close()


def get_all_urls():
    conn = psycopg2.connect(DATABASE_URL)

    with conn.cursor() as curs:
        select = '''SELECT id, name
                    FROM urls
                    ORDER BY id DESC;'''
        curs.execute(select)
        urls = curs.fetchall()
    conn.close()

    return urls
