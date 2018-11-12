Name: Vipul Gupta
Project: Project 1

Installation Instruction:

Install the necessary libraries which are included.
use: sudo apt-get install python3-<library>

Connect DHT22 sensor at GPIO 4 (Pin #7)

Files: proj1.py and proj1.ui

To execute: python3 proj1.py

Project Work:

A PyQt5 GUI application to display temperature and humidity values on the window along with date and time.

Project Additions:

(1) Conversion of temperature into Farenheit and Kelvin from Celcius
(2) Periodic refresh of values.
(3) Periodic graph plotting and Average value display of latest 20 values
(4) Login protection
(5) Alarm: As per the set threshold, warning message will be displayed whether it is below threshold or above threshold.

References:

http://www.pyqtgraph.org/documentation/how_to_use.html

http://embeddedlaboratory.blogspot.com/2018/04/design-gui-using-pyqt5-on-raspberry-pi.html

https://stackoverflow.com/questions/11812000/login-dialog-pyqt

https://matplotlib.org/users/pyplot_tutorial.html

https://www.geeksforgeeks.org/list-methods-python/

https://www.geeksforgeeks.org/list-methods-in-python-set-2-del-remove-sort-insert-pop-extend/

https://www.pythonforbeginners.com/basics/python-datetime-time-examples