import sys
from PyQt5 import QtWidgets

class GUI():
    def __init__(self, size=(500,500)):
        self.size = size
        self.window = None

    def start_window(self):
        return self._get_window()

    def _get_window(self):
        if self.window == None:
            self.window = QtWidgets.Qwidget()
            self.window.resize(500, 500)
            
        return self.window


