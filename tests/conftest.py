import unittest.mock
from typing import Type

import pytest

from eventscraper.eventdata import EventData
from eventscraper.scraper import Scraper
from eventscraper.webrequest import Request


@pytest.fixture(scope='session')
def scraper_dummy() -> Type[Scraper]:
    class DummyRequest(Request):
        def get_response(self, payload=None):
            filename = self._url.split('/')[-1]
            with open(f'tests/dummypages/{filename}') as f:
                return f.read()

    class ScraperDummy(Scraper):
        @classmethod
        @unittest.mock.patch('eventscraper.scraper.Request', new=DummyRequest)
        def scrape(cls, url) -> EventData:
            return super().scrape(url)

    return ScraperDummy
