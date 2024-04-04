import validator
from urllib.parse import urlparse
from page_analyzer.db import get_url_by_name


def validate(url):
    error = None

    if len(url) == 0 or len(url) > 255:
        error = 'Некорректный URL'
    elif not validator.url(url):
        error = 'Некорректный URL'
    else:
        parsed_url = urlparse(url)
        normalised_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
        url_found_db = get_url_by_name(normalised_url)

        if url_found_db:
            error = 'Страница уже существует'
        url = normalised_url

    valid = {'url': url, 'error': error}

    return valid
