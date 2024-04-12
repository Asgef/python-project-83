import validators
from urllib.parse import urlparse
from page_analyzer.db import get_url_by_name
from page_analyzer.constants import (
    ERROR_URL_TOO_LONG, ERROR_INVALID_URL, ERROR_URL_EXISTS
)


def validate(url) -> dict:
    '''
    Validate and normalize URLs.

    :param url: The URL to be validated.
    :type url: str
    :return: A dictionary containing a normalized URL and possible errors.
    :rtype: dict
    '''
    error = None

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

        url = normalised_url

    valid = {'url': url, 'error': error}

    return valid
