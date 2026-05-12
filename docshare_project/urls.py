from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    path('uploader/', views.uploader_document, name='uploader_document'),
    path('mes-documents/', views.mes_documents, name='mes_documents'),
    path('lire/<int:doc_id>/', views.lire_document, name='lire_document'),
    path('supprimer/<int:doc_id>/', views.supprimer_document, name='supprimer_document'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)