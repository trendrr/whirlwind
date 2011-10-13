from whirlwind.middleware.redis_session import Session

class SessionMiddleware():
    def __init__(self,request):
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