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


max_queue_messages = 1

region_name = 'us-east-2'
aws_access_key_id = 'AKIAJP6AFUMBOWK2ZPYA'
aws_secret_access_key = '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'
myQueueUrl='https://sqs.us-east-2.amazonaws.com/166395079358/Rpi.fifo'


sqs = boto3.resource('sqs', region_name=region_name,
		aws_access_key_id=aws_access_key_id,
		aws_secret_access_key=aws_secret_access_key)

queue = sqs.Queue(myQueueUrl)

#class for window dialog
class design_class(QDialog):
	
	def __init__(self):
		super(design_class,self).__init__()
		loadUi('proj3.ui', self)
		# buttons for refresh, exit
		self.pushButton.clicked.connect(self.on_pushBut_clicked)
		self.pushButton_2.clicked.connect(self.exit_clicked)
		self.pushButton_3.clicked.connect(self.cflag_clicked)	
		
		# 0 - celcius, 1 - farenheit
		self.tflag = 0
		self.label.setText('Will get Temperature values in Celcius')
		
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
