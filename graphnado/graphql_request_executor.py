from graphql import Source, execute, parse


class GraphQLRequestExecutor(object):
    def __init__(self, schema, query, variables, operation_name):
        self.schema = schema
        self.query = query
        self.variables = variables or {}
        self.operation_name = operation_name

    def perform(self):
        return execute(
            self.schema, self.ast, variable_values=self.variables,
            operation_name=self.operation_name
        )

    @property
    def source(self):
        return Source(self.query)

    @property
    def ast(self):
        return parse(self.source)
