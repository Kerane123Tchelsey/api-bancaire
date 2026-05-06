from django.db import models
from django.core.exceptions import ValidationError

# Modèle Banque
class Banque(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    code_swift = models.CharField(max_length=11, unique=True)
    adresse = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Banque"
        verbose_name_plural = "Banques"


# Modèle Utilisateur Bancaire
class UtilisateurBancaire(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)
    numero_compte = models.CharField(max_length=20, unique=True)
    solde = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    # Relation avec la banque
    banque = models.ForeignKey(Banque, on_delete=models.SET_NULL, null=True, related_name='utilisateurs')

    # Rôle admin
    is_admin = models.BooleanField(default=False)

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


# Modèle Transaction (Dépôt, Retrait, Virement)
class Transaction(models.Model):
    DEPOT = 'depot'
    RETRAIT = 'retrait'
    VIREMENT = 'virement'

    TYPE_CHOICES = [
        (DEPOT, 'Dépôt'),
        (RETRAIT, 'Retrait'),
        (VIREMENT, 'Virement'),
    ]

    EN_ATTENTE = 'en_attente'
    COMPLETEE = 'completee'
    ANNULEE = 'annulee'

    STATUT_CHOICES = [
        (EN_ATTENTE, 'En attente'),
        (COMPLETEE, 'Complétée'),
        (ANNULEE, 'Annulée'),
    ]

    expediteur = models.ForeignKey(
        UtilisateurBancaire,
        on_delete=models.CASCADE,
        related_name='transactions_envoyees',
        null=True,
        blank=True
    )
    destinataire = models.ForeignKey(
        UtilisateurBancaire,
        on_delete=models.CASCADE,
        related_name='transactions_recues'
    )

    montant = models.DecimalField(max_digits=15, decimal_places=2)
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default=EN_ATTENTE)
    description = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_completion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        if self.expediteur:
            return f"{self.expediteur.nom} → {self.destinataire.nom} : {self.montant} FCFA"
        return f"{self.type_transaction} → {self.destinataire.nom} : {self.montant} FCFA"

    class Meta:
        ordering = ['-date_creation']
