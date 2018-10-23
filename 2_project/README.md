Team Members: Vipul Gupta and Vipraja Patil
Project: Project 2 (Webserver)

Installation Instruction:

Install the necessary libraries which are included.
use: sudo pip3 install tornado

Connect DHT22 sensor at GPIO 4 (Pin #7)

Server Files: project2.py, project2.ui, login.ui
Client Files: client.html

To execute servevr: python3 project2.py
userid: vipraja
password:vipraja

To execute client: Open the client.html in any web browser.
userid: vipul
password: lol

Project Work:

A PyQt5 GUI application to display temperature and humidity values on the window along with date and time and building up a database on client using mySQL.
It also has a webserver on client side (using tornado) which fetches the values from server and displays on the web browser.

Project Additions:

(1) Conversion of temperature into Farenheit and Kelvin from Celcius
(2) Login authentication step both in client and server
(3) Multi-threaded execution of client code.

References:

https://os.mbed.com/cookbook/Websockets-Server

http://www.pyqtgraph.org/documentation/how_to_use.html

http://embeddedlaboratory.blogspot.com/2018/04/design-gui-using-pyqt5-on-raspberry-pi.html

https://stackoverflow.com/questions/11812000/login-dialog-pyqt

https://matplotlib.org/users/pyplot_tutorial.html

https://www.geeksforgeeks.org/list-methods-python/

https://www.geeksforgeeks.org/list-methods-in-python-set-2-del-remove-sort-insert-pop-extend/

https://www.pythonforbeginners.com/basics/python-datetime-time-examples