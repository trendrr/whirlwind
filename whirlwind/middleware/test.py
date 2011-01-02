class TestMiddleware():
    def __init__(self,request):
        print "TestMiddleware loaded"
    
    def request_hook(self):
        print "TestMiddleware.request_hook called"
    
    def response_hook(self):
        print "TestMiddleware.response_hook called"
    
    def view_hook(self,view):
        print "TestMiddleware.view_hook called"