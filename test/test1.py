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

class test_class(QDialog):
	def __init__(self):
		super(test_class,self).__init__()
		loadUi('test1.ui', self)
		self.setWindowTitle('TESTING PyQt5 GUI')
		self.pushButton.clicked.connect(self.on_pushBut_clicked)
		
	@pyqtSlot() 	#accepting signals
	def on_pushBut_clicked(self):
		
		# Sensor should be set to Adafruit_DHT.DHT11,
		# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
		sensor = Adafruit_DHT.DHT22
		pin = 4
		
		# Try to grab a sensor reading.  Use the read_retry method which will retry up
		# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		
		self.label_2.setText('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))



		
app=QApplication(sys.argv)
widget=test_class()
widget.show()
sys.exit(app.exec_())

