import graphene


class Query(graphene.ObjectType):
    hello = graphene.String(description='Hello you, Mr Hello World')

    def resolve_hello(self, args, context, info):
        return 'Hello, World!'


graphql_schema = graphene.Schema(query=Query)
