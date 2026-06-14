import pytest
from rest_framework.test import APIClient
from users.models import Banque, UtilisateurBancaire

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def banque(db):
    return Banque.objects.create(
        nom="Afriland First Bank",
        code_swift="CCEICMCX001",
        adresse="Yaoundé, Cameroun"
    )

@pytest.mark.django_db
def test_creer_utilisateur_valide(client, banque):
    """P1 — Données valides → 201 Created"""
    data = {
        "nom": "Dupont",
        "prenom": "Jean",
        "email": "jean.dupont@email.com",
        "telephone": "699000000",
        "numero_compte": "CMR001",
        "banque": banque.id,
        "statut": "actif"
    }
    response = client.post("/api/utilisateurs/", data, format="json")
    assert response.status_code == 201
    assert response.data["email"] == "jean.dupont@email.com"
    assert response.data["nom"] == "Dupont"

@pytest.mark.django_db
def test_creer_utilisateur_email_manquant(client, banque):
    """P2 — Email manquant → 400 Bad Request"""
    data = {
        "nom": "Dupont",
        "prenom": "Jean",
        "telephone": "699000000",
        "numero_compte": "CMR002",
        "banque": banque.id,
    }
    response = client.post("/api/utilisateurs/", data, format="json")
    assert response.status_code == 400

@pytest.mark.django_db
def test_creer_utilisateur_email_doublon(client, banque):
    """P2b — Email déjà existant → 400 Bad Request"""
    UtilisateurBancaire.objects.create(
        nom="Existant",
        prenom="User",
        email="doublon@email.com",
        telephone="699000001",
        numero_compte="CMR003",
        banque=banque
    )
    data = {
        "nom": "Nouveau",
        "prenom": "User",
        "email": "doublon@email.com",
        "telephone": "699000002",
        "numero_compte": "CMR004",
        "banque": banque.id,
    }
    response = client.post("/api/utilisateurs/", data, format="json")
    assert response.status_code == 400