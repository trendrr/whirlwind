import memcache
from whirlwind.util.singleton import Singleton

class Memcache(Singleton):
    db = None
    
    def __init__(self):
        self.pool = None
        
    @staticmethod
    def create(**kwargs):
        
        mc = memcache.Client([kwargs['host']], debug=0)
        if 'debug' in kwargs:
            print kwargs
            print mc
        
        Memcache.db = mc
        print Memcache.db
        
    @staticmethod
    def get(key):
        if Memcache.db == None:
            return None
        else:
            return Memcache.db.get(key)
        
    @staticmethod
    def set(key,val):
        if Memcache.db == None:
            return False
        else:
            return Memcache.db.set(key,val)