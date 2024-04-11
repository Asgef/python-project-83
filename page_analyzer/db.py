import psycopg2
from psycopg2.extras import RealDictCursor
from page_analyzer.constants import DATABASE_URL


def create_db_query(query, data=None, commit=False, fetchall=False):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(query, data)

            if commit:
                conn.commit()
                return

            elif fetchall:
                result = curs.fetchall()

            else:
                result = curs.fetchone()

        return result


def get_url_by_name(name):
    select = 'SELECT * FROM urls WHERE name=(%s)'
    return create_db_query(select, [name])


def get_url_by_id(id):
    select = 'SELECT * FROM urls WHERE id=(%s);'
    return create_db_query(select, [id])


def add_url_to_db(address):
    insert = 'INSERT INTO urls (name, created_at) VALUES (%s, %s);'
    data = (address['name'], address['created_at'])
    return create_db_query(insert, data, commit=True)


def get_all_urls():
    select = '''SELECT DISTINCT ON (urls.id)
                        urls.id AS id,
                        urls.name AS name,
                        url_checks.created_at AS last_check,
                        url_checks.status_code AS status_code
                FROM urls
                LEFT JOIN url_checks ON
                    urls.id = url_checks.url_id
                AND url_checks.id = (
                    SELECT MAX(id)
                    FROM url_checks
                    WHERE url_id = urls.id
                )
                ORDER BY urls.id DESC;'''
    return create_db_query(select, fetchall=True)


def add_check_to_db(data):
    insert = '''INSERT INTO url_checks (
                    url_id,
                    status_code,
                    h1,
                    title,
                    description,
                    created_at)
                VALUES
                    (%s, %s, %s, %s, %s, %s);'''

    data_check = (
        data['url_id'],
        data['status_code'],
        data['h1'],
        data['title'],
        data['description'],
        data['created_at']
    )
    return create_db_query(insert, data_check, commit=True)


def get_checks_by_id_url(url_id):
    select = 'SELECT * FROM url_checks WHERE url_id=(%s) ORDER BY id DESC;'
    return create_db_query(select, [url_id], fetchall=True)
