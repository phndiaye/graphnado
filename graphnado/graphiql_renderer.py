import os

from tornado import template

GRAPHIQL_VERSION = '0.7.1'


class GraphiQLRenderer(object):
    @classmethod
    def render(cls, query, result, variables, operation_name):
        loader = template.Loader(
            os.path.join(os.path.dirname(__file__), 'templates'))
        return loader.load('graphiql.html').generate(
            graphiql_version=GRAPHIQL_VERSION, query=query,
            result=result, variables=variables, operation_name=operation_name)
