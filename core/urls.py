schema_view = get_schema_view(
    openapi.Info(
        title="API Bancaire",
        default_version='v1',
        description="API pour gérer les utilisateurs d'un système bancaire",
        contact=openapi.Contact(email="contact@api-bancaire.local"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],  # ← déjà bon
)