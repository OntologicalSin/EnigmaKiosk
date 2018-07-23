import tornado.web, tornado.ioloop
from textparsing import parse_text
from speech import text_to_speech

file = "savthis.mp3"

items = [["", "", "", ""]]

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
        self.render('../Frontend/public/404.html')

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
        print(items)
        self.render('templates/public/index.html', items=items, noise=file)

class SaveHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):
        request = self.request.body.decode("utf-8")
        print(request)
        stuff = parse_text(request)
        text_to_speech(stuff[0])
        print(stuff)
        if stuff[1] is not None:
            with open("Data/foods.json") as r:
                newarr = ["Order",stuff[1][1],"entree","$2.00"]
                for num in range(stuff[1][2]):
                    items.append(newarr)
        self.redirect('/')

class ResetHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        global items
        items = [["","","",""]]
        self.redirect('/')