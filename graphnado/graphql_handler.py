import json
import re

import tornado.web
from graphql import GraphQLSchema

from .graphiql_renderer import should_render_graphiql, GraphiQLRenderer
from .graphql_request_executor import GraphQLRequestExecutor

GRAPHQL_SUPPORTED_METHODS = ['get', 'post']


class GraphQLHandler(tornado.web.RequestHandler):
    def initialize(self, schema, enable_graphiql=False):
        if not isinstance(schema, GraphQLSchema):
            raise TypeError('Schema must be an instance of GraphQLSchema')

        self.schema = schema
        self.enable_graphiql = enable_graphiql

    def prepare(self):
        if self.request.method.lower() not in GRAPHQL_SUPPORTED_METHODS:
            raise tornado.web.HTTPError(
                status_code=405,
                reason='GraphQL only supports GET and POST requests')

        self.accept_header_mimetypes = self.request.headers['Accept'] \
            .split(',')
        data = self._parse_body(self.request.body)
        self.graphql_params = self._get_graphql_params(data)

    def get(self):
        query, variables, id, operation_name = self.graphql_params

        if (self.enable_graphiql and
                should_render_graphiql(self.accept_header_mimetypes)):
            try:
                output = GraphiQLRenderer.render(
                    query=query, result=None, variables=variables,
                    operation_name=operation_name)
                self.write(output)
            except Exception as e:
                raise e

    def post(self):
        result, status_code = self._get_result()

        try:
            self.set_status(status_code)
            self.write(result)
        except Exception as e:
            raise e

    def _parse_body(self, body):
        if re.match(r'application/json', self.request.headers['Accept']):
            return json.loads(body.decode('utf-8'))

        return {}

    def _get_graphql_params(self, request_body):
        query = self.get_argument('query', None) or request_body.get('query')
        variables = self.get_argument('variables', None) or \
            request_body.get('variables')
        id = self.get_argument('id', None) or request_body.get('id')
        operation_name = self.get_argument('operationName', None) or \
            request_body.get('operationName')
        return [query, variables, id, operation_name]

    def _get_result(self):
        query, variables, id, operation_name = self.graphql_params

        graphql_execution_result = self._execute_graphql_request(
            query, variables, operation_name
        )

        return graphql_execution_result

    def _execute_graphql_request(self, query, variables, operation_name):
        if not query and self.enable_graphiql:
            raise tornado.web.HTTPError(
                status_code=400,
                reason='You must provide GraphiQl with a query string')

        req_executor = GraphQLRequestExecutor(
            self.schema, query, variables, operation_name)
        req_result = req_executor.perform()

        status_code = 200
        if req_result:
            response = {}

            if req_result.invalid:
                status_code = 400
            else:
                status_code = 200
                response['data'] = req_result.data
        else:
            response = None

        return response, status_code
