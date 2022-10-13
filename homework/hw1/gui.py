import sys
from methods import Calibration
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QGroupBox, QHBoxLayout, 
    QVBoxLayout, QPushButton, 
    QDialog, QWidget,
    QMainWindow, QFrame,
    QFileDialog, QComboBox, QLabel)
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
        
        self.intrinsic = None
        self.extrinsic_image = None

        # Good practice to have model class in view?
        self.cal = Calibration()
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

        # Extrinsic box within calibration section
        self.extrinsicBox = QGroupBox('1.3 Extrinsic')
        extLayout = QVBoxLayout()
        
        # Figure out how to make label look good
        #label = QLabel()
        #label.setText('Find Extrinsic')
        #label.setMargin(1)
        #extLayout.addWidget(label)
        
        qCombo = QComboBox()
        qCombo.addItems([str(i) for i in range(1, 16)])
        qCombo.currentIndexChanged.connect(self.set_extrinsic_image)
        extLayout.addWidget(qCombo)

        extBtn = QPushButton('Find Extrinsic', self)
        extBtn.clicked.connect(self.find_extrinsic_matrix)
        extLayout.addWidget(extBtn)

        calLayout.addLayout(extLayout) 

        # Set the main layout
        self.calibrationBox.setLayout(calLayout)
        
    def set_extrinsic_image(self, i):
        self.extrinsic_image = i + 1

    @pyqtSlot()
    def load_folder(self):
        self.dir_ = QFileDialog.getExistingDirectory(None, 'Select a folder', './', QFileDialog.ShowDirsOnly)
        print(f'Loading {self.dir_}')

        if self.dir_ == '':
            print('Choose a folder before advancing!')
            return

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

        if not self.dir_:
            print('You have to choose a directory first!')
            return

        self.cal.find_chessboard_corners_dir(self.dir_)
        print('Done')
 
    @pyqtSlot()
    def find_intrinsic_matrix(self):
        print('Finding intrinsice matrix...')
        self.cal.find_intrinsic_matrix()

    @pyqtSlot()
    def find_extrinsic_matrix(self):
        if self.extrinsic_image == None:
            print('You need to choose an image first!')
            return

        self.cal.find_extrinsic_matrix(self.extrinsic_image) 


app = QApplication(sys.argv)
gui = App()
sys.exit(app.exec_())
