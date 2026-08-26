# Utiliser une image Python officielle légère
FROM python:3.12-slim

# Éviter que Python ne génère des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# Éviter que Python ne mette en mémoire tampon les sorties (pour voir les logs en temps réel)
ENV PYTHONUNBUFFERED 1

# Créer le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires (pour Pillow, etc.)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code du projet
COPY . .

# Créer les dossiers nécessaires et donner les droits
RUN mkdir -p /app/staticfiles /app/media && chmod -R 777 /app

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposer le port par défaut de Hugging Face
EXPOSE 7860

# Commande pour lancer les migrations et démarrer le serveur gunicorn
# On crée le dossier media dans /data s'il n'existe pas
CMD mkdir -p /data/media && python manage.py migrate && gunicorn docshare_project.wsgi:application --bind 0.0.0.0:7860
