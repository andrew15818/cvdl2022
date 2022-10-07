import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout, QPushButton, QDialog

# Subclass this layout to add layouts
class GUI(QDialog):
    def __init__(self, size=(500,500)):
        self.app = QtWidgets.QApplication(sys.argv)
        super(GUI, self).__init__()
        
        
        self.size = size
        #self.window = None

        self.mainLayout = QGroupBox()
        #
        # Create Window and Layouts, widgets
        self.start_window()
        self.create_widgets()
        
    def start_window(self):
        return self._get_window()

    def _get_window(self):
        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle('P76107116 Camera Calibration :3')
        self.window.resize(500, 500)
            
        return self.window
    
    def create_widgets(self):
        # Layout for loading files and two images individually
        self.leftLayout = QVBoxLayout()
        self.loadFolderBtn = QPushButton('Load Folder', self)
        self.loadFolderBtn.clicked.connect(self.load_folder)

        self.loadLImageBtn = QPushButton('Load L Image', self)
        self.loadLImageBtn.clicked.connect(self.load_image)

        self.loadRImageBtn= QPushButton('Load R Image', self)
        self.loadRImageBtn.clicked.connect(self.load_image)

        self.leftLayout.addWidget(self.loadFolderBtn)
        self.leftLayout.addWidget(self.loadLImageBtn)
        self.leftLayout.addWidget(self.loadRImageBtn)

        self.mainLayout.setLayout(self.leftLayout)
    def show(self):
        self.window.show()

    def load_image(self):
        pass
    def load_folder(self):
        pass

gui = GUI()
gui.show()
sys.exit(gui.app.exec_())
