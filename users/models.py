from django.db import models

class UtilisateurBancaire(models.Model):
    """
    Modèle représentant un utilisateur dans le système bancaire
    """
    # Informations personnelles
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)
    
    # Informations bancaires
    numero_compte = models.CharField(max_length=20, unique=True)
    solde = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Statut du compte
    ACTIF = 'actif'
    INACTIF = 'inactif'
    SUSPENDU = 'suspendu'
    
    STATUT_CHOICES = [
        (ACTIF, 'Actif'),
        (INACTIF, 'Inactif'),
        (SUSPENDU, 'Suspendu'),
    ]
    
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default=ACTIF)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.numero_compte}"
    
    class Meta:
        verbose_name = "Utilisateur Bancaire"
        verbose_name_plural = "Utilisateurs Bancaires"
        ordering = ['-date_creation']
class Licence(models.Model):
    # Types de licence
    STANDARD = 'standard'
    PREMIUM = 'premium'
    BUSINESS = 'business'
    
    TYPE_CHOICES = [
        (STANDARD, 'Standard (Gratuite)'),
        (PREMIUM, 'Premium (9.99€/mois)'),
        (BUSINESS, 'Business (49.99€/mois)'),
    ]
    
    # Statuts de la licence
    ACTIVE = 'active'
    EXPIRED = 'expired'
    SUSPENDED = 'suspended'
    
    STATUT_CHOICES = [
        (ACTIVE, 'Active'),
        (EXPIRED, 'Expirée'),
        (SUSPENDED, 'Suspendue'),
    ]
    
    # Relations
    utilisateur = models.OneToOneField(UtilisateurBancaire, on_delete=models.CASCADE, related_name='licence')
    
    # Informations licence
    type_licence = models.CharField(max_length=20, choices=TYPE_CHOICES, default=STANDARD)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default=ACTIVE)
    
    # Plafonds
    plafond_transaction = models.DecimalField(max_digits=12, decimal_places=2, default=1000)
    plafond_journalier = models.DecimalField(max_digits=12, decimal_places=2, default=2000)
    limite_api_requetes = models.IntegerField(default=60)
    
    # Dates
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.utilisateur.email} - {self.get_type_licence_display()}"
    
    class Meta:
        verbose_name = "Licence"
        verbose_name_plural = "Licences"
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=UtilisateurBancaire)
def creer_licence_par_defaut(sender, instance, created, **kwargs):
    """Crée automatiquement une licence standard quand un utilisateur est créé"""
    if created:
        Licence.objects.create(
            utilisateur=instance,
            type_licence='standard',
            plafond_transaction=1000,
            plafond_journalier=2000,
            limite_api_requetes=60
        )
