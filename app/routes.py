from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory, abort
import secrets
import os.path
import logging
import time
import requests

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG,  # Niveau de log: DEBUG et plus élevés seront affichés
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])  # Log sur la console

app.logger.setLevel(logging.DEBUG)

users = {
    'admin': '8d4a487d59054f96f19d05419c846b8a96f19d05419c84',
}

secrets_bdd = {
    'admin': 'RETRO{Th1s_Is_mY_P3rs0nal_Secret_yOu_c4n_Flag_it}'
}

contact_messages = []
read_messages = []

normalize_page = ['secret','contact','login','register','static']

@app.route('/<page>/<path:subpath>')
def reach_correct_path(page,subpath):
    if page in normalize_page:
        page_var = globals().get(page)
        return page_var()
    else:
        abort(404)

@app.route('/')
def home():
    return redirect(url_for('login'))  # Redirige vers la page de connexion

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:  # Vérifie le mot de passe
            session['username'] = username
            return redirect(url_for('secret'))
        else:
            flash('Incorrect password or username.', 'danger')

    return render_template('login.html')  # Affiche le formulaire de connexion

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in users:  # Vérifie si l'utilisateur existe déjà
            users[username] = password  # Ajoute l'utilisateur
            secret = secrets.token_hex(16)
            secrets_bdd[username] = secret
            flash('Inscription successful. You can now login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already register', 'danger')

    return render_template('register.html')  # Affiche le formulaire d'enregistrement

@app.route('/secret')
def secret():
    if 'username' not in session:  # Vérifie si l'utilisateur est connecté
        return redirect(url_for('login'))  # Redirige vers la connexion si non connecté
    else:
        username = session['username']
        secret = secrets_bdd.get(username)
    return render_template('secret.html', username=username, secret=secret)  # Affiche le secret

@app.route('/contact', methods=['GET', 'POST'])
def contact():
        if 'username' not in session:  # Vérifie si l'utilisateur est connecté
            return redirect(url_for('login'))  # Redirige vers la connexion si non connecté
        elif request.method == 'POST':
            message = request.form['message']  # Récupère le message du formulaire
            contact_messages.append(message)  # Ajoute le message à la liste
            app.logger.debug('Message envoyé à l\'administrateur.')
            try:
                response = requests.get('http://puppeteer:3000/get_latest_message')
                if response.status_code == 200:
                    app.logger.debug('Puppeteer a récupéré la page avec succès!')
                else:
                    app.logger.debug(f"Erreur Puppeteer: {response.status_code}")
            except requests.RequestException as e:
                app.logger.debug(f"Erreur lors de la communication avec Puppeteer: {e}")

            return render_template('contact.html')
        return render_template('contact.html')  # Affiche le formulaire de contact

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()  # Efface la session de l'utilisateur
    flash('Successfully disconnected.', 'success')  # Affiche un message de succès
    return redirect(url_for('home'))  # Redirige vers la page d'accueil

#Fonction pour le bot_admin
@app.route('/get_latest_message')
def get_latest_message():
    global read_messages  # Indiquer que nous utilisons la variable globale
    if contact_messages:
        latest_message = contact_messages[-1]  # Récupère le dernier
        return latest_message  # Renvoie le message brut
    return 'empty', 204  # Aucun message, renvoie un code de statut 204 No Content
