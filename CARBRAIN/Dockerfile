# Choisir une image de base Python
FROM python:3.9-slim

# Ajouter les dépendances nécessaires et installer Google Chrome
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    libx11-xcb1 \
    libxcomposite1 \
    libxrandr2 \
    libglu1-mesa \
    libappindicator3-1 \
    libgbm1 \
    fonts-liberation \
    libasound2 \
    ca-certificates \
    libxss1 \
    libnss3 \
    && apt-get clean

# Ajouter le dépôt de Google Chrome
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | tee /etc/apt/trusted.gpg.d/google.asc
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list

# Mettre à jour et installer Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable

# Installer le gestionnaire de ChromeDriver pour une version compatible
RUN pip install --no-cache-dir undetected-chromedriver selenium webdriver-manager

# Copier ton script Python dans le conteneur
COPY . /app
WORKDIR /app

# Installer les dépendances Python nécessaires
RUN pip install -r requirements.txt

# Commande pour exécuter ton script Python
CMD ["python", "Class2.py"]
