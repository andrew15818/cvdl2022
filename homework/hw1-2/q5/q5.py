import torch
import random
import torchsummary
import torch.nn as nn
import torchvision.io as io
import torchvision.datasets as datasets
import torchvision.transforms as T
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
                nn.Dropout(p=0.5, inplace=False),
                nn.Linear(in_features=1024, out_features=512, bias=True),
                nn.ReLU(inplace=True),
                nn.Dropout(p=0.5, inplace=False),
                nn.Linear(in_features=512, out_features=10)
                )
        self.infAugs = T.Compose([T.Resize((224,224)),
                                        #T.ToTensor(),
                                        T.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))]
                                        )

        self.model.load_state_dict(state['model_state_dict'])
        self.accPath = 'acc.png'
        self.lossPath = 'loss.png'

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

    def show_data_augmentation(self, path):
        orig_img = plt.imread(path)
        orig_img = T.ToTensor()(orig_img)
        orig_img = orig_img.squeeze().permute(1, 2, 0)
         
        aug1 = T.RandomHorizontalFlip(p=1)(orig_img)
        aug2 = T.RandomRotation(degrees=10)(orig_img)
        aug3 = T.GaussianBlur(kernel_size=3)(orig_img)

        fig, axis = plt.subplots(nrows=1, ncols=3)
        axis[0].imshow(aug1)
        axis[1].imshow(aug2)
        axis[2].imshow(aug3)
        plt.show()

    # Show plot with both images
    def show_accuracy_loss(self):
        figure, axis = plt.subplots(nrows=2, ncols=1)
        im1 = plt.imread(self.accPath)
        im2 = plt.imread(self.lossPath)

        axis[0].imshow(im1)
        axis[1].imshow(im2)
        plt.show()

    def _run_model(self, img):
        feats = self.model.features(img)
        print(feats.shape)
        feats = torch.flatten(feats)
        feats = self.model.classifier(feats)
        return torch.nn.Softmax()(feats)

    # Get the prediction and return the class w/ confidence
    def inference(self, imagePath):
        result = None
        img = io.read_image(imagePath).float()
        img = self.infAugs(img)
        self.model.eval()
        pred = self._run_model(img)
        
        result = torch.argmax(pred).item()
        conf= torch.max(pred)
        result = classes[result]
        # ...
        print(f'Class: {result} conf: {conf}')
        return result, conf
        



