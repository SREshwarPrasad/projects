# backend/model_integration.py
import os
import requests
import joblib
import pickle
import numpy as np
from typing import Optional

# Put your file id here (you already verified it's correct)
DRIVE_FILE_ID = "1tp7eBVsiOsWG5FF2Tg8J045dMKmy9qQO"

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")

# Google Drive download helper (handles confirmation token for large files)
def _download_file_from_google_drive(file_id: str, dest_path: str, chunk_size=32768):
    session = requests.Session()
    URL = "https://docs.google.com/uc?export=download"

    response = session.get(URL, params={'id': file_id}, stream=True)
    token = None

    # If the file is large, Google Drive returns a confirm token in cookies
    for k, v in response.cookies.items():
        if k.startswith('download_warning'):
            token = v
            break

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    if response.status_code != 200:
        raise RuntimeError(f"Failed to download model: HTTP {response.status_code}")

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:  # filter out keep-alive
                f.write(chunk)

def download_model_if_missing():
    if os.path.exists(MODEL_PATH):
        return True
    try:
        print("Downloading model from Google Drive...")
        _download_file_from_google_drive(DRIVE_FILE_ID, MODEL_PATH)
        print("Model downloaded to", MODEL_PATH)
        return True
    except Exception as e:
        print("Model download failed:", e)
        return False

def load_model() -> Optional[object]:
    # Try to ensure model is present
    download_model_if_missing()

    if not os.path.exists(MODEL_PATH):
        print("Model file not found after attempting download.")
        return None

    # Try joblib (sklearn recommended), otherwise pickle
    try:
        m = joblib.load(MODEL_PATH)
        print("Model loaded with joblib.")
        return m
    except Exception as e:
        print("joblib.load failed:", e)

    try:
        with open(MODEL_PATH, "rb") as f:
            m = pickle.load(f)
        print("Model loaded with pickle.")
        return m
    except Exception as e:
        print("pickle.load failed:", e)

    return None

# load once at import time (app.py will import predict_yield_from_model)
_model = load_model()

def predict_yield_from_model(model_obj, data: dict):
    """
    Keep API identical to your previous function. If 'model_obj' param is passed
    (app.py already loads model into variable 'model') prefer that; fallback to
    the internal _model (downloaded one).
    """
    model_to_use = model_obj if model_obj is not None else _model

    # Build features (this must match how your model was trained).
    # We'll keep your previous heuristic: keys starting with 'feature' + area appended.
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
    # add area as last feature
    features.append(area_f)

    if model_to_use is None:
        # demo fallback: simple heuristic
        return _demo_yield(features)

    try:
        X = np.array([features], dtype=float)
        # support both scikit-learn predict and numpy outputs
        pred = model_to_use.predict(X)
        value = float(pred[0]) if hasattr(pred, "__len__") else float(pred)
        return {"yield_prediction": round(value, 4)}
    except Exception as e:
        # If model prediction fails, log and return demo fallback.
        print("Model predict failed:", e)
        return _demo_yield(features)

def _demo_yield(features):
    area = features[-1] if features else 1.0
    factor = 1.0 + (sum(features[:-1]) * 0.01 if len(features) > 1 else 0.1)
    val = round(area * factor * 100.0, 3)
    return {"yield_prediction": float(val), "notes": "demo fallback"}
