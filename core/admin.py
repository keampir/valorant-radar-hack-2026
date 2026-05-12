from django.contrib import admin
from .models import Document

# Cela permet de voir et de gérer les documents depuis l'interface admin
admin.site.register(Document)
