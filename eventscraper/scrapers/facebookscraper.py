from .applicationldjsonscraper import ApplicationLdJsonScraper


class FacebookEventScraper(ApplicationLdJsonScraper):
    """
    Scraper for Facebook events
    """
    @classmethod
    def matches(cls, url):
        return ('facebook.' in url and '/events/' in url) or 'fb.me' in url
