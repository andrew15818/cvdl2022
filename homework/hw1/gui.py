import sys
import methods
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QGroupBox, QHBoxLayout, 
    QVBoxLayout, QPushButton, 
    QDialog, QWidget,
    QMainWindow, QFrame,
    QFileDialog)
from PyQt5.QtCore import pyqtSlot

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
        
        self.createHorizontalLayouts()
        
        windowLayout = QHBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        windowLayout.addWidget(self.calibrationBox)
        self.setLayout(windowLayout)
        
        self.show()
    
    def createHorizontalLayouts(self):
        # Upload files
        self.horizontalGroupBox = QGroupBox("Load Images")
        layout = QVBoxLayout()
        
        loadFolderBtn = QPushButton('Load Folder', self)
        loadFolderBtn.clicked.connect(self.load_folder)
        layout.addWidget(loadFolderBtn)
        
        loadLImageBtn = QPushButton('Load L Image', self)
        loadLImageBtn.clicked.connect(self.load_image)
        layout.addWidget(loadLImageBtn)
        
        loadRImageBtn = QPushButton('Load R Image', self)
        loadRImageBtn.clicked.connect(self.load_image)
        layout.addWidget(loadRImageBtn)

        self.horizontalGroupBox.setLayout(layout)

        # Calibration Section
        self.calibrationBox = QGroupBox('1. Calibration')
        calLayout = QVBoxLayout()

        calBtn = QPushButton('1.1 Find Corners', self)
        calBtn.clicked.connect(self.find_corners)
        calLayout.addWidget(calBtn)

        intBtn = QPushButton('1.2 Find Intrinsic', self)
        intBtn.clicked.connect(self.find_intrinsic_matrix)
        calLayout.addWidget(intBtn)

        self.calibrationBox.setLayout(calLayout)
       
    @pyqtSlot()
    def load_folder(self):
        dir_ = QFileDialog.getExistingDirectory(None, 'Select a folder', './', QFileDialog.ShowDirsOnly)
        print(dir_)
        if dir_ == '':
            print('Choose a folder before advancing!')
            return

        methods.find_chessboard_corners_dir(dir_)
        print('Loading folder')

    @pyqtSlot()
    def load_image(self):
        img = QFileDialog.getOpenFileName(None, 
            'Select an image', './', 
            "Images (*.bmp *.png *jpg)")
        if img == None:
            print('Choose an image!')
            return 
        
        print('Loading image')

    @pyqtSlot()
    def find_corners(self):
        print('Finding corners in image...')
 
    @pyqtSlot()
    def find_intrinsic_matrix(self):
        print('Finding intrinsice matrix...')

app = QApplication(sys.argv)
gui = App()
sys.exit(app.exec_())
