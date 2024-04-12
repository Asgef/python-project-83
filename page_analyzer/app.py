from flask import (
    Flask,
    render_template,
    url_for,
    request,
    flash,
    get_flashed_messages,
    redirect,
    abort
)
from page_analyzer.db import (
    add_url_to_db, get_url_by_name,
    get_url_by_id, get_all_urls,
    add_check_to_db, get_checks_by_id_url
)
from page_analyzer.constants import (
    ERROR_INVALID_URL, ERROR_URL_EXISTS, ERROR_URL_TOO_LONG
)
from page_analyzer.validator import validate
from page_analyzer.check_url import get_check_url
from datetime import datetime
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    '''
    Render the main page

    :return: Renders the HTML template for index.html.
    '''
    return render_template('index.html')


@app.post('/urls')
def post_urls():
    '''
    Add a new URL. Check if it is in stock. Validate the URL.
    Add it to your database if this URL doesn't already exist.
    Raise an error if it occurs.

    :return: Redirect to this URL's page if it was added to the bd
    or already exists. Render index page with flash error message
    '''
    url = request.form.get('url')
    validated = validate(url)

    error = validated['error']
    url = validated['url']

    if error == ERROR_URL_EXISTS:
        id = get_url_by_name['id']
        flash('Страница уже существует', 'alert-info')

        return redirect(url_for('show_urls', id=id))

    elif error == ERROR_URL_TOO_LONG:

        flash('URL превышает 255 символов', 'alert-danger')
        messages = get_flashed_messages(with_categories=True)

        return render_template(
            'index.html',
            messages=messages,
            url=url
        ), 422

    elif error == ERROR_INVALID_URL:

        flash('Некорректный URL', 'alert-danger')
        messages = get_flashed_messages(with_categories=True)

        return render_template(
            'index.html',
            messages=messages,
            url=url
        ), 422

    address = {
        'name': url,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    add_url_to_db(address)
    id = get_url_by_name(url)['id']

    flash('Страница успешно добавлена', 'alert-success')
    return redirect(url_for('show_urls', id=id))


@app.get('/urls')
def get_list_urls():
    '''
    Render all previously added URLs and their last check dates, if any.

    :return: Render the HTML template for urls.html.
    '''
    urls = get_all_urls()

    return render_template(
        'urls.html',
        urls=urls
    )


@app.route('/urls/<int:id>')
def show_urls(id):
    '''
    Render information about a specific URL by its id in the db.
    Show information about checks and flash message if available.
    If there is no record with a specific id in the db,
    an 'HTTPException' exception is thrown.

    :param id: URL id in db.
    :return: Render the HTML template for show.html or
    raise an exception 'HTTPException'
    '''
    url = get_url_by_id(id)

    if not url:
        abort(404)

    else:
        checks = get_checks_by_id_url(id)
        messages = get_flashed_messages(with_categories=True)

        return render_template(
            'show.html',
            url=url,
            checks=checks,
            messages=messages
        )


@app.post('/urls/<int:id>/checks')
def check_url(id):
    '''
    Check a specific URL by its id in the db.
    Add verification data to the db or throw an exception.
    Create a flash message about the verification status.

    :param id: URL id in db.
    :return: Redirect to a page with a specific URL with updated data or
    an error message.
    '''
    url = get_url_by_id(id)['name']

    try:
        check = get_check_url(url)
        check['url_id'] = id
        check['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        add_check_to_db(check)
        flash('Страница успешно проверена', 'alert-success')

    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'alert-danger')

    return redirect(url_for(
        'show_urls',
        id=id
    ))


@app.errorhandler(404)
def page_not_found(error):
    '''
    Display a page with a '404' error if there is no record in the db by id.

    :return: Render the HTML template for 404.html.
    '''
    return render_template(
        '404.html'
    ), 404


if __name__ == '__main__':
    app.run()
