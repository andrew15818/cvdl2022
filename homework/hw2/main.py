import sys

import methods
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QDialog,
    QHBoxLayout, QGroupBox,
    QVBoxLayout, QPushButton,
    QFileDialog
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

        self.videoPath = None

    # Create all the buttons and input fields
    def _initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createLayouts()

        windowLayout = QHBoxLayout()

        self.setLayout(windowLayout)
        windowLayout.addWidget(self.horizontalGroupBox)
        windowLayout.addWidget(self.q1GroupBox)
        self.show()

    def makeButton(self, name, layout, callback):
        btn = QPushButton(name)
        btn.clicked.connect(callback)
        layout.addWidget(btn)

        return btn

    def createLayouts(self):
        self.horizontalGroupBox = QGroupBox("Load Videos and Images")
        mediaLayout = QVBoxLayout()

        loadVideoBtn = self.makeButton('Load Video', mediaLayout, self.loadVideo) 
        
        img1btn = self.makeButton('Load image 1', mediaLayout, self.loadImage1)
        img2btn = self.makeButton('Load image 2', mediaLayout, self.loadImage2)

        self.q1GroupBox = QGroupBox('Background subtraction')
        subLayout = QVBoxLayout()

        backsubBtn = self.makeButton('1.1 Background subtraction', subLayout, self.backgroundSubtraction)



        self.horizontalGroupBox.setLayout(mediaLayout)
        self.q1GroupBox.setLayout(subLayout)
    def _load_media(self):
        img = QFileDialog.getOpenFileName(None,
                                          'Select an image or video', '.',
                                          'All files (*.png *.jpg *.mp4)')
        return img[0]

    def loadVideo(self):
        file = self._load_media()
        if not file.endswith('.mp4'):
            print('The file you selected was not an mp4.')
            return
        self.videoPath = file
        print(f'Loaded {self.videoPath}')

    def loadImage1(self):
        pass
    def loadImage2(self):
        pass

    def backgroundSubtraction(self):
        if not self.videoPath:
            print('Select video file first')
            return
        methods.subtractBackground(self.videoPath)
        pass
        
if __name__=='__main__':
    app = QApplication(sys.argv)
    gui = App()
    sys.exit(app.exec_())
    pass
