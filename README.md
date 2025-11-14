# ehr

# Stroke Diagnosis AI System

## Overview
This project is a multi-module AI system for stroke diagnosis using medical imaging and clinical data. It includes data collection, image enhancement, clinical note generation, ICD-10 coding automation, and deployment with a user-friendly interface.

---

## Module 1: Data Collection and Preprocessing

**Objective:**  
Prepare imaging and clinical data for AI model training.

**Tasks:**  
- Collect diverse medical images (CT, MRI, X-ray, Ultrasound).  
- Load patient metadata and link to images.  
- Clean, label, and standardize data for AI.  
- Extract text from images using Tesseract OCR.  
- Convert images to CNN-ready arrays.

**Output:**  
- Cleaned patient metadata DataFrame.  
- Preprocessed images ready for training.  
- Extracted OCR text from scans.

---

## Module 2: Medical Imaging Enhancement

**Objective:**  
Enhance image quality using GenAI techniques.

**Tasks:**  
- Apply denoising and super-resolution to medical images.  
- Train enhancement models (optionally with Azure OpenAI).  
- Save enhanced images for better diagnostic input.

**Output:**  
- Enhanced medical images with improved clarity.  
- Models saved for future inference.

---

## Module 3: Clinical Note Generation & ICD-10 Coding Automation

**Objective:**  
Automate clinical note creation and ICD-10 coding.

**Tasks:**  
- Generate clinical notes from structured data and predictions.  
- Map diagnosis to ICD-10 codes automatically.  
- Use NLP pipelines for text generation and coding.

**Output:**  
- Textual clinical notes per patient/image.  
- ICD-10 codes aligned with diagnoses.

---

## Module 4: Integration and Deployment

**Objective:**  
Deploy AI models and integrate with clinical workflows.

**Tasks:**  
- Build a backend API (Flask or FastAPI) to serve predictions.  
- Create a frontend interface (Streamlit) for image upload and result display.  
- Test API with real images from patient folders.  
- Enable seamless usage by clinical staff.

**Output:**  
- Running backend API serving stroke diagnosis.  
- Streamlit app for uploading scans and viewing results.  
- Logs and error handling for robust deployment.

---

## How to Run


---

## Data Requirements

### 1. ehr_data.csv
- Contains overall patient data
- Required columns (case-insensitive):  
  - `patient_id`  
  - `stroke_type`  
  - `gender`  
  - `date_of_scan`  
  - `num_images` (optional)

### 2. clinical_notes.csv
- Contains clinical notes per patient  
- Required columns:  
  - `patient_id`  
  - `clinical_note`  
  - `ehr_text`  
  - `image_findings`

### 3. Patient Images
- Stored under `/data/images/{patient_id}/`  
- Supported formats: `.jpg`, `.jpeg`, `.png`

---

## How to Run

1. **Install dependencies**:

```bash
pip install -r requirements.txt
streamlit run app.py


---

## Folder Structure

=======
# AI Enhanced EHR Imaging & Documentation System

Project Goals
The core aims of this initiative are twofold:

Enhance Medical Imaging: Utilize GenAI to improve the clarity, interpretability, and reconstruction of medical images (e.g., X-rays, MRIs, CTs).
Automate Clinical Documentation: Automate routine administrative tasks, including clinical documentation and ICD-10 coding.
These enhancements are designed to minimize the time clinicians spend on non-clinical tasks, supporting faster, more accurate decision-making.The GenAI-driven components will be powered by Azure OpenAI.


Module 1: Data Collection and Preprocessing

Objective: Prepare imaging and clinical data to ensure readiness for AI model training and application.

Key Tasks:
--Collect diverse medical imaging datasets (X-ray, MRI, CT, ultrasound, DXA).

--Gather structured and unstructured EHR content, including patient notes and coding data.

--Clean, label, and standardize all data for compatibility with GenAI models.


Module 2: Medical Imaging Enhancement

Objective: Employ GenAI to enhance image quality and provide better support for diagnosis.

Key Tasks:
--Apply GenAI for denoising and realistic reconstruction of medical images.

--Improve image resolution and clarity to support better visualization for clinicians.

--Train image enhancement models using Azure OpenAI tools.


Module 3: Clinical Note Generation & ICD-10 Coding Automation

Objective: Automate routine documentation and coding tasks using Generative AI.

Key Tasks:
--Generate clinical notes based on structured data and doctor observations.

--Automate ICD-10 coding by mapping EHR input to standard classifications.

--Decrease documentation workload through seamless integration of GenAI tools.


Module 4: Integration and Deployment

Objective: Successfully deploy and integrate the enhanced EHR features into live clinical environments.

Key Tasks:
--Deploy trained GenAI models into real-time clinical workflows.

--Integrate the solution with existing hospital EHR systems for image processing and note generation.

--Provide necessary onboarding and training sessions for medical staff to ensure effective use of the new tools.
>>>>>>> bcf3260d6b5b2d9ebe713db4351202a8a60fc034
