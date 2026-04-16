from rest_framework import serializers
from .models import UtilisateurBancaire

class UtilisateurBancaireSerializer(serializers.ModelSerializer):
    """
    Serializer pour convertir les objets UtilisateurBancaire en JSON
    """
    
    class Meta:
        model = UtilisateurBancaire
        fields = '__all__'
        read_only_fields = ['id', 'date_creation', 'date_modification']
    
    # Validation : email unique
    def validate_email(self, value):
        if UtilisateurBancaire.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email existe déjà")
        return value
    
    # Validation : numéro de compte unique
    def validate_numero_compte(self, value):
        if UtilisateurBancaire.objects.filter(numero_compte=value).exists():
            raise serializers.ValidationError("Ce numéro de compte existe déjà")
        return value
    
    # Validation : téléphone (9 chiffres, commence par 6)
    def validate_telephone(self, value):
        # Vérifie que c'est bien un nombre
        if not value.isdigit():
            raise serializers.ValidationError("Le numéro de téléphone doit contenir uniquement des chiffres")
        
        # Vérifie la longueur
        if len(value) != 9:
            raise serializers.ValidationError("Le numéro de téléphone doit avoir exactement 9 chiffres")
        
        # Vérifie qu'il commence par 6
        if not value.startswith('6'):
            raise serializers.ValidationError("Le numéro de téléphone doit commencer par 6")
        
        return value