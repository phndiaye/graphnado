from graphql import Source, execute, parse, validate
from graphql.execution import ExecutionResult


class GraphQLRequestExecutor(object):
    def __init__(self, schema, query, variables, operation_name):
        self.schema = schema
        self.query = query
        self.variables = variables or {}
        self.operation_name = operation_name

    def perform(self):
        try:
            validation_errors = validate(self.schema, self.ast)
            if validation_errors:
                return ExecutionResult(errors=validation_errors, invalid=True)

            return execute(
                self.schema, self.ast, variable_values=self.variables,
                operation_name=self.operation_name
            )
        except Exception as e:
            return ExecutionResult(errors=[e], invalid=True)

    @property
    def source(self):
        return Source(self.query)

    @property
    def ast(self):
        return parse(self.source)
