from typing import Type

from eventscraper.scraper import Scraper


def test_bund1(scraper_dummy: Type[Scraper]):
    event_data = scraper_dummy.scrape('https://www.bund-sachsen.de/event/bund1.html')
    assert event_data.title == 'BUNDjugend Plenum'
    assert event_data.location == 'online'
    assert 'Dresden\n\nDas wöchentliche Plenum' in event_data.description
    assert event_data.description.endswith('zu erhalten!')
    assert event_data.url == 'https://www.bund-dresden.de/service/termine/detail/event/bundjugend-plenum-3/'
    assert event_data.start_date == '2022-03-21T12:00'
    assert event_data.end_date == '2022-06-01T12:00'
    assert event_data.organizer == 'BUNDjugend'

