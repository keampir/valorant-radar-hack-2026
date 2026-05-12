from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Document
from .forms import DocumentForm, RegisterForm
import os


# ── Catégories fixes ──────────────────────────────────────────────────────────
CATEGORIES = ['Cours', 'Examen', 'TP', 'Livre', 'Autre']


class MyLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        messages.success(self.request, f"Bienvenue, {self.request.user.username} ! 👋")
        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, "Identifiant ou mot de passe incorrect.")
        return super().form_invalid(form)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Compte créé avec succès ! Bienvenue, {user.username} 🎉")
            return redirect('home')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = RegisterForm()

    return render(request, 'core/register.html', {'form': form})


def home(request):
    documents = Document.objects.all().order_by('-date_upload')

    # ── Filtre catégorie ──────────────────────────────────────────────────────
    categorie_filtre = request.GET.get('categorie', '')
    if categorie_filtre:
        documents = documents.filter(categorie=categorie_filtre)

    # ── Recherche ─────────────────────────────────────────────────────────────
    search = request.GET.get('search', '')
    if search:
        documents = documents.filter(
            Q(titre__icontains=search) | Q(description__icontains=search)
        )

    # ── Pagination (12 docs par page) ─────────────────────────────────────────
    paginator = Paginator(documents, 12)
    page_num = request.GET.get('page', 1)
    documents_page = paginator.get_page(page_num)

    return render(request, 'core/home.html', {
        'documents': documents_page,
        'categories': CATEGORIES,
        'categorie_filtre': categorie_filtre,
        'search': search,
    })


def lire_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    return render(request, 'core/lire.html', {'document': document})


@login_required(login_url='login')
def uploader_document(request):
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB max

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if 'fichier' in request.FILES:
            fichier = request.FILES['fichier']
            if fichier.size > MAX_FILE_SIZE:
                messages.error(request, "Fichier trop volumineux ! Maximum : 10 MB.")
                return render(request, 'core/upload.html', {'form': form})

        if form.is_valid():
            document = form.save(commit=False)
            document.auteur = request.user

            # ── Tentative de conversion Word → PDF ───────────────────────────
            fichier = request.FILES.get('fichier')
            if fichier:
                nom = fichier.name.lower()
                if nom.endswith('.docx') or nom.endswith('.doc'):
                    try:
                        from docx2pdf import convert
                        import tempfile
                        from django.core.files.base import ContentFile

                        # Sauvegarder d'abord le fichier original
                        document.save()
                        orig_path = document.fichier.path

                        # Convertir en PDF
                        pdf_path = orig_path.rsplit('.', 1)[0] + '.pdf'
                        convert(orig_path, pdf_path)

                        # Remplacer le fichier par le PDF
                        if os.path.exists(pdf_path):
                            with open(pdf_path, 'rb') as f:
                                pdf_name = os.path.basename(pdf_path)
                                document.fichier.save(pdf_name, ContentFile(f.read()), save=True)
                            os.remove(orig_path)
                            os.remove(pdf_path)
                            messages.success(request, f"« {document.titre} » converti en PDF et publié !")
                            return redirect('home')
                    except ImportError:
                        # docx2pdf non installé — on garde le fichier original
                        pass
                    except Exception:
                        # Conversion échouée — on garde le fichier original
                        pass

            document.save()
            messages.success(request, f"« {document.titre} » publié avec succès !")
            return redirect('home')
        else:
            messages.error(request, "Erreur dans le formulaire. Vérifiez les champs.")
    else:
        form = DocumentForm()

    return render(request, 'core/upload.html', {'form': form})


@login_required(login_url='login')
def supprimer_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)

    if document.auteur != request.user:
        messages.error(request, "Vous ne pouvez pas supprimer ce document !")
        return redirect('home')

    if request.method == 'POST':
        titre = document.titre
        # Supprimer le fichier physique
        if document.fichier and os.path.exists(document.fichier.path):
            os.remove(document.fichier.path)
        document.delete()
        messages.success(request, f"« {titre} » a été supprimé.")
        return redirect('home')

    return render(request, 'core/confirmer_suppression.html', {'document': document})


@login_required(login_url='login')
def mes_documents(request):
    documents = Document.objects.filter(auteur=request.user).order_by('-date_upload')

    paginator = Paginator(documents, 12)
    page_num = request.GET.get('page', 1)
    documents_page = paginator.get_page(page_num)

    return render(request, 'core/mes_documents.html', {
        'documents': documents_page,
        'categories': CATEGORIES,
    })