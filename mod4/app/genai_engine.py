# app/genai_engine.py
import os
import numpy as np
from PIL import Image
import io
import cv2
from tqdm import tqdm

# Use the methods from your previous code
from typing import List, Tuple

# If using Real-ESRGAN python wrapper:
try:
    from realesrgan import RealESRGAN
    _HAS_REALESRGAN = True
except Exception:
    _HAS_REALESRGAN = False

# ---------------------------
# Utilities
# ---------------------------
def pil_to_gray_np(pil_img: Image.Image, target_size=(256,256)) -> np.ndarray:
    pil = pil_img.convert("L").resize(target_size)
    arr = np.array(pil).astype(np.float32) / 255.0
    return arr

def np_to_pil(img_np: np.ndarray) -> Image.Image:
    arr8 = (np.clip(img_np, 0, 1) * 255).astype('uint8')
    return Image.fromarray(arr8)

# ---------------------------
# GenAI enhancement (Real-ESRGAN)
# ---------------------------
class GenAIEngine:
    def __init__(self, model_path=None, device='cuda', scale=2):
        self.device = device
        self.scale = scale
        self.model_path = model_path
        self.model = None
        if _HAS_REALESRGAN:
            try:
                self.model = RealESRGAN(device, scale=scale)
                if model_path:
                    self.model.load_weights(model_path)
            except Exception as e:
                print("⚠️ RealESRGAN init error:", e)
                self.model = None

    def enhance_pil(self, pil_image: Image.Image) -> Image.Image:
        """Enhance a single PIL image via Real-ESRGAN (fallback: basic sharpening)."""
        if self.model:
            try:
                out = self.model.predict(pil_image)
                return out
            except Exception as e:
                print("⚠️ GenAI enhancement failed, falling back:", e)

        # Fallback: simple OpenCV sharpening if GenAI is not available
        img_gray = np.array(pil_image.convert("L"))
        kernel = np.array([[0, -1, 0],[-1, 5,-1],[0,-1,0]])
        sharpen = cv2.filter2D(img_gray, -1, kernel)
        return Image.fromarray(sharpen)

    def enhance_bytes(self, file_bytes: bytes) -> bytes:
        pil = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        out = self.enhance_pil(pil)
        buf = io.BytesIO()
        out.save(buf, format="PNG")
        return buf.getvalue()

# ---------------------------
# Feature extraction (adapted from user code)
# ---------------------------
def calculate_entropy(image: np.ndarray):
    hist = np.histogram(image, bins=256, range=(0, 1))[0]
    hist = hist / (hist.sum() + 1e-10)
    entropy = -np.sum(hist * np.log2(hist + 1e-10))
    return float(entropy)

def estimate_brain_area(image: np.ndarray):
    img_8bit = (image * 255).astype(np.uint8)
    try:
        _, thresh = cv2.threshold(img_8bit, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest)
            return float(area / (image.shape[0] * image.shape[1]))
    except Exception:
        return 0.0
    return 0.0

def extract_basic_features(pil_image: Image.Image, target_size=(256,256)):
    gray_np = pil_to_gray_np(pil_image, target_size)
    features = {
        "mean_intensity": float(np.mean(gray_np)),
        "std_intensity": float(np.std(gray_np)),
        "contrast": float(np.max(gray_np) - np.min(gray_np)),
        "entropy": calculate_entropy(gray_np),
        "brain_area_ratio": estimate_brain_area(gray_np)
    }
    return features
