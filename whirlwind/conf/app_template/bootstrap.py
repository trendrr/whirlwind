import sys,os

class Bootstrap():
    '''
    make sure the python path is set for this app
    '''
    def init_path(self):
        
        #split the current directory from the parent dirictory path
        parent_dir, dir = os.path.split(sys.path[0])
        
        #insert the parent directory into the front of the pythonpath list
        sys.path.insert(0,parent_dir)
    
#    def init_models(self):
#        # TODO: we should be able to do this via some kind of reflection.
#        from whirlwind.db.mongo import Mongo
#        from application.models.user import User
#        Mongo.db.register_models([User])
#    
    
    def main(self):
        #import tornado stuff
        import tornado.web, tornado.httpserver, tornado.ioloop, tornado.options
        from tornado.options import options
        from config import options_setup
        from whirlwind.db.mongo import Mongo
        
        #parse the app config
        tornado.options.parse_config_file(os.path.join(os.path.dirname(__file__),'config/settings.py'))
        #parse the command line args
        tornado.options.parse_command_line()
        
        #connect to our db using our options set in settings.py
        Mongo.create(host=options.db_host, port=options.db_port)
        
        from config.routes import route_list
        
        #register our model classes with mongo
#        self.init_models()
        
        #add in any app settings 
        settings = {
            "static_path": options.static_path,
            "cookie_secret": options.cookie_secret,
            "login_url": options.login_url,
        }
        
        #setup the controller action routes
        application = tornado.web.Application(route_list,**settings)
        
        #instantiate a server instance
        http_server = tornado.httpserver.HTTPServer(application)
        
        #bind server to port
        http_server.listen(options.port)
        print "Ready and listening"
        #start the server
        tornado.ioloop.IOLoop.instance().start()
    
    
    @staticmethod
    def run():
        bootstrap = Bootstrap()
        bootstrap.init_path()
        bootstrap.main()