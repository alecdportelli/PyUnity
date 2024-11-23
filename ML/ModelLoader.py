from PIL import Image
import torch
from torchvision import transforms
import numpy as np

from ML.TargetPosCNN import TargetPosCNN
from ML.TargetDataset import TargetDataset
from Utils.Constants import *


class ModelLoader:
    ''' 
    This class loads a trained model (.pt) and intakes a data type

    For this use case, the model is trained on position of a cube 
    within a simulation environment.
    '''
    def __init__(self, modelPath: str, imgWidth:int = 256, imgHeight:int = 256, device:str = DEVICE):
        self.modelPath = modelPath

        self.imgWidth = imgWidth
        self.imgHeight = imgHeight

        self.device = device

        self.model = TargetPosCNN()
        self.model.load_state_dict(torch.load(self.modelPath))
        self.model.to(self.device)

        self.transform = transforms.Compose([
            transforms.Resize((self.imgWidth, self.imgHeight)),  
            transforms.ToTensor(),         
        ])

    
    def Predict(self, currImage):
        """
        Make a prediction on a preprocessed image.

        Parameters:
        - image from PIL

        Returns:
        - np.ndarray: Predicted PIXEL position of the cube.
        """
        self.model.eval()
        image = self.transform(currImage).unsqueeze(0).to(DEVICE)
        with torch.no_grad():
            prediction = self.model(image)
        return prediction.cpu().numpy()
