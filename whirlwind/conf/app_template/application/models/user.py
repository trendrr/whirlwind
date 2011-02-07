from mongokit import *
import datetime
import hashlib, hmac, base64, re
from whirlwind.db.mongo import Mongo
from tornado import options

'''
normalizes a username or email address
'''
def normalize(username):
    if not username :
        return None
    #allow legal email address
    name = username.strip().lower()
    name = re.sub(r'[^a-z0-9\\.\\@_\\-~#]+', '', name)
    name = re.sub('\\s+', '_',name)
    
    #don't allow $ and . because they screw up the db.
    name = name.replace(".", "")
    name = name.replace("$", "")
    return name;

@Mongo.db.connection.register
class User(Document):
    structure = {
                 '_id':unicode,
                 'email':unicode,
                 'roles':list,
                 'password':unicode,
                 'created_at':datetime.datetime,
                 'history' : {
                              'last_login' : datetime.datetime,
                              'num_logins' : long
                              },
                 'timezone':unicode,
                 'suspended_at':datetime.datetime,
                 }
    use_dot_notation=True
    
    @staticmethod
    def normalize(username):
        return normalize(username)
        
    
    @staticmethod
    def lookup(username):
        return Mongo.db.ui.users.User.find_one({'_id' : normalize(username)})
        
        
    '''
    creates a new user instance. unsaved
    '''
    @staticmethod
    def instance(username, password):
        
        username = normalize(username)
        user = User()
        user.roles = [username]
        user['_id'] = username
        user.password = hashlib.sha1(password).hexdigest()
        user.created_at = datetime.datetime.utcnow()
        user.history = {
                        'num_logins' : 0
                        }
        return user
    
    
    def add_role(self, role):
        if not self.get('roles', False):
            self['roles'] = []
        
        if role in self['roles'] :
            return
        self['roles'].append(role)
        
    def remove_role(self, role):
        if not self.get('roles', False):
            self['roles'] = []
        try :
            while True:
                self['roles'].remove(role)
        except :
            pass
        
    def has_role(self, role):
        if not self.get('roles', False):
            self['roles'] = []
        if isinstance(role, basestring):
            return role in self['roles']
        else:
            for r in role:
                if r in self['roles']:
                    return True
    
    def name(self):
        return self._id
    
    def get_timezone(self):
        tz = self.get('timezone', None)
        if tz :
            return tz
        return 'America/New_York'
                
    def is_suspended(self):
        if self.get('suspended_at', None) == None :
            return False
        return self.suspended_at < datetime.datetime.utcnow()
     
