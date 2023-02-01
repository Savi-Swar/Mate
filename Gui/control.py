from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from numpy import ndarray
from camera import CamWindow, Camera
import cv2
import serial


from button import Button

ser = serial.Serial(port="/dev/cu.usbmodem101", baudrate=9600) 

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
    def keyPressEvent(self, e):
        if e.isAutoRepeat():
            if e.key() == Qt.Key_W:
                s = "FORWARD"
                ser.write(s.encode())

            if e.key() == Qt.Key_A:
                s = "LEFT"
                ser.write(s.encode())

            if e.key() == Qt.Key_S:
                s = "BACKWARD"
                ser.write(s.encode())

            if e.key() == Qt.Key_D:
                s = "RIGHT"   
                ser.write(s.encode())
            if e.key() == Qt.Key_U:
                s = "UP"
                ser.write(s.encode())

            if e.key() == Qt.Key_I:
                s = "DOWN"   
                ser.write(s.encode())
            if e.key() == Qt.Key_T:
                s = "CAMUP"
                ser.write(s.encode())

            if e.key() == Qt.Key_Y:
                s = "CAMDOWN"   
                ser.write(s.encode())
            if e.key() == Qt.Key_F:
                s = "CLAWUP"
                ser.write(s.encode())

            if e.key() == Qt.Key_C:
                s = "CLAWRIGHT"   
                ser.write(s.encode())
            if e.key() == Qt.Key_B:
                s = "CLAWLEFT"
                ser.write(s.encode())

            if e.key() == Qt.Key_V:
                s = "ClAWDOWN"   
                ser.write(s.encode())
            if e.key() == Qt.Key_N:
                s = "CLAWIN"
                ser.write(s.encode())

            if e.key() == Qt.Key_M:
                s = "CLAWOUT"   
                ser.write(s.encode())
        

    def keyReleaseEvent(self, e):
        s = "OFF"   
        ser.write(s.encode())
        


    def AutoWindow(self, checked):
        self.w = AutomationWindow()
        self.w.show()
    def Set(self, checked): 
        self.x = Manual()
        self.x.show()
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

    

