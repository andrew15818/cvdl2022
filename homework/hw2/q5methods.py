import torch
import random
import torchsummary
import numpy as np
import torch.nn as nn
import torchvision.models as models
import torchvision.io as io
import matplotlib.image as img
import matplotlib.pyplot as plt
import torchvision.datasets as datasets
import torchvision.transforms as transforms

from torch.utils.data import DataLoader

class q5Methods:
    def __init__(self):
        modelPath = 'models/r50_focal.pt'
        dataPath = 'Dataset_OpenCvDl_Hw2_Q5/inference_dataset'

        state = torch.load(modelPath, map_location=torch.device('cpu'))
        self.model = models.resnet50()
        self.model.fc = nn.Sequential(nn.Linear(2048, 1),
                                      nn.Sigmoid())
        self.model.load_state_dict(state['model_state_dict'])
        self.augs = transforms.Compose([transforms.Resize((224, 224)),
                                        #transforms.ToTensor(),
                                        transforms.Normalize(0.485, 0.456, 0.406)])
 
        self.dataset = datasets.ImageFolder(dataPath, transform=self.augs)

   
    def showModelStructure(self):
        torchsummary.summary(self.model,(3, 224, 224))

    def showImage(self):
        row, cols = 1, 2
        figure, axis  = plt.subplots(nrows=1, ncols=2)
        foundDoggo, foundCat = False, False
        # Choose random images until we find both doggo and cat
        while not foundDoggo and not foundCat:
            idx = random.randint(0, len(self.dataset)-1)
            img, label = self.dataset[idx]
            
            # Maybe the labels are reversed
            if label == 0:
                foundDog = True
                axis[0].set_title('Cat')
                axis[0].imshow(img)
            elif label == 1:
                foundCat = True
                axis[1].set_title('Dog')
                axis[1].imshow(img)
        plt.show()



    def showComparison(self):
        path = 'accuracies.png'
        im = img.imread(path)
        plt.imshow(im)
        plt.show()

    def showDistribution(self):
        path = 'classDistribution.png'
        im  = img.imread(path)
        plt.imshow(im)
        plt.show()

    def inference(self, imgPath):
        result = None
        
        img = io.read_image(imgPath).float()
        img = self.augs(img)
        self.model.eval()
        img = torch.unsqueeze(img, 0)
        pred = self.model(img)
        
        label = 'Cat' if pred.item() == 0 else 'Dog'
        return label
