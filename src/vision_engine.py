import cv2
import torch
import os
import time
import json
from ultralytics import YOLO

# ==========================================================
# 1. CONFIGURAÇÕES DE CAMINHO E HARDWARE
# ==========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Ajuste para subir uma pasta e entrar em /config
CONFIG_PATH = os.path.join(os.path.dirname(BASE_DIR), "config", "config.json")
PASTA_CAPTURES = os.path.join(os.path.dirname(BASE_DIR), "capturas_violacao")
CAMINHO_MODELO = os.path.join(os.path.dirname(BASE_DIR), "models", "best.pt")

if not os.path.exists(PASTA_CAPTURES): os.makedirs(PASTA_CAPTURES)

# Auto-detecção de Hardware (Crucial para sua GTX vs Notebook)
DEVICE = 0 if torch.cuda.is_available() else 'cpu'
HALF = True if torch.cuda.is_available() else False
print(f"📡 Engine rodando em: {DEVICE}")

# ==========================================================
# 2. FUNÇÕES DE APOIO
# ==========================================================
def mapear_ids_risco(config_camera, modelo_names):
    ids_perigo = []
    mapeamento = {
        "require_helmet": "sem capacete",
        "require_glasses": "sem oculos",
        "require_gloves": "sem luvas",
        "require_boots": "sem bota",
        "require_ear_protection": "sem protetor auricular",
        "require_mask": "sem mascara",
        "require_vest": "sem colete"
    }
    for chave, exigido in config_camera.items():
        if exigido is True and chave in mapeamento:
            termo = mapeamento[chave]
            for id_cls, nome_cls in modelo_names.items():
                if termo in nome_cls.lower():
                    ids_perigo.append(id_cls)
    return ids_perigo

# ==========================================================
# 3. INICIALIZAÇÃO
# ==========================================================
modelo = YOLO(CAMINHO_MODELO)

# Carregamento inicial
with open(CONFIG_PATH, 'r') as f:
    data_config = json.load(f)
    # Selecionamos a câmera desejada (ex: a do celular)
    CAM_ESCOLHIDA = "camera_celular_sergio" 
    config = data_config[CAM_ESCOLHIDA]

IDs_PERIGO = mapear_ids_risco(config, modelo.names)

cap = cv2.VideoCapture(config['source'])
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

frame_count = 0
tempo_ultima_foto = 0
contador_sequencial = 1
COOLDOWN_FOTO = 30 
LIMITE_CONFIRMACAO = 10
contador_violacao = 0

print(f"🚨 Monitorando: {[modelo.names[i] for i in IDs_PERIGO]}")

# ==========================================================
# 4. LOOP PRINCIPAL
# ==========================================================
while True:
    sucesso, frame = cap.read()
    if not sucesso: break

    frame_count += 1

    # RECARGA DINÂMICA: A cada 30 frames, lê o JSON para ver se o site mudou algo
    if frame_count % 30 == 0:
        try:
            with open(CONFIG_PATH, 'r') as f:
                data_refresh = json.load(f)
                config = data_refresh[CAM_ESCOLHIDA]
                IDs_PERIGO = mapear_ids_risco(config, modelo.names)
        except: pass

    # Inferência otimizada
    resultados = modelo.predict(source=frame, conf=0.45, imgsz=640, device=DEVICE, half=HALF, verbose=False)
    
    detecao_perigo = False
    for r in resultados:
        frame_anotado = r.plot()
        classes_detectadas = r.boxes.cls.tolist()
        if any(cls in IDs_PERIGO for cls in classes_detectadas):
            detecao_perigo = True

    # Lógica de Snapshot
    agora = time.time()
    if detecao_perigo:
        contador_violacao += 1
        if contador_violacao >= LIMITE_CONFIRMACAO and (agora - tempo_ultima_foto) > COOLDOWN_FOTO:
            nome_arq = f"{contador_sequencial:03d}_{time.strftime('%H%M%S')}.jpg"
            cv2.imwrite(os.path.join(PASTA_CAPTURES, nome_arq), frame_anotado)
            tempo_ultima_foto = agora
            contador_sequencial += 1
            print(f"📸 Snapshot: {nome_arq}")
    else:
        contador_violacao = 0

    cv2.imshow('SafeGuard IA', frame_anotado)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()