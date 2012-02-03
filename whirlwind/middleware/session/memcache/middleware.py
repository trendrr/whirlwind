from whirlwind.middleware.session.memcache import Session
from whirlwind.db.memcache_interface import Memcache
from tornado.options import options

class SessionMiddleware():
    def __init__(self,request):
        if options.memcache_host :
            Memcache.create(host=options.memcache_host)
        else:
            raise Exception('memcache.session.SessionMiddleware memcache settings not defined')
        
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