import sys
from q5methods import q5Methods
from PyQt5.QtGui import QPixmap
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

DATAPATH = 'Dataset_OpenCvDl_Hw2_Q5/inference_dataset'
class App(QDialog):
    def __init__(self):
        super().__init__()
        self.title = 'P76107116 Cats & Dogs :3'
        self.left = 500
        self.top =  500
        self.width = 500 
        self.height = 500
        self.imgPath = ''
        
        self.label = QtWidgets.QLabel(self)
        self.resultsLabel = QtWidgets.QLabel(self)

        self.createLayouts()
        self.setWindowTitle(self.title)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
                
        windowLayout = QHBoxLayout()
        windowLayout.addWidget(self.modelBox)
        windowLayout.addWidget(self.picBox)
        self.setLayout(windowLayout)

        self.q5m = q5Methods()
        self.show()
        

    def make_button(self, name, layout, callback):
        btn = QPushButton(name)
        btn.clicked.connect(callback)
        layout.addWidget(btn)

        return btn

    def createLayouts(self):
        self.modelBox = QGroupBox('5. ResNet50 Cats & Dogs')
        layout = QVBoxLayout()

        self.make_button('Load Image', layout, self.loadImage)

        self.make_button('1. Show Images', layout, self.showImage)

        self.make_button('2. Show Distribution',
                         layout,
                         self.showDistribution) 

        self.make_button('3. Show Model Structure',
                         layout,
                         self.showModelStructure)

        self.make_button('4. Show Model Comparison',
                         layout,
                         self.showComparison)

        self.make_button('5. Inference',
                         layout,
                         self.inference)


        self.modelBox.setLayout(layout)
        self.picBox = QGroupBox('Image')
        picLayout = QVBoxLayout()
        picLayout.addWidget(self.resultsLabel)
        picLayout.addWidget(self.label)
        self.picBox.setLayout(picLayout)

        self.label = QtWidgets.QLabel(self)
        self.resultsLabel = QtWidgets.QLabel(self)

        picLayout.addWidget(self.resultsLabel)
        picLayout.addWidget(self.label)

        self.picBox.setLayout(picLayout)
        
    def loadImage(self):
        img = QFileDialog.getOpenFileName(None,
                            'Select an image', '.',
                            "Images (*.bmp *.png *jpg)")
        self.imgPath = img[0]
        self.p = QPixmap(self.imgPath)
        self.label.setPixmap(self.p)


    def showImage(self):
        self.q5m.showImage()

    def showDistribution(self):
        self.q5m.showDistribution()

    def showModelStructure(self):
        self.q5m.showModelStructure()

    def showComparison(self):
        self.q5m.showComparison()

    def inference(self):
        if not self.imgPath:
            return
        label = self.q5m.inference(self.imgPath)
        self.resultsLabel.setText(f'Prediction: {label}')

if __name__=='__main__':
    app = QApplication(sys.argv)
    gui = App()
    sys.exit(app.exec_())
