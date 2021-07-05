import argparse
import json
import logging
import os

from scraper import Scraper

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

RESULT_FILE = 'result.json'

def main():
    if os.path.isfile(RESULT_FILE):
        os.remove(RESULT_FILE)

    # command line arguments
    parser = argparse.ArgumentParser(description='Tool for scraping event information from websites. '
                                     'Currently supported: Facebook')
    parser.add_argument('url', help='URL of the event')
    parser.add_argument('-v', action='store_true', default=False, help='More logging output')
    args = parser.parse_args()
    url = args.url
    verbose = args.v
    if verbose:
        log.setLevel(logging.DEBUG)

    # scrape data from url
    result = Scraper.scrape(url)
    log.info(f'result: {result}')
    with open(RESULT_FILE, 'w') as f:
        json.dump(result, f, indent=4)


main()
