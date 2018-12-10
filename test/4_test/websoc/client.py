#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect

import tornado.web
import tornado.websocket
import tornado.ioloop

import time


class Client(object):
    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout
        self.ioloop = IOLoop.instance()
        self.ws = None
        self.ms = 0
        self.length = 0
        #self.connect()
        #PeriodicCallback(self.keep_alive, 20000, io_loop=self.ioloop).start()    
        #self.ioloop.start()
        
    @gen.coroutine
    def connect(self):
        print ("trying to connect")
        
        try:
            self.ws = yield websocket_connect(self.url)
        except Exception as e:
            print("connection error")
        else:
            print("connected")
            self.ms = int(round(time.time()*1000))
            self.ws.write_message("msg")
            msg = yield self.ws.read_message()
            self.ms = int(round(time.time()*1000))-self.ms
            self.length = 1
            print(msg)
            self.ioloop.stop()


            
            
    @gen.coroutine
    def run(self):
        once = False
        while True:
            msg = yield self.ws.read_message()
            print(msg)
            if once:
                time.sleep(1)
                once = False
            else:
                time.sleep(1)
                once = True
            self.ws.write_message("msg")
            msg = yield self.ws.read_message()
            print('here')
            print(msg)
            if msg is None:
                print("connection closed")
                self.ws = None
                break

    def return_value(self):
        return [self.ms, self.length]


if __name__ == "__main__":
	client = Client("ws://localhost:3000", 5)
	
	for x in range(0, 3):
		print('Sending the '+str(x+1)+ 'Websocket msg')
		client.connect()
		client.ioloop.start()
		rc = client.return_value()
		print(rc[0])
		print(rc[1])
	
