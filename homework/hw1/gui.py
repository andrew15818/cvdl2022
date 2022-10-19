import sys
import methods
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QGroupBox, QHBoxLayout, 
    QVBoxLayout, QPushButton, 
    QDialog, QWidget,
    QMainWindow, QFrame,
    QFileDialog, QComboBox, QLabel,
    QLineEdit)
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
        self.dir_ = None
        self.leftImg = None
        self.rightImg = None
        
        self.intrinsic = None
        self.extrinsic_image = None

        # Good practice to have model class in view?
        self.cal = methods.Calibration()
        self.proj = methods.Projection()
        self.stereo = methods.Stereo()

        self.projectionText = None
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.createHorizontalLayouts()
        
        windowLayout = QHBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        windowLayout.addWidget(self.calibrationBox)
        windowLayout.addWidget(self.projectionBox)
        windowLayout.addWidget(self.stereoBox)
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
        loadLImageBtn.clicked.connect(self.load_left_image)
        layout.addWidget(loadLImageBtn)
        
        loadRImageBtn = QPushButton('Load R Image', self)
        loadRImageBtn.clicked.connect(self.load_right_image)
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

        extBtn = QPushButton('1.3 Find Extrinsic', self)
        extBtn.clicked.connect(self.find_extrinsic_matrix)
        extLayout.addWidget(extBtn)
        calLayout.addLayout(extLayout) 
        
        distBtn = QPushButton('1.4 Show Distortion', self)
        distBtn.clicked.connect(self.show_distortion)
        calLayout.addWidget(distBtn)

        undistBtn = QPushButton('1.5 Show Result', self)
        undistBtn.clicked.connect(self.show_undistorted)
        calLayout.addWidget(undistBtn)
        

        # Set the main layout
        self.calibrationBox.setLayout(calLayout)

        # Layout for problem 2
        self.projectionBox = QGroupBox('2. Projection')
        projLayout = QVBoxLayout()

        textBox = QLineEdit(maxLength=6)
        textBox.textEdited.connect(self.set_projection_text)
        projLayout.addWidget(textBox)
    
        showOnBtn = QPushButton('2.1 Show Words on Board', self) 
        showOnBtn.clicked.connect(self.project_on_board)
        projLayout.addWidget(showOnBtn)

        self.projectionBox.setLayout(projLayout)

        # Layout for Problem 3
        self.stereoBox = QGroupBox('3. Stereo Disparity Map')
        stereoLayout = QVBoxLayout()

        dispBtn = QPushButton('3.1 Stereo Disparity Map.')
        dispBtn.clicked.connect(self.show_stereo_disparity)
        stereoLayout.addWidget(dispBtn)

        corrBtn = QPushButton('3.2 Show Corresponding Point')
        corrBtn.clicked.connect(self.show_corresponding_point)
        stereoLayout.addWidget(corrBtn)

        self.stereoBox.setLayout(stereoLayout)

    def set_extrinsic_image(self, i):
        self.extrinsic_image = i + 1
    
    def set_projection_text(self, text):
        self.projectionText = text 

    @pyqtSlot()
    def load_folder(self):
        self.dir_ = QFileDialog.getExistingDirectory(None, 'Select a folder', './', QFileDialog.ShowDirsOnly)
        print(f'Loading {self.dir_}')

        if self.dir_ == '':
            print('Choose a folder before advancing!')
            return

    def _load_image(self, left=True):
        img = QFileDialog.getOpenFileName(None, 
            'Select an image', './', 
            "Images (*.bmp *.png *jpg)")
        if img == None:
            print('Choose an image!')
            return 
        if left:
            self.leftImg = img[0] 
        else:
            self.rightImg = img[0]
        return img[0]

    @pyqtSlot()
    def load_left_image(self):
        self.leftImg = self._load_image()
        print(f'loaded {self.leftImg}')
    
    @pyqtSlot()
    def load_right_image(self):
        self.rightImg = self._load_image()
        print(f'loaded {self.rightImg}')

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

    @pyqtSlot()
    def show_distortion(self):
        self.cal.show_distortion()

    @pyqtSlot()
    def show_undistorted(self):
        if self.extrinsic_image == None:
            print('You need to choose an image first!')
            return
        self.cal.show_undistorted(self.extrinsic_image)
            
    @pyqtSlot()
    def project_on_board(self):
        if self.projectionText == None:
            print('Type in a word first!')
            return
        elif self.dir_ == None:
            print('Choose a directory first!')
            return
        self.proj.project_on_board(self.dir_, self.projectionText)
    
    @pyqtSlot()
    def show_stereo_disparity(self):
        if not self.leftImg or not self.rightImg:
            print('Make sure you selected both images!')
            return
        self.stereo.get_disparity(self.leftImg, self.rightImg) 
    
    @pyqtSlot()
    def show_corresponding_point(self):
        if not self.leftImg or not self.rightImg:
            print('Come back with the images.')
            return
        self.stereo.find_corresponding_point() 
        


     
app = QApplication(sys.argv)
gui = App()
sys.exit(app.exec_())
