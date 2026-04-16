from django.urls import path
from . import views

urlpatterns = [
    # Liste des utilisateurs + création
    path('api/utilisateurs/', views.UtilisateurListCreateView.as_view(), name='liste_utilisateurs'),
    
    # Détail d'un utilisateur spécifique
    path('api/utilisateurs/<int:pk>/', views.UtilisateurDetailView.as_view(), name='detail_utilisateur'),
]