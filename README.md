# Scrape event data from websites

This Python tool scrapes event data from websites (currently only
Facebook) and returns the event information as JSON.

Using the below setup steps, the service will be installed as an
Apache Vhost that is accessible at http://127.0.0.1:5050

## Usage when running as Flask WSGI app

http://127.0.0.1:5050/api/scrape?url=https://www.facebook.com/events/12345

## Requirements

* Python 3.6 or higher
* Apache2 web server
* Tested on Ubuntu 20.04 LTS

**Initial setup**
```
./install_requirements.bash
./init_venv.bash
./install_apache2_vhost.bash
```

## Command line usage
```
source venv/bin/activate
python -m eventscraper <url>
```
If the exit code is 0, the scraped data is saved to
`result.json`.

For debugging purposes, the response for the URL request is
saved to `response.html`.

## Run as Docker container

Create container:

`sudo docker build -t eventscraper:1.3 .`

Run container:

`docker run -p 9080:80 eventscraper:1.3`

Save container:

`docker save eventscraper:1.3 | gzip > eventscraper-1.3.tar.gz`
