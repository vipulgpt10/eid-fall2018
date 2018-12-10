#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.options

import tornado.httpserver
import time

from tornado.options import define, options

define("port", default=3000 , help="run on the given port", type=int)

global n
n = 0

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MainHandler)]
        settings = dict(debug=True)
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.websocket.WebSocketHandler):
	def on_message(self, message):
		global n
		n += 1
		print('message received:')
		self.write_message(message)
		if n == 3:
			n = 0
			time.sleep(1)
			#tornado.ioloop.IOLoop.instance().stop()

	def check_origin(self, origin):
		return True

	def open(self):
		print("A client connected.")

	def on_close(self):
		print("A client disconnected")
		
		
		
			
			
			
def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
