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
from thrust_control import SerialComms

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.frame = QWidget()
        self.frame.setStyleSheet("background-color: #ffe7f6;")

        # setting font and size

        self.speed_label = QLabel("H Speed: 0.4 + 0.00R, V Speed: 0.04 + 0.00R")
        self.status_label = QLabel("[]")
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

        self.frame.layout.addWidget(self.speed_label)
        self.frame.layout.addWidget(self.status_label)

        self.frame.layout.addWidget(self.b_auto)
        self.frame.layout.addWidget(self.b_settings)

        self.frame.layout.addWidget(self.b_sensor)

        self.frame.layout.setContentsMargins(0,0,0,0)
        self.frame.layout.setSpacing(0)
        
        self.frame.setLayout(self.frame.layout)
        self.setCentralWidget(self.frame)

        #self.serial_thread = SerialThread(ser)
        #self.serial_thread.received_data.connect(self.handle_received_data)
        #self.serial_thread.start()

        self.sc = SerialComms("/dev/cu.usbserial-1210")
        self.horiz_speed = 0.32
        self.vert_speed = 0.32
        self.horiz_offset = 0.0
        self.vert_offset = 0.0

        self.updateSpeedLabel()
 
    @pyqtSlot(str)
    def handle_received_data(self, data):
        print(data)

    def updateSpeedLabel(self):
        self.speed_label.setText(f"H Speed: {self.horiz_speed:.2f} {'+' if self.horiz_offset >= 0 else '-'} {abs(self.horiz_offset):.2f}, \
        V Speed: {self.vert_speed:.2f} {'+' if self.vert_offset >= 0 else '-'} {abs(self.vert_offset):.2f}")
        self.status_label.setText(str(self.sc.values))

    def keyEvent(self, key, m):
        if key == Qt.Key_W:
            self.sc.forward(self.horiz_speed * m, self.horiz_offset)
        if key == Qt.Key_S:
            self.sc.forward(-self.horiz_speed * m, self.horiz_offset)
        if key == Qt.Key_D:
            self.sc.yaw(self.horiz_speed * m)
        if key == Qt.Key_A:
            self.sc.yaw(-self.horiz_speed * m)
        if key == Qt.Key_Q:
            self.sc.up(self.vert_speed * m, self.vert_offset)
        if key == Qt.Key_E:
            self.sc.up(-self.vert_speed * m, self.vert_offset)
        if key == Qt.Key_L:
            self.sc.roll(self.vert_speed * m)
        if key == Qt.Key_J:
            self.sc.roll(-self.vert_speed * m)
        if key == Qt.Key_I:
            self.sc.pitch(self.vert_speed * m)
        if key == Qt.Key_K:
            self.sc.pitch(-self.vert_speed * m)

        # non-releasable
        if m == 1:
            if key == Qt.Key_1:
                self.horiz_speed -= 0.04
            if key == Qt.Key_2:
                self.horiz_speed += 0.04
            if key == Qt.Key_3:
                self.vert_speed -= 0.04
            if key == Qt.Key_4:
                self.vert_speed += 0.04
            if key == Qt.Key_5:
                self.horiz_offset -= 0.01
            if key == Qt.Key_6:
                self.horiz_offset += 0.01
            if key == Qt.Key_7:
                self.vert_offset -= 0.01
            if key == Qt.Key_8:
                self.vert_offset += 0.01    
            if key == Qt.Key_C:
                self.sc.claw(20)
            if key == Qt.Key_V:
                self.sc.claw(-20)
            if key == Qt.Key_Backspace:
                self.sc.reset()

        self.horiz_speed = max(0.04, min(1, self.horiz_speed))
        self.vert_speed = max(0.04, min(1, self.vert_speed))

        self.sc.update()
        self.updateSpeedLabel()

    # Layout 1
    def keyPressEvent(self, e):
        if e.isAutoRepeat():
            pass
        if not e.isAutoRepeat():
            self.keyEvent(e.key(), 1)

    def keyReleaseEvent(self, e):
        self.keyEvent(e.key(), -1)

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
