🛡️ SafeGuard IA - Monitoramento Inteligente de EPIs
O SafeGuard IA é uma solução de Visão Computacional de ponta desenvolvida para as exigências da Indústria 4.0. Utilizando a arquitetura YOLOv8, o sistema automatiza a fiscalização de Equipamentos de Proteção Individual (EPIs), garantindo segurança em tempo real com uma gestão flexível, remota e integrada.

🚀 Funcionalidades Principais
🔍 Detecção Multiobjeto: Identificação simultânea de Capacete, Óculos, Luvas, Botas, Protetor Auricular, Máscara e Colete.

⚙️ Gestão Dinâmica: Painel administrativo (Streamlit) para ativar/desativar regras de segurança por câmera ou setor via JSON.

🌐 Acesso IoT: Dashboard acessível via 4G/5G através de tunelamento seguro com Ngrok e geração de QR Code automático.

📸 Snapshot de Violação: Captura automática de imagens quando uma infração é detectada, com lógica de cooldown para evitar spam de arquivos.

⚡ Automação Total: Script "Launcher" que orquestra o site e a IA em um único comando.

📂 Estrutura do Repositório
Plaintext
SAFEGUARDIA/
├── config/             # Configurações JSON (regras por câmera)
├── dataset/            # Banco de imagens (raw e processed)
├── models/             # Pesos da IA (best.pt)
├── src/                # Scripts de execução
│   ├── app.py          # Painel de Controle (Streamlit)
│   ├── automacaototal.py # Engine de Visão + Túnel Ngrok
│   └── launcher.py     # Orquestrador do Ecossistema
├── capturas_violacao/  # Logs visuais de infrações (Snapshots)
├── requirements.txt    # Dependências do projeto
└── README.md
🛠️ Guia do Desenvolvedor
1. Preparação do Ambiente
Bash
# Clone o repositório
git clone https://github.com/SergioJr06/SafeGuardIA.git
cd SafeGuardIA

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements.txt
2. Configuração do Ngrok
Antes de rodar, configure seu token de autenticação (necessário apenas uma vez):

Bash
ngrok config add-authtoken SEU_TOKEN_AQUI
3. Como Rodar (Automação Total)
Para subir o site e a IA simultaneamente, execute o launcher na raiz do projeto:

Bash
python src/launcher.py
📖 Manual do Usuário
O SafeGuard IA foi projetado para ser operado na palma da mão:

Acesso Remoto: Escaneie o QR Code gerado automaticamente no terminal para acessar o Dashboard no celular.

Configuração: No painel, escolha a câmera e marque quais EPIs devem ser fiscalizados. Clique em Salvar.

Verificação: A IA aplicará instantaneamente as novas regras no monitor principal e começará a salvar snapshots em caso de violação.

🛡️ Segurança e Boas Práticas
Este projeto utiliza um arquivo .gitignore para garantir que ambientes virtuais (venv/) e credenciais sensíveis não sejam expostos. Em ambiente de produção, recomenda-se o uso de variáveis de ambiente para o gerenciamento de tokens.

TOKEN NGROK - ngrok config add-authtoken "3BShhmi0NVr02DoKZQODZM1MVCr_44ttMqrFgeUiStWV9ehxJ"