@echo off
REM AIOS Workspace Launcher
REM STRICT NO EMOTICON POLICY ENFORCED

echo [AIOS] Launching development workspace
echo [POLICY] Professional development environment

REM Change to AIOS directory
cd /d "C:\dev\AIOS"

REM Launch VS Code with AIOS workspace
code "C:\dev\AIOS\AIOS.code-workspace"

echo [SUCCESS] AIOS workspace launched
pause
