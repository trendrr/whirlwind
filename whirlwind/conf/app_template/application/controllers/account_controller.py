from whirlwind.core.request import BaseRequest
from whirlwind.db.mongo import Mongo
from application.models.user import User
import datetime, hashlib
from tornado.web import authenticated
from whirlwind.view.decorators import route

@route('/logout')
class LogoutHandler(BaseRequest):
    def get(self):
        self.session['username'] = None
        self.session.destroy()
        #kill the session.
        self.redirect("/")

@route('/login')
class LoginHandler(BaseRequest):
    def get(self):
        template_values = {}
        template_values['next'] = self.get_argument('next','/')
        
        self.render_template('/account/login.html',**template_values)

    def post(self):
        username = self.get_argument("username",None)
        password = self.get_argument("password",None)
        
        if not username or not password:
            # do something
            self.flash.error = "You must enter a username and password to proceed. Please try again."
            self.redirect("/login")
            return
        
        pw = hashlib.sha1(password).hexdigest()
        username = User.normalize(username)
        user = User.lookup(username)
        
        #check the password.
        if not user or user['password'] != pw:
            # do something
            self.flash.error = "Login not valid"
            self.redirect("/login")
            return
        
        # check if user is suspended.
        if user.is_suspended() :
            self.flash.error = "Sorry the account you specified has been suspended."
            self.redirect("/")
            return
          

        user.history.last_login = datetime.datetime.utcnow()
        Mongo.db.ui.users.update({'_id': username}, {
                                                    '$set' : {'history.last_login': user.history.last_login},
                                                    '$inc' : {'history.num_logins' : 1}
                                                    })        
        #add to the session.
        self.session['username'] = user._id
        #check keep_logged_in
        if self.get_argument("keep_logged_in", False) == "on" :
            self.session['keep_logged_in'] = True
        
        self.set_current_user(user)
        self.flash.notice = "Welcome, %s" % user._id
        forwardUrl = self.get_argument('next','/')
        self.redirect(forwardUrl)

@route('/signup')
class SignupHandler(BaseRequest):
    def get(self):
        template_values = {}
        template_values['next'] = self.get_argument('next','/')
        
        self.render_template('/account/signup.html',**template_values)
    
    def post(self):
        username = self.get_argument("username",None)
        password = self.get_argument("password",None)
        
        if not username or not password:
            # do something
            self.flash.error = "You must enter a username and password to proceed. Please try again."
            self.redirect("/signup")
            return
        
        if password != self.get_argument("password2", None) :
            self.flash.error = "Passwords do not match. Please try again."
            self.redirect("/signup")
            return
        
        user = User.instance(username, password)
        Mongo.db.ui.users.insert(user)
        self.flash.info = "Successfully created your account, please log in."
        self.redirect("/login")
        
class PasswordChanger(BaseRequest):
    @authenticated
    def post(self):
        pw = hashlib.sha1(self.get_argument("password")).hexdigest()
        
        if self.get_current_user()['password'] != pw:
            # do something
            self.flash.error = "Password not valid, please try again"
            self.redirect("/settings")
            return
        
        newPw = self.get_argument('new_pw')
        newPw2 = self.get_argument('new_pw_again')
        if newPw != newPw2 :
            self.flash.error = "Passwords do not match, please try again"
            self.redirect("/settings")
            return
        
        password = hashlib.sha1(newPw).hexdigest()
        Mongo.db.ui.users.update({'_id': self.get_username()}, {
                                                    '$set' : {'password': password}
                                                    })       
        self.flash.success = "Successfully updated password"
        self.redirect('/settings')
