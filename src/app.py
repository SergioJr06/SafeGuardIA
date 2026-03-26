import streamlit as st
import json
import os

# --- Lógica de Caminho ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "..", "config", "config.json")

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

# 3. Gerar Checkboxes Dinamicamente
# Criamos duas colunas para o layout ficar mais limpo
col1, col2 = st.columns(2)
updated_values = {}

# Mapeamento de nomes técnicos para nomes amigáveis
labels = {
    "require_helmet": "Fiscalizar Capacete",
    "require_glasses": "Fiscalizar Óculos",
    "require_boots": "Fiscalizar Botas",
    "require_gloves": "Fiscalizar Luvas",
    "require_ear_protection": "Fiscalizar Protetor Auricular"
}

# Loop para criar os campos (pula a chave 'source')
for i, (key, value) in enumerate(config[cam_choice].items()):
    if key == "source":
        continue
    
    # Alterna entre col1 e col2
    target_col = col1 if i % 2 == 0 else col2
    label = labels.get(key, key.replace("require_", "Fiscalizar ").title())
    updated_values[key] = target_col.checkbox(label, value=value)

# 4. Botão Salvar
if st.button("💾 Salvar Configurações", use_container_width=True):
    config[cam_choice].update(updated_values)
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)
    st.success(f"Configurações de '{cam_choice}' salvas com sucesso!")