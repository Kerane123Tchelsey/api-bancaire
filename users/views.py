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
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction as db_transaction
from .models import UtilisateurBancaire, Transaction, Banque
from .serializers import UtilisateurBancaireSerializer, TransactionSerializer, BanqueSerializer

# Vues CRUD pour Banque
class BanqueListCreateView(generics.ListCreateAPIView):
    queryset = Banque.objects.all()
    serializer_class = BanqueSerializer

class BanqueDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Banque.objects.all()
    serializer_class = BanqueSerializer

# Dépôt
class DepotView(APIView):
    def post(self, request, utilisateur_id):
        try:
            utilisateur = UtilisateurBancaire.objects.get(id=utilisateur_id)
            montant = float(request.data.get('montant', 0))

            if montant <= 0:
                return Response({"erreur": "Le montant doit être positif"}, status=status.HTTP_400_BAD_REQUEST)

            with db_transaction.atomic():
                utilisateur.solde += montant
                utilisateur.save()

                Transaction.objects.create(
                    destinataire=utilisateur,
                    montant=montant,
                    type_transaction=Transaction.DEPOT,
                    statut=Transaction.COMPLETEE,
                    description=request.data.get('description', '')
                )

            return Response({
                "message": f"Dépôt de {montant} FCFA effectué",
                "nouveau_solde": utilisateur.solde
            }, status=status.HTTP_200_OK)

        except UtilisateurBancaire.DoesNotExist:
            return Response({"erreur": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

# Retrait
class RetraitView(APIView):
    def post(self, request, utilisateur_id):
        try:
            utilisateur = UtilisateurBancaire.objects.get(id=utilisateur_id)
            montant = float(request.data.get('montant', 0))

            if montant <= 0:
                return Response({"erreur": "Le montant doit être positif"}, status=status.HTTP_400_BAD_REQUEST)

            if utilisateur.solde < montant:
                return Response({"erreur": "Solde insuffisant"}, status=status.HTTP_400_BAD_REQUEST)

            with db_transaction.atomic():
                utilisateur.solde -= montant
                utilisateur.save()

                Transaction.objects.create(
                    expediteur=utilisateur,
                    destinataire=utilisateur,
                    montant=montant,
                    type_transaction=Transaction.RETRAIT,
                    statut=Transaction.COMPLETEE,
                    description=request.data.get('description', '')
                )

            return Response({
                "message": f"Retrait de {montant} FCFA effectué",
                "nouveau_solde": utilisateur.solde
            }, status=status.HTTP_200_OK)

        except UtilisateurBancaire.DoesNotExist:
            return Response({"erreur": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

# Virement
class VirementView(APIView):
    def post(self, request):
        expediteur_id = request.data.get('expediteur_id')
        destinataire_id = request.data.get('destinataire_id')
        montant = float(request.data.get('montant', 0))
        description = request.data.get('description', '')

        if not expediteur_id or not destinataire_id:
            return Response({"erreur": "expediteur_id et destinataire_id requis"}, status=status.HTTP_400_BAD_REQUEST)

        if montant <= 0:
            return Response({"erreur": "Le montant doit être positif"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            expediteur = UtilisateurBancaire.objects.get(id=expediteur_id)
            destinataire = UtilisateurBancaire.objects.get(id=destinataire_id)
        except UtilisateurBancaire.DoesNotExist:
            return Response({"erreur": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        if expediteur.solde < montant:
            return Response({"erreur": "Solde insuffisant"}, status=status.HTTP_400_BAD_REQUEST)

        with db_transaction.atomic():
            expediteur.solde -= montant
            destinataire.solde += montant
            expediteur.save()
            destinataire.save()

            Transaction.objects.create(
                expediteur=expediteur,
                destinataire=destinataire,
                montant=montant,
                type_transaction=Transaction.VIREMENT,
                statut=Transaction.COMPLETEE,
                description=description
            )

        return Response({
            "message": f"Virement de {montant} FCFA effectué de {expediteur.nom} vers {destinataire.nom}",
            "solde_expediteur": expediteur.solde,
            "solde_destinataire": destinataire.solde
        }, status=status.HTTP_200_OK)

# Suppression d'un utilisateur non-admin (réservé aux admins)
class SupprimerUtilisateurView(APIView):
    def delete(self, request, utilisateur_id):
        try:
            utilisateur_a_supprimer = UtilisateurBancaire.objects.get(id=utilisateur_id)

            if utilisateur_a_supprimer.is_admin:
                return Response({"erreur": "Impossible de supprimer un administrateur"}, status=status.HTTP_403_FORBIDDEN)

            # Ici, on suppose que l'admin qui fait la requête est identifié par `request.user`
            # Pour simplifier, on demande un `admin_id` dans la requête
            admin_id = request.data.get('admin_id')
            admin = UtilisateurBancaire.objects.get(id=admin_id)

            if not admin.is_admin:
                return Response({"erreur": "Seul un administrateur peut supprimer un utilisateur"}, status=status.HTTP_403_FORBIDDEN)

            utilisateur_a_supprimer.delete()
            return Response({"message": f"Utilisateur {utilisateur_a_supprimer.nom} supprimé avec succès"}, status=status.HTTP_200_OK)

        except UtilisateurBancaire.DoesNotExist:
            return Response({"erreur": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)
