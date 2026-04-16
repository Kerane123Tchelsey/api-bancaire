from django.contrib import admin
from .models import UtilisateurBancaire, Licence

@admin.register(UtilisateurBancaire)
class UtilisateurBancaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'email', 'numero_compte', 'solde', 'statut')
    list_filter = ('statut',)
    search_fields = ('nom', 'prenom', 'email', 'numero_compte')
    readonly_fields = ('id', 'date_creation', 'date_modification')

@admin.register(Licence)
class LicenceAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'type_licence', 'statut', 'date_debut')
    list_filter = ('type_licence', 'statut')
    search_fields = ('utilisateur__email',)