import tornado.ioloop
import tornado.web
from graphnado import GraphQLHandler

from schema import graphql_schema

if __name__ == '__main__':
    application = tornado.web.Application([
        (
            r'/graphql',
            GraphQLHandler,
            dict(schema=graphql_schema, enable_graphiql=True)
        ),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
