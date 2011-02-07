#grab the current path so we can set some thing automatically
import sys
app_path = sys.path[1]

#run mode
mode = "development"

#define a port for testing
port = 8000

#set static resources path
static_path = "%s/static" % app_path

#define a dir for mako to look for templates - relative to the app directory
template_dir = "%s/application/views" % app_path

#define a dir for mako to cache compiled templates
mako_modules_dir = "%s/tmp/mako_modules" % app_path

#define a log file... optionally just use the string 'db' to log it to mongo
log = "%s/tmp/log/application.log" % app_path

#define a database host
db_host = 'localhost'

#define the database port
db_port = 27017

#define the database name
db_name = 'test'

#you must define a cookie secret. you can use whirlwind-admin.py --generate-cookie-secret
cookie_secret = "setthistoyourowncookiesecret"

middleware_classes = [
    "whirlwind.middleware.flash.middleware.FlashMiddleware",
    "whirlwind.middleware.session.middleware.SessionMiddleware"
]