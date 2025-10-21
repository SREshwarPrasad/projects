import os
import requests
import joblib
import numpy as np

# ✅ Google Drive model file
MODEL_URL = "https://drive.google.com/uc?export=download&id=1tp7eBVsiOsWG5FF2Tg8J045dMKmy9qQO"
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")

def download_model():
    if not os.path.exists(MODEL_PATH):
        print("🔽 Downloading model from Google Drive...")
        os.makedirs(MODEL_DIR, exist_ok=True)
        r = requests.get(MODEL_URL, stream=True)
        if r.status_code == 200:
            with open(MODEL_PATH, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("✅ Model downloaded successfully.")
        else:
            print(f"⚠️ Download failed: {r.status_code}")

def load_model():
    download_model()
    try:
        return joblib.load(MODEL_PATH)
    except Exception as e:
        print(f"⚠️ Failed to load model: {e}")
        return None

model = load_model()

def predict_yield_from_model(model, data: dict):
    feature_keys = sorted([k for k in data.keys() if k.startswith("feature")])
    features = []
    for k in feature_keys:
        try:
            features.append(float(data.get(k, 0)))
        except:
            features.append(0.0)

    try:
        area = float(data.get("area", 0.0))
    except:
        area = 0.0
    features.append(area)

    if model is not None:
        try:
            X = np.array([features], dtype=float)
            pred = model.predict(X)
            return {"yield_prediction": float(pred[0])}
        except Exception:
            return {"yield_prediction": _demo_yield(features)}
    else:
        return {"yield_prediction": _demo_yield(features)}

def _demo_yield(features):
    area = features[-1] if features else 1.0
    factor = 1.0 + (sum(features[:-1]) * 0.01 if len(features) > 1 else 0.1)
    return round(area * factor * 100.0, 3)
