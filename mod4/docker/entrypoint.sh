#!/bin/bash
# Ensure model weights are in /app/assets if not present, instruct admin to place them
if [ ! -f /app/assets/RealESRGAN_x2plus.pth ]; then
  echo "⚠️ Model weights missing at /app/assets/RealESRGAN_x2plus.pth. Mount or place them there."
fi
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1
