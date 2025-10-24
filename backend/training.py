import torch
import torch.nn as nn
from torch.optim import Adam
from torchvision import models
import os

def train_model(train_loader, epochs=10, lr=0.001):
    # Load model
    model = models.resnet50(weights=None)
    num_ftrs = model.fc.in_features
    model.fc = nn.Sequential(nn.Dropout(0.5), nn.Linear(num_ftrs, 6))
    
    # Training setup
    criterion = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=lr)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    
    # Training loop
    for epoch in range(epochs):
        model.train()
        for batch in train_loader:
            inputs, labels = batch
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
    
    return model

if __name__ == "__main__":
    # Load processed data
    data = torch.load("data/processed/data.pt")
    train_loader = data['train_loader']
    
    # Train model
    model = train_model(train_loader)
    
    # Save model
    os.makedirs("backend", exist_ok=True)
    torch.save(model.state_dict(), "backend/saved_model.pth")
