import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor


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
        insert = 'INSERT INTO urls (name, created_at) VALUES (%s, %s);'
        curs.execute(insert, (address['name'], address['created_at']))
        conn.commit()
    conn.close()


def get_all_urls():
    conn = psycopg2.connect(DATABASE_URL)

    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        select = '''SELECT DISTINCT ON (urls.id)
                        urls.id AS id,
                        urls.name AS name,
                        url_checks.created_at AS last_check,
                        url_checks.status_code AS status_code
                    FROM urls
                    LEFT JOIN url_checks ON urls.id = url_checks.url_id
                    AND url_checks.id = (
                        SELECT MAX(id)
                        FROM url_checks
                        WHERE url_id = urls.id
                    )
                    ORDER BY urls.id DESC;'''
        curs.execute(select)
        urls = curs.fetchall()
    conn.close()

    return urls


def add_check_to_db(data):
    conn = psycopg2.connect(DATABASE_URL)

    with conn.cursor() as curs:
        insert = 'INSERT INTO url_checks (url_id, created_at) VALUES (%s, %s);'
        curs.execute(insert, (data['url_id'], data['created_at']))
        conn.commit()
    conn.close()


def get_checks_by_id_url(url_id):
    conn = psycopg2.connect(DATABASE_URL)

    with conn.cursor() as curs:
        select = 'SELECT * FROM url_checks WHERE url_id=(%s) ORDER BY id DESC;'
        curs.execute(select, [url_id])
        url = curs.fetchall()
    conn.close()

    return url
