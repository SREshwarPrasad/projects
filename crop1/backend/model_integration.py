import os
import requests
import joblib
import numpy as np

# 1️⃣ Write your Google Drive direct link here:
MODEL_URL = "https://drive.google.com/uc?export=download&id=1tp7eBVsiOsWG5FF2Tg8J045dMKmy9qQO"

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")

def download_model():
    if not os.path.exists(MODEL_PATH):
        print("Downloading model...")
        os.makedirs(MODEL_DIR, exist_ok=True)
        response = requests.get(MODEL_URL, stream=True)
        with open(MODEL_PATH, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print("Download complete!")

def load_model():
    download_model()
    try:
        return joblib.load(MODEL_PATH)
    except:
        return None

model = load_model()

def predict_yield_from_model(model, data: dict):
    # YOUR EXISTING LOGIC (leave it as-is)
    feature_keys = sorted([k for k in data.keys() if k.startswith("feature")])
    features = []
    for k in feature_keys:
        try:
            features.append(float(data.get(k, 0)))
        except:
            features.append(0.0)

    area = data.get("area")
    try:
        area_f = float(area) if area is not None else 0.0
    except:
        area_f = 0.0
    features.append(area_f)

    if model is not None:
        try:
            X = np.array([features], dtype=float)
            pred = model.predict(X)
            return {"yield_prediction": float(pred[0])}
        except:
            return {"yield_prediction": _demo_yield(features)}
    else:
        return {"yield_prediction": _demo_yield(features)}

def _demo_yield(features):
    area = features[-1] if features else 1.0
    factor = 1.0 + (sum(features[:-1]) * 0.01 if len(features) > 1 else 0.1)
    return round(area * factor * 100.0, 3)
