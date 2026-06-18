#!/bin/bash
cd "$(dirname "$0")"
echo "=========================================================="
echo "⚡ DÉMARRAGE DE SENTILYTICS (SAMSUNG SENTIMENT ANALYSIS) ⚡"
echo "=========================================================="

if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv venv
fi

echo "Activation de l'environnement..."
source venv/bin/activate

echo "Installation des dépendances..."
pip install -r requirements.txt > /dev/null

echo "Lancement du serveur..."
# Attendre 2 secondes et ouvrir le navigateur (Mac/Linux)
(sleep 2 && if command -v open > /dev/null; then open "http://localhost:8000/"; elif command -v xdg-open > /dev/null; then xdg-open "http://localhost:8000/"; fi) &

python server.py
