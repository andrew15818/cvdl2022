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

<<<<<<< HEAD
        self.mainLayout = QHBoxLayout()
        #
        # Create Window and Layouts, widgets
        self.start_window()
        self.create_widgets()
        self.mainLayout.addWidget(self.groupBox) 
        self.setLayout(self.mainLayout)
        print(self.children())

=======
        # Create Window and Layouts, widgets
        self.start_window()
        self.create_widgets()
        self.show() 
>>>>>>> 17845a8c942bcddbc4bc8a2ce373b8dd07948ae9
    def start_window(self):
        return self._get_window()

    def _get_window(self):
        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle('P76107116 Camera Calibration :3')
        self.window.resize(self.size[0], self.size[1])
            
        return self.window
    
    def create_widgets(self):
        # Layout for loading files and two images individually
        self.groupBox = QGroupBox("Files")
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

        self.groupBox.setLayout(self.leftLayout)
    def show(self):
        self.window.show()

    def load_image(self):
        print('Loaded image')
        pass
    def load_folder(self):
        print('Loaded folder')
        pass

class App(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'P76107116 camera calibration :3'
        self.left = 500
        self.top =  500
        self.width = 500 
        self.height = 500
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.createHorizontalLayout()
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        
        self.show()
    
    def createHorizontalLayout(self):
        self.horizontalGroupBox = QGroupBox("Files")
        layout = QVBoxLayout()
        
        buttonBlue = QPushButton('Load Folder', self)
        buttonBlue.clicked.connect(self.load_folder)
        layout.addWidget(buttonBlue)
        
        buttonRed = QPushButton('Load L Image', self)
        buttonRed.clicked.connect(self.load_image)
        layout.addWidget(buttonRed)
        
        buttonGreen = QPushButton('Load R Image', self)
        buttonGreen.clicked.connect(self.load_image)
        layout.addWidget(buttonGreen)
        
        self.horizontalGroupBox.setLayout(layout)
    
    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

    def load_folder(self):
        print('Loading folder')
    def load_image(self):
        print('Loading image')
 

gui = GUI()
gui.show()
sys.exit(gui.app.exec_())
