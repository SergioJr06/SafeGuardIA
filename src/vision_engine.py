import time
from ultralytics import YOLO
import cv2
import json

# Carrega o modelo YOLOv8 treinado
model = YOLO('models/best.pt')

def rodar_monitoramento():
    cap = cv2.VideoCapture(0)
    
    last_config_check = 0
    config = {}

    while True:
        # A cada 2 segundos, relê o arquivo para ver se algo mudou no site
        if time.time() - last_config_check > 2:
            with open('config/config.json', 'r') as f:
                config = json.load(f)["camera_webcam"]
            last_config_check = time.time()

        ret, frame = cap.read()
        results = model(frame) # IA detecta tudo

        # Lógica de decisão:
        for r in results:
            for box in r.boxes:
                classe = model.names[int(box.cls)]
                
                # SÓ GERA ALERTA SE ESTIVER MARCADO NO CONFIG
                if classe == "no_helmet" and config["require_helmet"]:
                    print("🚨 ALERTA: FALTA DE CAPACETE!")
                    # Aqui você desenha o quadrado vermelho no frame