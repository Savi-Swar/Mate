from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5 import QtCore
from numpy import ndarray
import cv2
import serial
import numpy as np
from cv.seagrass import count_squares





# ser = serial.Serial(port="/dev/cu.usbserial-140", baudrate=9600) 

class CamWindow(QWidget):
    def __init__(self):
    
        super().__init__()


        self.layout = QHBoxLayout()
        # self.layout.addWidget(Camera(0, "Rear View"))
        self.layout.addWidget(Camera(0, "Front View"))

        self.setLayout(self.layout)


class Camera(QWidget):
    def __init__(self, port, message, vertical=False):

        self.vertical = vertical
        
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)


        self.viewfinder = QLabel()
        self.viewfinder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(1000, 560)

        self.thread = VideoThread(port)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()


        self.layout = QVBoxLayout()
        self.layout.addWidget(self.viewfinder)

        self.label_1 = QLabel(message, self)
        self.label_1.setFont(QFont('Arial', 30))
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        
        self.label_1.setAlignment(QtCore.Qt.AlignHCenter)
        # self.label_1.setAlignment(QtCore.Qt.AlignTop)

        # self.layout.setContentsMargins(0,0,0,0)
        # self.layout.setSpacing(0)
        self.layout.addWidget(self.label_1)
        self.setLayout(self.layout)
        


    def close_event(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        if self.vertical:
            qt_img = qt_img.transformed(QTransform().rotate(90))
        self.viewfinder.setPixmap(qt_img)


    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(720, 480, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def capture_and_identify_coral(self):
        # Get the current frame from the camera
        current_frame = self.viewfinder.pixmap().toImage()

        # Convert the QImage to a numpy array (cv2 image)
        shape = (current_frame.height(), current_frame.width(), 3)
        current_frame = current_frame.convertToFormat(QImage.Format.Format_RGB888)
        ptr = current_frame.bits()
        ptr.setsize(current_frame.byteCount())
        current_frame = np.array(ptr).reshape(shape)

        # Convert the RGB888 image to BGR format for OpenCV
        current_frame = cv2.cvtColor(current_frame, cv2.COLOR_RGB2BGR)

        # Call the identify_coral function and print the results
        green_squares = count_squares(current_frame)
        print("Number of green squares:", green_squares)
        
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(ndarray)

    def __init__(self, port):
        super().__init__()

        self.running = True
        self.port = port

    def run(self):
        cap = cv2.VideoCapture(self.port)

        while self.running:
            ret, image = cap.read()
            if ret:
                self.change_pixmap_signal.emit(image)
                
        cap.release()
        
    def stop(self):
        self.running = False
        self.wait()
