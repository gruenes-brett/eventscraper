import random

from fake_useragent import UserAgent
from requests import Session
import logging
log = logging.getLogger(__name__)


class Request:
    # Request headers to choose from randomly
    HEADERS = [
        {
            'accept-language': 'en',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        },
        {
            'accept-language': 'en',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.71',
        },
        {
            'Accept-Language': 'en-US,en;q=0.5',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',
        }
    ]

    def __init__(self, url):
        self._url = url

    def get_response(self, payload=None):
        session = Session()
        session.headers.update(self._get_random_headers())
        log.info(f'Headers: {session.headers}')
        response = session.get(self._url, data=payload)
        if response.status_code != 200:
            raise ValueError(f'Bad response code: {response.status_code}')
        return response.text

    def _get_random_headers(self):
        ua = UserAgent(num_newest_uas=10)
        headers = random.choice(self.HEADERS).copy()
        # headers['User-Agent'] = ua.firefox
        return headers
