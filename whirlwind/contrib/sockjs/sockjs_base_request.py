from sockjs.tornado import SockJSConnection
from whirlwind.middleware import MiddlewareManager
from whirlwind.db.mongo import Mongo
import json

class SockjsBaseRequest(SockJSConnection):

	def __init__(self, application, request):
		SockJSConnection.__init__(self, application, request)
		self._current_user = None
		self.middleware_manager = MiddlewareManager(self)
		self.db = Mongo.db.ui
		self.middleware_manager.run_request_hooks()

	def get_current_user(self):
		return self._current_user

	def set_current_user(self, user):
		self._current_user = user

	def is_logged_in(self):
		return self.get_current_user() != None

	def send_message(self,message):
		if isinstance(message, basestring):
			self.send(message)
		else:
			self.send(json.dumps(message))