import streamlit as st
import json
import os

# --- Lógica de Caminho Profissional ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# app.py está em /src, então '..' volta para a raiz e entra em /config
CONFIG_PATH = os.path.join(os.path.dirname(BASE_DIR), "config", "config.json")

st.set_page_config(page_title="SafeGuard AI", page_icon="🛡️", layout="wide")

st.title("🛡️ SafeGuard AI - Painel de Controle")

# 1. Carregar Configurações
try:
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
except Exception as e:
    st.error(f"Erro ao carregar config.json: {e}")
    st.stop()

# 2. Seleção da Câmera
cam_choice = st.selectbox("Selecione a Câmera", list(config.keys()))

st.divider()
st.subheader(f"⚙️ Configurações para: {cam_choice}")

col1, col2 = st.columns(2)
updated_values = {}

# Mapeamento atualizado com as novas classes do Roboflow
labels = {
    "require_helmet": "Fiscalizar Capacete",
    "require_glasses": "Fiscalizar Óculos",
    "require_boots": "Fiscalizar Botas",
    "require_gloves": "Fiscalizar Luvas",
    "require_ear_protection": "Fiscalizar Protetor Auricular",
    "require_mask": "Fiscalizar Máscara (EPI)",
    "require_vest": "Fiscalizar Colete Refletivo"
}

# 3. Gerar Checkboxes Dinamicamente
items = [k for k in config[cam_choice].keys() if k != "source"]
for i, key in enumerate(items):
    value = config[cam_choice][key]
    target_col = col1 if i % 2 == 0 else col2
    label = labels.get(key, key.replace("require_", "Fiscalizar ").title())
    updated_values[key] = target_col.checkbox(label, value=value)

# 4. Botão Salvar
if st.button("💾 Salvar Configurações", use_container_width=True):
    config[cam_choice].update(updated_values)
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)
    st.success(f"Configurações de '{cam_choice}' salvas com sucesso!")