import json
import logging
import re
from abc import ABC
from typing import Dict, List, Callable

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

    @staticmethod
    def drop_invalid_lines(json_string: str):
        """Try to interpret json line by line and drop lines that give an error
        """
        output_lines = []
        for line in json_string.split('\n'):
            stripped_line = line.strip()
            if stripped_line and stripped_line.startswith('"') and stripped_line[-1] in '",':
                if stripped_line.endswith(','):
                    stripped_line = stripped_line[:-1]
                try:
                    json.loads(f'{{{stripped_line}}}')
                except Exception:
                    continue
            output_lines.append(line)
        return '\n'.join(output_lines)

    @staticmethod
    def remove_superfluous_commata(json_string: str):
        """Remove invalid commata before closing braces"""
        cleaned = re.sub(r'(?P<quote_or_brace>["\}]),(?P<spaces>\s)*(?P<brace>\})',
                         r'\g<quote_or_brace>\g<spaces>\g<brace>',
                         json_string)
        if cleaned != json_string:
            # If changed, there might be more to fix
            return ApplicationLdJsonScraper.remove_superfluous_commata(cleaned)
        return cleaned

    def _interpret_response(self, response: str):
        matches = self.PAYLOAD_MATCHER.findall(response)
        if not matches:
            raise ValueError(f'Response to {self._url} does not contain expected payload match')

        data = self._parse_json(matches[0], cleanup_methods=[
            self.convert_numbers_to_strings_in_json,
            self.clean_invalid_json,
            self.drop_invalid_lines,
            self.remove_superfluous_commata,
        ])

        event_data = EventData(
            title=data.get('name'),
            location=data.get('location', {}).get('name'),
            description=data.get('description'),
            url=data.get('url', self._url),
            start_date=data.get('startDate'),
            end_date=data.get('endDate'),
        )
        return event_data

    def _parse_json(self, json_string: str,
                    cleanup_methods: List[Callable[[str], str]]) -> Dict:
        try:
            data = json.loads(json_string)
        except json.JSONDecodeError as e:
            log.error(f'Could not interpret as json: {json_string}')
            log.error(f'Error in line {e.lineno} near "{json_string[e.pos-10:e.pos+10]}"')
            if cleanup_methods:
                log.info(f'Retrying with cleanup method {cleanup_methods[0].__name__}')
                return self._parse_json(cleanup_methods[0](json_string), cleanup_methods[1:])
            raise
        except Exception:
            log.error(f'Could not interpret as json: {json_string}')
            raise
        return data

    def _interpret_response_soup(self, response_soup) -> EventData:
        raise NotImplementedError

