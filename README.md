🛡️ SafeGuard IA - Monitoramento Inteligente de EPIs

O SafeGuard IA é uma solução de Visão Computacional de ponta, desenvolvida para a Indústria 4.0. Utilizando a arquitetura YOLOv8, o sistema automatiza a fiscalização de Equipamentos de Proteção Individual (EPIs), permitindo uma gestão flexível e remota através de um painel de controle dinâmico.
🚀 Funcionalidades

    Detecção Multiobjeto: Identificação em tempo real de: Capacete, Óculos, Luvas, Botas e Protetor Auricular.

    Gestão Dinâmica: Ative ou desative as regras de segurança por setor/câmera via interface web.

    Acesso IoT: Dashboard acessível via 4G/5G através de tunelamento seguro (ngrok).

    Processamento de Dados: Script automatizado para padronização de imagens de treinamento.

📂 Estrutura do Repositório

    src/: Scripts de execução (Dashboard, Utilidades e Visão).

    config/: Arquivos de configuração JSON das câmeras.

    models/: Pesos da Inteligência Artificial (best.pt).

    dataset/: Fotos de treinamento (Pastas raw e processed).

    docs/: Documentação técnica e manuais.

🛠️ Guia do Desenvolvedor (Instalação e Uso)
1. Preparação do Ambiente

Ao baixar o projeto (seja via Pendrive ou git clone), recrie o ambiente virtual para garantir o funcionamento das bibliotecas:
Bash

# Clone o repositório
git clone https://github.com/SEU_USUARIO/SafeGuardIA.git

# Crie e ative o ambiente virtual
python -m venv venv
.\venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

2. Fluxo de Trabalho

    Configuração do Painel: No terminal, rode streamlit run src/app.py para definir os EPIs obrigatórios.

    Preparação de Dados: Coloque fotos brutas em dataset/raw e rode python src/utils.py. As imagens tratadas irão para dataset/processed.

    Teste de Visão: Para validar a câmera e as detecções, rode python src/vision_engine.py.

📖 Manual do Usuário (Para Jurados e Gestores)

O SafeGuard IA foi projetado para ser operado na palma da mão. Siga estes passos para testar a solução:

    Acesso Remoto: Escaneie o QR Code ou acesse o link gerado pelo túnel ngrok no seu celular.

    Configuração de Regras: No painel exibido, escolha a câmera desejada e marque quais EPIs devem ser obrigatórios naquele momento. Clique em Salvar.

    Verificação: Observe o monitor de monitoramento. A IA aplicará instantaneamente as suas preferências, acusando infrações apenas para os itens que você selecionou.

📱 Gerando o QR Code de Acesso

Para facilitar o acesso do jurado durante a apresentação:

    Inicie o ngrok: ./ngrok http 8501.

    Copie a URL gerada e rode o script:

Bash

python src/utils/generate_qr.py https://link-do-ngrok.ngrok-free.app

    Abra o arquivo dashboard_qr.png gerado na raiz e apresente para escaneamento.