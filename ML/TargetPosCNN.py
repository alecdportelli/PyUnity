import torch.nn as nn
import torch.nn.functional as F

class TargetPosCNN(nn.Module):
    def __init__(self):
        super(TargetPosCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.fc1 = nn.Linear(64 * 64 * 64, 128)  # Flattened size: 64 * 64 * 64
        self.fc2 = nn.Linear(128, 2)  # Predict x, y


    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool(x)
        x = F.relu(self.conv2(x))
        x = self.pool(x)
        x = x.view(-1, 64 * 64 * 64)  # Flatten
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
