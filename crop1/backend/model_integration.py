# backend/model_integration.py
import numpy as np

def predict_yield_from_model(model, data: dict):
    """
    Return a dict with at least: {"yield_prediction": <float>}
    Accepts model (may be None). 'data' will include fields:
      - crop, season, state, district, area, area_unit, and optionally numeric features.
    If model is provided, this attempts to extract features in a generic way.
    Please adapt this function to match the exact model input schema.
    """
    # Simple feature extraction:
    # try to collect numeric features passed in data with keys 'feature1','feature2',...
    feature_keys = sorted([k for k in data.keys() if k.startswith("feature")])
    features = []
    for k in feature_keys:
        try:
            features.append(float(data.get(k, 0)))
        except:
            features.append(0.0)

    # include area as a core feature if numeric
    area = data.get("area")
    try:
        area_f = float(area) if area is not None else 0.0
    except:
        area_f = 0.0
    features.append(area_f)

    if model is not None:
        # Attempt model predict
        try:
            X = np.array([features], dtype=float)
            pred = model.predict(X)
            # Some models return an array; others a scalar
            if hasattr(pred, "__len__"):
                pred_val = float(pred[0])
            else:
                pred_val = float(pred)
            return {"yield_prediction": pred_val}
        except Exception as e:
            # fallback to demo below
            return {"yield_prediction": _demo_yield(features), "notes": f"model predict failed: {e}"}
    else:
        # Demo formula: yield = (area_in_hectares) * factor based on crop length of name
        return {"yield_prediction": _demo_yield(features)}

def _demo_yield(features):
    # very simple deterministic demo formula for testing the pipeline
    area = features[-1] if features else 1.0
    factor = 1.0 + (sum(features[:-1]) * 0.01 if len(features) > 1 else 0.1)
    return round(area * factor * 100.0, 3)  # arbitrary units (e.g., quintals)
