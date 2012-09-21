'''
Created on Aug 17, 2012
@author: matt
'''
from sockjs.tornado import SockJSRouter, SockJSConnection

class RouterConnection(SockJSConnection):
	__endpoints__ = {}

	def on_open(self, info):
		print 'Router', repr(info)

class ConnectionLoader(object):
	
	@staticmethod
	def load(package_name):
		loader = ConnectionLoader()
		return loader.init_connections(package_name)
		
	def init_connections(self,package_name):
		import pkgutil,sys
		
		package = __import__(package_name)
		controllers_module = sys.modules[package_name]
		
		prefix = controllers_module.__name__ + "."
		
		for importer, modname, ispkg in pkgutil.iter_modules(controllers_module.__path__, prefix):
			module = __import__(modname)
		
		#grab the routes defined via the route decorator
		connections = connection.get_connections()

		return connections

class connection(object):
	_connections = []

	def __init__(self, uri):
		self._uri = uri

	def __call__(self, _connection):
		"""gets called when we class decorate"""
		self._connections.append((self._uri, _connection))
		return _connection

	@classmethod
	def get_connections(self):
		return self._connections