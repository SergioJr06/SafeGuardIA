import sys
import cv2
import torch
import ultralytics
import streamlit
import roboflow
import paho.mqtt.client as mqtt

print("--- 🛡️ SafeGuard AI: Relatório de Saúde do Ambiente ---")
print(f"🐍 Python Version: {sys.version}")
print(f"📸 OpenCV: {cv2.__version__}")
print(f"🧠 PyTorch: {torch.__version__} | GPU disponível: {torch.cuda.is_available()}")
print(f"🚀 YOLO (Ultralytics): {ultralytics.__version__}")
print(f"📊 Streamlit: {streamlit.__version__}")
print(f"☁️ Roboflow: {roboflow.__version__}")
print(f"📡 MQTT Client: OK")
print("-" * 45)
print("✅ Se você leu tudo isso sem erros, seu ambiente está PRONTO!")