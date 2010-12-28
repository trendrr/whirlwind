from tornado.options import define

#run mode
define("mode", default="development", help="run in development or production mode")

#define a port for testing
define("port", default=8888, help="run on the given port", type=int)

#define the path for the app
define("static_path", default='resources', help="define the path for the app")

#define a dir for mako to look for templates - relative to the app directory
define("template_dir", default='/tmp/views', help="set the dir for mako to look for templates")

#define a dir for mako to cache compiled templates
define("mako_modules_dir",default='/tmp/templates/mako_modules', help="set the dir for mako to cache compiled templates")

#define a database host
define("db_host", default='localhost', help="connect to the db on this host")

#define the database port
define("db_port", default=27017, help="connect to the db on this port", type=int)

define("cookie_secret", default="mehungryforcookie", help="cookie secret for tornado secure cookies")
#should we enable sessions
define("enable_sessions", default=True, help="connect to the db of this name", type=bool)

define("login_url", default="/login", help="whats the login url")
