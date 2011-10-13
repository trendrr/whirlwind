from tornado.options import options

class MiddlewareManager():
    
    def __init__(self,request):
        self.request = request
        self.request_middleware = []
        self.response_middleware = []
        self.view_middleware = []
        self.load()
        
    def run_request_hooks(self):
        self.__run_hooks('request',self.request_middleware)
    
    def run_response_hooks(self):
        self.__run_hooks('response',self.response_middleware)
        
    def run_view_hooks(self,view):
        self.__run_hooks('view',self.view_middleware,view)
        
    def __run_hooks(self,type,middleware_classes,view=None):
        for middleware_class in middleware_classes:
            try:
                if(type == 'request'):
                    middleware_class.request_hook()
                if(type == 'response'):
                    middleware_class.response_hook()
                if(type == 'view'):
                    middleware_class.view_hook(view)
            except AttributeError:
                pass
    
    def load(self):
        if hasattr(options,'middleware_classes') and len(options.middleware_classes) > 0:
            for mclass in options.middleware_classes:
                modname, clsname = self.split_name(mclass)
                
                try:
                    mod = __import__(modname, globals(), locals(), [clsname], -1)
                except ImportError, ex:
                    print "module __import__ failed", ex
                
                try:
                    cls = getattr(mod, clsname)
                    inst = cls(self.request)
                except AttributeError, ex:
                    print "cant instantiate cls", ex
                
                if hasattr(inst,'view_hook'):
                    self.view_middleware.append(inst)
                if hasattr(inst,'request_hook'):
                    self.request_middleware.append(inst)
                if hasattr(inst,'response_hook'):
                    self.response_middleware.append(inst)
    
    def split_name(self,path):
        try:
            pos = path.rindex('.')
        except ValueError:
            raise Exception('%s is invalid' % path)
        
        return path[:pos], path[pos+1:]