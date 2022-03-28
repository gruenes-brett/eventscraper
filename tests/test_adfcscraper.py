from typing import Type

from eventscraper.scraper import Scraper


def test_adfc1(scraper_dummy: Type[Scraper]):
    event_data = scraper_dummy.scrape('https://touren-termine.adfc.de/radveranstaltung/adfc1.html')
    assert event_data.title == 'Globaler Klimastreik'
    assert event_data.location == 'Augustusplatz, 04109 Leipzig'
    assert 'Nach 100 Tagen Ampel-Koalition wird wohl feststehen:' in event_data.description
    assert event_data.description.endswith('Future auf die Straße.')
    assert event_data.url == 'https://touren-termine.adfc.de/radveranstaltung/adfc1.html'
    assert event_data.start_date == '2022-03-25T10:00'
    assert event_data.end_date == '2022-03-25T18:00'
    assert event_data.organizer == ''


def test_adfc2_problematic(scraper_dummy: Type[Scraper]):
    event_data = scraper_dummy.scrape('https://touren-termine.adfc.de/radveranstaltung/adfc2_problematic.html')
    assert event_data.title == 'Online moderieren und aktivieren (online)'
    assert event_data.location == 'Mohrenstraße 69, 10117 Berlin'
    assert event_data.description == '! Could not read description !'
    assert event_data.url == 'https://touren-termine.adfc.de/radveranstaltung/adfc2_problematic.html'
    assert event_data.start_date == '2022-04-09T10:00'
    assert event_data.end_date == '2022-04-09T13:00'
    assert event_data.organizer == ''
