from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def greeting():
    return 'Hello world'


if __name__ == '__main__':
    app.run()