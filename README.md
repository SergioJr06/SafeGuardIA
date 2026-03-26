🛡️ SafeGuard IA - Monitoramento Inteligente de EPIs

O SafeGuard IA é uma solução de Visão Computacional de ponta, desenvolvida para as exigências da Indústria 4.0. Utilizando a arquitetura YOLOv8, o sistema automatiza a fiscalização de Equipamentos de Proteção Individual (EPIs), garantindo segurança em tempo real com uma gestão flexível e remota.
🚀 Funcionalidades Principais

    🔍 Detecção Multiobjeto: Identificação em tempo real de Capacete, Óculos, Luvas, Botas e Protetor Auricular.

    ⚙️ Gestão Dinâmica: Painel administrativo para ativar/desativar regras de segurança por câmera ou setor via web.

    🌐 Acesso IoT: Dashboard acessível via 4G/5G através de tunelamento seguro com ngrok.

    📊 Processamento de Dados: Script automatizado para padronização e redimensionamento de imagens de treinamento.

📂 Estrutura do Repositório
Pasta/Arquivo	Descrição
src/	Scripts de execução (Dashboard, Utilitários e Visão).
config/	Arquivos JSON de configuração das regras por câmera.
models/	Pesos treinados da Inteligência Artificial (best.pt).
dataset/	Banco de imagens (Pastas raw e processed).
docs/	Documentação técnica, manuais e rascunhos.
requirements.txt	Lista de dependências para instalação rápida.
🛠️ Guia do Desenvolvedor
1. Preparação do Ambiente

Ao baixar o projeto, recrie o ambiente virtual para garantir o isolamento das bibliotecas:
Bash

# Clone o repositório
git clone https://github.com/SergioJr06/SafeGuardIA.git

# Entre na pasta
cd SafeGuardIA

# Crie e ative o ambiente virtual
python -m venv venv
.\venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

2. Fluxo de Trabalho

    Configuração: Rode streamlit run src/app.py para definir os EPIs obrigatórios.

    Dados: Coloque fotos brutas em dataset/raw e rode python src/utils.py.

    Monitoramento: Para validar as detecções, rode python src/vision_engine.py.

📖 Manual do Usuário (Para Jurados e Gestores)

O SafeGuard IA foi projetado para ser operado na palma da mão. Siga estes passos:

    Acesso Remoto: Escaneie o QR Code ou acesse o link gerado pelo túnel ngrok no seu celular.

    Configuração: No painel exibido, escolha a câmera e marque quais EPIs devem ser fiscalizados. Clique em Salvar.

    Verificação: Observe o monitor principal. A IA aplicará instantaneamente as regras, acusando infrações apenas para os itens selecionados.

📱 Gerando o QR Code de Acesso

Para facilitar o acesso durante a apresentação:

    Inicie o ngrok: ./ngrok http 8501.

    Copie a URL gerada e rode o comando:

Bash

python src/utils/generate_qr.py https://link-gerado.ngrok-free.app

    Abra o arquivo dashboard_qr.png na raiz do projeto para o escaneamento.

    [!TIP]
    Dica para a Banca: Este projeto demonstra a integração entre Visão Computacional, Redes (Tunneling) e Desenvolvimento Web para resolver problemas reais de Segurança do Trabalho.
