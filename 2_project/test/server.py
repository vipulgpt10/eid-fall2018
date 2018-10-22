
'''
https://os.mbed.com/cookbook/Websockets-Server
'''

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket

'''
This is a simple Websocket Echo server that uses the Tornado websocket handler.
Please run `pip install tornado` with python of version 2.7.9 or greater to install tornado.
This program will echo back the reverse of whatever it recieves.
Messages are output to the terminal for debuggin purposes. 
''' 
 
class WSHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print ('new connection')
      
	def on_message(self, message):
		print ('message received:  %s' % message)
        
		if (message == 'TlastC'):
			self.write_message('Last C req received; Timestamp 23:23:22')
			
		elif(message == 'TlastF'):
			self.write_message('Last F req received')
			
		elif(message == 'TavgC'):
			self.write_message('Avg C req received')
			
		elif(message == 'TavgF'):
			self.write_message('Avg F req received')
			
		elif(message == 'ThighC'):
			self.write_message('High C req received')
			
		elif(message == 'ThighF'):
			self.write_message('High F req received')
			
		elif(message == 'TlowC'):
			self.write_message('Low C req received')
			
		elif(message == 'TlowF'):
			self.write_message('Low F req received')
			
		elif(message == 'Hlast'):
			self.write_message('Last Hum req received')
			
		elif(message == 'Havg'):
			self.write_message('Avg Hum req received')
			
		elif(message == 'Hhigh'):
			self.write_message('High Hum req received')
			
		elif(message == 'Hlow'):
			self.write_message('Low Hum req received')
			
		else:
			self.write_message('Default req received')
 
	def on_close(self):
		print ('connection closed')
 
	def check_origin(self, origin):
		return True
 
application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print ('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
