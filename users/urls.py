from django.urls import path
from . import views

urlpatterns = [
    path('api/utilisateurs/', views.UtilisateurListCreateView.as_view(), name='liste_utilisateurs'),
    path('api/utilisateurs/<int:pk>/', views.UtilisateurDetailView.as_view(), name='detail_utilisateur'),
]