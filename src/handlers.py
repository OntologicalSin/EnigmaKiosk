import tornado.web, tornado.gen, tornado.escape, tornado.ioloop, wave
from utils import SpeechRec

items = [["", "", ""]]

class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        # Get username of current user from cookie
        return self.get_secure_cookie('user')

    def response_user_error(self, error):
        # Clear response, set status, and render template
        self.clear()
        self.set_status(400)
        self.render('templates/400.html', error=error)

    def response_not_found(self):
        # Clear response, set status, and render template
        self.clear()
        self.set_status(404)
        self.render('templates/404.html')

class LoginHandler(BaseHandler):

    def get(self):
        # Render and return login page
        self.render('templates/login.html')

    def post(self):
        # Handle login form and set username of logged in user to cookie
        self.set_secure_cookie('user', 'test')

        # Redirect to main page
        self.redirect('/')

class IndexHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        global items
        #print(items)
        self.render('templates/index.html', items=items)

class SaveHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):
        request = self.request.body
        print(request)


        # f = open('file.wav', 'wb')
        # f.write(request)
        # f.close()
        # print("Binary message written!")
        #
        # SpeechRec.smth(request)

        # form = cgi.FieldStorage()
        # print(form)
        # fname = form["audio"].filename
        # print("Got filename:", fname)  # in case of problems see if this looks ok
        # # global items
        # # items.append(["bigmac.jpg","$3.25","more info"])
        # self.redirect('/')
