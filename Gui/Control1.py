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


# With these lines:
ser = serial.Serial(port='COM12', baudrate=9600, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS)

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
pitchUpByte = b'\xC1'
pitchDownByte = b'\xC2'
rollRightByte = b'\xC3'
rollLeftByte = b'\xC4'
precision = b'\xF1'
regular = b'\xF2'
rapid = b'\xF3'
#optional if using IMU:
hoverByte = b'\xD1'
stopByte = b'\xB5'
buffer = []
speed = 2 #1 = precision, 2 = regular, 3 = precision
speedByte = None


def sendSerial(data):
    ser.write(HEADER)
    match speed:
        case 1:
            speedByte = precision
        case 2:
            speedByte = regular
        case 3:
            speedByte = rapid
    ser.write(speedByte)
    ser.write(data)
    ser.write(FOOTER)

# def foo(msg):
#     if type(msg) == bytes:
#         msg = msg[0]
#     out = 0b0
#     for i in range(8):
#         bit = msg & 1
#         msg >>= 1
#         out |= (0 if bit else 1)
#         out <<= 1
#     return bytes([out >> 1])

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
  
        # self.label.setFont(QFont('Arial', 25))
        self.cam = CamWindow()
        self.addBar = QHBoxLayout()
        # self.frame.layout.addWidget(self.addBar)
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
        if e.isAutoRepeat():

            if e.key() == Qt.Key_W: # FORWARD
                # ser.write(HEADER)
                # ser.write(forwByte)
                # ser.write(FOOTER)
                #buffer.append(forwByte)    
                sendSerial(forwByte)            
                    #ser.write(foo(struct.pack("<c", foo(HEADER))))
                    #ser.write(struct.pack("<c", foo(1)))
                    #ser.write(struct.pack("<c", foo(FOOTER)))

                    # val = struct.pack(">cHc", HEADER, 0, FOOTER)
                    # print(f"writing {val}")
                    # ser.write(val)



            if e.key() == Qt.Key_A: # LEFT
                # ser.write(HEADER)
                # ser.write(leftByte)
                # ser.write(FOOTER)
                #buffer.append(leftByte)
                sendSerial(leftByte)
                #     #ser.write(struct.pack(">cHc", HEADER, 2, FOOTER))

            if e.key() == Qt.Key_S: # BACKWARD
                # ser.write(HEADER)
                # ser.write(backByte)
                # ser.write(FOOTER)
                #buffer.append(backByte)
                sendSerial(backByte)
                #     #ser.write(struct.pack(">cHc", HEADER, 1, FOOTER))

            if e.key() == Qt.Key_D: # RIGHT
                # ser.write(HEADER)
                # ser.write(rightByte)
                # ser.write(FOOTER)
                #buffer.append(rightByte)
                sendSerial(rightByte)
                #     #ser.write(struct.pack(">cHc", HEADER, 3, FOOTER))
            
            if e.key() == Qt.Key_U: #UP
                # ser.write(HEADER)
                # ser.write(upByte)
                # ser.write(FOOTER)
                #buffer.append(upByte)
                sendSerial(upByte)
                #     #ser.write(struct.pack(">cHc", HEADER, 5, FOOTER))

            if e.key() == Qt.Key_I: # DOWN
                # ser.write(HEADER)
                # ser.write(downByte)
                # ser.write(FOOTER)
                #buffer.append(downByte)
                sendSerial(downByte)
                #     #ser.write(struct.pack(">cHc", HEADER, 4, FOOTER))
            #if e.key() == Qt.Key_X: # OFF
                # ser.write(HEADER)
                # ser.write(stopByte)
                # ser.write(FOOTER)
                #buffer.append(stopByte)
                #     #ser.write(struct.pack(">cHc", HEADER, 7, FOOTER))
            
                # if e.key() == Qt.Key_T:
                #     s = "CAMUP"
                #     ser.write(struct.pack(">cHc", HEADER, 7, FOOTER))
            
                # if e.key() == Qt.Key_Y:
                #     s = "CAMDOWN"   
                #     ser.write(struct.pack(">cHc", HEADER, 8, FOOTER))
            
            if e.key() == Qt.key.T:
                sendSerial(pitchUpByte)
            if e.key() == Qt.key.Y:
                sendSerial(pitchDownByte)
            if e.key() == Qt.key.G:
                sendSerial(rollLeftByte)
            if e.key() == Qt.key.H:
                sendSerial(rollRightByte)
            if e.key() == Qt.Key_N:
                # ser.write(HEADER)
                # ser.write(servOpenByte)
                # ser.write(FOOTER)
                #buffer.append(servOpenByte)
                sendSerial(servOpenByte)
                # #     s = "CLAWOPEN"
                #     ser.write(struct.pack(">cHc", HEADER, 9, FOOTER))

            if e.key() == Qt.Key_M:
                # ser.write(HEADER)
                # ser.write(servCloseByte)
                # ser.write(FOOTER)
                #buffer.append(servCloseByte)
                sendSerial(servCloseByte)
                # #     s = "CLAWCLOSE"   
                #     ser.write(struct.pack(">cHc", HEADER, 10, FOOTER))
            
                # if e.key() == Qt.Key_1:
                #     s = "Inc"
                #     ser.write(s.encode())
                # if e.key() == Qt.Key_2:
                #     s = "Dec"
                #     ser.write(s.encode())
                # if e.key() == Qt.Key_Z:
                #     s = "TiltUp"
                #     ser.write(s.encode())
                # if e.key() == Qt.Key_X:
                #     s = "TiltDown"
                #     ser.write(s.encode())
            if e.key() == Qt.Key_O:
                speed = 3
            if e.key() == Qt.Key_K:
                speed = 2
            if e.key() == Qt.Key.L:
                speed = 1


                

    def keyReleaseEvent(self, e):
        sendSerial(stopByte)
        #s = "OFF"
        #ser.write(s.encode())





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
            data = foo(raw_data).hex()
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
