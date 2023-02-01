from PyQt5.QtWidgets import QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtCore import Qt

from .button import Button

import cv2
import numpy as np
import sys


class AutomationControlBar(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(26, 26, 26);
                border-top-right-radius: 10px
            }
        """)

        self.parent = parent

        self.coral_button = Button('ui/icons/docking_icon.png', 'Identify Coral')

        self.transect_button = Button('ui/icons/transect_icon.png', 'Transect line')

        self.frogs_button = Button('ui/icons/morts_icon.png', 'Count Frogs')

        self.dock_button = Button('ui/icons/measure_icon.png', 'Dock ROV')

       



        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)

        self.layout.addWidget(self.coral_button)
        self.layout.addWidget(self.transect_button)
        self.layout.addWidget(self.dock_button)
        self.layout.addWidget(self.frogs_button)


        self.setLayout(self.layout)

        self.setFixedWidth(60)


    # def docking(self):
    #     selection, _ = QFileDialog.getOpenFileName(self, 'Select image', 'captures/IMAGES', 'Images (*.png *.jpg)')

    #     if selection:
    #         self.parent.selection.scrolling_label.setText(f'DOCKING\n{selection}')

    #         Docking(selection, None)

    # def transect(self):
    #     TransectLine(self.parent.parent.grid.down_cam.thread.cap, 0.1)
    #     self.parent.selection.scrolling_label.setText('TRANSECT LINE')

