import logging

from .applicationldjsonscraper import ApplicationLdJsonScraper

log = logging.getLogger(__name__)


class AdfcScraper(ApplicationLdJsonScraper):
    """
    Scraper for touren-termine.adfc.de

    """

    @classmethod
    def matches(cls, url):
        return 'touren-termine.adfc.de' in url and '/radveranstaltung/' in url
