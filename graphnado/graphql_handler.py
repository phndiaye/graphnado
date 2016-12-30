import tornado.web


GRAPHQL_SUPPORTED_METHODS = ['get', 'post']


class GraphQLHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, World')

    def prepare(self):
        if self.request.method.lower() not in GRAPHQL_SUPPORTED_METHODS:
            self.send_error(
                status_code=405,
                reason='GraphQL only supports GET and POST requests')
