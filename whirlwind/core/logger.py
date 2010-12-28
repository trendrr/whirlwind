import pymongo, datetime
from whirlwind.db.mongo import Mongo

'''
Database logger
'''
class Logger():

    def log(self, type, message, user=None, extended_info=None):
        log_data = {
            'created':datetime.datetime.utcnow(),
            'message':message,
            'type':type
        }
        
        if user:
            log_data['user'] = user._id
            
        if extended_info:
            log_data['extended_info'] = extended_info
        print log_data    
        Mongo.db.ui.log.insert(log_data)

    @staticmethod
    def message(type, message, user=None, extended_info=None):
        logger = Logger()
        logger.log(type, message, user, extended_info)
    
    @staticmethod
    def access(self, message, user, extended_info):
        Logger.message('access', message, user, extended_info)
        
    @staticmethod
    def info(message, user=None):
        Logger.message('info', message, user)
    
    @staticmethod
    def debug(message, user=None):
        Logger.message('debug', message, user)
    
    @staticmethod
    def error(message, user=None):
        Logger.message('error', message, user)
    
    @staticmethod
    def warn(message, user=None):
        Logger.message('warn', message, user)
