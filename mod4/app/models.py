# app/models.py
from pydantic import BaseModel
from typing import Dict, Optional

class EnhanceResponse(BaseModel):
    filename: str
    enhanced_image_base64: str

class FeaturesResponse(BaseModel):
    patient_id: str
    features: Dict[str, float]

class NoteRequest(BaseModel):
    patient_id: str
    features: Dict[str, float]
    sr_text: Optional[str] = None  # free text from clinician or OCR

def generate_clinical_note(patient_id: str, features: Dict[str, float], sr_text: str = None) -> str:
    # Simple templated note generator. In production you could call a controlled LLM
    note = []
    note.append(f"Patient: {patient_id}")
    note.append("Automated Image Analysis Summary:")
    for k, v in features.items():
        note.append(f" - {k}: {v:.4f}")
    if sr_text:
        note.append("\nClinician notes / OCR extracted:")
        note.append(sr_text)
    note.append("\nRecommendation: Review enhanced images and correlate with clinical exam.")
    return "\n".join(note)
