'''
Created on Aug 16, 2012

@author: matt

Here is an example of a chat websocket connection 
'''

#import tornadio2
#from whirlwind.db.redis_interface import Redis
#from whirlwind.contrib.tornadio2.router_connection import connection
#
#@connection('/chat')
#class ChatConnection(tornadio2.conn.SocketConnection):
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