import tornado.ioloop
import tornado.web
from graphnado import GraphQLHandler

if __name__ == '__main__':
    application = tornado.web.Application([
        (r'/graphql', GraphQLHandler)
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
