# backend/model_integration.py
import os
import joblib
import pickle
import numpy as np
import requests

# Try to import gdown, but allow fallback to requests
try:
    import gdown
except Exception:
    gdown = None

# Google Drive file ID (you said this is verified)
DRIVE_FILE_ID = "1tp7eBVsiOsWG5FF2Tg8J045dMKmy9qQO"
DRIVE_URL = f"https://drive.google.com/uc?export=download&id={DRIVE_FILE_ID}"

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")

def _download_with_gdown(url, dest):
    if gdown is None:
        return False
    try:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        gdown.download(url, dest, quiet=False)
        return os.path.exists(dest)
    except Exception as e:
        print("gdown download failed:", e)
        return False

def _download_with_requests(url, dest):
    try:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with requests.get(url, stream=True, allow_redirects=True) as r:
            if r.status_code != 200:
                print("requests download status:", r.status_code)
                return False
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        return os.path.exists(dest)
    except Exception as e:
        print("requests download failed:", e)
        return False

def download_model():
    if os.path.exists(MODEL_PATH):
        return True

    # Try gdown first
    if _download_with_gdown(DRIVE_URL, MODEL_PATH):
        print("Model downloaded via gdown.")
        return True

    # Try alternative direct download (may fail due to drive confirmation)
    if _download_with_requests(DRIVE_URL, MODEL_PATH):
        print("Model downloaded via requests.")
        return True

    print("Model download failed (ensure Drive share is 'Anyone with the link').")
    return False

def load_model():
    # Ensure model folder exists
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Attempt to load if file exists; otherwise attempt download
    if not os.path.exists(MODEL_PATH):
        download_model()

    if not os.path.exists(MODEL_PATH):
        print("No model found; running in demo mode.")
        return None

    # Try joblib first
    try:
        m = joblib.load(MODEL_PATH)
        print("Model loaded via joblib.")
        return m
    except Exception as e:
        print("joblib.load failed:", e)

    # Fallback to pickle
    try:
        with open(MODEL_PATH, "rb") as f:
            m = pickle.load(f)
        print("Model loaded via pickle.")
        return m
    except Exception as e:
        print("pickle.load failed:", e)

    return None

# Load at import
model = load_model()

def predict_yield_from_model(model_obj, data: dict):
    """
    Input: model_obj (could be None), data dict with keys: state,district,season,crop,area,area_unit,feature...
    Output: dict {"yield_prediction": float, ...}
    """
    model_to_use = model_obj if model_obj is not None else model

    # Build feature vector: any keys starting with 'feature' (sorted) and area appended.
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

    # If model present, try predict
    if model_to_use:
        try:
            X = np.array([features], dtype=float)
            pred = model_to_use.predict(X)
            val = float(pred[0]) if hasattr(pred, "__len__") else float(pred)
            return {"yield_prediction": round(val, 4)}
        except Exception as e:
            print("Model predict failed:", e)

    # Demo fallback: simple heuristic
    return _demo_yield(features)

def _demo_yield(features):
    area = features[-1] if features else 1.0
    factor = 1.0 + (sum(features[:-1]) * 0.01 if len(features) > 1 else 0.1)
    val = round(area * factor * 100.0, 3)
    return {"yield_prediction": float(val), "notes": "demo fallback"}
