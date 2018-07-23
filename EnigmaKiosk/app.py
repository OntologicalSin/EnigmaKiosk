import tornado.web, os
from handlers import LoginHandler, IndexHandler, SaveHandler, ResetHandler

class Application(tornado.web.Application):

    def __init__(self):
        # Define handlers
        handlers = [
            (r'/login', LoginHandler),
            (r'/', IndexHandler),
            (r'/send', SaveHandler),
            (r'/reset',ResetHandler),
            (r'/uploads/(.*)', tornado.web.StaticFileHandler, {'path': 'uploads'}),
            (r'/templates/(.*)', tornado.web.StaticFileHandler, {'path': 'templates'}),
        ]

        # Define options
        settings = {
            'cookie_secret': str(os.urandom(45)),
            'login_url': '/login',
        }

        # Initialize application
        super(Application, self).__init__(handlers, **settings)


if __name__ == '__main__':
    # Initialize HTTP server and run on 1337 port
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(4200)
    tornado.ioloop.IOLoop.instance().start()
