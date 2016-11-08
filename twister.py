import tornado.ioloop
import tornado.web
import json
from converters.json_api_converter import JsonApiConverter
from tornado.httpclient import AsyncHTTPClient

def asynchronous_fetch(urls):
    http_client = AsyncHTTPClient()
    return {url: http_client.fetch(url) for url in urls}

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class ConversionHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        result = JsonApiConverter(data).convert()
        self.write(json.dumps(result))

class MultiHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        results = {}

        requests = asynchronous_fetch(['https://www.apple.com',
          'https://www.google.com',
          'https://www.blueapron.com',
          'https://www.nytimes.com'
        ])

        for url, request in requests.items():
            result = yield request
            results[url] = str(result.body)

        self.write(json.dumps(results, encoding='latin1'))

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/convert", ConversionHandler),
        (r"/multi", MultiHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(3000)
    tornado.ioloop.IOLoop.current().start()
