import sys,os
from whirlwind.core.log import Log

class Bootstrap():
    def __init__(self):
        self.application = None
    
    '''
    make sure the python path is set for this app
    '''
    def init_path(self):
        
        #split the current directory from the parent dirictory path
        parent_dir, dir = os.path.split(sys.path[0])
        
        #insert the parent directory into the front of the pythonpath list
        sys.path.insert(0,parent_dir)
    
    def init_logging(self,log):
        if log == 'db':
            Log.create()
        else:
            Log.create('FILE',log)
    
    def main(self):
        #import tornado stuff
        import tornado.web, tornado.httpserver, tornado.ioloop, tornado.options
        from tornado.options import options
        from config import options_setup
        from whirlwind.db.mongo import Mongo
        from whirlwind.view.decorators import route
        
        #parse the app config
        tornado.options.parse_config_file(os.path.join(os.path.dirname(__file__),'config/settings.py'))
        #parse the command line args
        tornado.options.parse_command_line()
        
        #connect to our db using our options set in settings.py
        Mongo.create(host=options.db_host, port=options.db_port)
        
        from config.routes import route_list
        url_routes = route.get_routes()
        url_routes.extend(route_list)
        self.init_routes()
        
        #init a logger
        self.init_logging(options.log)
        
        #add in any app settings 
        settings = {
            "static_path": options.static_path,
            "cookie_secret": options.cookie_secret,
            "login_url": options.login_url,
        }
        
        #setup the controller action routes
        self.application = tornado.web.Application(url_routes,**settings)
        
        #instantiate a server instance
        http_server = tornado.httpserver.HTTPServer(self.application)
        
        #bind server to port
        http_server.listen(options.port)
        
        Log.info("Ready and listening")
        
        #start the server
        tornado.ioloop.IOLoop.instance().start()
    
    def init_routes(self):
        import pkgutil,sys,inspect
        import application.controllers
        package = application.controllers
        prefix = package.__name__ + "."
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
            module = __import__(modname)
    
    @staticmethod
    def run():
        bootstrap = Bootstrap()
        bootstrap.init_path()
        bootstrap.main()