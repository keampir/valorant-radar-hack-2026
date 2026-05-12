from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Document

# Catégories prédéfinies (source unique de vérité)
CATEGORIES_CHOICES = [
    ('', '-- Choisir une catégorie --'),
    ('Cours', '📚 Cours'),
    ('Examen', '📝 Examen / DS'),
    ('TP', '💻 TP / Exercices'),
    ('Livre', '📖 Livre'),
    ('Autre', '📄 Autre'),
]


class RegisterForm(UserCreationForm):
    """Formulaire d'inscription avec email obligatoire."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'votre@email.com'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Nom d'utilisateur"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Mot de passe'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmer le mot de passe'
        self.fields['username'].help_text = 'Lettres, chiffres et @/./+/-/_ uniquement.'
        self.fields['password1'].help_text = 'Au moins 8 caractères.'
        self.fields['password2'].help_text = ''

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class DocumentForm(forms.ModelForm):
    """Formulaire d'upload de document."""

    class Meta:
        model = Document
        fields = ['titre', 'description', 'fichier', 'categorie']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Cours de Réseaux — Chapitre 3'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Décrivez brièvement le contenu du document...'
            }),
            'fichier': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.ppt,.pptx,.txt'
            }),
            'categorie': forms.Select(
                choices=CATEGORIES_CHOICES,
                attrs={'class': 'form-select'}
            ),
        }
