#!/usr/bin/python

# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys 
import Adafruit_DHT

			# system functions
from PyQt5.QtCore import pyqtSlot #as PQS		 QtCore classs -- pyqtSlot func
from PyQt5.QtWidgets import QApplication,QDialog
from PyQt5.uic import loadUi 
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import pyqtgraph as pg




class design_class(QDialog):
	
	def __init__(self):
		super(design_class,self).__init__()
		loadUi('basic2.ui', self)
		#self.setWindowTitle('TESTING PyQt5 GUI')
		self.pushButton.clicked.connect(self.on_pushBut_clicked)
		self.pushButton_2.clicked.connect(self.exit_clicked)
		self.pushButton_4.clicked.connect(self.set_threshold)
		
		self.threshold_temp = 200.0
		self.threshold_hum = 100.0
		
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.timer_loop)
		self.timer.start(3000)
		
		
	@pyqtSlot() 	#accepting signals
	def on_pushBut_clicked(self):
		self.set_values()
		
	def exit_clicked(self):
		sys.exit(app.exec_())
		
	def timer_loop(self):
		self.set_values()
		self.check_threshold()
		self.timer.start(2000)
		
	def set_values(self):
		
		sensor = Adafruit_DHT.DHT22
		pin = 4
		
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		
		#conversion into Kelvin and Farenheit
		self.temp_k = temperature + 273.15
		self.temp_f = temperature*(1.8) + 32.0	
		self.temp_c = temperature
		self.hum = humidity

		self.label_3.setText('{0:0.1f} deg Celcius '.format(self.temp_c))
		self.label_4.setText('{0:0.1f} deg Farenheit  '.format(self.temp_f))
		self.label_5.setText('{0:0.1f} Kelvin  '.format(self.temp_k))
		
		self.label_6.setText('{0:0.1f}%'.format(humidity))
		

		
	def set_threshold(self):
		
		if self.lineEdit.text() == '' or self.lineEdit_2.text() == '':
			self.label_7.setText('Enter both Temperature and Humidity Threshold')
			return
		
		self.threshold_temp = float(self.lineEdit.text())
		self.threshold_hum = float(self.lineEdit_2.text())
		
		#self.label_7.setText(str(self.threshold_temp) + str(self.threshold_hum))
		
	def check_threshold(self):
		
		if self.hum >= self.threshold_hum and self.temp_c >= self.threshold_temp:
			self.label_7.setText('Humidity and Temperature Thresholds crossed!!')
			
		else:
			if self.temp_c >= self.threshold_temp:
				self.label_7.setText('Temperature Threshold crossed!!')
			
			else:
				if self.hum >= self.threshold_hum:
					self.label_7.setText('Humidity Threshold crossed!!')
				else:
					self.label_7.setText('Below Threshold')
			
			
		
		
			
		print (self.hum)
		print (self.temp_c)
		print (self.threshold_hum)
		print (self.threshold_temp)
			
		
		
		
	def plot_graph(self):
		l_tempc = []
		l_tempf = []
		l_tempk = []
		l_hum = []
		#pg.plot(data)

# login class
class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
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
            self.textPass.text() == 'vip_eid'):
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Bad user or password')



		
app=QApplication(sys.argv)

login = Login()

if login.exec_() == QtWidgets.QDialog.Accepted:
	widget=design_class()
	widget.show()
	sys.exit(app.exec_())

'''
while(1):
	widget.on_pushBut_clicked()
	time.sleep(2)
'''
