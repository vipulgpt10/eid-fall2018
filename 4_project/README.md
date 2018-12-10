#Project 4
Team Members: Vipul Gupta and Vipraja Patil Project: Project 4 (Protocol Profiling + AWS Client Server)

Installation Instruction:

Install the necessary libraries which are included. use: sudo pip3 install tornado

Connect DHT22 sensor at GPIO 4 (Pin #7)

Server Files: project3.py, project3.ui, login.ui protocol_server.py

Client Files: proj4.py, proj4.ui

To execute server for AWS iot: python3 project3.py userid: vipraja password:vipraja
To execute server for Protocol profiling: python3 protocol_server.py

To execute client: python3 proj4.py userid: vipulgpt10 password: lol

Project Work:
Protocol Profiling: Calculates the total and average roundtrip time of protocols: MQTT using Mosquitto broker, CoAP and Websocket

A PyQt5 GUI application to display temperature and humidity values on the window along with date and time and uploading data to AWS Server. 
It also has a client side (using tornado) which fetches the values from AWS server and displays on the interface.

References:

https://os.mbed.com/cookbook/Websockets-Server

http://www.pyqtgraph.org/documentation/how_to_use.html

http://embeddedlaboratory.blogspot.com/2018/04/design-gui-using-pyqt5-on-raspberry-pi.html

https://stackoverflow.com/questions/11812000/login-dialog-pyqt

https://matplotlib.org/users/pyplot_tutorial.html

https://www.geeksforgeeks.org/list-methods-python/

https://www.geeksforgeeks.org/list-methods-in-python-set-2-del-remove-sort-insert-pop-extend/

https://www.pythonforbeginners.com/basics/python-datetime-time-examples
