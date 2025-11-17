@echo off
REM AIOS VSCode Integration Server Launcher with venv auto-activation
setlocal
set AIOS_DIR=%~dp0
cd /d "%AIOS_DIR%"

REM Check if venv exists
if not exist "venv" (
    echo [AIOS] No venv found. Running setup_env.py to create environment...
    python setup_env.py
)

REM Activate venv (Windows)
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [AIOS] venv activation script not found! Running without venv.
)

REM Launch server
python aios_vscode_integration_server.py
pause
