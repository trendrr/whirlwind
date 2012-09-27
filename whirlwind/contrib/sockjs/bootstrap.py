'''
Created on Aug 16, 2012

@author: matt
'''
from whirlwind.core.bootstrap import Bootstrap as WhirlwindBootstrap
import os, logging
# from os import path as op
import tornado.web, tornado.options
from tornado.options import options
from config import options_setup
from whirlwind.db.mongo import Mongo
from whirlwind.contrib.sockjs.router_connection import ConnectionLoader,RouterConnection
from whirlwind.contrib.sockjs.multiplex import MultiplexConnection
from sockjs.tornado import SockJSRouter


class Bootstrap(WhirlwindBootstrap):
	def __init__(self):
		WhirlwindBootstrap.__init__(self)
		self.connection_router = None

	def init_mongo(self):
		#connect to mongo
		Mongo.create(
			host=options.db_host, 
			port=options.db_port
		)
	
	def init_connection_router(self):
		#init our url routes
		connections = ConnectionLoader.load('application.connections')
		
		#setup our multiplexed router connection 
		for conn in connections:
			RouterConnection.__endpoints__[conn[0]] = conn[1]

		# Create multiplexer
		router = MultiplexConnection.get(**RouterConnection.__endpoints__)

		# Register multiplexer
		self.connection_router = SockJSRouter(router, '/echo')


	def main(self,path):
		
		#parse the app config
		tornado.options.parse_config_file(os.path.join(path,'config/settings.py'))
		
		#parse the command line args
		tornado.options.parse_command_line()
		
		#init mongo singleton interface
		self.init_mongo()
		
		#init our standard tornado routes
		url_routes = self.init_routes()
		
		#init our sockjs connection router
		self.init_connection_router()
		
		#add in any app settings 
		app_settings = {
			"static_path": options.static_path,
			"cookie_secret": options.cookie_secret,
			"login_url": options.login_url
		}
		
		# Create application
		self.application = tornado.web.Application(
			self.connection_router.urls + url_routes,
			**app_settings
		)
		
		#set a logger level
		logging.getLogger().setLevel(logging.DEBUG)
		
		#log our start message
		logging.info("Ready and listening")

		#listen on our desired port
		self.application.listen(options.port)

		#start the tornado IO loop
		tornado.ioloop.IOLoop.instance().start()
	
	@staticmethod
	def run(path):
		bootstrap = Bootstrap()
		bootstrap.main(path)
