import datetime
import json
import locale
import logging
from typing import Dict

from bs4 import BeautifulSoup

from ..eventdata import EventData
from ..scraper import Scraper

log = logging.getLogger(__name__)

class BundEventScraper(Scraper):
    """
    Scraper for www.bund-sachsen.de

    """
    MONTHS = {
        'Januar=': 'January',
        'Februar': 'February',
        'März': 'March',
        'Mai': 'May',
        'Juni': 'June',
        'Juli': 'July',
        'Oktober': 'October',
        'Dezember': 'December',
    }
    @classmethod
    def matches(cls, url):
        return ('bund-sachsen.de' in url and '/event/' in url)

    def _interpret_response_soup(self, response_soup: BeautifulSoup) -> Dict:
        title = str(response_soup.title.string)
        url = self._get_meta_content(response_soup, 'og:url')

        details_soup = response_soup.find('div', class_='m-sidebar-content')
        start_date, end_date, location, organizer = self.__extract_details(details_soup)

        description = self._extract_description(response_soup)

        event_data = EventData(
            title=title,
            location=location,
            start_date=start_date,
            end_date=end_date,
            url=url,
            description=description,
            organizer=organizer,
        )
        return event_data

    def _get_meta_content(self, soup: BeautifulSoup, property: str):
        tag = soup.find('meta', attrs={'property': property})
        content = None
        if tag:
            content = tag.attrs.get('content')
        return str(content) if content else None

    def _extract_description(self, soup: BeautifulSoup):
        description_soup = soup.find('div', class_='das-hier-ist-column-main')
        lines = []
        if description_soup:
            for p in description_soup.find_all('p', class_=None):
                if p.text:
                    lines.append(str(p.text).strip())
            return '\n\n'.join(lines)
        return None

    def __extract_details(self, details_soup: BeautifulSoup):
        if not details_soup:
            log.warning('Sidebar content not found')
        detail_values = {}
        key = None
        for paragraph in details_soup.find_all('p', class_='rte-paragraph'):
            if key is None:
                key = str(paragraph.string).strip()
            else:
                detail_values[key] = str(paragraph.text).strip().replace('\n', ', ')
                key = None

        start_date = detail_values.get('Startdatum:')
        if start_date:
            start_date = self.__parse_german_date(start_date)
        end_date = detail_values.get('Enddatum:')
        if end_date:
            end_date = self.__parse_german_date(end_date)
        location = detail_values.get('Ort:')
        organizer = detail_values.get('Veranstalter:')
        return start_date, end_date, location, organizer

    def __parse_german_date(self, date_string):
        current_locale = locale.getlocale(locale.LC_TIME)
        for german, english in self.MONTHS.items():
            date_string = date_string.replace(german, english)
        try:
            date = datetime.datetime.strptime(date_string, '%d. %B %Y')
            return date.strftime('%Y-%m-%dT12:00')
        except Exception as e:
            log.exception(f'Could not parse date string "{date_string}"')
