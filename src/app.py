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
# 2. CSS GLOBAL — REDESIGN PROFISSIONAL
# ==========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

:root {
    --bg-base:       #07090f;
    --bg-surface:    #0c1018;
    --bg-elevated:   #111722;
    --bg-hover:      #161e2e;
    --border:        #1c2a3e;
    --border-light:  #243346;
    --accent:        #00e5c8;
    --accent-dim:    rgba(0,229,200,.12);
    --accent-glow:   rgba(0,229,200,.25);
    --danger:        #ff3e5e;
    --danger-dim:    rgba(255,62,94,.12);
    --warn:          #f0b429;
    --warn-dim:      rgba(240,180,41,.10);
    --info:          #4f8ef7;
    --info-dim:      rgba(79,142,247,.12);
    --text-primary:  #e8edf5;
    --text-secondary:#7a93b2;
    --text-muted:    #3e5470;
    --mono:          'IBM Plex Mono', monospace;
    --sans:          'IBM Plex Sans', sans-serif;
    --radius:        6px;
    --radius-lg:     10px;
}

html, body, [class*="css"] {
    font-family: var(--sans);
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
}

.stApp {
    background-color: var(--bg-base);
}

/* Subtle dot-grid background */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: radial-gradient(circle, rgba(0,229,200,.06) 1px, transparent 1px);
    background-size: 28px 28px;
    pointer-events: none;
    z-index: 0;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2.5rem 3.5rem 4rem 3.5rem !important;
    max-width: 1400px;
}

div[data-testid="InputInstructions"] { display: none !important; }

/* ── SCROLLBAR ─────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-surface); }
::-webkit-scrollbar-thumb { background: var(--border-light); border-radius: 3px; }

/* ── HEADER ─────────────────────────────────────────────── */
.sg-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.6rem 2.2rem;
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-top: 2px solid var(--accent);
    border-radius: var(--radius-lg);
    margin-bottom: 2.4rem;
    position: relative;
    overflow: hidden;
}
.sg-header::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 60px;
    background: linear-gradient(180deg, var(--accent-dim) 0%, transparent 100%);
    pointer-events: none;
}
.sg-logo-block { display: flex; align-items: center; gap: 14px; }
.sg-logo-icon {
    width: 46px; height: 46px;
    background: var(--accent-dim);
    border: 1px solid var(--accent);
    border-radius: var(--radius);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
}
.sg-title { font-size: 1.5rem; font-weight: 700; color: var(--text-primary); letter-spacing: 1.5px; text-transform: uppercase; }
.sg-sub { font-family: var(--mono); font-size: .65rem; color: var(--accent); letter-spacing: 3px; text-transform: uppercase; margin-top: 2px; }
.sg-status {
    display: flex; align-items: center; gap: 8px;
    font-family: var(--mono); font-size: .68rem; color: var(--text-secondary);
    letter-spacing: 1px;
}
.sg-status-dot {
    width: 7px; height: 7px;
    background: var(--accent); border-radius: 50%;
    box-shadow: 0 0 8px var(--accent);
    animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: .3; }
}

/* ── METRIC CARDS ───────────────────────────────────────── */
.metric-card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color .2s, transform .2s;
}
.metric-card:hover { transform: translateY(-2px); }
.metric-card.green  { border-top: 2px solid var(--accent);  }
.metric-card.red    { border-top: 2px solid var(--danger);  }
.metric-card.yellow { border-top: 2px solid var(--warn);    }
.metric-card.blue   { border-top: 2px solid var(--info);    }
.metric-card.green::after  { content:''; position:absolute; top:0; right:0; width:80px; height:80px; background: radial-gradient(circle at top right, var(--accent-dim), transparent 70%); }
.metric-card.red::after    { content:''; position:absolute; top:0; right:0; width:80px; height:80px; background: radial-gradient(circle at top right, var(--danger-dim), transparent 70%); }
.metric-card.yellow::after { content:''; position:absolute; top:0; right:0; width:80px; height:80px; background: radial-gradient(circle at top right, var(--warn-dim), transparent 70%); }
.metric-card.blue::after   { content:''; position:absolute; top:0; right:0; width:80px; height:80px; background: radial-gradient(circle at top right, var(--info-dim), transparent 70%); }
.metric-label { font-family: var(--mono); font-size: .62rem; letter-spacing: 2.5px; text-transform: uppercase; color: var(--text-muted); margin-bottom: .6rem; }
.metric-value { font-size: 2.4rem; font-weight: 700; color: var(--text-primary); line-height: 1; }
.metric-card.green  .metric-value { color: var(--accent); }
.metric-card.red    .metric-value { color: var(--danger); }
.metric-card.yellow .metric-value { color: var(--warn); }
.metric-card.blue   .metric-value { color: var(--info); }

/* ── TABS ───────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    font-family: var(--mono) !important;
    font-size: .72rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    padding: .6rem 1.4rem !important;
    border-radius: calc(var(--radius) - 1px) !important;
    border: none !important;
    transition: all .2s !important;
}
.stTabs [aria-selected="true"] {
    background: var(--bg-elevated) !important;
    color: var(--accent) !important;
    border: 1px solid var(--border-light) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.8rem !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"]    { display: none !important; }

/* ── FORM ELEMENTS ──────────────────────────────────────── */
.stSelectbox > div > div,
.stTextInput input {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border-light) !important;
    border-radius: var(--radius) !important;
    color: var(--text-primary) !important;
    font-family: var(--sans) !important;
}
.stSelectbox > div > div:focus-within,
.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--accent-dim) !important;
}
.stSelectbox label, .stTextInput label {
    font-family: var(--mono) !important;
    font-size: .65rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}

/* ── CHECKBOX ───────────────────────────────────────────── */
.stCheckbox { padding: .4rem 0 !important; }
.stCheckbox label {
    color: var(--text-secondary) !important;
    font-size: .9rem !important;
    gap: 10px !important;
    text-decoration: none !important;
    border-bottom: none !important;
}
.stCheckbox label span,
.stCheckbox label:hover span,
.stCheckbox label:focus span,
.stCheckbox label:focus-within span,
.stCheckbox label p {
    text-decoration: none !important;
    border-bottom: none !important;
    outline: none !important;
    margin: 0 !important;
}
/* caixa do checkbox */
.stCheckbox [data-baseweb="checkbox"] {
    border-color: var(--border-light) !important;
    background: var(--bg-elevated) !important;
    border-radius: 3px !important;
}
/* checked: caixa verde-teal */
.stCheckbox input:checked ~ div [data-baseweb="checkbox"],
.stCheckbox input:checked + div {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
}
/* checked: texto fica levemente mais claro, sem sublinhado */
.stCheckbox input:checked ~ div,
.stCheckbox input:checked ~ div span,
.stCheckbox input:checked ~ div p {
    color: var(--text-primary) !important;
    text-decoration: none !important;
}

/* ── BUTTONS ────────────────────────────────────────────── */
.stButton > button {
    background: var(--bg-elevated) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-light) !important;
    border-radius: var(--radius) !important;
    font-family: var(--mono) !important;
    font-size: .72rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    padding: .55rem 1.4rem !important;
    transition: all .2s !important;
}
.stButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background: var(--accent-dim) !important;
}
.stButton > button[kind="primary"] {
    background: var(--accent) !important;
    color: #07090f !important;
    border-color: var(--accent) !important;
    font-weight: 600 !important;
}
.stButton > button[kind="primary"]:hover {
    background: #00ffdf !important;
    box-shadow: 0 0 16px var(--accent-glow) !important;
    color: #07090f !important;
}

/* ── DATAFRAME ──────────────────────────────────────────── */
.stDataFrame {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    overflow: hidden !important;
}
.stDataFrame [data-testid="stDataFrameResizable"] {
    background: var(--bg-surface) !important;
}

/* ── SECTION HEADERS ────────────────────────────────────── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 2rem 0 1.2rem 0;
    padding-bottom: .8rem;
    border-bottom: 1px solid var(--border);
}
.section-header-label {
    font-family: var(--mono);
    font-size: .68rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--text-muted);
}
.section-header-line { flex: 1; height: 1px; background: var(--border); }

/* ── CONFIG SECTION ─────────────────────────────────────── */
.cam-title-block {
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: var(--radius);
    padding: .9rem 1.2rem;
    margin: 1.2rem 0 1.4rem 0;
    font-family: var(--mono);
    font-size: .78rem;
    color: var(--text-secondary);
    letter-spacing: 1px;
}
.cam-title-block span { color: var(--accent); font-weight: 600; }

.epi-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: .5rem;
    margin-bottom: 1.5rem;
}
.epi-item {
    display: flex; align-items: center; gap: 10px;
    padding: .75rem 1rem;
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    transition: border-color .2s;
}
.epi-item:hover { border-color: var(--border-light); }
.epi-item.active { border-color: var(--accent); background: var(--accent-dim); }

/* ── LOGIN ───────────────────────────────────────────────── */
.login-outer {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 60vh;
}
.login-wrap {
    width: 100%;
    max-width: 400px;
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-top: 2px solid var(--accent);
    border-radius: var(--radius-lg);
    padding: 3rem 2.5rem;
    text-align: center;
}
.login-badge {
    width: 60px; height: 60px;
    background: var(--accent-dim);
    border: 1px solid var(--accent);
    border-radius: var(--radius-lg);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.8rem;
    margin: 0 auto 1.4rem auto;
}
.login-title { font-size: 1.4rem; font-weight: 700; color: var(--text-primary); letter-spacing: 2px; text-transform: uppercase; }
.login-sub { font-family: var(--mono); font-size: .62rem; color: var(--accent); letter-spacing: 3px; margin-top: .3rem; }
.login-divider { height: 1px; background: var(--border); margin: 1.8rem 0; }
.stTextInput input {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border-light) !important;
    color: var(--text-primary) !important;
    text-align: center !important;
    letter-spacing: 6px !important;
    font-family: var(--mono) !important;
    font-size: 1rem !important;
}

/* ── GALLERY ────────────────────────────────────────────── */
.gallery-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.4rem;
}
.gallery-count {
    font-family: var(--mono);
    font-size: .65rem;
    color: var(--text-muted);
    letter-spacing: 2px;
    text-transform: uppercase;
}
.gallery-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-bottom: 1.5rem;
}
.gallery-thumb {
    position: relative;
    aspect-ratio: 16/9;
    overflow: hidden;
    border-radius: var(--radius);
    border: 1px solid var(--border);
    cursor: pointer;
    background: var(--bg-elevated);
    transition: all .2s;
}
.gallery-thumb:hover {
    border-color: var(--accent);
    box-shadow: 0 0 0 1px var(--accent), 0 4px 20px rgba(0,229,200,.15);
    transform: scale(1.02);
}
.gallery-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
.gallery-thumb-overlay {
    position: absolute; inset: 0;
    background: rgba(0,0,0,.5);
    display: flex; align-items: center; justify-content: center;
    opacity: 0; transition: opacity .2s;
    color: white; font-size: .75rem;
    font-family: var(--mono);
    letter-spacing: 1px;
}
.gallery-thumb:hover .gallery-thumb-overlay { opacity: 1; }

/* Modal lightbox */
.lightbox-overlay {
    position: fixed; inset: 0; z-index: 9999;
    background: rgba(7,9,15,.95);
    display: flex; align-items: center; justify-content: center;
    backdrop-filter: blur(8px);
}
.lightbox-inner {
    position: relative;
    max-width: 90vw; max-height: 90vh;
    display: flex; flex-direction: column; align-items: center;
    gap: 16px;
}
.lightbox-img {
    max-width: 85vw; max-height: 75vh;
    border-radius: var(--radius-lg);
    border: 1px solid var(--border-light);
    box-shadow: 0 24px 80px rgba(0,0,0,.6);
    object-fit: contain;
}
.lightbox-nav {
    display: flex; align-items: center; gap: 16px;
}
.lightbox-btn {
    width: 44px; height: 44px;
    background: var(--bg-elevated);
    border: 1px solid var(--border-light);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer; font-size: 1.1rem;
    color: var(--text-primary);
    transition: all .15s;
}
.lightbox-btn:hover { border-color: var(--accent); color: var(--accent); background: var(--accent-dim); }
.lightbox-counter {
    font-family: var(--mono); font-size: .7rem;
    color: var(--text-muted); letter-spacing: 2px;
    min-width: 80px; text-align: center;
}
.lightbox-close {
    position: absolute; top: -16px; right: -16px;
    width: 36px; height: 36px;
    background: var(--bg-elevated);
    border: 1px solid var(--border-light);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer; font-size: .85rem;
    color: var(--text-secondary);
    transition: all .15s;
}
.lightbox-close:hover { border-color: var(--danger); color: var(--danger); }
.lightbox-filename {
    font-family: var(--mono); font-size: .65rem;
    color: var(--text-muted); letter-spacing: 1px;
    background: var(--bg-elevated);
    padding: .35rem .8rem;
    border-radius: 20px;
    border: 1px solid var(--border);
}

/* Log table */
.log-header {
    display: flex; align-items: center; gap: 10px;
    padding: .9rem 1.2rem;
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: var(--radius) var(--radius) 0 0;
    font-family: var(--mono); font-size: .65rem;
    letter-spacing: 2px; text-transform: uppercase;
    color: var(--text-muted);
}

/* Alerts / info */
.stAlert {
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
    background: var(--bg-elevated) !important;
}
.stSuccess { border-color: var(--accent) !important; }
.stWarning { border-color: var(--warn) !important; }

/* Dividers */
hr { border-color: var(--border) !important; }

/* ── MOBILE RESPONSIVO (≤ 768px) ───────────────────────── */
@media (max-width: 768px) {

    /* Padding geral menor */
    .block-container {
        padding: 1rem 1rem 2.5rem 1rem !important;
    }

    /* Header: empilha verticalmente */
    .sg-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
        padding: 1.1rem 1.2rem;
    }
    .sg-status {
        font-size: .6rem;
        letter-spacing: .5px;
    }
    .sg-title { font-size: 1.1rem; }

    /* Cards de métrica: 2 por linha */
    [data-testid="column"] {
        min-width: 0 !important;
    }
    .metric-card {
        padding: .9rem 1rem;
    }
    .metric-value { font-size: 1.7rem; }
    .metric-label { font-size: .55rem; letter-spacing: 1.5px; }

    /* Tabs: texto menor para caber */
    .stTabs [data-baseweb="tab"] {
        font-size: .6rem !important;
        letter-spacing: .8px !important;
        padding: .5rem .7rem !important;
    }

    /* Galeria: 2 colunas no mobile em vez de 4 */
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(n+3) {
        display: block !important;
    }

    /* Carrossel: botões de nav maiores (área de toque) */
    .stButton > button {
        min-height: 44px !important;
        font-size: .65rem !important;
    }

    /* Bloco de câmera selecionada */
    .cam-title-block {
        font-size: .68rem;
        padding: .7rem .9rem;
    }

    /* Selectbox e inputs ocupam largura total */
    .stSelectbox, .stTextInput {
        width: 100% !important;
    }

    /* Login: ajuste de largura */
    .stTextInput input {
        font-size: .85rem !important;
        letter-spacing: 4px !important;
    }

    /* Dataframe: permite scroll horizontal */
    .stDataFrame {
        overflow-x: auto !important;
    }

    /* Section headers: menos margem */
    .section-header {
        margin: 1.2rem 0 .8rem 0 !important;
    }
}

/* ── MOBILE PEQUENO (≤ 480px) ───────────────────────────── */
@media (max-width: 480px) {
    .sg-title  { font-size: .95rem; letter-spacing: 1px; }
    .sg-sub    { font-size: .55rem; letter-spacing: 2px; }
    .metric-value { font-size: 1.45rem; }

    /* Tabs: cabe em uma linha sem overflow */
    .stTabs [data-baseweb="tab"] {
        font-size: .55rem !important;
        padding: .45rem .5rem !important;
        letter-spacing: .5px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# 3. FUNÇÕES DE APOIO
# ==========================================================
def carregar_full_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return {"cameras": {}}

def salvar_full_config(dados):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        json.dump(dados, f, indent=4)

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
# 4. AUTENTICAÇÃO
# ==========================================================
if "autenticado" not in st.session_state: st.session_state.autenticado = False
if "view_mode" not in st.session_state: st.session_state.view_mode = "grid"
if "foto_idx" not in st.session_state: st.session_state.foto_idx = 0

if not st.session_state.autenticado:
    st.markdown("""
    <div style="display:flex;align-items:center;justify-content:center;min-height:55vh;">
        <div style="text-align:center;">
            <div style="width:64px;height:64px;background:rgba(0,229,200,.1);border:1px solid #00e5c8;border-radius:10px;
                        display:flex;align-items:center;justify-content:center;font-size:1.9rem;margin:0 auto 1.2rem auto;">
                🛡️
            </div>
            <div style="font-size:1.4rem;font-weight:700;color:#e8edf5;letter-spacing:2px;text-transform:uppercase;">
                SafeGuard IA
            </div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:.6rem;color:#00e5c8;
                        letter-spacing:4px;text-transform:uppercase;margin-top:4px;">
                ◆ ACESSO RESTRITO ◆
            </div>
            <div style="height:1px;background:#1c2a3e;margin:1.8rem auto;width:320px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_mid, col_r = st.columns([1, 1.2, 1])
    with col_mid:
        senha = st.text_input("credencial de acesso", type="password", placeholder="••••••••")
        if st.button("→   AUTENTICAR", type="primary", use_container_width=True):
            if senha == "senai123":
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("⛔   Credencial inválida — acesso negado")
    st.stop()

# ==========================================================
# 5. DASHBOARD PRINCIPAL
# ==========================================================
now_str = datetime.now().strftime("%d/%m/%Y  %H:%M")

st.markdown(f"""
<div class="sg-header">
    <div class="sg-logo-block">
        <div class="sg-logo-icon">🛡️</div>
        <div>
            <div class="sg-title">SafeGuard IA</div>
            <div class="sg-sub">Painel de Controle Administrativo</div>
        </div>
    </div>
    <div class="sg-status">
        <div class="sg-status-dot"></div>
        SISTEMA ATIVO &nbsp;|&nbsp; {now_str}
    </div>
</div>
""", unsafe_allow_html=True)

# ── Métricas ──────────────────────────────────────────────
full_data = carregar_full_config()
cameras_dict = full_data.get("cameras", {})
total_viol, hoje_viol = contar_violacoes()
num_fotos = len([f for f in os.listdir(PASTA_CAPTURES) if f.endswith((".jpg", ".png"))]) if os.path.exists(PASTA_CAPTURES) else 0

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-card green"><div class="metric-label">Câmeras Ativas</div><div class="metric-value">{len(cameras_dict)}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card red"><div class="metric-label">Total Violações</div><div class="metric-value">{total_viol}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card yellow"><div class="metric-label">Violações Hoje</div><div class="metric-value">{hoje_viol}</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-card blue"><div class="metric-label">Evidências</div><div class="metric-value">{num_fotos}</div></div>', unsafe_allow_html=True)

st.markdown("<div style='height:1.8rem'></div>", unsafe_allow_html=True)

# ==========================================================
# 6. ABAS
# ==========================================================
aba_config, aba_relatorio = st.tabs(["⚙️   REGRAS POR CÂMERA", "📋   EVIDÊNCIAS"])

# ── ABA CONFIGURAÇÕES ─────────────────────────────────────
with aba_config:
    if not cameras_dict:
        st.warning("Nenhuma câmera encontrada no config.json")
    else:
        st.markdown('<div class="section-header"><div class="section-header-label">Selecionar câmera</div><div class="section-header-line"></div></div>', unsafe_allow_html=True)

        id_selecionada = st.selectbox(
            "Câmera",
            options=list(cameras_dict.keys()),
            format_func=lambda x: cameras_dict[x]["nome"],
            label_visibility="collapsed"
        )

        cam_config = cameras_dict[id_selecionada]

        st.markdown(f"""
        <div class="cam-title-block">
            CONFIGURANDO &nbsp;→&nbsp; <span>{cam_config['nome']}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header"><div class="section-header-label">EPIs Obrigatórios</div><div class="section-header-line"></div></div>', unsafe_allow_html=True)

        nomes_epis = {
            "require_helmet":        ("⛑️", "Capacete de Segurança"),
            "require_glasses":       ("🥽", "Óculos de Proteção"),
            "require_gloves":        ("🧤", "Luvas de Proteção"),
            "require_boots":         ("🥾", "Botas de Segurança"),
            "require_ear_protection":("🎧", "Protetor Auricular"),
            "require_mask":          ("😷", "Máscara de Proteção"),
            "require_vest":          ("🦺", "Colete de Sinalização"),
        }

        col_a, col_b = st.columns(2)
        novos_valores = cam_config.copy()

        for idx, (chave, (icone, nome)) in enumerate(nomes_epis.items()):
            with (col_a if idx < 4 else col_b):
                novos_valores[chave] = st.checkbox(
                    f"{icone}  {nome}",
                    value=cam_config.get(chave, False),
                    key=f"chk_{id_selecionada}_{chave}"
                )

        st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)

        col_btn, _ = st.columns([1, 3])
        with col_btn:
            if st.button("💾   SALVAR ALTERAÇÕES", type="primary", use_container_width=True):
                full_data["cameras"][id_selecionada] = novos_valores
                salvar_full_config(full_data)
                st.success(f"✅  Configurações da **{cam_config['nome']}** salvas com sucesso.")

# ── ABA EVIDÊNCIAS ────────────────────────────────────────
with aba_relatorio:

    # ── Gallery section ──────────────────────────────────
    st.markdown('<div class="section-header"><div class="section-header-label">Galeria de Evidências</div><div class="section-header-line"></div></div>', unsafe_allow_html=True)

    IMG_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp", ".gif")
    fotos = []
    if os.path.exists(PASTA_CAPTURES):
        fotos = sorted(
            [f for f in os.listdir(PASTA_CAPTURES) if f.lower().endswith(IMG_EXTS)],
            reverse=True  # mais recentes primeiro
        )

    if len(fotos) > 0:

        # ── LIGHTBOX (carousel) ───────────────────────────
        if st.session_state.view_mode == "carousel":
            idx = st.session_state.foto_idx
            foto_atual = fotos[idx]
            foto_path  = os.path.join(PASTA_CAPTURES, foto_atual)

            # Top bar
            col_back, col_spacer = st.columns([1, 5])
            with col_back:
                if st.button("← Voltar à grade"):
                    st.session_state.view_mode = "grid"
                    st.rerun()

            st.markdown(f"""
            <div style="text-align:center;margin:.5rem 0 .3rem 0;">
                <span style="font-family:var(--mono,monospace);font-size:.62rem;color:#3e5470;
                             letter-spacing:2px;text-transform:uppercase;">
                    {idx + 1} / {len(fotos)}
                </span>
            </div>
            """, unsafe_allow_html=True)

            # Image
            st.image(foto_path, use_container_width=True)

            # Filename
            st.markdown(f"""
            <div style="text-align:center;margin:.6rem 0;">
                <span style="font-family:var(--mono,monospace);font-size:.65rem;color:#7a93b2;
                             background:#111722;padding:.3rem .9rem;border-radius:20px;
                             border:1px solid #1c2a3e;letter-spacing:1px;">
                    {foto_atual}
                </span>
            </div>
            """, unsafe_allow_html=True)

            # Nav buttons
            c_prev, c_counter, c_next = st.columns([1, 2, 1])
            with c_prev:
                if st.button("← Anterior", use_container_width=True, disabled=(idx == 0)):
                    st.session_state.foto_idx -= 1
                    st.rerun()
            with c_counter:
                st.markdown(f"""
                <div style="text-align:center;padding:.55rem 0;
                            font-family:var(--mono,monospace);font-size:.68rem;
                            color:#7a93b2;letter-spacing:2px;">
                    {idx + 1} de {len(fotos)}
                </div>
                """, unsafe_allow_html=True)
            with c_next:
                if st.button("Próxima →", use_container_width=True, disabled=(idx >= len(fotos) - 1)):
                    st.session_state.foto_idx += 1
                    st.rerun()

        # ── GRID ─────────────────────────────────────────
        else:
            st.markdown(f"""
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;">
                <span style="font-family:var(--mono,monospace);font-size:.62rem;color:#3e5470;
                             letter-spacing:2px;text-transform:uppercase;">
                    {len(fotos)} evidência(s) encontrada(s) — mais recentes primeiro
                </span>
            </div>
            """, unsafe_allow_html=True)

            cols_per_row = 4
            for row_start in range(0, len(fotos), cols_per_row):
                cols = st.columns(cols_per_row)
                for col_idx, foto in enumerate(fotos[row_start:row_start + cols_per_row]):
                    with cols[col_idx]:
                        foto_path = os.path.join(PASTA_CAPTURES, foto)
                        st.image(foto_path, use_container_width=True)

                        btn_label = foto[:18] + "…" if len(foto) > 20 else foto
                        if st.button(
                            f"🔍 Ampliar",
                            key=f"open_{row_start + col_idx}",
                            use_container_width=True
                        ):
                            st.session_state.foto_idx = row_start + col_idx
                            st.session_state.view_mode = "carousel"
                            st.rerun()

    else:
        st.markdown("""
        <div style="text-align:center;padding:3.5rem 2rem;
                    background:#0c1018;border:1px solid #1c2a3e;
                    border-radius:10px;">
            <div style="font-size:2rem;margin-bottom:.8rem;">📂</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:.7rem;
                        color:#3e5470;letter-spacing:2px;text-transform:uppercase;">
                Nenhuma evidência capturada
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Log table ─────────────────────────────────────────
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header"><div class="section-header-label">Log de Eventos</div><div class="section-header-line"></div></div>', unsafe_allow_html=True)

    if os.path.exists(LOG_PATH):
        df = pd.read_csv(LOG_PATH).sort_values(by="Data_Hora", ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.markdown("""
        <div style="font-family:'IBM Plex Mono',monospace;font-size:.65rem;
                    color:#3e5470;letter-spacing:2px;text-align:center;padding:1.5rem 0;">
            NENHUM REGISTRO ENCONTRADO
        </div>
        """, unsafe_allow_html=True)