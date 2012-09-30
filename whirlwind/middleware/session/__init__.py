import pymongo, uuid, datetime
from datetime import timedelta
from whirlwind.db.mongo import Mongo

try:
	from config.settings import cookie_domain
except ImportError:
	pass
'''
MongoDb Session backend for Tornado 
'''
class Session():
	
	'''
	constructor... load or create the session
	'''
	def __init__(self,request_handler):
		#create a data changed flag
		self.data_changed = False
		self.saved = False
		
		#look for a sessionId
		# we allow a sessionId param, as this is necessary to get authenticated ajax requests from the 
		# api.
		self.session_id = request_handler.get_argument('xdt', request_handler.get_secure_cookie("sessionId"))
		
		
		if not self.session_id or not self.__lookup_session(request_handler) :
			self.__create()
			if 'cookie_domain' in locals():
				request_handler.set_secure_cookie("sessionId", self.session_id, domain=cookie_domain)
			else:
				request_handler.set_secure_cookie("sessionId", self.session_id)
#		print self.data
		
	'''
	destructor... updates the session db in mongo if our session data has been changed
	'''
	def __del__(self):
#		print "session destruction" 
		self.save()
		
		
	'''
		finalizes and saves the session.  if not called explicitly then 
		this will be called in the destructor.
	'''
	def save(self):
		if self.saved :
#			print 'already saved. skipping'
			return
			
		updateHours = 8
			
		if self['keep_logged_in'] :
			updateHours = 24*7 #if you checked keep me logged in then we roll by a week
		
		self.data['expires'] = datetime.datetime.utcnow() + timedelta(hours=updateHours)
		
		if self.data_changed:
			#update the timestamp for rolling session timeout
			#update the session data in mongo
			Mongo.db.ui.sessions.save(self.data)
		else :
			# just update the expires field so rolling timeout works.
			Mongo.db.ui.sessions.update({'_id':self.session_id},{'$set' : {'expires' : self.data['expires']}})	
#			print "SAVING session expires", self.data['expires']
		self.saved = True
		self.data_changed = False


	'''
	get a value from our session
	'''
	def __getitem__(self, key):
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
		self.data_changed = True
		self.saved = False
		
	'''
	delete a value from our session
	'''
	def __delitem__(self, key):
		del self.data[key]
		self.data_changed = True
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
		self.data = {
			'_id':self.session_id,
			'expires':datetime.datetime.utcnow() + timedelta(hours=8)
		}
		Mongo.db.ui.sessions.insert(self.data)
		
	'''
	lookup a session from the db based on the session id
	
	returns true on successful lookup, false if expired.
	'''
	def __lookup_session(self, request_handler):
		self.data = Mongo.db.ui.sessions.find_one({'_id': self.session_id})
		
		if not self.data:
			print "session not found in database"
			return False
		
		#check if this session has expired.
		print "session expires:", self.data['expires']
		if not self.data['expires'] or self.data['expires'] < datetime.datetime.utcnow() :
			print "SESSION EXPIRED!"
			self.destroy() #delete it from the database..
			return False
		
		#load the user
		if self['lookup_key']:
			key = self['lookup_key']
			user = Mongo.db.ui.users.User.find_one({key: self[key]})
			request_handler.set_current_user(user)
		elif self['username']:
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
		Mongo.db.ui.sessions.remove({'_id': self.session_id})
		self.data_changed = False
		self.saved = True