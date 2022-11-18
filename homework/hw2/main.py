import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidges import (
    QApplication
        )
from PyQt5.QtCore import pyqtSlot

class App(QDialog):
    def __init__(self):
        super().__init__()
        self.title = 'P76107116 Homework 2 :3'
        self.left = 600
        self.top = 600
        self.width = 600
        self.height = 600

        self._initUI()

    # Create all the buttons and input fields
    def _initUI(self):
        pass
if __name__=='__main__':
    app = QApplication(sys.argv)
    gui = App()
    sys.exit(app.exec_())
    pass
