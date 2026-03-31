import subprocess
import time
import sys
import os

def iniciar_sistema():
    print("🛡️ Iniciando SafeGuard IA Ecosystem...")

    # 1. PEGAR O CAMINHO ONDE O SCRIPT ESTÁ
    CAMINHO_ATUAL = os.path.dirname(os.path.abspath(__file__))

    # 2. LOCALIZAR A RAIZ REAL (SafeGuardIA)
    # Se existe uma pasta 'src' aqui dentro, este é o ROOT.
    if os.path.exists(os.path.join(CAMINHO_ATUAL, "src")):
        ROOT_DIR = CAMINHO_ATUAL
    # Se não existe, mas o script está DENTRO de 'src', o ROOT é o pai.
    elif os.path.basename(CAMINHO_ATUAL) == "src":
        ROOT_DIR = os.path.dirname(CAMINHO_ATUAL)
    else:
        # Fallback caso você rode de um lugar totalmente aleatório
        ROOT_DIR = CAMINHO_ATUAL 

    # 3. DEFINIR CAMINHOS ABSOLUTOS
    APP_PATH = os.path.join(ROOT_DIR, "src", "app.py")
    IA_PATH = os.path.join(ROOT_DIR, "src", "automacaototal.py")

    print(f"📂 Raiz Detectada: {ROOT_DIR}")
    print(f"🌐 App: {APP_PATH}")
    print(f"👁️ IA:  {IA_PATH}")

    # Validação Física
    if not os.path.exists(APP_PATH) or not os.path.exists(IA_PATH):
        print("❌ ERRO: Arquivos não encontrados! Verifique se a pasta 'src' está correta.")
        return

    # 4. DISPARAR PROCESSOS
    print("🌐 Abrindo Painel de Controle...")
    # 'cwd=ROOT_DIR' garante que o Streamlit saiba onde procurar o /config
    p_web = subprocess.Popen(["streamlit", "run", APP_PATH], shell=True, cwd=ROOT_DIR)

    time.sleep(6)

    print("👁️ Abrindo Engine de Visão e Túnel Ngrok...")
    try:
        # Rodamos a IA também a partir da raiz
        p_ia = subprocess.Popen([sys.executable, IA_PATH], cwd=ROOT_DIR)
        p_ia.wait()
    except KeyboardInterrupt:
        print("\n🛑 Encerrando sistema...")
        p_web.terminate()
        p_ia.terminate()

if __name__ == "__main__":
    iniciar_sistema()   