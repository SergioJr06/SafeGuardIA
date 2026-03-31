import cv2
import torch
import os
import time
import json
import qrcode
from pyngrok import ngrok
from ultralytics import YOLO

# ==========================================================
# 1. CONFIGURAÇÕES DE CAMINHO E PASTAS
# ==========================================================
# Caminho absoluto para evitar o erro de src/src
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

CONFIG_PATH = os.path.join(ROOT_DIR, "config", "config.json")
MODELO_PATH = os.path.join(ROOT_DIR, "models", "best.pt")
PASTA_CAPTURES = os.path.join(ROOT_DIR, "capturas_violacao")

if not os.path.exists(PASTA_CAPTURES):
    os.makedirs(PASTA_CAPTURES)

# ==========================================================
# 2. FUNÇÕES DE APOIO (Lógica de Negócio)
# ==========================================================
def mapear_ids_risco(config_camera, modelo_names):
    """Mapeia o que o JSON pede para fiscalizar com as classes da IA"""
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
# 3. INICIALIZAÇÃO DO SISTEMA
# ==========================================================
# 3.1 Ngrok (O Token deve estar configurado no seu PC)
try:
    url_publica = ngrok.connect(8501,"http").public_url
    print(f"\n🌍 DASHBOARD ONLINE: {url_publica}")
    qr = qrcode.QRCode()
    qr.add_data(url_publica)
    qr.print_ascii() 
except Exception as e:
    print(f"⚠️ Erro ao subir Ngrok: {e}. Verifique se a porta 5000 está livre.")

# 3.2 IA e Câmera
modelo = YOLO(MODELO_PATH)
device = 0 if torch.cuda.is_available() else 'cpu'

# Carregamento Inicial do JSON
with open(CONFIG_PATH, 'r') as f:
    data_config = json.load(f)
    CAM_ESCOLHIDA = "camera_webcam" # Ou automatize a escolha
    config = data_config[CAM_ESCOLHIDA]

IDs_PERIGO = mapear_ids_risco(config, modelo.names)
cap = cv2.VideoCapture(config['source'])
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Variáveis de Controle
frame_count = 0
tempo_ultima_foto = 0
COOLDOWN_FOTO = 30 
LIMITE_CONFIRMACAO = 10 # Debounce para evitar falso positivo
contador_violacao = 0
contador_sequencial = 1

print(f"👁️ Engine de Visão Ativa em {device}...")

# ==========================================================
# 4. LOOP PRINCIPAL
# ==========================================================
while True:
    sucesso, frame = cap.read()
    if not sucesso: break

    frame_count += 1

    # RECARGA DINÂMICA: Lê o JSON a cada 2 segundos aprox.
    if frame_count % 30 == 0:
        try:
            with open(CONFIG_PATH, 'r') as f:
                config_refresh = json.load(f)[CAM_ESCOLHIDA]
                IDs_PERIGO = mapear_ids_risco(config_refresh, modelo.names)
        except:
            pass # Pula se o arquivo estiver sendo escrito pelo Streamlit

    # Inferência
    results = modelo.predict(source=frame, conf=0.45, imgsz=640, device=device, verbose=False)
    frame_anotado = results[0].plot()
    
    # Lógica de Risco
    classes_detectadas = results[0].boxes.cls.tolist()
    detecao_perigo = any(cls in IDs_PERIGO for cls in classes_detectadas)

    # Snapshot com Antifalha e Cooldown
    agora = time.time()
    if detecao_perigo:
        contador_violacao += 1
        if contador_violacao >= LIMITE_CONFIRMACAO and (agora - tempo_ultima_foto) > COOLDOWN_FOTO:
            data_hora = time.strftime("%Y%m%d_%H%M%S")
            nome_arq = f"{contador_sequencial:03d}_{data_hora}.jpg"
            cv2.imwrite(os.path.join(PASTA_CAPTURES, nome_arq), frame_anotado)
            
            print(f"📸 VIOLAÇÃO SALVA: {nome_arq}")
            tempo_ultima_foto = agora
            contador_sequencial += 1
    else:
        contador_violacao = 0

    # Interface Visual
    status_txt = "RISCO!" if detecao_perigo else "SEGURO"
    cor_txt = (0, 0, 255) if detecao_perigo else (0, 255, 0)
    cv2.putText(frame_anotado, f"STATUS: {status_txt}", (20, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, cor_txt, 3)

    cv2.imshow('SafeGuard IA - Engine Monitor', frame_anotado)

    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()