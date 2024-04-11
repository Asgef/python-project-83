import validators
from urllib.parse import urlparse
from page_analyzer.db import get_url_by_name


ERROR_INVALID_URL = 1
ERROR_URL_EXISTS = 2
ERROR_URL_TOO_LONG = 3


def validate(url):
    error = None
    id = None

    if len(url) > 255:
        error = ERROR_URL_TOO_LONG
    elif not validators.url(url):
        error = ERROR_INVALID_URL
    else:
        parsed_url = urlparse(url)
        normalised_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
        url_found_db = get_url_by_name(normalised_url)

        if url_found_db:
            error = ERROR_URL_EXISTS
            id = url_found_db[0]

        url = normalised_url

    valid = {'id': id, 'url': url, 'error': error}

    return valid
