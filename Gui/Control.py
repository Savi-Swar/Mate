from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from numpy import ndarray
from camera import CamWindow, Camera
import cv2
import serial
import struct
import threading
import time

from button import Button

ser = serial.Serial(port='/dev/cu.usbserial-1220', baudrate=9600, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS)

# Check if the connection is successful

HEADER = b'\xab'
FOOTER = b'\xb3'
forwByte = b'\xA3'
backByte = b'\xA4'
upByte = b'\xA5'
downByte = b'\xA6'
rightByte = b'\xA7'
leftByte = b'\xA8'
servOpenByte = b'\xA9'
servCloseByte = b'\xA0'
stopByte = b'\xB5'
msg = b'\xB7'
precision = b'\xF1'
regular = b'\xF2'
rapid = b'\xF3'
pitchUpByte = b'\xC1'
pitchDownByte = b'\xC2'
rollRightByte = b'\xC3'
rollLeftByte = b'\xC4'
speed = 2

def foo(msg):
    if type(msg) == bytes:
        msg = msg[0]
    out = 0b0
    for i in range(8):
        bit = msg & 1
        msg >>= 1
        out |= (0 if bit else 1)
        out <<= 1
    return bytes([out >> 1])

def sendSerial(data):

        ser.write(HEADER)
        if speed == 1:
            speedByte = precision
        elif speed == 2:
            speedByte = regular
        elif speed == 3:
            speedByte = rapid
        ser.write(speedByte)
        ser.write(data)
        ser.write(FOOTER)
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.frame = QWidget()
        self.frame.setStyleSheet("background-color: #ffe7f6;")

        
        # setting font and size


        self.b_auto = Button("Gui/img/automation.png", "Automation Panel")
        self.b_settings = Button("Gui/img/automation.png", "Settings Panel")
        self.b_sensor = Button("Gui/img/automation.png", "Sensor Panel")

        self.b_sensor.move(500,500)
        self.frame.layout = QVBoxLayout()
        
        self.logo = QLabel(self)
        self.pixmap = QPixmap('logo.png')
        self.logo.setPixmap(self.pixmap)
        self.logo.resize(self.pixmap.width(),
                          self.pixmap.height())
        
        self.label = QLabel("Your Text", self)  # Add this line
  
        self.label.setFont(QFont('Arial', 25))
        self.cam = CamWindow()
        self.addBar = QHBoxLayout()
        addBarWidget = QWidget()
        addBarWidget.setLayout(self.addBar)
        self.frame.layout.addWidget(addBarWidget)
        self.frame.layout.addWidget(self.cam)
        self.b_auto.clicked.connect(self.AutoWindow)
        self.b_settings.clicked.connect(self.Set)

        self.frame.layout.addWidget(self.logo)

        self.frame.layout.addWidget(self.b_auto)
        self.frame.layout.addWidget(self.b_settings)

        self.frame.layout.addWidget(self.b_sensor)

        self.frame.setLayout(self.frame.layout)
        self.setCentralWidget(self.frame)

        self.serial_thread = SerialThread(ser)
        self.serial_thread.received_data.connect(self.handle_received_data)
        self.serial_thread.start()
 
    @pyqtSlot(str)
    def handle_received_data(self, data):
        print(data)

    # Layout 1
    def keyPressEvent(self, e):
        global msg
        global speed
        if e.isAutoRepeat():

            if e.key() == Qt.Key_W: # FORWARD
                if msg != forwByte:
                    msg = forwByte
                    sendSerial(forwByte)


            if e.key() == Qt.Key_A: # LEFT
                if msg != leftByte:
                    msg = leftByte
                    sendSerial(leftByte)


            if e.key() == Qt.Key_S: # BACKWARD
                if msg != backByte:
                    msg = backByte
                    sendSerial(backByte)


            if e.key() == Qt.Key_D: # RIGHT
                if msg != rightByte:

                    msg = rightByte
                    sendSerial(rightByte)

          
            if e.key() == Qt.Key_U: #UP
                if msg != upByte:

                    msg = upByte
                    sendSerial(upByte)


            if e.key() == Qt.Key_I: # DOWN
                if msg != downByte:

                    msg = downByte
                    sendSerial(downByte)

            if e.key() == Qt.Key_X: # OFF
                    msg = stopByte
                    sendSerial(stopByte)

            if e.key() == Qt.Key_T:
                if msg != pitchUpByte:

                    msg = pitchUpByte
                    sendSerial(pitchUpByte)
            if e.key() == Qt.Key_Y:
                if msg != pitchDownByte:

                    msg = pitchDownByte
                    sendSerial(pitchDownByte)
            if e.key() == Qt.Key_G:
                if msg != rollLeftByte:

                    msg = rollLeftByte
                    sendSerial(rollLeftByte)
            if e.key() == Qt.Key_H:
                if msg != rollRightByte:

                    msg = rollRightByte
                    sendSerial(rollRightByte)
          
           
           
        if not e.isAutoRepeat():
            if e.key() == Qt.Key_O:
                speed = 3
            if e.key() == Qt.Key_K:
                speed = 2
            if e.key() == Qt.Key_L:
                speed = 1
            if e.key() == Qt.Key_N:

                if msg != servOpenByte:

                    msg = servOpenByte
                    sendSerial(servOpenByte)

           

            if e.key() == Qt.Key_M:
                if msg != servCloseByte:

                    msg = servCloseByte
                    sendSerial(servCloseByte)


            
                

    def keyReleaseEvent(self, e):
        global msg
        msg = stopByte
        sendSerial(stopByte)

    def AutoWindow(self, checked):
        self.w = AutomationWindow()
        self.w.show()
    def Set(self, checked): 
        self.x = Manual()
        self.x.show()
class SerialThread(QThread):
    received_data = pyqtSignal(str)

    def __init__(self, port):
        super(SerialThread, self).__init__()
        self.port = port

    def run(self):
        while True:
            raw_data = self.port.read()
            print(f"Raw data: {raw_data}")
            data = raw_data.hex()
            self.received_data.emit(data)
class AutomationWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.coral_button = Button('ui/icons/docking_icon.png', 'Identify Coral')
        self.transect_button = Button('ui/icons/transect_icon.png', 'Transect line')
        self.frogs_button = Button('ui/icons/morts_icon.png', 'Count Frogs')
        self.dock_button = Button('ui/icons/measure_icon.png', 'Dock ROV')
        self.layout.setSpacing(10)
        self.layout.addWidget(self.coral_button)
        self.layout.addWidget(self.transect_button)
        self.layout.addWidget(self.dock_button)
        self.layout.addWidget(self.frogs_button)
        self.setLayout(self.layout)
        self.setWindowTitle('Automation')
# class SensorWindow(QWidget):
#     """
#     This "window" is a QWidget. If it has no parent, it
#     will appear as a free-floating window as we want.
#     """
#     def __init__(self):
#         super().__init__()
#         self.layout = QVBoxLayout()
#         self.coral_button = Button('ui/icons/docking_icon.png', 'Identify Coral')
#         self.transect_button = Button('ui/icons/transect_icon.png', 'Transect line')
#         self.frogs_button = Button('ui/icons/morts_icon.png', 'Count Frogs')
#         self.dock_button = Button('ui/icons/measure_icon.png', 'Dock ROV')
#         self.layout.setSpacing(10)
#         self.layout.addWidget(self.coral_button)
#         self.layout.addWidget(self.transect_button)
#         self.layout.addWidget(self.dock_button)
#         self.layout.addWidget(self.frogs_button)
#         self.setLayout(self.layout)
#         self.setWindowTitle('Automation')
class Manual(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.percent = QLabel('Thruster Percentage: 62%')
        self.six = Button('ui/icons/docking_icon.png', 'Six Thrusters')
        self.four = Button('ui/icons/transect_icon.png', 'Four Thrusters')
        self.manual = Button('ui/icons/transect_icon.png', 'Moor Array')


        self.layout.setSpacing(10)
        self.layout.addWidget(self.percent)
        self.layout.addWidget(self.six)    
        self.layout.addWidget(self.four)
        self.layout.addWidget(self.manual)


        self.setLayout(self.layout)
        self.setWindowTitle('Settings')


if __name__ == '__main__':
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
