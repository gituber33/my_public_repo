# Utiliser une image de base Python
#FROM python:3.9-slim
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

#Exposer le port de l'application
EXPOSE 5000

# Commande pour démarrer l'application
CMD ["python", "app.py"]
