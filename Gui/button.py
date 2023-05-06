from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

class Button(QPushButton):
    def __init__(self, icon, tip):
        super().__init__()

        # self.setFocusPolicy(Qt.NoFocus)

        self.setStyleSheet("""
            QPushButton {
                background: rgb(255,163,185);
            }
            QPushButton:hover {
                background: rgb(255,123,98);
            }
        """)
        self.setText(tip)
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(40,40))
        self.setToolTip(tip)
