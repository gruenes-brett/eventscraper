# Scrape event data from websites

This Python tool scrapes event data from websites (currently only
Facebook) and returns the event information as JSON.

## Requirements

* Python 3.6 or higher
* pipenv

**Initial setup**
```
pip install pipenv
pipenv sync
```

## Usage
```
pipenv run scrape <url>
```
If the exit code is 0, the scraped data is saved to
`result.json`.

For debugging purposes, the response for the URL request is
saved to `response.html`.