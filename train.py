import torch
import torch.nn
from torchvision.transforms import transforms
from torch.utils.data import random_split, DataLoader
import torch.nn as nn
import torch.optim as optim

from Utils.Constants import *
from ML.TargetDataset import TargetDataset
from ML.TargetPosCNN import TargetPosCNN

# Roots from constants file 
IMG_DIR = ROOT + IMGS
JSON_DIR = ROOT + JSON

''' -------------------------------------------------- '''
'''            INIT THE TRAINING COMPONENTS            '''
''' -------------------------------------------------- '''
transform = transforms.Compose([
    transforms.Resize((256, 256)),  # Resize the image to 256x256
    transforms.ToTensor(),         # Convert the image to a PyTorch tensor
])

td = TargetDataset(
    IMG_DIR,
    JSON_DIR,
    transform
)


''' -------------------------------------------------- '''
'''                 PREPARE THE DATA                   '''
''' -------------------------------------------------- '''
# Split dataset into training and testing
train_size = int(0.8 * len(td))
test_size = len(td) - train_size
train_dataset, test_dataset = random_split(td, [train_size, test_size])

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)


''' -------------------------------------------------- '''
'''                SET UP ALL THE DEVICES              '''
''' -------------------------------------------------- '''
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = TargetPosCNN().to(device)
criterion = nn.MSELoss()  # Mean squared error for regression
optimizer = optim.Adam(model.parameters(), lr=0.001)


''' -------------------------------------------------- '''
'''                    !!!!TRAIN!!!!                   '''
''' -------------------------------------------------- '''
def train_model(model, train_loader, criterion, optimizer, epochs=10):
    print("Training...")
    model.train()
    for epoch in range(epochs):
        total_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            
            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {total_loss / len(train_loader):.4f}")
    print("Training complete!")


train_model(model, train_loader, criterion, optimizer, epochs=50)

# Save model
torch.save(model.state_dict(), "BlockDetectionModel.pth")

