import os
import json
from PIL import Image
import torch
from torch.utils.data import Dataset

class TargetDataset(Dataset):
    def __init__(self, image_dir, json_dir, transform=None):
        self.image_dir = image_dir
        self.json_dir = json_dir
        self.transform = transform
        self.image_filenames = [f for f in os.listdir(image_dir) if f.endswith(".png")]

    def __len__(self):
        return len(self.image_filenames)

    def __getitem__(self, idx):
        img_name = self.image_filenames[idx]
        img_path = os.path.join(self.image_dir, img_name)
        json_path = os.path.join(self.json_dir, img_name.replace(".png", ".json"))
        
        # Load image
        image = Image.open(img_path)
        if self.transform:
            image = self.transform(image)
        
        # Load JSON metadata
        with open(json_path, 'r') as f:
            metadata = json.load(f)
            label = torch.tensor([metadata["PixelPosition"]["x"], metadata["PixelPosition"]["y"]], dtype=torch.float32)
        
        return image, label
