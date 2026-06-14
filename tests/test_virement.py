import pytest
from decimal import Decimal
from rest_framework.test import APIClient
from users.models import Banque, UtilisateurBancaire

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def deux_utilisateurs(db):
    banque = Banque.objects.create(
        nom="UBA Cameroun",
        code_swift="UNAFCMCX001",
        adresse="Douala, Cameroun"
    )
    expediteur = UtilisateurBancaire.objects.create(
        nom="Kamga",
        prenom="Pierre",
        email="pierre.kamga@email.com",
        telephone="677111111",
        numero_compte="CMR030",
        solde=Decimal("80000.00"),
        banque=banque
    )
    destinataire = UtilisateurBancaire.objects.create(
        nom="Biya",
        prenom="Anne",
        email="anne.biya@email.com",
        telephone="677222222",
        numero_compte="CMR031",
        solde=Decimal("20000.00"),
        banque=banque
    )
    return expediteur, destinataire

@pytest.mark.django_db
def test_virement_valide(client, deux_utilisateurs):
    """P1 — Virement valide → 200 OK"""
    expediteur, destinataire = deux_utilisateurs
    data = {
        "expediteur_id": expediteur.id,
        "destinataire_id": destinataire.id,
        "montant": 5000,
        "description": "Virement test"
    }
    response = client.post("/api/virements/", data, format="json")
    assert response.status_code == 200
    assert "message" in response.data

@pytest.mark.django_db
def test_virement_ids_manquants(client):
    """P2 — IDs manquants → 400 Bad Request"""
    data = {
        "montant": 5000,
        "description": "Test sans IDs"
    }
    response = client.post("/api/virements/", data, format="json")
    assert response.status_code == 400

@pytest.mark.django_db
def test_virement_montant_negatif(client, deux_utilisateurs):
    """P3 — Montant négatif → 400 Bad Request"""
    expediteur, destinataire = deux_utilisateurs
    data = {
        "expediteur_id": expediteur.id,
        "destinataire_id": destinataire.id,
        "montant": -1000,
        "description": "Test négatif"
    }
    response = client.post("/api/virements/", data, format="json")
    assert response.status_code == 400

@pytest.mark.django_db
def test_virement_utilisateur_inexistant(client, deux_utilisateurs):
    """P4 — Utilisateur inexistant → 404 Not Found"""
    expediteur, destinataire = deux_utilisateurs
    data = {
        "expediteur_id": 9999,
        "destinataire_id": destinataire.id,
        "montant": 5000,
        "description": "Test 404"
    }
    response = client.post("/api/virements/", data, format="json")
    assert response.status_code == 404

@pytest.mark.django_db
def test_virement_solde_insuffisant(client, deux_utilisateurs):
    """P5 — Solde insuffisant → 400 Bad Request"""
    expediteur, destinataire = deux_utilisateurs
    data = {
        "expediteur_id": expediteur.id,
        "destinataire_id": destinataire.id,
        "montant": 500000,
        "description": "Test solde insuffisant"
    }
    response = client.post("/api/virements/", data, format="json")
    assert response.status_code == 400