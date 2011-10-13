import pymongo, uuid, datetime
from datetime import timedelta
from whirlwind.db.mongo import Mongo
from whirlwind.db.memcache_interface import Memcache
from application.models.user import User
import memcache

try:
    import simplejson as json
except ImportError:
    import json

'''
Redis Session backend for Tornado 


sudo easy_install python-memcache

'''
class Session():
    
    '''
    constructor... load or create the session
    '''
    def __init__(self,request_handler):
        
        self.saved = False
        
        #look for a sessionId
        # we allow a sessionId param, as this is necessary to get authenticated ajax requests from the 
        # api.
        self.session_id = request_handler.get_argument('xdt', request_handler.get_secure_cookie("sessionId"))
        
        
        if not self.session_id or not self.__lookup_session(request_handler) :
            self.__create()
            request_handler.set_secure_cookie("sessionId", self.session_id)
#        print self.data
        
    '''
    destructor... updates the session db in redis if our session data has been changed
    '''
    def __del__(self):
#        print "session destruction" 
        self.save()
        
        
    '''
        finalizes and saves the session.  if not called explicitly then 
        this will be called in the destructor.
    '''
    def save(self):
        if self.saved :
#            print 'already saved. skipping'
            return
            
        updateHours = 1
            
        if self['keep_logged_in'] :
            updateHours = 24*7 #if you checked keep me logged in then we roll by a week
        
        expires = datetime.datetime.utcnow() + timedelta(hours=updateHours)
        # Save the data as a json string
        Memcache.db.set(self.session_id, json.dumps(self.data),expires);
       
        self.saved = True


    '''
    get a value from our session
    '''
    def __getitem__(self, key):
        if key == '_id' :
            return self.session_id
        
        try:
            return self.data[key]
        except KeyError:
            self.data.update({key:None})
            return None
   
    '''
    set a value in our session
    '''
    def __setitem__(self, key, value):
        if not self.session_id:
            #no session yet so lets create a session
            self.__create()
        self.data[key] = value
        self.saved = False
        
    '''
    delete a value from our session
    '''
    def __delitem__(self, key):
        del self.data[key]
        self.saved = False
    
    '''
    get a session value or return an optional default value
    '''
    def get(self,key,default=None):
        #grab a value from the session object
        val = self.__getitem__(key)
        #if the val isn't there return the default
        if val == None:
            return default
        else:
            return val
    
    '''
    private helper functions
    '''
    def __create(self):
        #generate a session id
        self.__generate_session_id()
        #insert the new doc into mongo
        print "creating new session"
        #store the session_id in a secure cookie
        self.data = {}
        
    '''
    lookup a session from the db based on the session id
    
    returns true on successful lookup, false if expired.
    '''
    def __lookup_session(self, request_handler):
        val = Memcache.db.get(self.session_id)
        if not val :
            return False

        self.data = json.loads(val)        
        #load the user
        if self['username']:
            user = Mongo.db.ui.users.User.find_one({'_id': self['username']})
            request_handler.set_current_user(user)

        return True
        
    '''
    generate a uniqe id for our session
    '''
    def __generate_session_id(self):
        self.session_id = str(uuid.uuid4())
    
    
    '''
    destroys the current session.  deletes from the database. 
    '''
    def destroy(self):
        Memcache.db.delete(self.session_id)
        self.saved = True