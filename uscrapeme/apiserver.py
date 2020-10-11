from flask import Flask, request, jsonify, abort, Response

from uscrapeme.scraper import Scraper


class ApiServer(Flask):

    def __init__(self, *args, **kwargs):
        Flask.__init__(self, *args, **kwargs)
        self._setup_endpoints()

    def _setup_endpoints(self):
        @self.route('/api/scrape', methods=['GET'])
        def scrape():
            url = request.args.get('url', None)
            if url is None:
                abort(Response('Missing parameter: url', status=400))
            try:
                data = Scraper.scrape(url)
            except Exception as e:
                abort(Response(f'Could not get event data from {url}: {e}', status=500))
            return jsonify({'url': url, 'data': data})

server = ApiServer(__name__)

if __name__ == '__main__':
    server.run(debug=False)
