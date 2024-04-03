from flask import (
    Flask,
    render_template,
    url_for,
    request
)
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/urls', methods=['POST'])
# def get_urls():
#     url = request.form.get('url')
#     errors = 


if __name__ == '__main__':
    app.run()
