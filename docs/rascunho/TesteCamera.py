import cv2
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "..", "config", "config.json")

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

# Pega a primeira câmera que aparecer no arquivo
primeira_cam = list(config.keys())[3]
dados_da_cam = config[primeira_cam]

# Tenta pegar 'source', se não tiver, tenta 'ip'
source = dados_da_cam.get('source', dados_da_cam.get('ip'))

if source is None:
    print(f"❌ Erro: Não achei 'source' ou 'ip' em {primeira_cam}")
    print(f"Chaves disponíveis: {list(dados_da_cam.keys())}")
else:
    print(f"✅ Tentando conectar em: {source}")
    cap = cv2.VideoCapture(source)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Aguardando stream...")
            continue
        cv2.imshow("SafeGuard IA - Visualizando Celular", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()