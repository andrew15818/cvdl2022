import torch
import random
import torchsummary
import torch.nn as nn
import torchvision.datasets as datasets
import torchvision.models as models
import matplotlib.pyplot as plt

from torch.utils.data import Dataset


classes = {
        0: 'airplane',
        1: 'automobile',
        2: 'bird',
        3: 'cat',
        4: 'deer',
        5: 'dog',
        6: 'frog',
        7: 'horse',
        8: 'ship',
        9: 'truck'
}
class ModelInterface():
    # Set the path for CIFAR-10
    def __init__(self, root='/home/poncedeleon/usb/'):
        # Load pretrained models onto CPU
        state = torch.load('vgg19_full.pt', 
                                map_location=torch.device('cpu'))
        
        # Change the model classifier to fit hw description
        self.model = models.vgg19()
        self.model.classifier = nn.Sequential(
                nn.Linear(in_features=25088, out_features=1024, bias=True),
                nn.ReLU(inplace=True),
                nn.Dropout(p=0.5, inplace=True),
                nn.Linear(in_features=1024, out_features=512, bias=True),
                nn.ReLU(inplace=True),
                nn.Dropout(p=0.5, inplace=False),
                nn.Linear(in_features=512, out_features=10)
                )

        self.model.load_state_dict(state['model_state_dict'])

        self.dataset = datasets.CIFAR10(root, download=False, train=True)

    def summary(self):
        torchsummary.summary(self.model, (3, 224, 224))


    # Load dataset, show 9 random images
    def show_image_grid(self):
        figure = plt.figure() 
        cols, rows = 3, 3
        for i in range(1, cols * rows +1):
            # Choose random number
            idx = random.randint(0,len(self.dataset)) 
            img, label = self.dataset[idx]
            figure.add_subplot(rows, cols, i)
            plt.title(classes[label])
            plt.axis('off')
            plt.imshow(img, cmap="gray")
        plt.show()

    def inference(self):
        pass



