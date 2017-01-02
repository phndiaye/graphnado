import tornado.web
from graphql import GraphQLSchema

from .graphiql_renderer import GraphiQLRenderer

GRAPHQL_SUPPORTED_METHODS = ['get', 'post']
MARKUP_CONTENT_TYPES = [
    'text/html', 'application/xhtml+xml', 'application/xml;q=0.9'
]


class GraphQLHandler(tornado.web.RequestHandler):
    def initialize(self, schema, enable_graphiql=False):
        if not isinstance(schema, GraphQLSchema):
            raise TypeError('Schema must be an instance of GraphQLSchema')
        self.enable_graphiql = enable_graphiql

    def prepare(self):
        if self.request.method.lower() not in GRAPHQL_SUPPORTED_METHODS:
            raise tornado.web.HTTPError(
                status_code=405,
                reason='GraphQL only supports GET and POST requests')

    def get(self):
        query, variables, id, operation_name = self.graphql_params
        if self.enable_graphiql and self._should_render_graphiql():
            try:
                output = GraphiQLRenderer.render(
                    query=query, result={}, variables=variables,
                    operation_name=operation_name)
                self.write(output)
            except Exception as e:
                raise e

    def _should_render_graphiql(self):
        accept_mimetypes = self.request.headers['Accept'].split(',')
        return True if self._wants_html(accept_mimetypes) else False

    def _wants_html(self, content_types):
        return set(MARKUP_CONTENT_TYPES).issubset(content_types)
