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
from validator import validate, ERROR_INVALID_URL, ERROR_URL_EXISTS
from page_analyzer.db import add_url_to_db, get_url_by_name
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

    if error == ERROR_INVALID_URL:
        id = validated['id']
        flash('Страница уже существует', 'error')

        return redirect(url_for('show', id=id))

    elif error == ERROR_URL_EXISTS:
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
    return redirect(url_for('show', id=id))


if __name__ == '__main__':
    app.run()
