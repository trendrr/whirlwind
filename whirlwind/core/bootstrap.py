import sys,os
from whirlwind.core.log import Log

class Bootstrap():
    def __init__(self):
        self.application = None
        self.init_path()
    
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
    
    def main(self,path):
        #import tornado stuff
        import tornado.web, tornado.httpserver, tornado.ioloop, tornado.options
        from tornado.options import options
        from config import options_setup
        from whirlwind.db.mongo import Mongo
        
        #parse the app config
        tornado.options.parse_config_file(os.path.join(path,'config/settings.py'))
        #parse the command line args
        tornado.options.parse_command_line()
        
        #connect to our db using our options set in settings.py
        Mongo.create(host=options.db_host, port=options.db_port)
        
        #init our url routes
        url_routes = self.init_routes()
        
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
        
        #log our start message
        Log.info("Ready and listening")
        
        #start the server
        tornado.ioloop.IOLoop.instance().start()
    
    def init_routes(self):
        from whirlwind.core.routes import RouteLoader
        return RouteLoader.load('application.controllers')
    
    @staticmethod
    def run(path):
       (Bootstrap()).main(path)
