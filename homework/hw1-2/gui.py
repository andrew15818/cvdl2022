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
        self.title = 'P76107116 Feature matching :3'
        self.left = 500
        self.top =  500
        self.width = 500 
        self.height = 500
        self.initUI()
        self.dir_ = None
        self.leftImg = None
        self.rightImg = None

        # Imgs used for feature detection
        self.siftImage = None
        self.matchImage = None
        self.features = methods.Features()
        
       
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.createHorizontalLayouts()
        
        windowLayout = QHBoxLayout()
        windowLayout.addWidget(self.siftBox)
        self.setLayout(windowLayout)
        
        self.show()
    def make_button(self, name, layout, callback):
        btn = QPushButton(name)
        btn.clicked.connect(callback)
        layout.addWidget(btn)

        return btn

    def createHorizontalLayouts(self):
        # Layout for Problem 4
        self.siftBox = QGroupBox('4. SIFT')
        siftLayout = QVBoxLayout()

        btn = self.make_button('Load Image 1', siftLayout, self.load_sift_image)
        #siftLayout.addWidget(btn)

        btn = self.make_button('Load Image 2', siftLayout, self.load_match_image)
        #siftLayout.addWidget(btn)

        btn = self.make_button('4.1 Keypoints', siftLayout, self.find_keypoints)
        #siftLayout.addWidget(btn)

        btn = self.make_button('4.2 Matched Keypoints', siftLayout, self.match_images)
        
        self.siftBox.setLayout(siftLayout)

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
            'Select an image', '.', 
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
    def find_keypoints(self):
        if not self.siftImage:
            print('Please choose first!')
            return
        self.features.find_image_features(self.siftImage)
        

    @pyqtSlot()
    def match_images(self):
        if not self.siftImage or not self.matchImage:
            print('Load both images first!')
            return
        self.features.match_images(self.siftImage, self.matchImage)

        
    # image for which we find the features, then match 
    @pyqtSlot()
    def load_sift_image(self):
        self.siftImage = self._load_image()        
        print(f'loaded {self.siftImage}')
    
    @pyqtSlot()
    def load_match_image(self):
        self.matchImage = self._load_image()
        print(f'loaded {self.matchImage}')


     
app = QApplication(sys.argv)
gui = App()
sys.exit(app.exec_())
