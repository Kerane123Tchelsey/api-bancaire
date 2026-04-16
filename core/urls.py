from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API Bancaire",
        default_version='v1',
        description="API pour gérer les utilisateurs d'un système bancaire",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],  # ← AJOUTE CETTE LIGNE
)