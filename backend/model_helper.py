# model_helper.py
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
import numpy as np
import cv2

# --- START: car cascade helper (paste after imports) ---
# Path & loader for the car cascade
DEFAULT_CAR_CASCADE_PATH = os.path.join(os.path.dirname(__file__), "cascades", "car_cascade.xml")
_car_cascade = None

def _get_car_cascade(path: str = DEFAULT_CAR_CASCADE_PATH):
    """Lazy-load and return a cv2.CascadeClassifier for car detection."""
    global _car_cascade
    if _car_cascade is None:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Car cascade not found at: {path}")
        _car_cascade = cv2.CascadeClassifier(path)
        if _car_cascade.empty():
            raise RuntimeError(f"Failed to load cascade classifier from: {path}")
    return _car_cascade

def detect_car_in_frame(frame_bgr: np.ndarray,
                        scaleFactor: float = 1.1,
                        minNeighbors: int = 3,
                        minSize: tuple = (60, 60)):
    """
    Run Haar cascade on a BGR frame (OpenCV style).
    Returns (found: bool, boxes: list_of_[x,y,w,h])
    """
    cascade = _get_car_cascade()
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    boxes = cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize)
    # boxes could be an empty tuple or numpy array
    if isinstance(boxes, tuple) or len(boxes) == 0:
        return False, []
    # convert to python lists
    return True, [list(map(int, b)) for b in boxes]
# --- END: car cascade helper ---

# Preprocessing (must match training)
IMG_SIZE = 224
_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Default classes (from SOW). Put exact order in classes.txt to be safe.
DEFAULT_CLASSES = [
    "Front Normal",
    "Front Breakage",
    "Front Crushed",
    "Rear Normal",
    "Rear Breakage",
    "Rear Crushed"
]

class CarClassifierEfficientNet(nn.Module):
    def __init__(self, num_classes=6, dropout_rate=0.5):
        super().__init__()
        # instantiate architecture only (no pretrained weights download)
        self.model = models.efficientnet_b0(weights=None)
        num_ftrs = self.model.classifier[1].in_features
        self.model.classifier = nn.Sequential(
            nn.Dropout(dropout_rate),
            nn.Linear(num_ftrs, num_classes)
        )

    def forward(self, x):
        return self.model(x)

def _strip_prefix(state_dict, prefix):
    new = {}
    for k, v in state_dict.items():
        if k.startswith(prefix):
            new[k[len(prefix):]] = v
        else:
            new[k] = v
    return new

def _add_prefix(state_dict, prefix):
    return {prefix + k: v for k, v in state_dict.items()}

def _clean_state(state_dict):
    # remove common wrappers: 'module.' and trailing prefixes like 'model.' if present
    sd = dict(state_dict)
    # If keys start with 'module.', strip it
    any_module = any(k.startswith("module.") for k in sd.keys())
    if any_module:
        sd = _strip_prefix(sd, "module.")
    # If keys start with 'model.' but underlying model expects keys without 'model.', we'll handle later
    return sd

def load_class_list(classes_path="classes.txt"):
    if os.path.exists(classes_path):
        with open(classes_path, "r", encoding="utf-8") as f:
            classes = [line.strip() for line in f if line.strip()]
        if len(classes) > 0:
            return classes
    return DEFAULT_CLASSES

def _attempt_load_state(model, raw_state):
    """
    Try a few permutations to match keys between raw_state and model.state_dict().
    Returns (success_bool, loaded_state_dict, info_str)
    """
    model_sd = model.state_dict()
    attempts = []

    # base cleaning (strip module.)
    base = _clean_state(raw_state)

    # build candidate versions
    candidates = []
    candidates.append(base)
    candidates.append(_strip_prefix(base, "model."))      # try removing 'model.' if present
    candidates.append(_add_prefix(base, "model."))        # try adding 'model.' prefix
    # also try variations adding/removing both (safeguard)
    candidates.append(_strip_prefix(_strip_prefix(base, "model."), "module."))
    # unique by keyset to avoid duplicate attempts
    seen_keysets = set()
    for cand in candidates:
        ks = tuple(sorted(cand.keys()))
        if ks in seen_keysets:
            continue
        seen_keysets.add(ks)
        # build filtered cand to only keys that match model_sd keys (best-effort)
        filtered = {k: v for k, v in cand.items() if k in model_sd}
        # but also try loading full cand (some keys might be prefix variants)
        attempts.append((cand, filtered))

    # Try each attempt: first filtered (matching keys), then raw candidate
    for cand_full, cand_filtered in attempts:
        try_list = [cand_filtered, cand_full]
        for cand in try_list:
            try:
                # use strict=False to allow partial loads
                res = model.load_state_dict(cand, strict=False)
                info = f"Loaded with strict=False. Missing keys: {len(res.missing_keys)}. Unexpected keys: {len(res.unexpected_keys)}."
                return True, res, info
            except Exception as ex:
                # continue to next attempt
                last_ex = ex
                continue
    return False, None, f"All attempts failed. Last exception: {last_ex if 'last_ex' in locals() else 'none'}"

def load_model(state_dict_path: str, classes_path: str = "classes.txt"):
    """
    Robust model loader. Detects whether provided state_dict matches ResNet-like or EfficientNet-like keys,
    instantiates a matching architecture, and attempts several loading strategies.
    Returns (model, classes)
    """
    classes = load_class_list(classes_path)
    num_classes = len(classes)

    raw = torch.load(state_dict_path, map_location=device)

    # if raw is a whole model object (nn.Module), try returning it directly
    if not isinstance(raw, dict):
        try:
            raw.to(device)
            raw.eval()
            return raw, classes
        except Exception:
            # fallthrough to dict-based handling
            pass

    # raw is a state_dict (dict of tensors)
    raw_keys = list(raw.keys())
    key_sample = " ".join(raw_keys[:10])

    # detect architecture by key patterns
    uses_resnet = any("layer1." in k or "conv1.weight" in k or k.startswith("model.layer") or "model.conv1" in k for k in raw_keys)
    uses_efficient = any("features." in k or "model.features" in k or "efficientnet" in k for k in raw_keys)

    tried_info = []

    if uses_resnet:
        # instantiate ResNet50 and adapt head
        print("Detected ResNet-like keys in state_dict -> trying ResNet50 loader.")
        resnet = models.resnet50(weights=None)
        num_ftrs = resnet.fc.in_features
        resnet.fc = nn.Sequential(nn.Dropout(0.5), nn.Linear(num_ftrs, num_classes))
        resnet = resnet.to(device)
        ok, res, info = _attempt_load_state(resnet, raw)
        print(info)
        if ok:
            return resnet.eval(), classes
        tried_info.append(("resnet", info))

    if uses_efficient:
        print("Detected EfficientNet-like keys in state_dict -> trying EfficientNet-B0 loader.")
        eff = CarClassifierEfficientNet(num_classes=num_classes).to(device)
        ok, res, info = _attempt_load_state(eff, raw)
        print(info)
        if ok:
            return eff.eval(), classes
        tried_info.append(("efficientnet", info))

    # fallback: try both architectures even if not detected
    print("Fallback: trying ResNet50 then EfficientNet-B0 as last resort.")
    if not uses_resnet:
        try:
            resnet = models.resnet50(weights=None)
            num_ftrs = resnet.fc.in_features
            resnet.fc = nn.Sequential(nn.Dropout(0.5), nn.Linear(num_ftrs, num_classes))
            resnet = resnet.to(device)
            ok, res, info = _attempt_load_state(resnet, raw)
            print("ResNet fallback:", info)
            if ok:
                return resnet.eval(), classes
        except Exception as e:
            print("ResNet fallback failed:", e)

    if not uses_efficient:
        try:
            eff = CarClassifierEfficientNet(num_classes=num_classes).to(device)
            ok, res, info = _attempt_load_state(eff, raw)
            print("EfficientNet fallback:", info)
            if ok:
                return eff.eval(), classes
        except Exception as e:
            print("EfficientNet fallback failed:", e)

    # if we reach here, all load attempts failed
    raise RuntimeError(f"Could not load model from {state_dict_path}. Tried architectures: {tried_info}")

def pil_to_tensor(img_pil: Image.Image):
    return _transform(img_pil).unsqueeze(0).to(device)

def frame_to_tensor(frame_bgr: np.ndarray):
    # OpenCV BGR -> PIL RGB
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    pil = Image.fromarray(rgb)
    return pil_to_tensor(pil)

def predict_from_frame(model, frame_bgr: np.ndarray, classes=None):
    """
    frame_bgr: OpenCV BGR image (numpy array)
    returns: (label, confidence, probs_list)
    """
    x = frame_to_tensor(frame_bgr)
    with torch.no_grad():
        outputs = model(x)
        if isinstance(outputs, (tuple, list)):
            outputs = outputs[0]
        probs = F.softmax(outputs, dim=1).cpu().numpy()[0]
        idx = int(probs.argmax())
        label = (classes[idx] if classes is not None and idx < len(classes) else str(idx))
        confidence = float(probs[idx])
    return label, confidence, probs.tolist()
