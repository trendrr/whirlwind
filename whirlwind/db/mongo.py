from mongokit import Connection
from tornado.options import options
from whirlwind.util.singleton import Singleton

'''
    Singleton mongo connection
'''
class Mongo(Singleton):
    
    db = None
    
    def __init__(self):
        self.connection = None
    
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
       
        