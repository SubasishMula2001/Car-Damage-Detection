import torch
import json
from model_helper import load_model

def evaluate_model(model, test_loader):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.eval()
    
    correct = 0
    total = 0
    
    with torch.no_grad():
        for batch in test_loader:
            inputs, labels = batch
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    accuracy = 100 * correct / total
    return {"accuracy": accuracy}

if __name__ == "__main__":
    # Load model and data
    model, _ = load_model("backend/saved_model.pth")
    data = torch.load("data/processed/data.pt")
    test_loader = data['test_loader']
    
    # Evaluate
    metrics = evaluate_model(model, test_loader)
    
    # Save metrics
    with open("metrics.json", "w") as f:
        json.dump(metrics, f)
