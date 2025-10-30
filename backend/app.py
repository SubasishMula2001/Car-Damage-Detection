import os
import io
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from PIL import Image
import numpy as np
import cv2
# from model_helper import load_model, predict_from_frame  # backend local import
# from .model_helper import load_model, predict_from_frame
from .model_helper import load_model, predict_from_frame, detect_car_in_frame

# from model_helper import load_model, predict_from_frame

# Paths
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.environ.get("MODEL_PATH", os.path.join(BASE_DIR, "saved_model.pth"))
SAVE_DIR = os.environ.get("SAVE_DIR", os.path.join(BASE_DIR, "server_captures"))
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")

os.makedirs(SAVE_DIR, exist_ok=True)

app = FastAPI(title="Car Damage Detection API — Private Mode")

# Allow browser UI to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend files
if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# Load model once
model, classes = load_model(MODEL_PATH)

# Response schema
class PredictResponse(BaseModel):
    label: str
    confidence: float
    probs: List[float]
    saved_filename: Optional[str] = None

# @app.post("/predict-file", response_model=PredictResponse)
# async def predict_file(file: UploadFile = File(...)):
#     """
#     Receives an uploaded frame (from webcam snapshot),
#     runs inference, saves snapshot if damage, and returns result.
#     """
#     contents = await file.read()
#     image = Image.open(io.BytesIO(contents)).convert("RGB")
#     frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

#     label, confidence, probs = predict_from_frame(model, frame, classes=classes)

#     saved_filename = None
#     if "normal" not in label.lower() and confidence >= 0.5:
#         ts = __import__("datetime").datetime.utcnow().strftime("%Y%m%d_%H%M%S")
#         fname = f"{ts}_{label.replace(' ', '_')}_{int(confidence*100)}.jpg"
#         fpath = os.path.join(SAVE_DIR, fname)
#         cv2.imwrite(fpath, frame)
#         saved_filename = fname

#     return {
#         "label": label,
#         "confidence": float(confidence),
#         "probs": probs,
#         "saved_filename": saved_filename,
#     }
@app.post("/predict-file", response_model=PredictResponse)
async def predict_file(file: UploadFile = File(...)):
    """
    Receives an uploaded frame (from webcam snapshot),
    checks if frame contains a car via cascade, then runs inference.
    """
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # 1) Check for car presence using cascade
    try:
        has_car, boxes = detect_car_in_frame(frame)
    except FileNotFoundError as fnf:
        # Cascade missing -> raise a clear error
        raise RuntimeError(str(fnf))
    except Exception as e:
        raise RuntimeError(f"Error running car cascade: {e}")

    if not has_car:
        # No car detected: return a clear, consistent response
        empty_probs = [0.0] * len(classes)
        return {
            "label": "No Car Detected",
            "confidence": 1.0,
            "probs": empty_probs,
            "saved_filename": None,
        }
        

    # 2) If car detected -> proceed with model inference
    label, confidence, probs = predict_from_frame(model, frame, classes=classes)

    saved_filename = None
    if "normal" not in label.lower() and confidence >= 0.5:
        ts = __import__("datetime").datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        fname = f"{ts}_{label.replace(' ', '_')}_{int(confidence*100)}.jpg"
        fpath = os.path.join(SAVE_DIR, fname)
        cv2.imwrite(fpath, frame)
        saved_filename = fname

    # Optionally you can return boxes if frontend needs to draw them:
    return {
        "label": label,
        "confidence": float(confidence),
        "probs": probs,
        "saved_filename": saved_filename,
    }

@app.get("/")
def read_root():
    return {"message": "Car Damage Detection API. Open /static/index.html for the UI."}
