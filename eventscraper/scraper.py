import json
import logging
import os
import re

from .webrequest import Request

log = logging.getLogger(__name__)

class Scraper:
    """
    Base class and entry point for website specific scrapers
    """
    RESPONSE_FILE = 'response.html'
    @classmethod
    def get_scrapers(cls):
        return [FacebookEventScraper]

    @classmethod
    def scrape(cls, url):
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

    def _scrape(self):
        r = Request(self._url)
        text = r.get_response()
        try:
            with open(self.RESPONSE_FILE, 'w') as f:
                f.write(text)
        except Exception as e:
            log.warning(str(e))
        return self._interpret_response(text)

    def _interpret_response(self, response: str):
        raise NotImplementedError()


class FacebookEventScraper(Scraper):
    """
    Scraper for Facebook events

    Very basic implementation:
    The event information is embedded in a <script></script> block as plain JSON. This is
    great, also it doesn't seem to work for every events.

    TODO: Improvement needed
    """
    PAYLOAD_MATCHER = re.compile(r'<script type="application/ld\+json".*>(.*"startDate".*"name".*)</script>')
    @classmethod
    def matches(cls, url):
        return ('facebook.' in url and '/events/' in url) or 'fb.me' in url

    def _interpret_response(self, response: str):
        matches = self.PAYLOAD_MATCHER.findall(response)
        if not matches:
            raise ValueError(f'Response to {self._url} does not contain expected payload match')
        return json.loads(matches[0])
