#import our controller handler classes
from application.controllers import site_controller
from application.controllers import account_controller

#from application.controllers import help_controller

#  will choose the FIRST match it comes too
route_list = [
    (r'/', site_controller.IndexHandler),
    (r'/login', account_controller.LoginHandler),
    (r'/logout', account_controller.LogoutHandler),
    (r'/signup', account_controller.SignupHandler)
]
