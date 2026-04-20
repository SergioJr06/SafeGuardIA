import subprocess
import time
import sys
import os

# ==========================================================
# SafeGuard IA — Launcher
# Inicia o painel Streamlit e o engine de visão em sequência.
# ==========================================================

def iniciar_sistema():
    print("SafeGuard IA — Iniciando ecosystem...")

    # Detecta a raiz do projeto (pasta que contém /src)
    CAMINHO_ATUAL = os.path.dirname(os.path.abspath(__file__))

    if os.path.exists(os.path.join(CAMINHO_ATUAL, "src")):
        ROOT_DIR = CAMINHO_ATUAL
    elif os.path.basename(CAMINHO_ATUAL) == "src":
        ROOT_DIR = os.path.dirname(CAMINHO_ATUAL)
    else:
        ROOT_DIR = CAMINHO_ATUAL

    APP_PATH = os.path.join(ROOT_DIR, "src", "app.py")
    IA_PATH  = os.path.join(ROOT_DIR, "src", "automacaototal.py")

    print(f"  Raiz do projeto : {ROOT_DIR}")
    print(f"  Painel (app)    : {APP_PATH}")
    print(f"  Engine de visao : {IA_PATH}")

    # Valida arquivos antes de disparar processos
    erros = []
    if not os.path.exists(APP_PATH):
        erros.append(f"  [ERRO] Painel nao encontrado: {APP_PATH}")
    if not os.path.exists(IA_PATH):
        erros.append(f"  [ERRO] Engine nao encontrado: {IA_PATH}")

    if erros:
        for e in erros:
            print(e)
        print("Verifique se a pasta 'src' esta no lugar correto e tente novamente.")
        return

    # Inicia o painel Streamlit
    print("\n[1/2] Iniciando painel de controle (Streamlit)...")
    p_web = subprocess.Popen(
        ["streamlit", "run", APP_PATH],
        shell=(sys.platform == "win32"),
        cwd=ROOT_DIR
    )

    # Aguarda o Streamlit subir antes de abrir a engine
    print("      Aguardando Streamlit inicializar (6s)...")
    time.sleep(6)

    # Inicia o engine de visao + ngrok
    print("[2/2] Iniciando engine de visao e tunel ngrok...")
    p_ia = None
    try:
        p_ia = subprocess.Popen(
            [sys.executable, IA_PATH],
            cwd=ROOT_DIR
        )
        p_ia.wait()

    except KeyboardInterrupt:
        print("\nEncerrando sistema (Ctrl+C recebido)...")

    finally:
        if p_ia is not None and p_ia.poll() is None:
            p_ia.terminate()
        if p_web.poll() is None:
            p_web.terminate()
        print("Sistema encerrado.")


if __name__ == "__main__":
    iniciar_sistema()