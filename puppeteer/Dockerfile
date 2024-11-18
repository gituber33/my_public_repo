# Utiliser une image de Node.js de base
FROM node:16-slim

# Installer des dépendances supplémentaires pour Chromium
RUN apt-get update && apt-get install -y \
  wget \
  ca-certificates \
  fonts-liberation \
  libappindicator3-1 \
  libasound2 \
  libatk-bridge2.0-0 \
  libatk1.0-0 \
  libcups2 \
  libdbus-1-3 \
  libgdk-pixbuf2.0-0 \
  libnspr4 \
  libnss3 \
  libx11-xcb1 \
  libxcomposite1 \
  libxdamage1 \
  libxrandr2 \
  libgbm1 \
  libnss3 \
  xdg-utils

# Créer un répertoire de travail et y copier les fichiers nécessaires
WORKDIR /app
COPY package.json /app/
RUN npm install

# Copier le reste des fichiers
COPY . /app/

CMD ["node","./puppet_master.js"]
