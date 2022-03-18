import json
import logging
import os
import re
from typing import Dict

from bs4 import BeautifulSoup

from .eventdata import EventData
from .webrequest import Request

log = logging.getLogger(__name__)

class Scraper:
    """
    Base class and entry point for website specific scrapers
    """
    RESPONSE_FILE = 'response.html'
    @classmethod
    def get_scrapers(cls):
        from .scrapers.bundscraper import BundEventScraper
        from .scrapers.facebookscraper import FacebookEventScraper
        return [FacebookEventScraper, BundEventScraper]

    @classmethod
    def scrape(cls, url) -> EventData:
        if os.path.isfile(cls.RESPONSE_FILE):
            os.remove(cls.RESPONSE_FILE)
        for scraper_class in cls.get_scrapers():
            if scraper_class.matches(url):
                scraper = scraper_class(url)
                break
        else:
            raise ValueError(f'No matching scraper found for URL {url}')
        return scraper._scrape()

    @classmethod
    def matches(cls, url):
        raise NotImplementedError()

    def __init__(self, url: str):
        self._url = url

    def _scrape(self) -> EventData:
        r = Request(self._url)
        text = r.get_response()
        try:
            with open(self.RESPONSE_FILE, 'w') as f:
                f.write(text)
        except Exception as e:
            log.warning(str(e))
        try:
            return self._interpret_response(text)
        except NotImplementedError:
            soup = BeautifulSoup(text, 'html.parser')
            return self._interpret_response_soup(soup)

    def _interpret_response(self, response_text: str) -> Dict:
        raise NotImplementedError()

    def _interpret_response_soup(self, response_soup: BeautifulSoup) -> Dict:
        raise NotImplementedError()


