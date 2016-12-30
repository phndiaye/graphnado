import tornado.web


class GraphQLHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, World')
