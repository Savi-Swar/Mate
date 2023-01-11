from PyQt5.QtWidgets import QVBoxLayout, QWidget, QMainWindow, QWidget, QApplication
from PyQt5.QtCore import Qt

from button import Button

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(26, 26, 26);
                border-top-right-radius: 10px
            }
        """)

        self.parent = QWidget()

        self.info_button = Button('ui/icons/prac.png', 'Info')
        self.info_button.clicked.connect(self.info)

        self.console_button = Button('ui/icons/prac.png', 'Console')
        self.console_button.clicked.connect(self.console)

        # self.console_window = ConsoleWindow()
        self.automation_button = Button('ui/icons/prac.png', 'Automation')
        self.automation_button.clicked.connect(self.automation)

        self.quit_button = Button('ui/icons/prac.png', 'Quit')
        self.quit_button.clicked.connect(self.quit)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)

        self.layout.addWidget(self.info_button)
        self.layout.addWidget(self.console_button)
        self.layout.addWidget(self.automation_button)
        self.layout.addWidget(self.quit_button)

        self.setLayout(self.layout)

        self.setFixedWidth(60)
    def automation(self):
        self.automation_button.setDisabled(True)
        self.parent.automation_window.show()

    def info(self):
        if self.parent.thruster_display.isVisible():
            self.parent.thruster_display.hide()
            self.parent.axis_display.hide()
        else:
            self.parent.thruster_display.show()
            self.parent.axis_display.show()

        print(self.height())


    def console(self):
        if self.parent.console.isVisible():
            self.parent.console.hide()
        else:
            self.parent.console.show()

    def quit(self):
        # access camera from other windows and close + threads
        # self.parent.status_thread.stop()
        print('\033[93m\033[1mSuccessfully stopped Crimson UI\033[0m') 

        exit()


if __name__ == '__main__':
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()