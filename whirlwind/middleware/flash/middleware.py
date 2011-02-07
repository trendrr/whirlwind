from whirlwind.middleware.flash import Flash

class FlashMiddleware():
    def __init__(self,request):
        self.request = request
    
    def request_hook(self):
#        assert hasattr(self.request, 'session'), "FlashMiddleware requires SessionMiddleware to be installed."
        
        #add a flash member to the request object
        self.request.flash = Flash()
    
    def response_hook(self):
        if len(self.request.flash) > 0:
            self.request.session['flash'] = self.request.flash
    
    def view_hook(self,view):
        #check if we have any flash messages set in the session
        if self.request.session.get('flash',False):     
            #add it to our template context args   
            view['flash'] = self.request.session['flash']
            
            #remove the flash from the session
            del self.request.session['flash']
        else:
            #required in case we add flash without redirecting
            if len(self.request.flash):
                view['flash'] = self.request.flash
                
