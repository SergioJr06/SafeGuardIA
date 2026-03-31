import cv2
import torch
import os
import time
import json
from ultralytics import YOLO

# ==========================================================
# 1. CARREGAMENTO DE CONFIGURAÇÕES (JSON)
# ==========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_CONFIG = os.path.join(os.path.dirname(BASE_DIR), "configs.json")

def carregar_configuracoes():
    try:
        with open(CAMINHO_CONFIG, 'r') as f:
            data = json.load(f)
            # Pegamos a primeira câmera do JSON
            config = list(data.values())[0]
            return config
    except Exception as e:
        print(f"Erro ao carregar JSON: {e}")
        return None
        


config = carregar_configuracoes()
if not config: exit()

# ==========================================================
# 2. CONFIGURAÇÕES DE CAMINHO E PASTAS
# ==========================================================
PASTA_CAPTURES = os.path.join(os.path.dirname(BASE_DIR), "capturas_violacao")
if not os.path.exists(PASTA_CAPTURES): os.makedirs(PASTA_CAPTURES)

CAMINHO_MODELO = os.path.join(os.path.dirname(BASE_DIR), "models", "best.pt")
modelo = YOLO(CAMINHO_MODELO)

# ==========================================================
# 3. MAPEAMENTO DINÂMICO DE RISCO (Baseado no JSON)
# ==========================================================
def mapear_ids_risco(config, modelo_names):
    ids_perigo = []
    # Mapeia as chaves do JSON para termos contidos nas classes do YOLO
    mapeamento = {
        "require_helmet": "sem capacete",
        "require_glasses": "sem oculos",
        "require_gloves": "sem luvas",
        "require_boots": "sem bota",
        "require_ear_protection": "sem protetor auricular"
    }
    
    for chave, exigido in config.items():
        if exigido is True and chave in mapeamento:
            termo = mapeamento[chave]
            for id_cls, nome_cls in modelo_names.items():
                if termo in nome_cls.lower():
                    ids_perigo.append(id_cls)
    return ids_perigo

IDs_PERIGO = mapear_ids_risco(config, modelo.names)
print(f"🚨 Monitorando riscos ativos: {[modelo.names[i] for i in IDs_PERIGO]}")

# ==========================================================
# 4. LOOP DE PROCESSAMENTO OTIMIZADO
# ==========================================================
cap = cv2.VideoCapture(config['source'])
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Variáveis de controle de captura
contador_violacao = 0
LIMITE_CONFIRMACAO = 10 
COOLDOWN_FOTO = 30 # Segundos entre fotos da mesma infração
tempo_ultima_foto = 0
contador_sequencial = 1

while True:
    sucesso, frame = cap.read()
    if not sucesso: break

    # Inferência
    resultados = modelo.predict(source=frame, conf=0.45, imgsz=640, verbose=False)
    
    detecao_perigo = False
    for r in resultados:
        frame_anotado = r.plot()
        classes_detectadas = r.boxes.cls.tolist()
        if any(cls in IDs_PERIGO for cls in classes_detectadas):
            detecao_perigo = True

    # --- LÓGICA DE SNAPSHOT COM COOLDOWN ---
    agora = time.time()
    if detecao_perigo:
        contador_violacao += 1
        # Só tira foto se: atingiu o limite de frames E passou o tempo de cooldown
        if contador_violacao >= LIMITE_CONFIRMACAO and (agora - tempo_ultima_foto) > COOLDOWN_FOTO:
            data_hora = time.strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"{contador_sequencial:03d}_{data_hora}.jpg"
            cv2.imwrite(os.path.join(PASTA_CAPTURES, nome_arquivo), frame_anotado)
            
            print(f"📸 Snapshot salvo: {nome_arquivo}")
            tempo_ultima_foto = agora
            contador_sequencial += 1
    else:
        contador_violacao = 0 # Reseta se a área ficar segura

    # Interface
    status = "ALERTA" if detecao_perigo else "NORMAL"
    cor = (0, 0, 255) if detecao_perigo else (0, 255, 0)
    cv2.putText(frame_anotado, f"STATUS: {status}", (20, 50), 2, 1.2, cor, 3)
    cv2.imshow('SafeGuard IA - Integrado', frame_anotado)

    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()