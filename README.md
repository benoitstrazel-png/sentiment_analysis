# Sentilytics — Samsung Analytics Dashboard

Sentilytics est un dashboard d'analyse de sentiments pour les avis produits Samsung France. Il permet d'extraire, d'analyser et de visualiser les retours clients à travers une interface épurée et moderne.

## 🚀 Lancement en local

Le projet a été standardisé pour s'exécuter facilement, peu importe votre système d'exploitation. Un environnement virtuel Python sera automatiquement créé lors du premier lancement.

### Prérequis
- **Python 3.8+** installé sur votre machine.

---

### Pour Mac et Linux 🍏🐧

Ouvrez un terminal, placez-vous à la racine du projet et exécutez le script de démarrage :

```bash
# Donnez les droits d'exécution au script (une seule fois)
chmod +x start.sh

# Lancez le dashboard
./start.sh
```
*Le script va créer l'environnement virtuel, installer les dépendances, lancer le serveur et ouvrir votre navigateur automatiquement à l'adresse `http://localhost:8000/`.*

*(Alternativement, vous pouvez simplement double-cliquer sur le fichier `start.command` depuis le Finder sur Mac).*

---

### Pour Windows 🪟

Ouvrez l'Explorateur de fichiers, allez dans le dossier du projet et double-cliquez simplement sur le fichier :

**`start.bat`**

*Ce script créera automatiquement l'environnement virtuel (`venv`), installera toutes les librairies requises, démarrera le serveur local et ouvrira le dashboard dans votre navigateur.*
