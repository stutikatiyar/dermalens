import torch
from torchvision import models, transforms
from PIL import Image
import cv2

# 7-class ISIC (example)
NUM_CLASSES = 7

# transform for derm model
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


def load_model(weights_path):
    from torchvision import models
    import torch

    model = models.resnet18(weights=None)

    # 🔴 CRITICAL FIX: set correct output layer BEFORE loading
    model.fc = torch.nn.Linear(model.fc.in_features, 7)

    state = torch.load(weights_path, map_location="cpu")
    model.load_state_dict(state)

    model.eval()
    return model


def predict(model, image_np):
    image = Image.fromarray(cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))
    tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(tensor)
        probs = torch.nn.functional.softmax(output[0], dim=0)

    confidence = torch.max(probs).item()
    predicted_class = torch.argmax(probs).item()

    return predicted_class, confidence