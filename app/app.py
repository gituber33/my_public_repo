from flask import Flask, session
from flask_session import Session
from routes import *  # Importer tes routes
import logging
import time

logging.basicConfig(level=logging.DEBUG,  # Niveau de log: DEBUG et plus élevés seront affichés
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])  # Log sur la console

# Configuration de l'application
app.secret_key = secrets.token_hex(32)  # Remplace par une clé secrète sécurisée
app.config['SESSION_TYPE'] = 'filesystem'  # Utiliser le système de fichiers pour stocker les sessions
app.config['SESSION_PERMANENT'] = False  # Les sessions ne sont pas permanentes
app.config['SESSION_USE_SIGNER'] = True  # Signe les cookies de session pour plus de sécurité

# Initialiser Flask-Session
Session(app)

# Lancement de l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Rendre l'application accessible
