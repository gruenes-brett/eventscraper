import json
import os
import re

from uscrapeme.webrequest import Request

class Scraper:
    @classmethod
    def get_scrapers(cls):
        return [FacebookEventScraper]

    @classmethod
    def scrape(cls, url):
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
        with open('response.html', 'w') as f:
            f.write(text)
        return self._interpret_response(text)

    def _interpret_response(self, response: str):
        raise NotImplementedError()


class FacebookEventScraper(Scraper):
    PAYLOAD_MATCHER = re.compile(r'<script type="application/ld\+json".*>(.*"startDate".*"name".*)</script>')
    @classmethod
    def matches(cls, url):
        return 'facebook.' in url and '/events/' in url

    def _interpret_response(self, response: str):
        matches = self.PAYLOAD_MATCHER.findall(response)
        if not matches:
            raise ValueError(f'Response to {self._url} does not contain expected payload match')
        return json.loads(matches[0])

