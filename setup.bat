@echo off
color 0B
echo ===================================================
echo        SafeGuard IA - Instalador do Sistema
echo ===================================================
echo.

:: 1. Verifica se o Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] O Python nao foi encontrado neste computador!
    echo Por favor, instale o Python e tente novamente.
    pause
    exit /b
)

:: 2. Cria o Ambiente Virtual (Sem pedir admin)
echo [*] A verificar Ambiente Virtual (venv)...
if not exist "venv\Scripts\activate.bat" (
    echo [*] A criar novo Ambiente Virtual... Isto pode demorar um pouco.
    python -m venv venv
) else (
    echo [+] Ambiente Virtual ja existe.
)

:: 3. Ativa a VENV e instala os requisitos
echo [*] A instalar/atualizar dependencias do requirements.txt...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul
pip install -r requirements.txt

:: 4. Finalizacao
echo.
echo ===================================================
echo       Instalacao Concluida com Sucesso!
echo ===================================================
echo.
echo Para iniciar o SafeGuard IA, execute o ficheiro:
echo iniciar_sistema.bat
echo.
pause