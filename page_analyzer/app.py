from flask import (
    Flask,
    render_template,
    url_for,
    request,
    flash,
    get_flashed_messages,
    redirect
)
from page_analyzer.db import (
    add_url_to_db, get_url_by_name,
    get_url_by_id, get_all_urls,
    add_check_to_db, get_checks_by_id_url
)
from page_analyzer.validator import (
    validate, ERROR_INVALID_URL, ERROR_URL_EXISTS
)
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
    return render_template('index.html')


@app.post('/urls')
def post_urls():

    url = request.form.get('url')
    validated = validate(url)
    
    error = validated['error']
    url = validated['url']

    if error == ERROR_URL_EXISTS:
        id = validated['id']
        flash('Страница уже существует', 'alert-info')

        return redirect(url_for('show_urls', id=id))

    elif error == ERROR_INVALID_URL:
        flash('Некорректный URL', 'alert-warning')

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
    id = get_url_by_name(url)[0]

    flash('Страница успешно добавлена', 'alert-success')
    return redirect(url_for('show_urls', id=id))


@app.get('/urls')
def get_list_urls():
    urls = get_all_urls()

    return render_template(
        'urls.html',
        urls=urls
    )


@app.route('/urls/<int:id>')
def show_urls(id):
    data_url = get_url_by_id(id)

    if not data_url:
        return 'Page not found', 404

    else:
        url = {
            'id': data_url[0],
            'name': data_url[1],
            'created_at': data_url[2].strftime('%Y-%m-%d')
        }

        data_checks = get_checks_by_id_url(id)
        checks = [
            {
                'id': id,
                'status_code': status_code,
                'h1': h1,
                'title': title,
                'description': description,
                'created_at': date.strftime('%Y-%m-%d')
            }
            for id, _, status_code, h1, title, description, date in data_checks
        ]

        messages = get_flashed_messages(with_categories=True)

        return render_template(
            'show.html',
            url=url,
            checks=checks,
            messages=messages
        )


@app.post('/urls/<int:id>/checks')
def check_url(id):
    data_url = get_url_by_id(id)
    url = data_url[1]

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
    return render_template(
        '404.html'
    ), 404


if __name__ == '__main__':
    app.run()
