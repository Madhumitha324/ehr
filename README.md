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

1. **Train Model:**  
   Run `train.py` to train the stroke classification model.

2. **Start Backend API:**  
   Run `module4_backend.py` to launch the prediction server.

3. **Test API:**  
   Run `test_api.py` to send sample images and get predictions.

4. **Start Frontend:**  
   Run `python -m streamlit run module4_streamlit.py` to launch the user interface.

---

## Folder Structure

