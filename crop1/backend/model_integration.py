import os
import joblib
import numpy as np
import gdown

# Google Drive Model URL (replace with your own ID if changed)
MODEL_ID = "1tp7eBVsiOsWG5FF2Tg8J045dMKmy9qQO"
MODEL_URL = f"https://drive.google.com/uc?id={MODEL_ID}"

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")

def download_model():
    """Download model from Google Drive if not found"""
    if not os.path.exists(MODEL_PATH):
        os.makedirs(MODEL_DIR, exist_ok=True)
        print("Downloading model from Google Drive...")
        try:
            gdown.download(MODEL_URL, MODEL_PATH, quiet=False)
            print("✅ Model downloaded successfully!")
        except Exception as e:
            print("⚠️ Model download failed:", e)

def load_model():
    download_model()
    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            print("✅ Model loaded successfully.")
            return model
        except Exception as e:
            print("⚠️ Model loading failed:", e)
    else:
        print("⚠️ Model file not found even after download.")
    return None

model = load_model()

def predict_yield_from_model(model, data):
    """Perform model prediction"""
    features = []
    for key, val in data.items():
        try:
            features.append(float(val))
        except:
            features.append(0.0)
    if model:
        try:
            X = np.array([features])
            prediction = model.predict(X)[0]
            return {"yield_prediction": float(prediction)}
        except Exception as e:
            print("⚠️ Prediction failed:", e)
    return {"yield_prediction": 0.0, "demo": True}
