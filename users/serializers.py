from rest_framework import serializers
from .models import UtilisateurBancaire, Banque, Transaction

class BanqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banque
        fields = '__all__'

class UtilisateurBancaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilisateurBancaire
        fields = '__all__'
        read_only_fields = ['id', 'date_creation', 'date_modification']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['id', 'date_creation', 'date_completion', 'statut']
