import sys
import q5 # Is this file necessary?
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

class App(QDialog):
    def __init__(self):
        super().__init__()
        self.title = 'P76107116 CIFAR10 training :3'
        self.left = 500
        self.right = 500
        self.top = 500
        self.width = 500
        # Path for inference image
        self.imgPath = None
        self.pic = QPixmap()

        self.model = q5.ModelInterface()
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        #self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.createLayout()
        
        windowLayout = QHBoxLayout()
        windowLayout.addWidget(self.modelBox)
        windowLayout.addWidget(self.picBox)
        self.setLayout(windowLayout)
        
        self.show()

    def make_button(self, name, layout, callback):
        btn = QPushButton(name)
        btn.clicked.connect(callback)
        layout.addWidget(btn)

        return btn

    def createLayout(self):
        self.modelBox = QGroupBox('5. VGG19 Test')
        layout = QVBoxLayout()
        self.make_button('Load Image',
                         layout,
                         self.load_image)
        self.make_button('5.1 Show Training Images', 
                         layout, 
                         self.show_image_grid)

        self.make_button('5.2 Show Model Structure', 
                         layout, 
                         self.show_model_structure)

        self.make_button('5.3 Show Data Augmentation', 
                         layout, 
                         self.show_data_augmentation)

        self.make_button('5.4 Show Accuracy and Loss',
                         layout,
                         self.show_accuracy_loss)

        self.make_button('5.5 Inference',
                         layout,
                         self.inference)
        self.modelBox.setLayout(layout) 
        
        self.picBox = QGroupBox('Image')
        picLayout = QVBoxLayout()
        self.label = QtWidgets.QLabel(self)
        picLayout.addWidget(self.label)
        
        self.picBox.setLayout(picLayout)

    def load_image(self):
        self.imgPath = QFileDialog.getOpenFileName(None,
                                                   'Select inference image', '.'
                                                   'Images (*.bmp *.png *.jpg)'
                                                    )
        print(f'loaded {self.imgPath}')
        self.p = QPixmap(self.imgPath[0])
        self.label.setPixmap(self.p)

    def show_image_grid(self):
        self.model.show_image_grid()
        pass
    def show_model_structure(self):
        self.model.summary()
        pass
    def show_data_augmentation(self):
        pass
    def show_accuracy_loss(self):
        pass
    def inference(self):
        pass

app = QApplication(sys.argv)
gui = App()
sys.exit(app.exec_())
