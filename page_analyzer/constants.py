import os
from dotenv import load_dotenv


load_dotenv()


ERROR_INVALID_URL = 'Incorrect URL'
ERROR_URL_EXISTS = 'Page already exists'
ERROR_URL_TOO_LONG = 'URL exceeds 255 characters'

DATABASE_URL = os.getenv('DATABASE_URL')
