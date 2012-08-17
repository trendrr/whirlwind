'''
Created on Aug 16, 2012

@author: matt
'''
from whirlwind.core.bootstrap import Bootstrap
import os, logging, tornadio2
from os import path as op
import tornado.web, tornado.options
from tornado.options import options
from config import options_setup #@UnresolvedImport
from whirlwind.db.mongo import Mongo
from whirlwind.db.redis_interface import Redis
from whirlwind.contrib.tornadio2.router_connection import ConnectionLoader,\
	RouterConnection

class Bootstrap(Bootstrap):
	def __init__(self):
		Bootstrap.__init__(self)
		self.iorouter = None
	
	def init_redis(self):
		#connect to redis
		Redis.create(
			host=options.redis_host, 
			port=options.redis_port, 
			db=options.redis_db, 
			connection_pool=True
		)
		
	def init_mongo(self):
		#connect to mongo
		Mongo.create(
			host=options.db_host, 
			port=options.db_port
		)
	
	def init_iorouter(self):
		#init our url routes
		connections = ConnectionLoader.load('application.connections')
		
		#setup our multiplexed router connection 
		for conn in connections:
			RouterConnection.__endpoints__[conn[0]] = conn[1]

		# Create tornadio2 router
		self.iorouter = tornadio2.router.TornadioRouter(
			RouterConnection, dict(websocket_check=True)
		)

	def main(self,path):
		
		#parse the app config
		tornado.options.parse_config_file(os.path.join(path,'config/settings.py'))
		
		#parse the command line args
		tornado.options.parse_command_line()
		
		#init mongo singleton interface
		self.init_mongo()
		
		#init redis singleton interface
		self.init_redis()
		
		#init our url routes
		url_routes = self.init_routes()
		
		#init our tornadio2 router
		self.init_iorouter()
		
		#add in any app settings 
		app_settings = {
			"static_path": options.static_path,
			"cookie_secret": options.cookie_secret,
			"login_url": options.login_url,
			"flash_policy_port":843,
			"flash_policy_file":op.join(options.app_path, '/static/misc/flashpolicy.xml'),
			"socket_io_port":options.port
		}
		
		# Create application
		self.application = tornado.web.Application(
			self.iorouter.apply_routes(url_routes),
			**app_settings
		)
		
		#set a logger level
		logging.getLogger().setLevel(logging.DEBUG)
		
		#log our start message
		logging.info("Ready and listening")
		
		#start up the server
		tornadio2.server.SocketServer(self.application)
	
	@staticmethod
	def run(path):
		bootstrap = Bootstrap()
		bootstrap.main(path)