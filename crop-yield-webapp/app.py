import os
import pickle
import numpy as np
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

MODEL_PATH = "crop_yield_model.pkl"
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    MODEL_AVAILABLE = True
else:
    print("Model file not found. Running in demo mode.")
    model = None
    MODEL_AVAILABLE = False


# Lists
STATES = [
"Andaman and Nicobar Islands","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh",
"Chhattisgarh","Dadra and Nagar Haveli","Daman and Diu","Delhi","Goa","Gujarat","Haryana",
"Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Laddakh","Madhya Pradesh",
"Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan",
"Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"
]

TN_DISTRICTS = [
"ARIYALUR","CHENGALPATTU","CHENNAI","COIMBATORE","CUDDALORE","DHARMAPURI","DINDIGUL","ERODE",
"KALLAKURICHI","KANCHIPURAM","KANNIYAKUMARI","KARUR","KRISHNAGIRI","MADURAI","NAGAPATTINAM",
"NAMAKKAL","PERAMBALUR","PUDUKKOTTAI","RAMANATHAPURAM","RANIPET","SALEM","SIVAGANGA","TENKASI",
"THANJAVUR","THE NILGIRIS","THENI","THIRUVALLUR","THIRUVARUR","THOOTHUKUDI","TIRUCHIRAPPALLI",
"TIRUNELVELI","TIRUPATHUR","TIRUPPUR","TIRUVANNAMALAI","TUTICORIN","VELLORE","VILLUPURAM","VIRUDHUNAGAR"
]

SEASONS = ["Autumn","Kharif","Rabi","Summer","Whole Year","Winter"]

CROPS = [
"Arecanut","Arhar/Tur","Bajra","Banana","Barley","Black pepper","Cardamom","Cashewnut","Castor seed",
"Coconut","Coriander","Cotton(lint)","Cowpea(Lobia)","Dry Ginger","Dry chillies","Garlic","Ginger","Gram",
"Groundnut","Guar seed","Horse-gram","Jowar","Jute","Khesari","Linseed","Maize","Masoor","Mesta",
"Moong(Green Gram)","Moth","Niger seed","Oilseeds total","Onion","Other Cereals","Other Kharif pulses",
"Other Rabi pulses","Other Summer Pulses","Peas & beans (Pulses)","Potato","Ragi","Rapeseed &Mustard",
"Rice","Safflower","Sannhamp","Sesamum","Small millets","Soyabean","Sugarcane","Sunflower","Sweet potato"
]

# Simple ETc estimation
SEASON_INFO = {
    "Autumn": {"ETo": 4.0, "length_days": 90},
    "Kharif": {"ETo": 5.0, "length_days": 120},
    "Rabi": {"ETo": 3.5, "length_days": 120},
    "Summer": {"ETo": 6.0, "length_days": 90},
    "Whole Year": {"ETo": 4.5, "length_days": 365},
    "Winter": {"ETo": 3.0, "length_days": 90}
}

GENERIC_KC = 0.9
CROP_KC_MAP = {
    "Rice": 1.15,
    "Sugarcane": 1.25,
    "Maize": 1.05,
    "Cotton(lint)": 0.8,
    "Potato": 0.9,
    "Banana": 1.1,
    "Onion": 0.75
}

def estimate_et_and_water(season_name, crop_name, area_ha):
    si = SEASON_INFO.get(season_name, {"ETo":4.5,"length_days":120})
    ETo = si["ETo"]
    days = si["length_days"]
    Kc = CROP_KC_MAP.get(crop_name, GENERIC_KC)
    etc_mm = ETo * Kc * days
    water_m3 = etc_mm * area_ha * 10.0
    water_m3_per_ha = etc_mm * 10.0
    return {"ETc_mm": round(etc_mm,2), "water_m3": round(water_m3,2), "water_m3_per_ha": round(water_m3_per_ha,2), "ETo":ETo, "Kc":Kc, "days":days}

@app.route("/")
def index():
    return render_template("index.html",
                           states=STATES,
                           tn_districts=TN_DISTRICTS,
                           seasons=SEASONS,
                           crops=CROPS)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    try:
        state_num = float(data.get("state"))
        district_num = float(data.get("district"))
        season_num = float(data.get("season"))
        crop_num = float(data.get("crop"))
        area = float(data.get("area"))
    except Exception as e:
        return jsonify({"error":"Invalid or missing numeric input", "detail": str(e)}), 400

    production_default = 0.0
    x = np.array([[state_num, district_num, season_num, crop_num, area, production_default]], dtype=float)

    if model is None:
        return jsonify({"error":"Model file not found on server. Place 'crop_yield_model.pkl' in the app root."}), 500

    try:
        if MODEL_AVAILABLE:
            pred = model.predict(x)
            predicted_yield = float(pred[0])
        else:
            predicted_yield = round(2.5 * float(data.get("area", 1)), 2)
    except Exception as e:
        return jsonify({"error":"Prediction failed", "detail": str(e)}), 500

    season_idx = int(season_num) - 1
    crop_idx = int(crop_num) - 1
    season_name = SEASONS[season_idx] if 0 <= season_idx < len(SEASONS) else SEASONS[0]
    crop_name = CROPS[crop_idx] if 0 <= crop_idx < len(CROPS) else "Unknown"
    et_info = estimate_et_and_water(season_name, crop_name, area)

    result = {
        "predicted_yield": round(predicted_yield, 4),
        "yield_units": "model units",
        "ETc_mm": et_info["ETc_mm"],
        "water_m3_total": et_info["water_m3"],
        "water_m3_per_ha": et_info["water_m3_per_ha"],
        "assumptions": {
            "production_default_used": production_default,
            "ETc_method": "estimated from season-average ETo and generic crop coefficient (Kc)",
            "ETo_mm_per_day": et_info["ETo"],
            "Kc_used": et_info["Kc"],
            "season_length_days": et_info["days"]
        }
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
