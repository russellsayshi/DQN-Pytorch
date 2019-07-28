import torch
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self, width, height):
        super().__init__()
        self.fc1 = nn.Linear(width*height*3, width*height*2)
        self.fc2 = nn.Linear(width*height*2, width*height*1)
        self.fc3 = nn.Linear(width*height*1, 4)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = F.leaky_relu(self.fc1(x))
        x = F.leaky_relu(self.fc2(x))
        x = F.leaky_relu(self.fc3(x))
        x = self.sigmoid(x)
        return x
