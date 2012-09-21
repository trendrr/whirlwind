'''
Created on Sep 21, 2012

@author: matt

Here is an example of a chat websocket connection 
'''

#from whirlwind.contrib.sockjs.router_connection import connection
#from sockjs.tornado import SockJSConnection

#
#@connection('chat')
#class ChatConnection(SockJSConnection):
#    # Class level variable
#    participants = set()
#
#    def on_open(self, info):
#        self.send("Welcome from the server.")
#        self.participants.add(self)
#
#    def on_message(self, message):
#        # Pong message back
#        for p in self.participants:
#            p.send(message)
#
#    def on_close(self):
#        self.participants.remove(self)