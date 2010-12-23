#run mode
mode = "development"

#define a port for testing
port = 8888

#set static resources path
static_path = '/path/to/your/python/apps/whirlwind/static'

#define a dir for mako to look for templates - relative to the app directory
template_dir = '/path/to/your/python/apps/whirlwind/templates'

#define a dir for mako to cache compiled templates
mako_modules_dir = '/path/to/your/python/apps/whirlwind/templates/mako_modules'

#define a database host
db_host = 'localhost'

#define the database port
db_port = 27017

cookie_secret = "fillmein"

#should we enable sessions
enable_sessions = True