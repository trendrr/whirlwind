from tornado.options import define
import logging

#version
define("version", default="0.1", help="app version")

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

#define the database name
define("db_name", default="ui", help="the name of the database to use")

define("cookie_secret", default="mehungryforcookie", help="cookie secret for tornado secure cookies")

define("login_url", default="/login", help="whats the login url")

define("middleware_classes", default="", help="placeholder for the middleware_classes", multiple=True)

define("log", default="", help="the logfile")

define("redis_host", default=None)

define("redis_port", default=6379, type=int)

define("redis_db", default=0, type=int)

define("memcache_host", default=None)
