from django.urls import path
from . import views

urlpatterns = [
    # Utilisateurs
    path('utilisateurs/', views.UtilisateurListCreateView.as_view(), name='liste_utilisateurs'),
    path('utilisateurs/<int:pk>/', views.UtilisateurDetailView.as_view(), name='detail_utilisateur'),
    path('utilisateurs/supprimer/<int:utilisateur_id>/', views.SupprimerUtilisateurView.as_view(), name='supprimer_utilisateur'),

    # Banques
    path('banques/', views.BanqueListCreateView.as_view(), name='liste_banques'),
    path('banques/<int:pk>/', views.BanqueDetailView.as_view(), name='detail_banque'),

    # Dépôt et retrait
    path('comptes/<int:utilisateur_id>/depot/', views.DepotView.as_view(), name='depot'),
    path('comptes/<int:utilisateur_id>/retrait/', views.RetraitView.as_view(), name='retrait'),

    # Virement
    path('virements/', views.VirementView.as_view(), name='virement'),
]
