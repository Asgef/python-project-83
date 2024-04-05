from flask import (
    Flask,
    render_template,
    url_for,
    request,
    flash,
    get_flashed_messages,
    redirect
)
from dotenv import load_dotenv
from page_analyzer.db import add_url_to_db, get_url_by_name, get_url_by_id
from page_analyzer.validator import (
    validate, ERROR_INVALID_URL, ERROR_URL_EXISTS
)
import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def post_urls():

    url = request.form.get('url')
    validated = validate(url)
    error = validated['error']
    url = validated['url']
    print(error)

    if error == ERROR_URL_EXISTS:
        id = validated['id']
        flash('Страница уже существует', 'error')

        return redirect(url_for('show_urls', id=id))

    elif error == ERROR_INVALID_URL:
        flash('Некорректный URL', 'error')

        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html',
            messages=messages,
            url=url
        ), 422

    add_url_to_db(url)
    id = get_url_by_name(url)[0]

    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_urls', id=id))


@app.route('/urls/<int:id>', methods=['GET'])
def show_urls(id):
    data_url = get_url_by_id(id)
    # checks

    if not data_url:
        return 'Page not found', 404

    else:
        url = {
            'id': data_url[0],
            'name': data_url[1],
            'created_at': data_url[2].strftime('%Y-%m-%d')
        }

        messages = get_flashed_messages(with_categories=True)

        return render_template(
            'show.html',
            url=url,
            messages=messages
        )


if __name__ == '__main__':
    app.run()
