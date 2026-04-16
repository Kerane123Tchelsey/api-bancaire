from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import UtilisateurBancaire
from .serializers import UtilisateurBancaireSerializer

# Vue pour lister ET créer des utilisateurs
class UtilisateurListCreateView(generics.ListCreateAPIView):
    """
    GET /api/utilisateurs/ - Liste tous les utilisateurs
    POST /api/utilisateurs/ - Crée un nouvel utilisateur
    """
    queryset = UtilisateurBancaire.objects.all()
    serializer_class = UtilisateurBancaireSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                'message': 'Utilisateur créé avec succès',
                'utilisateur': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Erreur lors de la création',
            'erreurs': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# Vue pour obtenir, modifier ou supprimer un utilisateur spécifique
class UtilisateurDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/utilisateurs/<id>/ - Détails d'un utilisateur
    PUT /api/utilisateurs/<id>/ - Modifier un utilisateur
    DELETE /api/utilisateurs/<id>/ - Supprimer un utilisateur
    """
    queryset = UtilisateurBancaire.objects.all()
    serializer_class = UtilisateurBancaireSerializer