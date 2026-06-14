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
        nom="Ecobank Cameroun",
        code_swift="ECOCMCAX001",
        adresse="Yaoundé, Cameroun"
    )
    return UtilisateurBancaire.objects.create(
        nom="Ngo",
        prenom="Marie",
        email="marie.ngo@email.com",
        telephone="655000000",
        numero_compte="CMR020",
        solde=Decimal("50000.00"),
        banque=banque
    )

# ============================================================
# F3 — RETRAIT BANCAIRE
# P1 : Retrait valide → 200 OK
# P2 : Montant négatif → 400 Bad Request
# P3 : Solde insuffisant → 400 Bad Request
# P4 : Utilisateur inexistant → 404 Not Found
# ============================================================

@pytest.mark.django_db
def test_retrait_valide(client, utilisateur):
    """P1 — Retrait valide → 200 OK"""
    response = client.post(
        f"/api/comptes/{utilisateur.id}/retrait/",
        {"montant": 10000, "description": "Retrait test"},
        format="json"
    )
    assert response.status_code == 200
    assert "nouveau_solde" in response.data
    assert response.data["nouveau_solde"] == 40000.0

@pytest.mark.django_db
def test_retrait_montant_negatif(client, utilisateur):
    """P2 — Montant négatif → 400 Bad Request"""
    response = client.post(
        f"/api/comptes/{utilisateur.id}/retrait/",
        {"montant": -5000, "description": "Test négatif"},
        format="json"
    )
    assert response.status_code == 400
    assert "erreur" in response.data

@pytest.mark.django_db
def test_retrait_solde_insuffisant(client, utilisateur):
    """P3 — Solde insuffisant → 400 Bad Request"""
    response = client.post(
        f"/api/comptes/{utilisateur.id}/retrait/",
        {"montant": 100000, "description": "Test solde insuffisant"},
        format="json"
    )
    assert response.status_code == 400
    assert "erreur" in response.data

@pytest.mark.django_db
def test_retrait_utilisateur_inexistant(client):
    """P4 — Utilisateur inexistant → 404 Not Found"""
    response = client.post(
        "/api/comptes/9999/retrait/",
        {"montant": 5000, "description": "Test 404"},
        format="json"
    )
    assert response.status_code == 404