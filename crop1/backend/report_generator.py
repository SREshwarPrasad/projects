# backend/report_generator.py
from fpdf import FPDF
from docx import Document
from docx.shared import Pt
from io import BytesIO
import datetime

def generate_report_pdf_bytes(data: dict, language="en"):
    """
    Returns the PDF file contents as bytes.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "CropAssist - Yield Report", ln=True, align="C")
    pdf.ln(4)

    pdf.set_font("Arial", size=10)
    pdf.cell(0, 6, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(4)

    # Farmer details
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Farmer / User Details", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 6, f"Requested by: {data.get('requested_by', '')}", ln=True)
    pdf.cell(0, 6, f"Full name: {data.get('fullname','')}", ln=True)
    pdf.cell(0, 6, f"Date of birth: {data.get('dob','')}", ln=True)
    pdf.ln(4)

    # Agronomic input summary
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Inputs", ln=True)
    pdf.set_font("Arial", size=10)
    for k in ["state", "district", "season", "crop", "area", "area_unit"]:
        if k in data:
            pdf.cell(0, 6, f"{k.capitalize()}: {data.get(k)}", ln=True)
    # other inputs
    for key, val in data.items():
        if key.startswith("feature") or key not in {"requested_by","fullname","dob","state","district","season","crop","area","area_unit"}:
            pdf.cell(0, 6, f"{key}: {val}", ln=True)

    pdf.ln(6)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Prediction", ln=True)
    pdf.set_font("Arial", size=12)
    pred = data.get("yield_prediction", "")
    pdf.cell(0, 8, f"Predicted yield: {pred}", ln=True)

    # small footer
    pdf.ln(10)
    pdf.set_font("Arial", size=8)
    pdf.multi_cell(0, 5, "This is a computer-generated report from CropAssist. The model used can be replaced by placing model.pkl in the backend directory.", align="L")

    out = BytesIO()
    out.write(pdf.output(dest="S").encode("latin1"))
    return out.getvalue()

def generate_report_docx_bytes(data: dict, language="en"):
    doc = Document()
    h = doc.add_heading("CropAssist - Yield Report", level=1)
    doc.add_paragraph(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    doc.add_heading("Farmer / User Details", level=2)
    p = doc.add_paragraph()
    p.add_run(f"Requested by: {data.get('requested_by','')}\n")
    p.add_run(f"Full name: {data.get('fullname','')}\n")
    p.add_run(f"Date of birth: {data.get('dob','')}\n")

    doc.add_heading("Inputs", level=2)
    for k in ["state", "district", "season", "crop", "area", "area_unit"]:
        if k in data:
            doc.add_paragraph(f"{k.capitalize()}: {data.get(k)}")

    doc.add_heading("Prediction", level=2)
    doc.add_paragraph(f"Predicted yield: {data.get('yield_prediction','')}")

    doc.add_paragraph("\nThis is a computer-generated report from CropAssist. The model used can be replaced by placing model.pkl in the backend directory.")
    out = BytesIO()
    doc.save(out)
    return out.getvalue()
