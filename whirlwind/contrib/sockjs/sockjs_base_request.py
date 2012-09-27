from sockjs.tornado import SockJSConnection
from whirlwind.db.mongo import Mongo
import json


class SockjsBaseRequest(SockJSConnection):

	def __init__(self, session):
		SockJSConnection.__init__(self, session)
		self.db = Mongo.db.ui

	def send_message(self,message):
		if isinstance(message, basestring):
			self.send(message)
		else:
			self.send(json.dumps(message))
