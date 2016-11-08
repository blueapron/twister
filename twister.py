import tornado.ioloop
import tornado.web
import json
from converters.json_api_converter import JsonApiConverter

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class ConversionHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        result = JsonApiConverter(data).convert()
        self.write(json.dumps(result))

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/convert", ConversionHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(3000)
    tornado.ioloop.IOLoop.current().start()
