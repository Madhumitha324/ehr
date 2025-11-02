# app/fhir_client.py
import requests
import base64
import json
from typing import Optional

class SimpleFHIRClient:
    def __init__(self, base_url: str, bearer_token: Optional[str] = None):
        """
        base_url: e.g. https://hapi.fhir.server/fhir
        bearer_token: if your FHIR server requires a token (SMART on FHIR)
        """
        self.base = base_url.rstrip('/')
        self.headers = {'Content-Type': 'application/fhir+json'}
        if bearer_token:
            self.headers['Authorization'] = f'Bearer {bearer_token}'

    def push_document_reference(self, patient_id: str, file_bytes: bytes, filename: str, mime='image/png'):
        url = f"{self.base}/DocumentReference"
        payload = {
            "resourceType": "DocumentReference",
            "status": "current",
            "type": {"text": "Enhanced Stroke Image"},
            "subject": {"reference": f"Patient/{patient_id}"},
            "content": [
                {
                    "attachment": {
                        "contentType": mime,
                        "data": base64.b64encode(file_bytes).decode('utf-8'),
                        "title": filename
                    }
                }
            ]
        }
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.status_code, resp.text

    def push_observation(self, patient_id: str, code_text: str, value_dict: dict):
        url = f"{self.base}/Observation"
        payload = {
            "resourceType": "Observation",
            "status": "final",
            "code": {"text": code_text},
            "subject": {"reference": f"Patient/{patient_id}"},
            "component": [{"code": {"text": k}, "valueString": str(v)} for k, v in value_dict.items()]
        }
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.status_code, resp.text
