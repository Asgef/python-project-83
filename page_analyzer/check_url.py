import requests
from bs4 import BeautifulSoup


def get_check_url(address):
    '''
    Get site data by its URL, including HTTP response code, h1 tag, head tag,
    and a meta description tag.

    :param url: The URL to be check.
    :type url: str
    :return: A dictionary containing data received from a site by its URL
    :rtype: dict
    '''
    rqsts = requests.get(address, timeout=3)

    if rqsts.status_code != 200:
        raise requests.RequestException

    check = {'status_code': rqsts.status_code}
    data_page = BeautifulSoup(rqsts.text, 'html.parser')

    h1_tag = data_page.find('h1')
    title_tag = data_page.find('title')
    description_tag = data_page.find('meta', attrs={'name': 'description'})

    check['h1'] = h1_tag.text.strip() if h1_tag else ''
    check['title'] = title_tag.text.strip() if title_tag else ''
    check['description'] = description_tag['content'].strip() \
        if description_tag else ''

    return check
