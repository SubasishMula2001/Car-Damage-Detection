import os
import torch
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms

def prepare_data(data_dir, test_size=0.2, seed=42):
    """Prepare and split the dataset"""
    torch.manual_seed(seed)
    
    # Define transforms
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])
    
    # Load dataset
    dataset = datasets.ImageFolder(data_dir, transform=transform)
    
    # Split dataset
    train_size = int((1 - test_size) * len(dataset))
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = random_split(dataset, [train_size, test_size])
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    
    return train_loader, test_loader

if __name__ == "__main__":
    # Create processed data directory
    os.makedirs("data/processed", exist_ok=True)
    
    # Process and save data
    # train_loader, test_loader = prepare_data("data")
    train_loader, test_loader = prepare_data("data/raw")

    torch.save({
        'train_loader': train_loader,
        'test_loader': test_loader
    }, "data/processed/data.pt")
