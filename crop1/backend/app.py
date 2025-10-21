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
from backend.report_generator import generate_report_pdf_bytes, generate_report_docx_bytes
from backend.model_integration import predict_yield_from_model, model as default_model

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

# Try to use default_model loaded in model_integration
model = default_model

# ---------- Routes ----------
@app.route("/")
def index():
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
    # Build history items: only include prediction_saved entries for the dashboard table
    enriched = []
    for h in history:
        if h["action"].startswith("prediction_saved:"):
            try:
                payload = json.loads(h["action"].split("prediction_saved:")[1])
            except Exception:
                payload = {}
            enriched.append({
                "id": h["id"],
                "username": h["username"],
                "crop": payload.get("crop", ""),
                "state": payload.get("state", ""),
                "district": payload.get("district", ""),
                "season": payload.get("season", ""),
                "area": payload.get("area", ""),
                "area_unit": payload.get("area_unit", ""),
                "timestamp": h["timestamp"]
            })
    return render_template("dashboard.html", username=username, history=enriched)

@app.route("/logout")
def logout():
    username = session.get("username")
    if username:
        save_login_history(username, "logout")
        session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json() or {}
    username = session.get("username", "guest")
    data["username"] = username
    data["timestamp"] = datetime.now().isoformat()

    try:
        prediction = predict_yield_from_model(model, data)
    except Exception as e:
        app.logger.exception("Prediction failed; returning demo output")
        prediction = {"yield_prediction": 0.0, "notes": f"demo fallback: {str(e)}"}

    save_login_history(username, f"predicted:{data.get('crop','unknown')}")
    return jsonify(prediction)

@app.route("/download_report", methods=["POST"])
def download_report():
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

# ---------------- Save prediction ---------------- #
@app.route("/save_prediction", methods=["POST"])
def save_prediction():
    if "username" not in session:
        return jsonify({"error": "not_logged_in"}), 401

    payload = request.get_json() or {}
    username = session["username"]

    try:
        save_login_history(username, f"prediction_saved:{json.dumps(payload)}")
        return jsonify({"status": "saved"})
    except Exception as e:
        app.logger.exception("Failed to save prediction")
        return jsonify({"error": "save_failed", "details": str(e)}), 500

# ---------------- Show saved predictions ---------------- #
@app.route("/predictions")
def predictions():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    history = get_login_history(username)

    preds = []
    for h in history:
        msg = h["action"]
        if msg.startswith("prediction_saved:"):
            try:
                data = json.loads(msg.split("prediction_saved:")[1])
                data["timestamp"] = h["timestamp"]
                preds.append(data)
            except Exception:
                continue

    return render_template("predictions.html", username=username, predictions=preds)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
