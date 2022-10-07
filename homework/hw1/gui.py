import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QGroupBox, QHBoxLayout, 
    QVBoxLayout, QPushButton, 
    QDialog, QWidget,
    QMainWindow, QFrame)

# Subclass this layout to add layouts
class GUI(QMainWindow):
    def __init__(self, size=(500,500)):
        self.app = QtWidgets.QApplication(sys.argv)
        super(GUI, self).__init__()
        
        
        self.size = size
        #self.window = None

        # Create Window and Layouts, widgets
        self.start_window()
        self.create_widgets()
        self.show() 
    def start_window(self):
        return self._get_window()

    def _get_window(self):
        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle('P76107116 Camera Calibration :3')
        self.window.resize(500, 500)
            
        return self.window
    
    def create_widgets(self):
        self.mainFrame = QtWidgets.QFrame(self)
        self.mainFrame.setStyleSheet('background-color: rgba(150, 0, 0, 1);')
        self.setCentralWidget(self.mainFrame)
        self.leftLayout = QtWidgets.QVBoxLayout(self.mainFrame)

        loadFolderFrame = QtWidgets.QFrame(self.mainFrame)
        self.leftLayout.addWidget(loadFolderFrame)
        loadFolderLayout = QtWidgets.QHBoxLayout(loadFolderFrame)
       
        loadFolderBtn = QtWidgets.QPushButton('Load Folder', loadFolderFrame) 
        loadFolderLayout.addWidget(loadFolderBtn)
    def show(self):
        self.window.show()

    def load_image(self):
        print('Loaded image')
        pass
    def load_folder(self):
        print('Loaded folder')
        pass


gui = GUI()
gui.show()
sys.exit(gui.app.exec_())
