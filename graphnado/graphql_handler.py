import json

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

    def write_error(self, status_code, **kwargs):
        kwargs['status_code'] = status_code
        if status_code == 405:
            kwargs['message'] = 'Unsupported Http method'
        else:
            kwargs['message'] = kwargs['message'] or 'Unknown Error'
        self.response = kwargs
        self._write_json()

    def _write_json(self):
        output = json.dumps(self.response)
        self.write(output)
