import redis
from whirlwind.util.singleton import Singleton

class Redis(Singleton):
	db = None
	
	def __init__(self):
		pass
	
	@staticmethod
	def create(**kwargs):
		if 'connection_pool' in kwargs and kwargs['connection_pool'] == True:
			r = redis.Redis(
				host=kwargs['host'],
				port=kwargs['port'],
				db=kwargs['db'],
				connection_pool=redis.ConnectionPool()
			)
		else:
			r = redis.Redis(
				host=kwargs['host'],
				port=kwargs['port'],
				db=kwargs['db']
			)
		
		if 'debug' in kwargs:
			print r
		
		Redis.db = r