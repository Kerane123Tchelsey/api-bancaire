from django.contrib.admin import AdminSite
from django.contrib import admin

class BanqueAdminSite(AdminSite):
    site_header = "Administration Bancaire"
    site_title = "Ma Banque - Interface Admin"
    index_title = "Bienvenue sur l'interface d'administration"
    site_url = "/"

# Remplacer l'admin par défaut
admin_site = BanqueAdminSite(name='myadmin')

# Enregistrer tous les modèles existants
from users.models import UtilisateurBancaire, Licence
from django.contrib.auth.models import User, Group

admin_site.register(UtilisateurBancaire)
admin_site.register(Licence)
admin_site.register(User)
admin_site.register(Group)