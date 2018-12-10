#!/usr/bin/python


import sys 
import boto3
import json


# system functions and importing libraries
from PyQt5.QtCore import pyqtSlot #		 QtCore classs -- pyqtSlot func
from PyQt5.QtWidgets import QApplication,QDialog
from PyQt5.uic import loadUi 
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import matplotlib.pyplot as plt
import numpy as np
import time
import datetime


import paho.mqtt.client as mqtt
import socket
import time

import asyncio
from aiocoap import *


from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect

import tornado.web
import tornado.websocket
import tornado.ioloop

import time


max_queue_messages = 1

region_name = 'us-east-2'
aws_access_key_id = 'AKIAJP6AFUMBOWK2ZPYA'
aws_secret_access_key = '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'
myQueueUrl='https://sqs.us-east-2.amazonaws.com/166395079358/Rpi.fifo'


sqs = boto3.resource('sqs', region_name=region_name,
		aws_access_key_id=aws_access_key_id,
		aws_secret_access_key=aws_secret_access_key)

queue = sqs.Queue(myQueueUrl)

#average times for roundtrip
global time1 
global time2 
global time3 

time1 = [0] *20
time2 = [0] *20
time3 = [0] *20

global a1
global a2
global a3

a1 = 0
a2 = 0
a3 = 0


# MQTT
class MQTTClient(object):
    def __init__(self):
        self.response = None
        self.ms = 0
        self.client = mqtt.Client()
        self.client.connect('10.0.0.246', 1883, 60)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe("topic/out")

    def on_message(self, client, userdate, msg):
        self.ms = int(round(time.time()*1000))-self.ms
        msg = msg.payload.decode().split(',')
        length = len(msg)
        self.response = [self.ms, length]
        self.client.disconnect()
        

    def publish(self, topic, msg):
        self.response = None
        self.ms = int(round(time.time()*1000))
        self.client.publish(topic, msg)
        while self.response == None:
            self.client.loop_forever()
        self.client.reconnect()
        return self.response

    def disconnect(self):
        self.client.disconnect()
        
# COAP
class COAPClient(object):
    def __init__(self):
        self.ms = 0
        self.length = 0
        self.context = None
        asyncio.get_event_loop().run_until_complete(self.create_context())

    async def create_context(self):
        self.context = await Context.create_client_context()

    async def put(self, msg):
        self.ms = int(round(time.time()*1000))
        request = Message(code=PUT, payload=bytes(msg, 'utf-8'))
        request.opt.uri_host = '10.0.0.236'
        request.opt.uri_path = ("other", "block")
        response = await self.context.request(request).response
        self.ms = int(round(time.time()*1000))-self.ms
        self.length = len(response.payload.decode().split(','))
    
    def return_value(self):
        return [self.ms, self.length]

# WebSocket

class Client(object):
    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout
        self.ioloop = IOLoop.instance()
        self.ws = None
        self.ms = 0
        self.length = 0
        
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


    def return_value(self):
        return [self.ms, self.length]


def start_profiling():
	
	global time1 
	global time2 
	global time3 

	global a1 
	global a2 
	global a3 
	mqtt_instance = MQTTClient()     
	
	for x in range(0, 20):
		print('[MQTT] Publishing #'+str(x+1))
		rc = mqtt_instance.publish("topic/incoming", 'msg')
		print('[MQTT] Received')
		print(rc[0])
		time1.append(rc[0])
	a1 = sum(time1)/20.0
		
	coap_instance = COAPClient()
	for x in range(0, 20):
		print('[COAP] PUT msg #'+str(x+1))
		asyncio.get_event_loop().run_until_complete(coap_instance.put('msg'))
		print('[COAP] Received')
		rc = coap_instance.return_value()
		print(rc[0])
		time2.append(rc[0])
	a2 = sum(time2)/20.0
		
	client = Client("ws://10.0.0.236:3000", 5)
	for x in range(0, 20):
		print('Websocket msg#'+str(x+1))
		client.connect()
		client.ioloop.start()
		rc = client.return_value()
		print(rc[0])
		time3.append(rc[0])
	a3 = sum(time3)/20.0



#class for window dialog
class design_class(QDialog):
	
	def __init__(self):
		super(design_class,self).__init__()
		loadUi('proj4.ui', self)
		# buttons for refresh, exit
		self.pushButton.clicked.connect(self.on_pushBut_clicked)
		self.pushButton_2.clicked.connect(self.exit_clicked)
		self.pushButton_3.clicked.connect(self.cflag_clicked)
		self.pushButton_4.clicked.connect(self.profile)	
		
		# 0 - celcius, 1 - farenheit
		self.tflag = 0
		self.label.setText('Will get Temperature values in Celcius')
		self.label_2.setText('0')
		self.label_3.setText('0')
		self.label_4.setText('0')
		
		#list for graph
		self.tlast_list = [0] * 10
		self.tavg_list = [0] * 10
		self.thigh_list = [0] * 10
		self.tlow_list = [0] * 10
		
		self.hlast_list = [0] * 10
		self.havg_list = [0] * 10
		self.hhigh_list = [0] * 10
		self.hlow_list = [0] * 10
		
		self.stime_list = [0] * 10
		self.etime_list = [0] * 10
		
		self.idx_list = [0] * 10
		
		for i in range(10):
			self.idx_list[i] = i + 1
		
		
	@pyqtSlot() 	#accepting signals
	# Get values button
	def on_pushBut_clicked(self):
		
		self.receive_values()
		self.update_table()
		self.plot_graph()
		
	# exit button
	def exit_clicked(self):
		sys.exit(app.exec_())
		
	# C/F Flag button
	def cflag_clicked(self):
		if (self.tflag == 0):
			self.tflag = 1
			self.label.setText('Will get Temperature values in Farenheit')
			
		else:
			self.tflag = 0
			self.label.setText('Will get Temperature values in Celcius')
			
	def profile(self):
		global time1 
		global time2 
		global time3 

		global a1 
		global a2 
		global a3 
			
		start_profiling()
		self.label_2.setText('{0:0.4f} ms'.format(a1))
		self.label_3.setText('{0:0.4f} ms'.format(a2))
		self.label_4.setText('{0:0.4f} ms'.format(a3))
		
		self.plot_graph_protocol()
			
	

	# receive values from AWS SQS FIFO
	def receive_values(self):
		messages_to_delete = []
		
		self.tlast_list = [0] * 10
		self.tavg_list = [0] * 10
		self.thigh_list = [0] * 10
		self.tlow_list = [0] * 10
		
		self.hlast_list = [0] * 10
		self.havg_list = [0] * 10
		self.hhigh_list = [0] * 10
		self.hlow_list = [0] * 10
		
		self.stime_list = [0] * 10
		self.etime_list = [0] * 10
		
		message = queue.receive_messages(
			MaxNumberOfMessages=10,
			WaitTimeSeconds=1) 
			
		my_time = datetime.datetime.now().strftime("%H:%M:%S %y-%m-%d")
	
		for msg in message:
			# process message body
			body = json.loads(msg.body)
			
			self.stime_list.pop(0)
			self.etime_list.pop(0)

			self.tlast_list.pop(0)
			self.tavg_list.pop(0)
			self.thigh_list.pop(0)
			self.tlow_list.pop(0)
			
			self.hlast_list.pop(0)
			self.havg_list.pop(0)
			self.hhigh_list.pop(0)
			self.hlow_list.pop(0)
			
			if(self.tflag == 0):
				self.tlast_list.append(body['TClast'])
				self.tavg_list.append(body['TCavg'])
				self.thigh_list.append(body['TChigh'])
				self.tlow_list.append(body['TClow'])
			else:
				self.tlast_list.append(body['TFlast'])
				self.tavg_list.append(body['TFavg'])
				self.thigh_list.append(body['TFhigh'])
				self.tlow_list.append(body['TFlow'])	
			
			self.stime_list.append(body['time'])
			self.etime_list.append(str(my_time))	
			
			self.hlast_list.append(body['Hlast'])
			self.havg_list.append(body['Havg'])
			self.hhigh_list.append(body['Hhigh'])
			self.hlow_list.append(body['Hlow'])
			
			
			# add message to delete
			messages_to_delete.append({
				'Id': msg.message_id,
				'ReceiptHandle': msg.receipt_handle
			})

		# if you don't receive any notifications the
		# messages_to_delete list will be empty
		if len(messages_to_delete) == 0:
			return
		# delete messages to remove them from SQS queue
		# handle any errors
		else:
			delete_response = queue.delete_messages(
				Entries=messages_to_delete)

	#Update values in table
	def update_table(self):
		
		#update start time
		for i in range(10):
			self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(self.stime_list[9-i]))
			
		#update end time
		for i in range(10):
			self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(self.etime_list[9-i]))
			
		#update last temp
		for i in range(10):
			self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(self.tlast_list[9-i]))
		
		#update avg temp
		for i in range(10):
			self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(self.tavg_list[9-i]))
			
		#update high temp
		for i in range(10):
			self.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(self.thigh_list[9-i]))
			
		#update low temp
		for i in range(10):
			self.tableWidget.setItem(i, 5, QtWidgets.QTableWidgetItem(self.tlow_list[9-i]))
			
		#update last hum
		for i in range(10):
			self.tableWidget.setItem(i, 6, QtWidgets.QTableWidgetItem(self.hlast_list[9-i]))
			
		#update avg hum
		for i in range(10):
			self.tableWidget.setItem(i, 7, QtWidgets.QTableWidgetItem(self.havg_list[9-i]))
			
		#update high hum
		for i in range(10):
			self.tableWidget.setItem(i, 8, QtWidgets.QTableWidgetItem(self.hhigh_list[9-i]))
			
		#update low hum
		for i in range(10):
			self.tableWidget.setItem(i, 9, QtWidgets.QTableWidgetItem(self.hlow_list[9-i]))
			
		
	# plot both the graphs after updating values
	def plot_graph(self):
		
		plt.clf()
		
		plt.subplot(311)
		plt.plot(self.idx_list, self.tlast_list, 'b',
				self.idx_list, self.tavg_list, 'r--',
				self.idx_list, self.thigh_list, 'g^',
				self.idx_list, self.tlow_list, 'y*')
		plt.xlabel('Blue-Latest, Red-Average, Green-Highest, Yellow-Lowest')
		plt.ylabel('Temperature (Celcius)')
		plt.title('Temperature Graph')
		plt.grid(True)
		
		plt.subplot(313)
		plt.plot(self.idx_list, self.hlast_list, 'b',
				self.idx_list, self.havg_list, 'r--',
				self.idx_list, self.hhigh_list, 'g^',
				self.idx_list, self.hlow_list, 'y*')
		plt.xlabel('Blue-Latest, Red-Average, Green-Highest, Yellow-Lowest')
		plt.ylabel('Humidity (%)')
		plt.title('Humidity Graph')
		plt.grid(True)
		plt.draw()			
		plt.pause(0.001)
		plt.ion()
		plt.show()
		
	# plot both the graphs after updating values
	def plot_graph_protocol(self):
		
		global time1 
		global time2 
		global time3 

		global a1 
		global a2 
		global a3 
		
		sum1 = sum(time1)
		sum2 = sum(time2)
		sum3 = sum(time3)
		
		idx = [1, 2, 3]
		pkts = [20, 20, 20]
		avgt = [a1, a2, a3]
		totalt = [sum1, sum2, sum3]
		
		plt.clf()
		
		plt.subplot(511)
		plt.bar(idx, pkts, color='b', width=0.5)
		plt.xlabel('1 - MQTT, 2 - CoAP, 3 - WebSocket')
		plt.ylabel('Number of packets')
		plt.title('Packets sent/received')
		plt.grid(True)
		
		plt.subplot(513)
		plt.bar(idx, avgt, color='g', width=0.5)
		plt.xlabel('1 - MQTT, 2 - CoAP, 3 - WebSocket')
		plt.ylabel('Time (ms)')
		plt.title('Average roundtime')
		plt.autoscale(tight=True)
		plt.grid(True)
		
		plt.subplot(515)
		plt.bar(idx, totalt, color='g', width=0.5)
		plt.xlabel('1 - MQTT, 2 - CoAP, 3 - WebSocket')
		plt.ylabel('Time (ms)')
		plt.title('Total roundtime')
		plt.autoscale(tight=True)
		plt.grid(True)
		plt.draw()			
		plt.pause(0.001)
		plt.ion()
		plt.show()

		

# login class
class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setWindowTitle('LOGIN')
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        if (self.textName.text() == 'vipulgpt10' and
            self.textPass.text() == 'lol'):
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Bad user or password')



#run application		
app=QApplication(sys.argv)

login = Login()

if login.exec_() == QtWidgets.QDialog.Accepted:
	widget=design_class()
	widget.show()
	sys.exit(app.exec_())
