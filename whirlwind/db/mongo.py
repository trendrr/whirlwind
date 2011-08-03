from mongokit import Connection
from tornado.options import options


'''
    Singleton mongo connection
'''
class Mongo(object):
    
    db = None
    
    def __init__(self):
        self.connection = None
    
    '''
        make this a singleton
    '''
    def __new__(type):
        if not '_the_instance' in type.__dict__:
            type._the_instance = object.__new__(type)
        return type._the_instance
    
    '''
        register a collection of mongokit model objects
    '''
    def register_models(self,models):
        self.connection.register(models)
    
    '''
        Accessor for ui specific database.
    '''   
    @property
    def ui(self):
        return self.connection[options.db_name]
    
    '''
        Useage:
        from whirlwind.db.mongo import Mongo
        Mongo.create(host='host.com', port='23423', username='mongouser', password='password')
    '''
    @staticmethod
    def create(**kwargs):
        db = Mongo()
        db.connection = Connection(kwargs['host'],kwargs['port'])
        Mongo.db = db
        if 'debug' in kwargs:
            print Mongo.db.connection
       
        