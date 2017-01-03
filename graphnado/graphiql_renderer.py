import os
import json

from tornado import template

GRAPHIQL_VERSION = '0.7.1'
MARKUP_CONTENT_TYPES = [
    'text/html', 'application/xhtml+xml', 'application/xml;q=0.9'
]


def request_wants_html(mimetypes):
    return set(MARKUP_CONTENT_TYPES).issubset(mimetypes)


def should_render_graphiql(accept_header_mimetypes):
    return True if request_wants_html(accept_header_mimetypes) else False


class GraphiQLRenderer(object):
    @classmethod
    def render(cls, query, result, variables, operation_name):
        loader = template.Loader(
            os.path.join(os.path.dirname(__file__), 'templates'))
        return loader.load('graphiql.html').generate(
            graphiql_version=GRAPHIQL_VERSION, query=json.dumps(query),
            result=json.dumps(result), variables=json.dumps(variables),
            operation_name=json.dumps(operation_name))
