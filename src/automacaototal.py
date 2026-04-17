import cv2
import torch
import os
import time
import json
import qrcode
import csv
from datetime import datetime
from pyngrok import ngrok
from ultralytics import YOLO

# ==========================================================
# 1. CONFIGURAÇÕES DE CAMINHO E PASTAS
# ==========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

CONFIG_PATH = os.path.join(ROOT_DIR, "config", "config.json")
MODELO_PATH = os.path.join(ROOT_DIR, "models", "best.pt")
PASTA_CAPTURES = os.path.join(ROOT_DIR, "capturas_violacao")
LOG_PATH = os.path.join(ROOT_DIR, "relatorio_violacoes.csv") # <-- Banco de Dados

if not os.path.exists(PASTA_CAPTURES):
    os.makedirs(PASTA_CAPTURES)

# ==========================================================
# 2. FUNÇÕES DE APOIO E LOG DE DADOS
# ==========================================================
def registrar_violacao(tipo, conf, foto_nome):
    """Grava a infração no arquivo CSV"""
    file_exists = os.path.isfile(LOG_PATH)
    with open(LOG_PATH, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Data_Hora", "Infracao", "Confianca", "Arquivo_Foto"])
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([agora, tipo, f"{conf:.2f}", foto_nome])

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
# 3.1 Ngrok
try:
    url_publica = ngrok.connect(8501, "http").public_url
    print(f"\n🌍 DASHBOARD ONLINE: {url_publica}")
    qr = qrcode.QRCode()
    qr.add_data(url_publica)
    qr.print_ascii() 
except Exception as e:
    print(f"⚠️ Erro ao subir Ngrok: {e}. Verifique se a porta 8501 está livre.")

# 3.2 IA
modelo = YOLO(MODELO_PATH)
device = 0 if torch.cuda.is_available() else 'cpu'
print(f"👁️ Engine de Visão Ativa em {device}...")

# ==========================================================
# 4. LOOP PRINCIPAL (COM RESILIÊNCIA ANTI-FALHA)
# ==========================================================
# Este 'while True' externo garante que se a câmera cair, o sistema recomeça
while True:
    try:
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
        LIMITE_CONFIRMACAO = 60
        contador_violacao = 0
        contador_sequencial = 1

        # Loop interno rodando enquanto a câmera estiver viva
        while cap.isOpened():
            sucesso, frame = cap.read()
            if not sucesso:
                print("⚠️ Falha na leitura do frame. Tentando reconectar a câmera...")
                break # Quebra o loop interno para tentar ligar a câmera de novo

            frame_count += 1

            # RECARGA DINÂMICA: Lê o JSON a cada 30 frames
            if frame_count % 30 == 0:
                try:
                    with open(CONFIG_PATH, 'r') as f:
                        config_refresh = json.load(f)[CAM_ESCOLHIDA]
                        IDs_PERIGO = mapear_ids_risco(config_refresh, modelo.names)
                except:
                    pass

            # Inferência
            results = modelo.predict(source=frame, conf=0.35, imgsz=960, device=device, verbose=False)
            frame_anotado = results[0].plot()
            
            # --- NOVA LÓGICA DE RISCO (Extraindo nomes para o CSV) ---
            classes_detectadas = results[0].boxes.cls.tolist()
            confiancas = results[0].boxes.conf.tolist()
            
            infracoes_atuais = []
            maior_conf = 0.0

            # Verifica qual classe perigosa foi detectada e pega o nome e confiança
            for i, cls_id in enumerate(classes_detectadas):
                if cls_id in IDs_PERIGO:
                    nome_infracao = modelo.names[int(cls_id)]
                    infracoes_atuais.append(nome_infracao)
                    if confiancas[i] > maior_conf:
                        maior_conf = confiancas[i]

            detecao_perigo = len(infracoes_atuais) > 0

            # Snapshot com Antifalha, Cooldown e Gravação no CSV
            agora = time.time()
            if detecao_perigo:
                contador_violacao += 1
                if contador_violacao >= LIMITE_CONFIRMACAO and (agora - tempo_ultima_foto) > COOLDOWN_FOTO:
                    data_hora = time.strftime("%Y%m%d_%H%M%S")
                    nome_arq = f"{contador_sequencial:03d}_{data_hora}.jpg"
                    cv2.imwrite(os.path.join(PASTA_CAPTURES, nome_arq), frame_anotado)
                    
                    # Salva no Banco de Dados (CSV)
                    nomes_infracao_str = ", ".join(set(infracoes_atuais))
                    registrar_violacao(nomes_infracao_str, maior_conf, nome_arq)
                    
                    print(f"📸 VIOLAÇÃO SALVA E REGISTRADA: {nome_arq}")
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

            if cv2.waitKey(1) & 0xFF == ord('q'): 
                cap.release()
                cv2.destroyAllWindows()
                exit() # Sai completamente do programa

    except Exception as e:
        print(f"🔥 Erro crítico na execução: {e}. Reiniciando sistema em 5 segundos...")
        time.sleep(5)