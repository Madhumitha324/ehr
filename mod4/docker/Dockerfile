# Use a base image with CUDA if you target GPU; otherwise use python:3.10-slim
FROM nvidia/cuda:11.8-runtime-ubuntu22.04

# Basic deps
RUN apt-get update && apt-get install -y \
    build-essential libgl1 \
    libsm6 libxrender1 libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app/ /app
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /app/requirements.txt

# Expose
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
