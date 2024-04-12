import psycopg2
from psycopg2.extras import RealDictCursor
from page_analyzer.constants import DATABASE_URL


def create_db_query(query, data=None, commit=False, fetchall=False):
    '''
    Create and execute an SQL query to the database.

    :param query: The SQL query to be executed.
    :type query: str
    :param data: Data required to create a request
    :type data: typle
    :param commit:If True, commit the changes to the database.
    :type commit: bool
    :param fetchall:If True, fetch all rows; if False, fetch one row.
    :type fetchall: bool
    :return: The result of the query execution.
    '''
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
    '''
    Get data about a url by its name

    :param name: The name of the URL.
    :type: str
    :return: URL data
    '''
    select = 'SELECT * FROM urls WHERE name=(%s)'
    return create_db_query(select, [name])


def get_url_by_id(id):
    '''
    Get data about a url by its id

    :param name: The id of the URL.
    :type: int
    :return: URL data
    '''
    select = 'SELECT * FROM urls WHERE id=(%s);'
    return create_db_query(select, [id])


def get_all_urls():
    '''
    Get data about all URLs with information about the last check.

    :return: URL data
    '''
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


def get_checks_by_id_url(url_id):
    '''
    Get data about all checks for a specific URL by its id.

    :param name: The id of the URL.
    :type: int
    :return: Check data
    '''
    select = 'SELECT * FROM url_checks WHERE url_id=(%s) ORDER BY id DESC;'
    return create_db_query(select, [url_id], fetchall=True)


def add_url_to_db(address):
    '''
    Add data about the new site to the database

    :param name: A dictionary containing the site name and
    the date the entry was created
    :type: dict
    '''
    insert = 'INSERT INTO urls (name, created_at) VALUES (%s, %s);'
    data = (address['name'], address['created_at'])
    return create_db_query(insert, data, commit=True)


def add_check_to_db(data):
    '''
    Add data about a new site check to the database

    :param name: A dictionary containing site verification data.
    :type: dict
    '''
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
