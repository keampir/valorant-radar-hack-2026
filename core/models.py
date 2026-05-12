from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    # Titre du document (ex: Cours de Réseaux)
    titre = models.CharField(max_length=255)
    
    # Description longue du contenu
    description = models.TextField(blank=True)
    
    # Le fichier lui-même. Django va le mettre dans le dossier 'documents/'
    fichier = models.FileField(upload_to='documents/')
    
    # Catégorie (ex: Cours, Examen, Livre)
    categorie = models.CharField(max_length=100)
    
    # L'utilisateur qui a posté (lié à la table User de Django)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Date et heure d'envoi automatique
    date_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
