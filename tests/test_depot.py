import pytest
from decimal import Decimal
from rest_framework.test import APIClient
from users.models import Banque, UtilisateurBancaire

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def utilisateur(db):
    banque = Banque.objects.create(
        nom="SCB Cameroun",
        code_swift="SCBCCMCX001",
        adresse="Douala, Cameroun"
    )
    return UtilisateurBancaire.objects.create(
        nom="Martin",
        prenom="Paul",
        email="paul.martin@email.com",
        telephone="677000000",
        numero_compte="CMR010",
        solde=Decimal("10000.00"),
        banque=banque
    )

# ============================================================
# F2 — DÉPÔT BANCAIRE
# P1 : Dépôt valide → 200 OK
# P2 : Montant négatif → 400 Bad Request
# P3 : Montant zéro → 400 Bad Request
# P4 : Utilisateur inexistant → 404 Not Found
# ============================================================

@pytest.mark.django_db
def test_depot_valide(client, utilisateur):
    """P1 — Dépôt valide → 200 OK"""
    response = client.post(
        f"/api/comptes/{utilisateur.id}/depot/",
        {"montant": 5000, "description": "Dépôt test"},
        format="json"
    )
    assert response.status_code == 200
    assert "nouveau_solde" in response.data
    assert response.data["nouveau_solde"] == 15000.0

@pytest.mark.django_db
def test_depot_montant_negatif(client, utilisateur):
    """P2 — Montant négatif → 400 Bad Request"""
    response = client.post(
        f"/api/comptes/{utilisateur.id}/depot/",
        {"montant": -1000, "description": "Test négatif"},
        format="json"
    )
    assert response.status_code == 400
    assert "erreur" in response.data

@pytest.mark.django_db
def test_depot_montant_zero(client, utilisateur):
    """P3 — Montant zéro → 400 Bad Request"""
    response = client.post(
        f"/api/comptes/{utilisateur.id}/depot/",
        {"montant": 0, "description": "Test zéro"},
        format="json"
    )
    assert response.status_code == 400

@pytest.mark.django_db
def test_depot_utilisateur_inexistant(client):
    """P4 — Utilisateur inexistant → 404 Not Found"""
    response = client.post(
        "/api/comptes/9999/depot/",
        {"montant": 5000, "description": "Test 404"},
        format="json"
    )
    assert response.status_code == 404