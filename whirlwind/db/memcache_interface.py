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