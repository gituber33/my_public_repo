from flask import Flask, session
from flask_session import Session
from routes import *  # Importer tes routes
import logging
import time

logging.basicConfig(level=logging.DEBUG,  # Niveau de log: DEBUG et plus élevés seront affichés
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])  # Log sur la console

# Configuration de l'application
app.secret_key = secrets.token_hex(32)  
app.config['SESSION_TYPE'] = 'filesystem'  
app.config['SESSION_PERMANENT'] = False  
app.config['SESSION_USE_SIGNER'] = True
app.config['DEBUG'] = False 

# Initialiser Flask-Session
Session(app)

# Lancement de l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Rendre l'application accessible
