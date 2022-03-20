import json
import logging
import re
from abc import ABC

from ..eventdata import EventData
from ..scraper import Scraper


log = logging.getLogger(__name__)


class ApplicationLdJsonScraper(Scraper, ABC):
    """
    Scraper base class for pages that supply event information in
    a <script type="application/ld+json"> ... </script> block as plain JSON.
    """
    PAYLOAD_MATCHER = re.compile(r'<script type="application/ld\+json".*>\s*(\{.*"@type":\s*"Event".*\})\s*</script>', flags=re.DOTALL)

    @staticmethod
    def convert_numbers_to_strings_in_json(json_string: str):
        """
        Replace integer values with strings by adding quotes around them. Otherwise
        json.loads() will fail when encountering numbers that start with 0 (such as 01234)
        """
        return re.sub(r'(?P<before>"\s*:\s*)(?P<number>\d+)(?P<after>\s*,?)',
                      r'\g<before>"\g<number>"\g<after>', json_string)

    @staticmethod
    def clean_invalid_json(json_string: str):
        """Remove weird trailing characters in json string
        """
        return re.sub(r',\s*<!----><!---->\s*\}', '}', json_string)

    def _interpret_response(self, response: str):
        matches = self.PAYLOAD_MATCHER.findall(response)
        if not matches:
            raise ValueError(f'Response to {self._url} does not contain expected payload match')
        fixed_json_string = self.convert_numbers_to_strings_in_json(matches[0])
        fixed_json_string = self.clean_invalid_json(fixed_json_string)
        try:
            data = json.loads(fixed_json_string)
        except Exception:
            log.error(f'Could not interpret as json: {fixed_json_string}')
            raise

        event_data = EventData(
            title=data.get('name'),
            location=data.get('location', {}).get('name'),
            description=data.get('description'),
            url=data.get('url', self._url),
            start_date=data.get('startDate'),
            end_date=data.get('endDate'),
        )
        return event_data

    def _interpret_response_soup(self, response_soup) -> EventData:
        raise NotImplementedError

