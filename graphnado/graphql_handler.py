import tornado.web
from graphql import GraphQLSchema


GRAPHQL_SUPPORTED_METHODS = ['get', 'post']


class GraphQLHandler(tornado.web.RequestHandler):
    def initialize(self, schema, enable_graphiql=False):
        if not isinstance(schema, GraphQLSchema):
            raise TypeError('Schema must be an instance of GraphQLSchema')

    def get(self):
        self.write('Hello, World')

    def prepare(self):
        if self.request.method.lower() not in GRAPHQL_SUPPORTED_METHODS:
            raise tornado.web.HTTPError(
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
