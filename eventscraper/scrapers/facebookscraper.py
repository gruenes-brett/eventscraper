import json
import re

from ..eventdata import EventData
from ..scraper import Scraper

class FacebookEventScraper(Scraper):
    """
    Scraper for Facebook events

    Very basic implementation:
    The event information is embedded in a <script></script> block as plain JSON. This is
    great, also it doesn't seem to work for every events.
    """
    PAYLOAD_MATCHER = re.compile(r'<script type="application/ld\+json".*>(.*"startDate".*"name".*)</script>')
    @classmethod
    def matches(cls, url):
        return ('facebook.' in url and '/events/' in url) or 'fb.me' in url

    def _interpret_response(self, response: str):
        matches = self.PAYLOAD_MATCHER.findall(response)
        if not matches:
            raise ValueError(f'Response to {self._url} does not contain expected payload match')
        data = json.loads(matches[0])

        event_data = EventData(
            title=data.get('name'),
            location=data.get('location', {}).get('name'),
            description=data.get('description'),
            url=data.get('url'),
            start_date=data.get('startDate'),
            end_date=data.get('endDate'),
        )
        return event_data
