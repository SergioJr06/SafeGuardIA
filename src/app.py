import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
import os
from datetime import datetime

# ==========================================================
# 1. CAMINHOS ABSOLUTOS
# ==========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

CONFIG_PATH = os.path.join(ROOT_DIR, "config", "config.json")
LOG_PATH    = os.path.join(ROOT_DIR, "relatorio_violacoes.csv")
PASTA_CAPTURES = os.path.join(ROOT_DIR, "capturas_violacao")

st.set_page_config(
    page_title="SafeGuard IA",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================================
# 2. CSS GLOBAL (Com correções visuais)
# ==========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;700;900&display=swap');

/* ── Reset & base ───────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Exo 2', sans-serif;
    background-color: #0a0e17 !important;
    color: #c8d6e5 !important;
}

.stApp {
    background-color: #0a0e17;
    background-image:
        linear-gradient(rgba(0,220,200,.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,220,200,.03) 1px, transparent 1px);
    background-size: 40px 40px;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 3rem 3rem !important; }

/* ── Ocultar o irritante "Press Enter to apply" ──────── */
div[data-testid="InputInstructions"] {
    display: none !important;
    visibility: hidden !important;
}

/* ── Cabeçalho customizado ──────────────────────────── */
.sg-header {
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 1.4rem 2rem;
    background: linear-gradient(135deg, #0d1b2a 0%, #112240 100%);
    border: 1px solid #1e3a5f;
    border-left: 4px solid #00dcc8;
    border-radius: 8px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 24px rgba(0,220,200,.08);
}
.sg-header-icon { font-size: 2.4rem; }
.sg-header-title { font-size: 1.9rem; font-weight: 900; letter-spacing: 2px; color: #ffffff; text-transform: uppercase; line-height: 1.1; }
.sg-header-sub { font-family: 'Share Tech Mono', monospace; font-size: .75rem; color: #00dcc8; letter-spacing: 3px; text-transform: uppercase; margin-top: 2px; }
.sg-header-status { margin-left: auto; text-align: right; }

/* ── Cartões de métrica ─────────────────────────────── */
.metric-card { background: linear-gradient(135deg, #0d1b2a, #112240); border: 1px solid #1e3a5f; border-radius: 8px; padding: 1.2rem 1.4rem; position: relative; }
.metric-card::before { content: ''; position: absolute; top: 0; left: 0; width: 3px; height: 100%; }
.metric-card.green::before  { background: #00dcc8; }
.metric-card.red::before    { background: #ff4757; }
.metric-card.yellow::before { background: #ffa502; }
.metric-card.blue::before   { background: #5352ed; }
.metric-label { font-family: 'Share Tech Mono', monospace; font-size: .68rem; letter-spacing: 2px; text-transform: uppercase; color: #5f7b99; margin-bottom: .35rem; }
.metric-value { font-size: 2.2rem; font-weight: 900; line-height: 1; color: #ffffff; }

/* ── UI Elements ──────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] { background: #0d1b2a; border-bottom: 1px solid #1e3a5f; border-radius: 8px 8px 0 0; padding: 0 1rem; }
.stTabs [data-baseweb="tab"] { font-family: 'Exo 2', sans-serif; font-weight: 600; color: #5f7b99 !important; text-transform: uppercase; padding: .9rem 1.4rem; background: transparent !important; border:none !important; }
.stTabs [aria-selected="true"] { color: #00dcc8 !important; border-bottom: 2px solid #00dcc8 !important; }
.stTabs [data-baseweb="tab-panel"] { background: #0d1b2a; border: 1px solid #1e3a5f; border-top: none; border-radius: 0 0 8px 8px; padding: 1.8rem; }
.stCheckbox [data-testid="stCheckbox"] { background: #112240 !important; border: 1px solid #1e3a5f !important; border-radius: 6px !important; padding: .7rem 1rem; }
.stButton > button[kind="primary"] { background: linear-gradient(135deg, #00dcc8, #0097a7) !important; color: #0a0e17 !important; font-weight: 700 !important; letter-spacing: 1.5px !important; }

/* ── Login page (Ajuste de Espaçamento e Estilo) ────── */
.login-wrap { max-width: 420px; margin: 6vh auto 0 auto; background: linear-gradient(160deg, #0d1b2a, #112240); border: 1px solid #1e3a5f; border-top: 3px solid #00dcc8; border-radius: 12px; padding: 3.5rem 2.4rem; text-align: center; }
.login-icon { font-size: 3.5rem; margin-bottom: 1rem; }
.login-title { font-size: 1.6rem; font-weight: 900; color: #fff; margin-bottom: 2rem; } /* Mais espaço aqui */
.stTextInput label { 
    color: #5f7b99 !important; 
    font-size: 0.75rem !important; 
    font-weight: 400 !important; 
    letter-spacing: 3px !important; 
    text-align: center !important; 
    display: block !important; 
    margin-bottom: 8px !important; 
}
.stTextInput input { background: #0a0e17 !important; color: #c8d6e5 !important; text-align: center !important; padding: 0.8rem !important; font-size: 1.2rem !important; letter-spacing: 5px !important;}
.sg-section-title { font-size: .72rem; font-family: 'Share Tech Mono', monospace; letter-spacing: 3px; color: #00dcc8; border-bottom: 1px solid #1e3a5f; padding-bottom: .6rem; margin: 1.5rem 0 1.2rem 0; }
</style>
""", unsafe_allow_html=True)

# ==========================================================
# 3. FUNÇÕES DE APOIO
# ==========================================================
def carregar_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f: return json.load(f)
    return {}

def salvar_config(dados):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w') as f: json.dump(dados, f, indent=4)

def contar_violacoes():
    if os.path.exists(LOG_PATH):
        try:
            df = pd.read_csv(LOG_PATH)
            hoje = datetime.now().strftime("%Y-%m-%d")
            hoje_count = len(df[df["Data_Hora"].str.startswith(hoje)]) if "Data_Hora" in df.columns else 0
            return len(df), hoje_count
        except: return 0, 0
    return 0, 0

# ==========================================================
# 4. CONTROLE DE ESTADO (Login e Galeria)
# ==========================================================
if "autenticado" not in st.session_state: st.session_state.autenticado = False
if "view_mode" not in st.session_state: st.session_state.view_mode = "grid" # Pode ser "grid" ou "carousel"
if "foto_idx" not in st.session_state: st.session_state.foto_idx = 0

# --- TELA DE LOGIN ---
if not st.session_state.autenticado:
    st.markdown('<div class="login-wrap"><div class="login-icon">🛡️</div><div class="login-title">SafeGuard IA</div><div style="color:#00dcc8; font-family: \'Share Tech Mono\', monospace; letter-spacing: 2px; font-size: 0.75rem;">⬡ ACESSO RESTRITO ⬡</div><br></div>', unsafe_allow_html=True)
    col_l, col_mid, col_r = st.columns([1, 1.6, 1])
    with col_mid:
        # O texto "SENHA DE ADMINISTRADOR" agora está mais sutil pelo CSS
        senha = st.text_input("credencial de segurança", type="password", label_visibility="visible")
        st.write("<br>", unsafe_allow_html=True)
        if st.button("🔓  AUTENTICAR", type="primary", use_container_width=True):
            if senha == "senai123":
                st.session_state.autenticado = True
                st.rerun()
            else: st.error("⛔  Credencial inválida — acesso negado.")
    st.stop()

# ==========================================================
# 5. CABEÇALHO PRINCIPAL E RELÓGIO NATIVO
# ==========================================================
st.markdown("""
<div class="sg-header">
    <div class="sg-header-icon">🛡️</div>
    <div>
        <div class="sg-header-title">SafeGuard IA</div>
        <div class="sg-header-sub">Painel de Controle Administrativo</div>
    </div>
    <div class="sg-header-status">
        <span style="display:inline-block; width:10px; height:10px; background:#00dcc8; border-radius:50%; box-shadow:0 0 8px #00dcc8; margin-right:6px;"></span>
        <span style="font-family:'Share Tech Mono', monospace; font-size:0.78rem; color:#00dcc8;">SISTEMA ATIVO</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Relógio Injetado via IFrame (Garante que o Javascript não será bloqueado pelo Streamlit)
components.html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
        body { margin: 0; overflow: hidden; background: transparent; color: #5f7b99; font-family: 'Share Tech Mono', monospace; font-size: 14px; text-align: right; }
        #clock { letter-spacing: 2px; }
    </style>
    <div id="clock">Carregando Horário...</div>
    <script>
        setInterval(() => {
            const now = new Date();
            document.getElementById('clock').innerHTML = now.toLocaleDateString('pt-BR') + ' &nbsp;|&nbsp; ' + now.toLocaleTimeString('pt-BR');
        }, 1000);
    </script>
""", height=25)

# ==========================================================
# 6. CARTÕES DE MÉTRICAS E LÓGICA PRINCIPAL
# ==========================================================
configs = carregar_config()
total_viol, hoje_viol = contar_violacoes()
num_fotos = len([f for f in os.listdir(PASTA_CAPTURES) if f.endswith((".jpg", ".png"))]) if os.path.exists(PASTA_CAPTURES) else 0

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card green"><div class="metric-label">Câmeras Ativas</div><div class="metric-value green">{len(configs)}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card {"red" if total_viol>0 else "green"}"><div class="metric-label">Violações Totais</div><div class="metric-value {"red" if total_viol>0 else "green"}">{total_viol}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card {"yellow" if hoje_viol>0 else "green"}"><div class="metric-label">Violações Hoje</div><div class="metric-value {"yellow" if hoje_viol>0 else "green"}">{hoje_viol}</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-card blue"><div class="metric-label">Evidências Salvas</div><div class="metric-value" style="color:#5352ed">{num_fotos}</div></div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# 7. ABAS PRINCIPAIS
# ==========================================================
aba_config, aba_relatorio = st.tabs(["⚙️   REGRAS DE EPIs", "📋   HISTÓRICO E EVIDÊNCIAS"])

# ── ABA 1: CONFIGURAÇÕES ──────────────────────────────────
with aba_config:
    if not configs: st.error("⚠️  Arquivo config.json não encontrado.")
    else:
        cam_selecionada = st.selectbox("Câmera", list(configs.keys()), label_visibility="collapsed")
        nomes_epis = {
            "require_helmet": ("⛑️", "Capacete de Segurança"), "require_glasses": ("🥽", "Óculos de Proteção"),
            "require_gloves": ("🧤", "Luvas de Proteção"), "require_boots": ("🥾", "Botas de Segurança"),
            "require_ear_protection":("🎧", "Protetor Auricular"), "require_mask": ("😷", "Máscara de Proteção"), "require_vest": ("🦺", "Colete de Sinalização")
        }
        novas_regras = {'source': configs[cam_selecionada].get('source', 0)}
        col_a, col_b = st.columns(2)
        itens = list(nomes_epis.keys())
        for idx, chave in enumerate(itens):
            icone, nome = nomes_epis[chave]
            with (col_a if idx < 4 else col_b):
                novas_regras[chave] = st.checkbox(f"{icone}  {nome}", value=configs[cam_selecionada].get(chave, False))
        
        st.write("<br>", unsafe_allow_html=True)
        if st.button("💾   SALVAR CONFIGURAÇÕES", type="primary"):
            configs[cam_selecionada] = novas_regras
            salvar_config(configs)
            st.success("✅  Regras atualizadas com sucesso!")

# ── ABA 2: EVIDÊNCIAS (Estilo Google Drive: Grade -> Carrossel)
with aba_relatorio:
    st.markdown('<div class="sg-section-title">Registro Fotográfico</div>', unsafe_allow_html=True)

    if os.path.exists(PASTA_CAPTURES) and num_fotos > 0:
        # Pega as fotos e inverte (as mais novas primeiro)
        fotos_invertidas = sorted([f for f in os.listdir(PASTA_CAPTURES) if f.endswith((".jpg", ".png"))])[::-1]
        
        # MODO 1: CARROSSEL EXPANDIDO
        if st.session_state.view_mode == "carousel":
            if st.button("🔙 Voltar para a Grade", type="primary"):
                st.session_state.view_mode = "grid"
                st.rerun()
                
            st.write("---")
            max_idx = len(fotos_invertidas) - 1
            col_nav1, col_img, col_nav2 = st.columns([1, 4, 1])
            
            with col_nav1:
                st.write("<br>"*8, unsafe_allow_html=True)
                if st.button("⬅️ Anterior", disabled=(st.session_state.foto_idx == 0)):
                    st.session_state.foto_idx -= 1
                    st.rerun()
                    
            with col_img:
                foto_atual = fotos_invertidas[st.session_state.foto_idx]
                st.image(os.path.join(PASTA_CAPTURES, foto_atual), use_container_width=True)
                st.markdown(f"<div style='text-align:center; color:#00dcc8; font-family:monospace; margin-top:10px;'>Foto {st.session_state.foto_idx + 1} de {len(fotos_invertidas)}: {foto_atual}</div>", unsafe_allow_html=True)
                
            with col_nav2:
                st.write("<br>"*8, unsafe_allow_html=True)
                if st.button("Próxima ➡️", disabled=(st.session_state.foto_idx == max_idx)):
                    st.session_state.foto_idx += 1
                    st.rerun()
                    
        # MODO 2: GRADE (O Padrão)
        else:
            cols = st.columns(4)
            for i, foto in enumerate(fotos_invertidas):
                with cols[i % 4]:
                    # Exibe a miniatura
                    st.image(os.path.join(PASTA_CAPTURES, foto), use_container_width=True)
                    # Botão para expandir esta foto específica
                    if st.button(f"🔍 Expandir", key=f"btn_{i}", use_container_width=True):
                        st.session_state.foto_idx = i
                        st.session_state.view_mode = "carousel"
                        st.rerun()
    else:
        st.info("📂  Nenhuma evidência capturada no momento.")
        
    st.write("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sg-section-title">Log de Banco de Dados</div>', unsafe_allow_html=True)
    if os.path.exists(LOG_PATH):
        try: st.dataframe(pd.read_csv(LOG_PATH).sort_values(by="Data_Hora", ascending=False), use_container_width=True, height=200)
        except: st.info("📭  Banco de dados vazio.")