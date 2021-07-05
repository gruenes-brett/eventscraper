# Scrape event data from websites

This Python tool scrapes event data from websites (currently only
Facebook) and returns the event information as JSON.

## Requirements

* Python 3.6 or higher
* pipenv

**Initial setup**
```
pip3 install pipenv
pipenv sync
```

## Command line usage
```
pipenv run scrape <url>
```
If the exit code is 0, the scraped data is saved to
`result.json`.

For debugging purposes, the response for the URL request is
saved to `response.html`.

## Run as Docker container

Create container:

`sudo docker build -t uscrapeme .`

Run container:

`docker run -p 9080:80 uscrapeme`

## Install as Flask app running on apache2

1. Make sure to initialize the venv inside the current
   project directory

   `./init_venv.bash`
2. The current directory contents must be readable by
   the apache user

   ```
   sudo chmod -R g+r .
   sudo chown -R :www-data .
   ```

3. Install apache2 WSGI module

   `sudo apt install libapache2-mod-wsgi-py3`

4. Install a virtual host that calls the WSGI script

    `./install_apache2_vhost.bash`

    You will be prompted for the port the app should be running on.
    (e.g., 8080)

### Usage via GET request

http://localhost:8080/api/scraper?url=https://www.facebook.com/events/12345