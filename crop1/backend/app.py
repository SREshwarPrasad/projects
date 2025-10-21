# backend/app.py
import os
import json
import pickle
from datetime import datetime
from io import BytesIO

from flask import (
    Flask, render_template, request, redirect, url_for,
    session, jsonify, send_file, flash
)
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

from backend.database import (
    init_db, get_user, create_user, save_login_history,
    get_login_history, delete_login_entry, update_login_entry
)
from backend.report_generator import (
    generate_report_pdf_bytes, generate_report_docx_bytes
)
from backend.model_integration import predict_yield_from_model


# App setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "..", "frontend", "templates"),
            static_folder=os.path.join(BASE_DIR, "..", "frontend", "static"))
app.secret_key = os.environ.get("FLASK_SECRET", "super-secret-key")
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)

# Ensure DB exists
init_db()

# Load model (if available). Place your model file as backend/model.pkl
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
model = None
if os.path.exists(MODEL_PATH):
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
            app.logger.info("Model loaded from %s", MODEL_PATH)
    except Exception as e:
        app.logger.warning("Failed to load model: %s", e)
else:
    app.logger.warning("No model.pkl found at %s; app will run in demo mode", MODEL_PATH)

# ---------- Routes ----------

@app.route("/")
def index():
    # Serves the entry page (frontend/templates/index.html)
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = get_user(username)
        if user and check_password_hash(user["password"], password):
            session["username"] = username
            save_login_history(username, "login")
            return redirect(url_for("dashboard"))
        error = "Invalid credentials"
        flash(error, "danger")
    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        fullname = request.form.get("fullname", "").strip()
        dob = request.form.get("dob", "").strip()
        if get_user(username):
            error = "User already exists"
            flash(error, "danger")
        else:
            hashed = generate_password_hash(password)
            create_user(username, hashed, fullname, dob)
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))
    return render_template("register.html", error=error)


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    history = get_login_history(username)
    return render_template("dashboard.html", username=username, history=history)


@app.route("/logout")
def logout():
    username = session.get("username")
    if username:
        save_login_history(username, "logout")
        session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/predict", methods=["POST"])
def predict():
    """
    Expects JSON with keys:
    - state, district, season, crop, area, area_unit, additional numeric features...
    The model integration function will decide which features to use.
    """
    data = request.get_json() or {}
    # ensure expected fields
    username = session.get("username", "guest")
    data["username"] = username
    data["timestamp"] = datetime.now().isoformat()

    try:
        prediction = predict_yield_from_model(model, data)
    except Exception as e:
        app.logger.exception("Prediction failed; returning demo output")
        prediction = {"yield_prediction": 0.0, "notes": f"demo fallback: {str(e)}"}

    # Save login history entry for predict (optional)
    save_login_history(username, f"predicted:{data.get('crop','unknown')}")
    return jsonify(prediction)


@app.route("/download_report", methods=["POST"])
def download_report():
    """
    Expects JSON:
      {
        "report_type": "pdf" or "docx",
        "language": "en",
        "data": { ... }  # prediction + user details
      }
    Returns a file as attachment.
    """
    payload = request.get_json() or {}
    rpt_type = payload.get("report_type", "pdf").lower()
    language = payload.get("language", "en")
    data = payload.get("data", {})

    username = session.get("username", "guest")
    data["requested_by"] = username

    try:
        if rpt_type == "docx":
            file_bytes = generate_report_docx_bytes(data)
            mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            filename = f"report_{username}.docx"
        else:
            file_bytes = generate_report_pdf_bytes(data)
            mime = "application/pdf"
            filename = f"report_{username}.pdf"

        return send_file(
            BytesIO(file_bytes),
            mimetype=mime,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        app.logger.exception("Failed to generate report")
        return jsonify({"error": "Report generation failed", "details": str(e)}), 500


@app.route("/save_prediction", methods=["POST"])
def save_prediction():
    if "username" not in session:
        return jsonify({"error": "not_logged_in"}), 401
    payload = request.get_json() or {}
    # create a simple table 'predictions' in DB, or reuse login_history to store JSON
    # Example: save into login_history as type 'prediction' (quick implementation)
    username = session["username"]
    pred = json.dumps(payload)
    save_login_history(username, f"prediction:{pred}")
    return jsonify({"status": "saved"})


