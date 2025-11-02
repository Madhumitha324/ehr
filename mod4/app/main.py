# app/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import base64
import io
from PIL import Image
import os

# Local imports (make sure these exist)
from .genai_engine import GenAIEngine, extract_basic_features
from .fhir_client import SimpleFHIRClient
from .models import generate_clinical_note, NoteRequest

# ---------------------------------------------------------
# ⚙️ Initialize the FastAPI App
# ---------------------------------------------------------
app = FastAPI(title="Stroke GenAI Image Service (Module 4)")

# ---------------------------------------------------------
# 🌍 Enable CORS for frontend integration
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# 🤖 Load GenAI Enhancement Model
# ---------------------------------------------------------
MODEL_PATH = os.environ.get("REALESRGAN_WEIGHTS", "/app/assets/RealESRGAN_x2plus.pth")
device = os.environ.get("DEVICE", "cpu")
genai = GenAIEngine(model_path=MODEL_PATH, device=device, scale=2)

# ---------------------------------------------------------
# 🏥 Configure FHIR Client (Hospital System)
# ---------------------------------------------------------
FHIR_BASE = os.environ.get("FHIR_BASE", "http://localhost:8080/fhir")
FHIR_TOKEN = os.environ.get("FHIR_TOKEN", None)
fhir_client = SimpleFHIRClient(FHIR_BASE, bearer_token=FHIR_TOKEN)

# ---------------------------------------------------------
# 🧠 Endpoint 1 — Enhance Stroke Image
# ---------------------------------------------------------
@app.post("/enhance/")
async def enhance_image(patient_id: str, file: UploadFile = File(...)):
    """
    Enhance medical image using GenAI model and return base64 string.
    Also stores the enhanced image in the FHIR system (if configured).
    """
    content = await file.read()
    enhanced_bytes = genai.enhance_bytes(content)
    encoded = base64.b64encode(enhanced_bytes).decode("utf-8")

    # Try to store in FHIR
    try:
        status, text = fhir_client.push_document_reference(
            patient_id, enhanced_bytes, file.filename, mime=file.content_type
        )
    except Exception as e:
        status, text = None, str(e)

    return {
        "filename": file.filename,
        "enhanced_image_base64": encoded,
        "fhir_status": status,
        "fhir_resp": text,
    }

# ---------------------------------------------------------
# 📊 Endpoint 2 — Extract Basic Image Features
# ---------------------------------------------------------
@app.post("/features/")
async def features(patient_id: str, file: UploadFile = File(...)):
    """
    Extracts features (like lesion area, hemorrhage probability, etc.)
    from stroke MRI image, and pushes data to FHIR as Observations.
    """
    content = await file.read()
    pil = Image.open(io.BytesIO(content)).convert("RGB")
    feats = extract_basic_features(pil)

    # Try to store features in FHIR
    try:
        status, text = fhir_client.push_observation(
            patient_id, "Automated Image Features", feats
        )
    except Exception as e:
        status, text = None, str(e)

    return {
        "patient_id": patient_id,
        "features": feats,
        "fhir_status": status,
        "fhir_resp": text,
    }

# ---------------------------------------------------------
# 📝 Endpoint 3 — Generate Clinical Note + Save Locally
# ---------------------------------------------------------
@app.post("/generate_note/")
async def generate_note_endpoint(req: NoteRequest):
    """
    Generates a clinical note for stroke analysis, stores it both locally
    and optionally in a connected FHIR server.
    """
    # Step 1: Generate the note
    note = generate_clinical_note(req.patient_id, req.features, req.sr_text)

    # Step 2: Save locally
    try:
        output_dir = os.path.join(os.getcwd(), "outputs")
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"{req.patient_id}_note.txt")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(note)

        local_status = f"✅ Note saved locally at: {file_path}"
    except Exception as e:
        local_status = f"❌ Failed to save note locally: {str(e)}"

    # Step 3: Push note to FHIR
    try:
        doc_bytes = note.encode("utf-8")
        status, text = fhir_client.push_document_reference(
            req.patient_id, doc_bytes, "auto_note.txt", mime="text/plain"
        )
    except Exception as e:
        status, text = None, str(e)

    # Step 4: Return combined result
    return {
        "note": note,
        "local_status": local_status,
        "fhir_status": status,
        "fhir_resp": text,
    }

# ---------------------------------------------------------
# 🏁 Root Endpoint — Health Check
# ---------------------------------------------------------
@app.get("/")
def root():
    return {"message": "✅ Stroke EHR GenAI Deployment API is running successfully."}
