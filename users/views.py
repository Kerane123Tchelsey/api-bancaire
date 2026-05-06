from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UtilisateurBancaire
from .serializers import UtilisateurBancaireSerializer

class UtilisateurListCreateView(generics.ListCreateAPIView):
    queryset = UtilisateurBancaire.objects.all()
    serializer_class = UtilisateurBancaireSerializer

class UtilisateurDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UtilisateurBancaire.objects.all()
    serializer_class = UtilisateurBancaireSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']  # ← AJOUT DE PATCH
