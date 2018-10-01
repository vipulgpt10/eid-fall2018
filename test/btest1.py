# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'basic1.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(612, 353)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 20, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAutoFillBackground(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(60, 200, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setAutoFillBackground(True)
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(90, 280, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(18)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(380, 280, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(18)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(290, 20, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setAutoFillBackground(True)
        self.label_3.setFrameShape(QtWidgets.QFrame.Box)
        self.label_3.setLineWidth(1)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(290, 80, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(18)
        self.label_4.setFont(font)
        self.label_4.setAutoFillBackground(True)
        self.label_4.setFrameShape(QtWidgets.QFrame.Box)
        self.label_4.setLineWidth(1)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(290, 140, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(18)
        self.label_5.setFont(font)
        self.label_5.setAutoFillBackground(True)
        self.label_5.setFrameShape(QtWidgets.QFrame.Box)
        self.label_5.setLineWidth(1)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(290, 200, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(18)
        self.label_6.setFont(font)
        self.label_6.setAutoFillBackground(True)
        self.label_6.setFrameShape(QtWidgets.QFrame.Box)
        self.label_6.setLineWidth(1)
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Temperatufre and Humidity"))
        self.label.setText(_translate("Dialog", "Temperature:"))
        self.label_2.setText(_translate("Dialog", "Humidity:"))
        self.pushButton.setText(_translate("Dialog", "Reftresh"))
        self.pushButton_2.setText(_translate("Dialog", "Exit"))
        
        # User code
        self.pushButton.clicked.connect(self.on_pushBut_clicked)
        self.pushButton_2.clicked.connect(self.exit_clicked)
        
	def on_pushBut_clicked(self):
		
		# Sensor should be set to Adafruit_DHT.DHT11,
		# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
		sensor = Adafruit_DHT.DHT22
		pin = 4
		
		
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		
		temp_k = temperature + 273.15
		temp_f = temperature*(1.8) + 32.0
		
		data = [0,2,1,4,5,3,9,6,0,7]
		
		#self.label_2.setText('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
		self.label_3.setText('{0:0.1f} *Celcius '.format(temperature))
		self.label_4.setText('{0:0.1f} *Farenheit  '.format(temp_f))
		self.label_5.setText('{0:0.1f} Kelvin  '.format(temp_k))
		
		self.label_6.setText('{0:0.1f}%'.format(humidity))
		
		pg.plot(data)
		
	def exit_clicked(self):
		sys.exit(app.exec_())
		
if name == "__main__":
	import sys
	app=QtWidgets.QApplication(sys.argv)
	widget=design_class()

