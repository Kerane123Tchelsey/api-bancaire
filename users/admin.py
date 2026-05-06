from django.contrib import admin
from .models import UtilisateurBancaire, Banque, Transaction

@admin.register(UtilisateurBancaire)
class UtilisateurBancaireAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'numero_compte', 'solde', 'banque', 'is_admin', 'statut')
    list_filter = ('statut', 'is_admin', 'banque')
    search_fields = ('nom', 'prenom', 'email', 'numero_compte')

@admin.register(Banque)
class BanqueAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code_swift', 'adresse')
    search_fields = ('nom', 'code_swift')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('destinataire', 'montant', 'type_transaction', 'statut', 'date_creation')
    list_filter = ('type_transaction', 'statut')
    search_fields = ('destinataire__nom', 'expediteur__nom')
