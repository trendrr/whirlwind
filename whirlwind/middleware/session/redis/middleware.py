from whirlwind.middleware.session.redis import Session
from whirlwind.db.redis_interface import Redis
from tornado.options import options

class SessionMiddleware():
    def __init__(self,request):
        if options.redis_host :
            Redis.create(host=options.redis_host, port=options.redis_port, db=options.redis_db, connection_pool=True)
        else:
            raise Exception('redis_session.SessionMiddleware redis settings not defined')
        
        self.request = request
    
    def request_hook(self):
        #add a session member to the request object
        self.request.session = Session(self.request)
    
    def response_hook(self):
        #save the session
        self.request.session.save()
        
        #delete the session from the session
        del self.request.session
    
    def view_hook(self,view):
        #add the session to the view so its accessable in our template
        view['session'] = self.request.session