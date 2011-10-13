import redis
from whirlwind.util.singleton import Singleton

class Redis(Singleton):
    db = None
    
    def __init__(self):
        self.pool = None
        
    @staticmethod
    def create(**kwargs):
        r = redis.Redis(host=kwargs['host'],port=kwargs['port'],db=kwargs['db'])
        
        if 'debug' in kwargs:
            print r
        
        Redis.db = r