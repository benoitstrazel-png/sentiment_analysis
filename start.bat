@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ==========================================================
echo ⚡ DÉMARRAGE DE SENTILYTICS (SAMSUNG SENTIMENT ANALYSIS) ⚡
echo ==========================================================

if not exist venv\ (
    echo Création de l'environnement virtuel...
    python -m venv venv
)

echo Activation de l'environnement...
call venv\Scripts\activate.bat

echo Installation des dépendances...
pip install -r requirements.txt > nul

echo Lancement du serveur...
start "Sentilytics" "http://localhost:8000/"

python server.py
pause
