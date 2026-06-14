import pytest
from decimal import Decimal
from rest_framework.test import APIClient
from users.models import Banque, UtilisateurBancaire

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def utilisateurs(db):
    banque = Banque.objects.create(
        nom="Bicec Cameroun",
        code_swift="BICOCMCX001",
        adresse="Yaoundé, Cameroun"
    )
    admin = UtilisateurBancaire.objects.create(
        nom="Admin",
        prenom="Super",
        email="admin@email.com",
        telephone="677333333",
        numero_compte="CMR040",
        solde=Decimal("0.00"),
        is_admin=True,
        banque=banque
    )
    utilisateur_normal = UtilisateurBancaire.objects.create(
        nom="Normal",
        prenom="User",
        email="normal@email.com",
        telephone="677444444",
        numero_compte="CMR041",
        solde=Decimal("0.00"),
        is_admin=False,
        banque=banque
    )
    non_admin = UtilisateurBancaire.objects.create(
        nom="NonAdmin",
        prenom="User",
        email="nonadmin@email.com",
        telephone="677555555",
        numero_compte="CMR042",
        solde=Decimal("0.00"),
        is_admin=False,
        banque=banque
    )
    return admin, utilisateur_normal, non_admin

# ============================================================
# F5 — SUPPRIMER UTILISATEUR
# P1 : Suppression valide → 200 OK
# P2 : Tentative suppression admin → 403 Forbidden
# P3 : Demandeur non admin → 403 Forbidden
# P4 : Utilisateur inexistant → 404 Not Found
# ============================================================

@pytest.mark.django_db
def test_supprimer_utilisateur_valide(client, utilisateurs):
    """P1 — Suppression valide par admin → 200 OK"""
    admin, utilisateur_normal, non_admin = utilisateurs
    response = client.delete(
        f"/api/utilisateurs/supprimer/{utilisateur_normal.id}/",
        {"admin_id": admin.id},
        format="json"
    )
    assert response.status_code == 200
    assert not UtilisateurBancaire.objects.filter(
        id=utilisateur_normal.id
    ).exists()

@pytest.mark.django_db
def test_supprimer_admin_interdit(client, utilisateurs):
    """P2 — Tentative suppression admin → 403 Forbidden"""
    admin, utilisateur_normal, non_admin = utilisateurs
    response = client.delete(
        f"/api/utilisateurs/supprimer/{admin.id}/",
        {"admin_id": admin.id},
        format="json"
    )
    assert response.status_code == 403

@pytest.mark.django_db
def test_supprimer_par_non_admin(client, utilisateurs):
    """P3 — Demandeur non admin → 403 Forbidden"""
    admin, utilisateur_normal, non_admin = utilisateurs
    response = client.delete(
        f"/api/utilisateurs/supprimer/{utilisateur_normal.id}/",
        {"admin_id": non_admin.id},
        format="json"
    )
    assert response.status_code == 403

@pytest.mark.django_db
def test_supprimer_utilisateur_inexistant(client, utilisateurs):
    """P4 — Utilisateur inexistant → 404 Not Found"""
    admin, utilisateur_normal, non_admin = utilisateurs
    response = client.delete(
        "/api/utilisateurs/supprimer/9999/",
        {"admin_id": admin.id},
        format="json"
    )
    assert response.status_code == 404